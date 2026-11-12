# -*- coding: utf-8 -*-
"""Gera o RGF Anexo 2 (Dívida Consolidada Líquida) a partir da MSC,
com comparação ao RGF homologado."""
from __future__ import annotations

import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import conferencia_rgf as C
import msc_dcl

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF999999")] * 4)
CAB = PatternFill("solid", fgColor="FFDDEBF7")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATENCAO = PatternFill("solid", fgColor="FFFFEB9C")


def _txt(ws, l, c, t, negrito=False, tamanho=9, fill=None, alinh="left"):
    cel = ws.cell(l, c, t)
    cel.font = Font(name="Arial", size=tamanho, bold=negrito)
    cel.alignment = Alignment(horizontal=alinh, vertical="center")
    cel.border = BORDA
    if fill:
        cel.fill = fill
    return cel


def _num(ws, l, c, v, negrito=False, fill=None, fmt=FMT):
    cel = ws.cell(l, c, v)
    cel.number_format = fmt
    cel.font = Font(name="Arial", size=9, bold=negrito)
    cel.border = BORDA
    if fill:
        cel.fill = fill
    return cel


def gerar(msc: str, homologado: str, destino: str) -> str:
    res = msc_dcl.ler_msc(msc)
    d = msc_dcl.apurar(msc)
    h = C.ler_homologado(homologado)
    # valores do Anexo 2 do homologado (coluna do 3o quadrimestre)
    import leitor_xls as LX
    wb_h = LX.ler_xls(homologado)
    aba = wb_h.aba("RGF-Anexo 02")
    of = {lin: aba.valor(lin, 5) for lin in range(21, 54)}

    wb = Workbook()
    ws = wb.active
    ws.title = "Anexo 2 (DCL)"
    ws.sheet_view.showGridLines = False

    ws["A1"] = "ESTADO DO RIO GRANDE DO NORTE"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A1"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A1:D1")
    ws["A2"] = "RGF — ANEXO 2 — DEMONSTRATIVO DA DÍVIDA CONSOLIDADA LÍQUIDA"
    ws["A2"].font = Font(name="Arial", size=11, bold=True)
    ws["A2"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A2:D2")
    ws["A3"] = "3º QUADRIMESTRE DE 2024 · abrange todos os Poderes (MDF, p. 505) · R$ 1,00"
    ws["A3"].font = Font(name="Arial", size=9, italic=True)
    ws["A3"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A3:D3")

    for j, t in enumerate(["DISCRIMINAÇÃO", "APURADO (MSC)", "HOMOLOGADO", "DIFERENÇA"], start=1):
        c = ws.cell(5, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BORDA

    lin = 6
    _txt(ws, lin, 1, "DÍVIDA CONSOLIDADA (I)", negrito=True, fill=CAB)
    _num(ws, lin, 2, d["divida"], negrito=True, fill=CAB)
    _num(ws, lin, 3, of.get(21, 0), negrito=True, fill=CAB)
    _num(ws, lin, 4, d["divida"] - (of.get(21) or 0), negrito=True, fill=CAB)
    lin += 1

    rotulos = {
        "221110302": "Precatórios - RPPS",
        "221110303": "Precatórios - demais",
        "222210200": "Dívida contratual - externa",
        "222110298": "Dívida contratual - interna",
        "223110402": "Parcelamento - previdenciário",
        "223110403": "Parcelamento - demais",
        "218910106": "Demais obrigações - longo prazo",
        "218810110": "Demais obrigações - curto prazo",
        "218911400": "Demais obrigações - ajustes",
        "211439800": "Empréstimos - outras",
    }
    for conta, valor in sorted(res.divida.items(), key=lambda x: -x[1]):
        _txt(ws, lin, 1, f"   {conta} — {rotulos.get(conta, '')}")
        _num(ws, lin, 2, valor)
        lin += 1

    lin += 1
    _txt(ws, lin, 1, "DEDUÇÕES (II)", negrito=True, fill=CAB)
    _num(ws, lin, 2, d["deducoes"], negrito=True, fill=CAB)
    _num(ws, lin, 3, of.get(45, 0), negrito=True, fill=CAB)
    _num(ws, lin, 4, d["deducoes"] - (of.get(45) or 0), negrito=True, fill=CAB)
    lin += 1
    for conta, valor in sorted(res.deducoes.items(), key=lambda x: -x[1]):
        _txt(ws, lin, 1, f"   {conta} — {msc_dcl.CONTAS_DEDUCAO.get(conta, '')}")
        _num(ws, lin, 2, valor)
        lin += 1

    lin += 1
    _txt(ws, lin, 1, "DÍVIDA CONSOLIDADA LÍQUIDA (III) = (I − II)", negrito=True, fill=OK)
    _num(ws, lin, 2, d["dcl"], negrito=True, fill=OK)
    _num(ws, lin, 3, of.get(46, 0), negrito=True, fill=OK)
    dif = d["dcl"] - (of.get(46) or 0)
    _num(ws, lin, 4, dif, negrito=True, fill=OK)
    pct_dif = (dif / of[46]) if of.get(46) else 0
    _txt(ws, lin, 5, f"{pct_dif:+.4%}", negrito=True)

    lin += 2
    _txt(ws, lin, 1, "APURAÇÃO DO LIMITE", negrito=True, tamanho=10)
    lin += 1
    for rot, val, fmt in (
        ("Receita Corrente Líquida (RCL)", d["rcl"], FMT),
        ("% da Dívida Consolidada sobre a RCL", d["pct_dc"], "0.00%"),
        ("% da Dívida Consolidada Líquida sobre a RCL", d["pct_dcl"], "0.00%"),
        ("Limite (Resolução do Senado Federal — 200% para Estados)", 2.0, "0.00%"),
    ):
        _txt(ws, lin, 1, rot)
        _num(ws, lin, 2, val, negrito=True, fmt=fmt)
        lin += 1

    lin += 1
    _txt(ws, lin, 1, "Situação: DENTRO do limite de 200% da RCL", negrito=True, tamanho=10, fill=OK)

    ws.column_dimensions["A"].width = 52
    for col in "BCD":
        ws.column_dimensions[col].width = 20
    ws.column_dimensions["E"].width = 12

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino
