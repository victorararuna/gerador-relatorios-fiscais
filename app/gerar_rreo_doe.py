# -*- coding: utf-8 -*-
"""Extração de tabelas impressas do DOE-RN por coordenada X.

O PDF do Diário Oficial traz as tabelas como texto posicionado: o rótulo fica
numa faixa de X à esquerda e cada coluna de valores numa faixa própria. Para
reconstruir a tabela:

1. coleta os X de todos os fragmentos que são números e agrupa em clusters
   (as colunas numéricas);
2. cada fragmento é atribuído à coluna cujo centro está mais próximo;
3. o que ficar à esquerda da primeira coluna é o rótulo da linha;
4. linhas sem número e com X na faixa do rótulo são continuação do rótulo
   anterior (quebra de linha do PDF) e são concatenadas.
"""
from __future__ import annotations

import os
import re
import sys
import zlib
from typing import Dict, List, Tuple

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import leitor_pdf as LP

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF7F7F7F")] * 4)
TIT = PatternFill("solid", fgColor="FFBDD7EE")
SEC = PatternFill("solid", fgColor="FFF2F2F2")

RE_NUMERO = re.compile(r"^-?[\d.]+,\d{2}$")
TOLERANCIA_COLUNA = 60.0     # distancia maxima entre valores da mesma coluna


def _paginas(caminho: str) -> List[LP.Pagina]:
    d = open(caminho, "rb").read()
    streams = []
    for m in LP.RE_STREAM.finditer(d):
        bruto = m.group(1)
        u = None
        for t in (bruto, bruto.rstrip(b"\r\n")):
            try:
                u = zlib.decompress(t)
                break
            except Exception:
                pass
        if u and b"BT" in u and (b"Tj" in u or b"TJ" in u):
            streams.append(u)
    return [LP.Pagina(i + 1, LP._itens_de_stream(s, i + 1)) for i, s in enumerate(streams)]


def _numero(txt: str):
    t = txt.strip()
    if not RE_NUMERO.match(t) or t.count(",") != 1:
        return None
    try:
        return float(t.replace(".", "").replace(",", "."))
    except ValueError:
        return None


def _detectar_colunas(pagina) -> List[float]:
    """Clusters de X dos fragmentos numericos, ordenados da esquerda p/ direita."""
    xs = []
    for linha in pagina.linhas():
        for it in linha:
            if _numero(it.texto) is not None:
                xs.append(it.x)
    if not xs:
        return []
    xs.sort()
    clusters: List[List[float]] = [[xs[0]]]
    for x in xs[1:]:
        if x - clusters[-1][-1] <= TOLERANCIA_COLUNA:
            clusters[-1].append(x)
        else:
            clusters.append([x])
    return [sum(c) / len(c) for c in clusters]


def _linhas_tabela(pagina) -> List[Tuple[str, Dict[int, float]]]:
    """(rotulo, {indice_coluna: valor}) para cada linha da pagina."""
    colunas = _detectar_colunas(pagina)
    if not colunas:
        return []
    limite_rotulo = colunas[0] - 40
    saida: List[Tuple[str, Dict[int, float]]] = []

    for linha in pagina.linhas():
        itens = sorted(linha, key=lambda i: i.x)
        rotulo_partes: List[str] = []
        valores: Dict[int, float] = {}

        for it in itens:
            n = _numero(it.texto)
            if n is not None and it.x >= limite_rotulo:
                # coluna mais proxima
                idx = min(range(len(colunas)), key=lambda k: abs(colunas[k] - it.x))
                valores[idx] = valores.get(idx, 0.0) + n
            elif it.x < limite_rotulo:
                rotulo_partes.append(it.texto)

        rotulo = re.sub(r"\s+", " ", " ".join(rotulo_partes)).strip()

        # linha de continuacao do rotulo anterior (sem valores)
        if rotulo and not valores and saida:
            anterior_rotulo, anterior_vals = saida[-1]
            saida[-1] = (re.sub(r"\s+", " ", f"{anterior_rotulo} {rotulo}").strip(),
                         anterior_vals)
            continue

        if rotulo or valores:
            saida.append((rotulo, valores))
    return saida


def _aba(wb: Workbook, nome: str, titulo: str, paginas: List[LP.Pagina],
         n_colunas: int) -> None:
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    ws["A1"] = titulo
    ws["A1"].font = Font(name="Arial", size=10, bold=True)
    ws["A1"].fill = TIT
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n_colunas + 1)
    ws.row_dimensions[1].height = 30

    ws["A2"] = ("ESTADO DO RIO GRANDE DO NORTE · RREO 6º BIMESTRE 2024 · "
                "DOE-RN de 30/01/2025 · Em reais · extração por coordenada X")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n_colunas + 1)

    lin = 4
    for pagina in paginas:
        for rotulo, valores in _linhas_tabela(pagina):
            if not rotulo:
                continue
            negrito = bool(re.match(r"^\d+(-|\.)\s", rotulo)) or rotulo.isupper()
            c = ws.cell(lin, 1, rotulo)
            c.font = Font(name="Arial", size=8, bold=negrito)
            c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            c.border = BORDA
            if negrito:
                c.fill = SEC
            for idx in range(n_colunas):
                if idx in valores:
                    cel = ws.cell(lin, 2 + idx, round(valores[idx], 2))
                    cel.number_format = FMT
                    cel.font = Font(name="Arial", size=8, bold=negrito)
                    cel.border = BORDA
                    if negrito:
                        cel.fill = SEC
            ws.row_dimensions[lin].height = 22 if len(rotulo) > 70 else 13
            lin += 1
        lin += 1

    ws.column_dimensions["A"].width = 80
    from openpyxl.utils import get_column_letter
    for k in range(n_colunas):
        ws.column_dimensions[get_column_letter(2 + k)].width = 18

    lin += 1
    c = ws.cell(lin, 1, "Fonte: DOE-RN de 30/01/2025 (RREO 6º bimestre/2024). Anexo não "
                        "integrado ao arquivo consolidado do Siconfi. "
                        "Colunas reconstruídas pela posição X dos valores.")
    c.font = Font(name="Arial", size=7, italic=True, color="FF666666")
    ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=n_colunas + 1)


def gerar(caminho_pdf: str, destino: str) -> str:
    paginas = _paginas(caminho_pdf)
    wb = Workbook()
    wb.remove(wb.active)

    _aba(wb, "RREO-Anexo 08",
         "RREO - ANEXO 8 (LDB, art. 72) — Demonstrativo das Receitas e Despesas com "
         "Manutenção e Desenvolvimento do Ensino (MDE)",
         [paginas[42], paginas[43]], n_colunas=2)

    _aba(wb, "RREO-Anexo 12",
         "RREO - ANEXO 12 (LC nº 141/2012) — Demonstrativo das Receitas e Despesas "
         "com Ações e Serviços Públicos de Saúde",
         [paginas[48]], n_colunas=6)

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino


if __name__ == "__main__":
    origem = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\victo\Downloads\2025-01-30.pdf"
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saida", "RREO_2024_B6_Anexos_08_12.xlsx")
    print(gerar(origem, saida))
