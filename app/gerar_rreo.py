# -*- coding: utf-8 -*-
"""Gera os demonstrativos do RREO no layout oficial do Siconfi.

Diferentemente do RGF — cujos arquivos vêm sem rótulo e exigem apuração pela
MSC —, o arquivo do RREO traz a estrutura completa de cada anexo: identificação,
grupo, quadro, rótulo, cabeçalho de colunas, linhas e valores. O gerador
reproduz essa estrutura em XLSX formatado e acrescenta uma aba de verificações.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import leitor_xls as LX

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF7F7F7F")] * 4)
CAB = PatternFill("solid", fgColor="FFD9E1F2")
TIT = PatternFill("solid", fgColor="FFBDD7EE")
SEC = PatternFill("solid", fgColor="FFF2F2F2")
TOT = PatternFill("solid", fgColor="FFFFF2CC")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")

# rotulos que marcam linha de total
PREFIXOS_TOTAL = ("TOTAL", "SUBTOTAL", "RECEITAS (EXCETO", "DESPESAS (EXCETO",
                  "RECEITAS CORRENTES", "RECEITAS DE CAPITAL", "DESPESAS CORRENTES",
                  "DESPESAS DE CAPITAL", "RECEITA CORRENTE LÍQUIDA", "RESULTADO",
                  "SALDO", "= RECEITA", "= DESPESA")


import re as _re

_RE_CTRL = _re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _limpar(texto: str) -> str:
    """Remove caracteres de controle que o Excel nao aceita."""
    return _RE_CTRL.sub("", texto or "").strip()


def _eh_total(rotulo: str) -> bool:
    r = rotulo.strip().upper()
    return any(r.startswith(p) for p in PREFIXOS_TOTAL)


def _carregar_catalogo(nome_aba: str):
    """Rotulos minerados do projeto para os anexos que vem sem rotulo no XLS."""
    import json
    sufixo = nome_aba.replace("RREO-Anexo ", "").split(" ")[0].strip()
    caminho = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "dados", "catalogo", f"rotulos_RREO_{sufixo}.json")
    if not os.path.exists(caminho):
        return []
    try:
        dados = json.load(open(caminho, encoding="utf-8"))
    except Exception:
        return []
    rotulos = []
    for bloco in dados.get("blocos", []):
        rotulos.extend(r.get("texto", "") for r in bloco.get("rotulos", []))
    return rotulos


def _copiar_aba(wb: Workbook, origem, nome: str) -> Dict[str, float]:
    """Copia uma aba do RREO para o XLSX formatado. Devolve alguns totais."""
    catalogo = _carregar_catalogo(nome)
    idx_catalogo = 0
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    totais: Dict[str, float] = {}

    ncols = max(origem.max_col, 2)
    for j in range(1, ncols + 1):
        ws.column_dimensions[get_column_letter(j)].width = 16 if j > 1 else 62

    for lin in range(1, origem.max_lin + 1):
        texto = _limpar(origem.texto(lin, 1))
        valores = [origem.valor(lin, c) for c in range(2, ncols + 1)]
        numeros = [v for v in valores if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if numeros and catalogo:
            if not texto and idx_catalogo < len(catalogo):
                texto = _limpar(catalogo[idx_catalogo])
            idx_catalogo += 1

        if not texto and not numeros:
            continue

        # identificacao e blocos de titulo
        if texto.startswith(("RREO", "RELATÓRIO", "VERSÃO", "VIGÊNCIA", "Ente:", "Poder:",
                             "Instituição:", "Exercício:", "Periodicidade:", "Período:",
                             "Grupo:", "Quadro:", "Rótulo:")):
            c = ws.cell(lin, 1, texto)
            negrito = texto.startswith(("RREO", "RELATÓRIO", "Grupo:", "Quadro:"))
            c.font = Font(name="Arial", size=9 if negrito else 8, bold=negrito)
            if texto.startswith(("Grupo:", "Quadro:")):
                c.fill = SEC
            continue

        eh_total = _eh_total(texto)
        c = ws.cell(lin, 1, texto)
        c.font = Font(name="Arial", size=8, bold=eh_total)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        c.border = BORDA
        if eh_total:
            c.fill = SEC

        for j, v in enumerate(valores, start=2):
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                cel = ws.cell(lin, j, round(v, 2))
                cel.number_format = FMT
                cel.font = Font(name="Arial", size=8, bold=eh_total)
                cel.border = BORDA
                if eh_total:
                    cel.fill = SEC

        # guarda os totais para a conferencia
        if eh_total:
            totais[texto.strip()[:60]] = sum(numeros) if numeros else 0.0

        ws.row_dimensions[lin].height = 24 if len(texto) > 58 else 13

    return totais


def _aba_verificacoes(wb: Workbook, dados: List[Tuple[str, str, float, float, str]]) -> None:
    ws = wb.create_sheet("Verificações")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "VERIFICAÇÕES — RREO"
    ws["A1"].font = Font(name="Arial", size=12, bold=True)
    ws["A2"] = ("Conferência das identidades contábeis de cada anexo. "
                "Verde: confere; amarelo: diferença até 1%; vermelho: acima.")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, t in enumerate(["Anexo", "Verificação", "Valor A", "Valor B",
                           "Diferença", "Situação"], start=1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BORDA

    lin = 5
    for anexo, rotulo, a, b, obs in dados:
        ws.cell(lin, 1, anexo).font = Font(name="Arial", size=8)
        ws.cell(lin, 2, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((3, a), (4, b)):
            c = ws.cell(lin, j, round(v, 2))
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        dif = round(a, 2) - round(b, 2)
        c = ws.cell(lin, 5, dif)
        c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        base = abs(b) if b else 1
        if abs(dif) < 0.01:
            situacao, cor = "confere", OK
        elif abs(dif) / base <= 0.01:
            situacao, cor = "até 1%", ATEN
        else:
            situacao, cor = "divergente", RUIM
        c = ws.cell(lin, 6, situacao)
        c.font = Font(name="Arial", size=8, bold=situacao != "confere")
        for j in range(1, 7):
            ws.cell(lin, j).border = BORDA
            ws.cell(lin, j).fill = cor
        lin += 1

    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 58
    for col in "CDEF":
        ws.column_dimensions[col].width = 18


# verificacoes de identidade por anexo: (anexo, rotulo, chaveA, chaveB)
VERIFICACOES = [
    ("Anexo 01", "Receitas correntes = impostos + contribuições + patrimonial + "
                 "agropecuária + industrial + serviços + transferências + outras",
     "RECEITAS CORRENTES", None),
]


def _valores_da_linha(aba, prefixo: str, coluna: int = 2):
    """Valores de uma linha cujo rotulo comeca com o prefixo."""
    for lin in range(1, aba.max_lin + 1):
        rot = _limpar(aba.texto(lin, 1)).upper()
        if rot.startswith(prefixo.upper()):
            v = aba.valor(lin, coluna)
            if isinstance(v, (int, float)):
                return float(v)
    return None


def gerar(caminho_xls: str, destino: str) -> str:
    """Gera o RREO completo em XLSX, uma aba por anexo, com verificacoes."""
    wb_origem = LX.ler_xls(caminho_xls)
    wb = Workbook()
    wb.remove(wb.active)

    for nome in wb_origem.nomes:
        if not nome.startswith("RREO-Anexo"):
            continue
        _copiar_aba(wb, wb_origem.aba(nome), nome)

    dados = []

    # --- Anexo 1: identidades do balanco orcamentario
    if "RREO-Anexo 01" in wb_origem.nomes:
        a = wb_origem.aba("RREO-Anexo 01")
        rec = _valores_da_linha(a, "RECEITAS (EXCETO")
        desp = _valores_da_linha(a, "DESPESAS (EXCETO")
        sub_rec = _valores_da_linha(a, "SUBTOTAL DAS RECEITAS")
        sub_desp = _valores_da_linha(a, "SUBTOTAL DAS DESPESAS")
        if rec is not None and desp is not None:
            dados.append(("Anexo 01", "Receitas (exceto intra) x Despesas (exceto intra)",
                          rec, desp, ""))
        if sub_rec is not None and sub_desp is not None:
            dados.append(("Anexo 01", "Subtotal receitas (III) x Subtotal despesas (X)",
                          sub_rec, sub_desp, ""))

    # --- Anexo 3: RCL
    if "RREO-Anexo 03" in wb_origem.nomes:
        a = wb_origem.aba("RREO-Anexo 03")
        rec_corr = _valores_da_linha(a, "RECEITAS CORRENTES (I)")
        ded = _valores_da_linha(a, "DEDUÇÕES (II)")
        rcl = _valores_da_linha(a, "RECEITA CORRENTE LÍQUIDA (III)")
        if rec_corr is not None and ded is not None and rcl is not None:
            dados.append(("Anexo 03", "RCL (III) = Receitas Correntes (I) - Deduções (II)",
                          rcl, rec_corr - ded, ""))

    # --- Anexo 4: previdencia
    if "RREO-Anexo 04" in wb_origem.nomes:
        a = wb_origem.aba("RREO-Anexo 04")
        rp = _valores_da_linha(a, "RECEITAS PREVIDENCIÁRIAS")
        dp = _valores_da_linha(a, "DESPESAS PREVIDENCIÁRIAS")
        if rp is not None and dp is not None:
            dados.append(("Anexo 04", "Receitas Previdenciárias x Despesas Previdenciárias",
                          rp, dp, ""))

    # --- Anexo 6: resultado primario
    if "RREO-Anexo 06" in wb_origem.nomes:
        a = wb_origem.aba("RREO-Anexo 06")
        for lin in range(1, a.max_lin + 1):
            rot = _limpar(a.texto(lin, 1)).upper()
            if "RESULTADO PRIMÁRIO" in rot and rot.startswith("RESULTADO PRIMÁRIO"):
                v = a.valor(lin, 2)
                if isinstance(v, (int, float)):
                    dados.append(("Anexo 06", "Resultado primário (V)", float(v), 0.0, ""))
                break

    # --- Anexo 7: restos a pagar
    if "RREO-Anexo 07" in wb_origem.nomes:
        a = wb_origem.aba("RREO-Anexo 07")
        insc = _valores_da_linha(a, "RESTOS A PAGAR NÃO PROCESSADOS")
        pag = _valores_da_linha(a, "RESTOS A PAGAR PROCESSADOS")
        if insc is not None and pag is not None:
            dados.append(("Anexo 07", "RP não processados x RP processados",
                          insc, pag, ""))

    _aba_verificacoes(wb, dados)

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino


if __name__ == "__main__":
    origem = sys.argv[1] if len(sys.argv) > 1 else r"D:\\Downloads\\SICONFI_RREO_171_BIMESTRAL_6.xls"
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saida", "RREO_2024_B6_STN.xlsx")
    print(gerar(origem, saida))
