# -*- coding: utf-8 -*-
"""Geração dos demonstrativos fiscais a partir do rascunho.

Saídas:
  - .xlsx : planilha formatada no padrão dos demonstrativos do MDF
  - .html : versão para impressão (Ctrl+P → PDF no navegador)

O desenho da tabela vem do rascunho (blocos, colunas e rótulos); este módulo
acrescenta o enquadramento oficial (título, base legal, nota de rodapé),
a formatação numérica e a hierarquia visual.
"""
from __future__ import annotations

import html
import os
import re
import unicodedata
from typing import Dict, List, Optional

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins

import anexos as cat
from modelo import Anexo, Bloco, Coluna, Documento, Linha, Periodo

MESES = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO",
         "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

FMT_MOEDA = '#,##0.00;[Red]-#,##0.00;"-"'
FMT_PCT = '#,##0.00;[Red]-#,##0.00;"-"'
ROTULO_PADRAO = "DISCRIMINAÇÃO"

BORDA_FINA = Border(*[Side(style="thin", color="FF000000")] * 4)
FUNDO_CABECALHO = PatternFill("solid", fgColor="FFE7E6E6")
FUNDO_TOTAL = PatternFill("solid", fgColor="FFF2F2F2")


def rotulo_periodo(periodo: Optional[Periodo], documento: str) -> str:
    """Ex.: 'JANEIRO A AGOSTO 2026 / 4º BIMESTRE (JULHO-AGOSTO)'."""
    if not periodo:
        return ""
    fim = min(periodo.meses, 12)
    extenso = f"JANEIRO A {MESES[fim - 1]} {periodo.exercicio}"
    if periodo.periodicidade.upper().startswith("BIM"):
        ini = max(0, fim - 2)
        faixa = f"{MESES[ini]}-{MESES[fim - 1]}" if ini != fim - 1 else MESES[fim - 1]
        return f"{extenso} / {periodo.rotulo.upper()} ({faixa})"
    if periodo.periodicidade.upper().startswith("QUAD"):
        ini = max(0, fim - 4)
        faixa = f"{MESES[ini]}-{MESES[fim - 1]}"
        return f"{extenso} / {periodo.rotulo.upper()} ({faixa})"
    return extenso


def _slug(txt: str) -> str:
    """Nome de arquivo seguro: sem acento, sem pontuação, caixa alta."""
    base = unicodedata.normalize("NFKD", txt)
    base = "".join(c for c in base if not unicodedata.combining(c))
    base = re.sub(r"[^A-Za-z0-9 ]", "", base).strip().upper()
    return re.sub(r"\s+", "_", base)[:60]


def _titulo_aba(nome: str) -> str:
    """openpyxl não aceita []:*?/\\ e limita a 31 caracteres."""
    limpo = re.sub(r"[\[\]:*?/\\]", "-", nome).strip()
    return (limpo or "Quadro")[:31]


def _vazio(linha: Linha) -> bool:
    return not linha.rotulo.strip() and not any(v is not None for v in linha.valores.values())


def nome_arquivo(doc: Documento, anexo: Anexo, ext: str) -> str:
    info = cat.info(anexo.documento, anexo.numero)
    titulo = info.titulo if info else f"Anexo {anexo.numero}"
    per = doc.periodo
    letra = "B" if anexo.documento.upper() == "RREO" else "Q"
    sufixo = f"{per.exercicio}_{letra}{per.numero}" if per else ""
    return f"{anexo.documento}_{sufixo}_{anexo.numero:02d}_{_slug(titulo)}.{ext}"


# ---------------------------------------------------------------------------
# XLSX
# ---------------------------------------------------------------------------
def rotular_colunas(bloco: Bloco, doc: Documento, anexo: Anexo) -> None:
    """Completa titulos de coluna ausentes no rascunho.

    Alguns anexos (RCL, previdenciario) chegam do Siconfi sem o cabecalho das
    colunas mensais. Quando todas as colunas monetarias estao sem titulo,
    sintetizamos a serie de 12 meses do MDF (<MR-11>..<MR>) seguida de total.
    """
    monetarias = [c for c in bloco.colunas if c.tipo != "percentual"]
    if not monetarias:
        return
    sem_titulo = sum(1 for c in monetarias if not c.titulo.strip()
                     or c.titulo.strip().lower().startswith("coluna "))
    if sem_titulo < len(monetarias):
        return
    # serie mensal de 12 meses: inequivoca apenas no Anexo 3 (RCL)
    if anexo.numero == 3 and anexo.documento.upper() == "RREO" and len(monetarias) >= 12:
        for i, col in enumerate(monetarias[:12]):
            col.titulo = f"<MR-{11 - i}>" if i < 11 else "<MR>"
            col.superior = col.superior or "EVOLUÇÃO DA RECEITA REALIZADA NOS ÚLTIMOS 12 MESES"
        for j, col in enumerate(monetarias[12:]):
            col.titulo = "TOTAL (ÚLTIMOS 12 MESES)" if j == 0 else f"Valor {j + 1}"
    else:
        for j, col in enumerate(monetarias):
            col.titulo = "Valor" if j == 0 else f"Valor {j + 1}"


def gerar_xlsx(doc: Documento, anexo: Anexo, destino: str) -> str:
    info = cat.info(anexo.documento, anexo.numero)
    wb = Workbook()
    wb.remove(wb.active)

    for i, bloco in enumerate(anexo.blocos):
        ws = wb.create_sheet(_titulo_aba(bloco.quadro or f"Quadro {i + 1}"))
        rotular_colunas(bloco, doc, anexo)
        _preencher_aba(ws, doc, anexo, bloco, info, primeira=(i == 0))

    if not wb.sheetnames:
        ws = wb.create_sheet("Demonstrativo")
        _preencher_aba(ws, doc, anexo, Bloco(quadro="Vazio"), info, True)

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino


def _preencher_aba(ws, doc: Documento, anexo: Anexo, bloco: Bloco,
                   info: Optional[cat.AnexoInfo], primeira: bool) -> None:
    n_cols = max(1, len(bloco.colunas))
    ultima = 1 + n_cols
    ws.sheet_view.showGridLines = False

    lin = 1
    if primeira:
        cabecalho = [
            (doc.ente.nome.upper(), 12, True, False),
            ("RELATÓRIO RESUMIDO DA EXECUÇÃO ORÇAMENTÁRIA" if anexo.documento.upper() == "RREO"
             else "RELATÓRIO DE GESTÃO FISCAL", 10, True, False),
            (info.titulo if info else bloco.quadro, 11, True, False),
            (info.subtitulo if info else "", 9, False, False),
            (rotulo_periodo(doc.periodo, anexo.documento), 9, False, False),
            (info.base_legal if info else "", 8, False, False),
            ("R$ 1,00", 8, False, True),
        ]
        for texto, tam, negrito, italico in cabecalho:
            if not texto:
                lin += 1
                continue
            c = ws.cell(lin, 1, texto)
            c.font = Font(name="Arial", size=tam, bold=negrito, italic=italico)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            if ultima > 1:
                ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=ultima)
            ws.row_dimensions[lin].height = 26 if tam >= 11 else 16
            lin += 1
        lin += 1
    elif bloco.quadro:
        c = ws.cell(lin, 1, bloco.quadro)
        c.font = Font(name="Arial", size=10, bold=True)
        c.alignment = Alignment(horizontal="left", vertical="center")
        if ultima > 1:
            ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=ultima)
        lin += 2

    # ---- cabeçalho da tabela: 2 faixas, coluna A mesclada na vertical ----
    if bloco.colunas:
        linha_sup = lin
        if bloco.titulo_tabela:
            _cel_cabecalho(ws, linha_sup, 1, bloco.titulo_tabela)
        for j, col in enumerate(bloco.colunas, start=2):
            _cel_cabecalho(ws, linha_sup, j, col.superior)
        ws.row_dimensions[linha_sup].height = 22

        linha_col = linha_sup + 1
        for j, col in enumerate(bloco.colunas, start=2):
            _cel_cabecalho(ws, linha_col, j, col.titulo)
        if not bloco.titulo_tabela:
            _cel_cabecalho(ws, linha_col, 1, bloco.quadro or ROTULO_PADRAO)
        ws.row_dimensions[linha_col].height = 32

        if not bloco.titulo_tabela:
            ws.merge_cells(start_row=linha_sup, start_column=1, end_row=linha_col, end_column=1)
        lin = linha_col + 1

    # ---- linhas ----
    for row in bloco.linhas:
        if _vazio(row):
            lin += 1
            continue
        cel_rot = ws.cell(lin, 1, row.rotulo.strip())
        cel_rot.alignment = Alignment(horizontal="left", vertical="center",
                                      wrap_text=False, indent=min(row.nivel * 2, 8))
        cel_rot.border = BORDA_FINA
        negrito = row.negrito or row.total
        for j, col in enumerate(bloco.colunas, start=2):
            cel = ws.cell(lin, j, row.valor(col.chave))
            cel.number_format = FMT_PCT if col.tipo == "percentual" else FMT_MOEDA
            cel.alignment = Alignment(horizontal="right", vertical="center")
            cel.border = BORDA_FINA
        for j in range(1, 2 + len(bloco.colunas)):
            alvo = ws.cell(lin, j)
            alvo.font = Font(name="Arial", size=8, bold=negrito)
            if row.total:
                alvo.fill = FUNDO_TOTAL
        lin += 1

    # ---- rodapé ----
    lin += 1
    if info and info.nota:
        c = ws.cell(lin, 1, info.nota)
        c.font = Font(name="Arial", size=7, italic=True)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        if ultima > 1:
            ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=ultima)

    # ---- largura e impressão ----
    ws.column_dimensions["A"].width = 62
    for j in range(2, 2 + len(bloco.colunas)):
        ws.column_dimensions[get_column_letter(j)].width = 17

    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.3, right=0.3, top=0.5, bottom=0.5)


def _cel_cabecalho(ws, linha: int, col: int, texto: str) -> None:
    if not texto:
        return
    c = ws.cell(linha, col, texto)
    c.font = Font(name="Arial", size=7, bold=True)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.fill = FUNDO_CABECALHO
    c.border = BORDA_FINA


# ---------------------------------------------------------------------------
# HTML (impressão → PDF)
# ---------------------------------------------------------------------------
_CSS = """
@page { size: A4 landscape; margin: 8mm; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 9pt; color:#000; }
h1 { font-size: 11pt; text-align:center; margin:0; }
h2 { font-size: 10pt; text-align:center; margin:2px 0 0; }
h3 { font-size: 9pt; text-align:center; font-weight:normal; margin:2px 0; }
.legenda { text-align:right; font-size:8pt; }
table { border-collapse: collapse; width:100%; margin-top:6px; }
th, td { border: 0.5pt solid #000; padding: 1.5px 3px; font-size: 7.5pt; }
th { background:#e7e6e6; text-align:center; font-weight:bold; }
td.rot { text-align:left; }
td.num { text-align:right; font-variant-numeric: tabular-nums; }
tr.total td { font-weight:bold; background:#f2f2f2; }
.n0{} .n1{padding-left:10px} .n2{padding-left:20px} .n3{padding-left:30px} .n4{padding-left:40px}
.nota { font-size:7pt; font-style:italic; margin-top:6px; }
"""


def fmt_moeda(v: Optional[float]) -> str:
    if v is None:
        return "-"
    s = f"{v:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_html(doc: Documento, anexo: Anexo, destino: str) -> str:
    info = cat.info(anexo.documento, anexo.numero)
    partes = ["<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'>",
              f"<title>{html.escape(doc.ente.nome)} – {html.escape(info.titulo if info else '')}</title>",
              f"<style>{_CSS}</style></head><body>"]
    for i, bloco in enumerate(anexo.blocos):
        if i == 0 and info:
            partes.append(f"<h1>{html.escape(doc.ente.nome.upper())}</h1>")
            partes.append("<h2>RELATÓRIO RESUMIDO DA EXECUÇÃO ORÇAMENTÁRIA</h2>"
                          if anexo.documento.upper() == "RREO" else
                          "<h2>RELATÓRIO DE GESTÃO FISCAL</h2>")
            partes.append(f"<h2>{html.escape(info.titulo)}</h2>")
            if info.subtitulo.strip():
                partes.append(f"<h3>{html.escape(info.subtitulo)}</h3>")
            partes.append(f"<h3>{html.escape(rotulo_periodo(doc.periodo, anexo.documento))}</h3>")
            partes.append(f"<h3>{html.escape(info.base_legal)}</h3>")
            partes.append("<div class='legenda'>R$ 1,00</div>")
        elif bloco.quadro:
            partes.append(f"<h3 style='margin-top:10px'>{html.escape(bloco.quadro)}</h3>")

        if not bloco.colunas:
            continue
        partes.append("<table><thead>")
        sup = [c.superior for c in bloco.colunas]
        if any(sup):
            partes.append("<tr><th></th>" + "".join(f"<th>{html.escape(s)}</th>" for s in sup) + "</tr>")
        partes.append("<tr><th>" + html.escape(bloco.quadro or ROTULO_PADRAO) + "</th>"
                      + "".join(f"<th>{html.escape(c.titulo)}</th>" for c in bloco.colunas)
                      + "</tr></thead><tbody>")
        for row in bloco.linhas:
            if _vazio(row):
                continue
            classe = "total" if row.total else ""
            celulas = "".join(f"<td class='num'>{fmt_moeda(row.valor(col.chave))}</td>"
                              for col in bloco.colunas)
            partes.append(f"<tr class='{classe}'><td class='rot n{min(row.nivel, 4)}'>"
                          f"{html.escape(row.rotulo.strip())}</td>{celulas}</tr>")
        partes.append("</tbody></table>")
    if info and info.nota:
        partes.append(f"<div class='nota'>{html.escape(info.nota)}</div>")
    partes.append("</body></html>")

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))
    return destino


# ---------------------------------------------------------------------------
# orquestração
# ---------------------------------------------------------------------------
def gerar_documento(doc: Documento, pasta_saida: str,
                    formatos: List[str] = ("xlsx", "html")) -> List[Dict]:
    saidas: List[Dict] = []
    for anexo in doc.anexos:
        info = cat.info(anexo.documento, anexo.numero)
        linhas = [l for b in anexo.blocos for l in b.linhas if l.valores]
        com_rotulo = [l for l in linhas if l.rotulo.strip()]
        cobertura = len(com_rotulo) / len(linhas) if linhas else 0.0
        if info and not info.aplica_estado:
            saidas.append(dict(anexo=anexo.chave, status="nao_aplicavel",
                               mensagem="anexo simplificado (municipios < 50 mil hab.); "
                                        "nao se aplica ao Estado"))
            continue
        if (info and info.precisa_rotulos and cobertura < 0.5) or not anexo.blocos:
            saidas.append(dict(anexo=anexo.chave, status="sem_rotulos",
                               mensagem="rascunho traz apenas valores; requer catálogo de rótulos (Fase 2)"))
            continue
        sub = os.path.join(pasta_saida, f"{doc.tipo}_{doc.periodo.exercicio}_P{doc.periodo.numero}")
        os.makedirs(sub, exist_ok=True)
        reg: Dict = dict(anexo=anexo.chave, status="ok", arquivos=[])
        if "xlsx" in formatos:
            reg["arquivos"].append(gerar_xlsx(doc, anexo, os.path.join(sub, nome_arquivo(doc, anexo, "xlsx"))))
        if "html" in formatos:
            reg["arquivos"].append(gerar_html(doc, anexo, os.path.join(sub, nome_arquivo(doc, anexo, "html"))))
        saidas.append(reg)
    return saidas
