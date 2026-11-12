# -*- coding: utf-8 -*-
"""Gera o Anexo 1 apurado pela Matriz de Saldos Contábeis, comparado ao RGF
homologado no Siconfi."""
from __future__ import annotations

import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import conferencia_rgf as C
import msc_pessoal as M

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF999999")] * 4)
CAB = PatternFill("solid", fgColor="FFDDEBF7")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATENCAO = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")

RCL = 17259989216.73


def _txt(ws, linha, coluna, texto, negrito=False, tamanho=9, fill=None, alinhamento="left"):
    c = ws.cell(linha, coluna, texto)
    c.font = Font(name="Arial", size=tamanho, bold=negrito)
    c.alignment = Alignment(horizontal=alinhamento, vertical="center")
    c.border = BORDA
    if fill:
        c.fill = fill
    return c


def _num(ws, linha, coluna, valor, negrito=False, fill=None, formato=FMT):
    c = ws.cell(linha, coluna, valor)
    c.number_format = formato
    c.font = Font(name="Arial", size=9, bold=negrito)
    c.border = BORDA
    if fill:
        c.fill = fill
    return c


def gerar(msc: str, homologado: str, destino: str) -> str:
    r = M.ler_msc(msc)
    L = M.apurar(r)
    ne = M.nao_executada(r)
    env = M.deducao_enfermagem(r)
    h = C.ler_homologado(homologado)

    vinculados = M.deducao_vinculados(r)

    bruta = (L["vencimentos"] + L["patronal"] + L["aposentadorias"] + L["pensoes"]
             + L["terceirizacao"] + ne)
    deducao = (L["judiciais"] + L["exercicios_anteriores"] + L["indenizacoes"]
               + env["deducao"] + vinculados)
    liquida = bruta - deducao

    wb = Workbook()
    ws = wb.active
    ws.title = "Anexo 1 (MSC)"
    ws.sheet_view.showGridLines = False

    ws["A1"] = "ESTADO DO RIO GRANDE DO NORTE"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A1"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A1:E1")
    ws["A2"] = "RGF — ANEXO 1 — DESPESA COM PESSOAL · 3º QUADRIMESTRE DE 2024"
    ws["A2"].font = Font(name="Arial", size=11, bold=True)
    ws["A2"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A2:E2")
    ws["A3"] = "Apuração a partir da Matriz de Saldos Contábeis · POs 10111 + 10112 + 60611 · R$ 1,00"
    ws["A3"].font = Font(name="Arial", size=9, italic=True)
    ws["A3"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A3:E3")

    for j, t in enumerate(["DISCRIMINAÇÃO", "APURADO (MSC)", "HOMOLOGADO (Siconfi)",
                           "DIFERENÇA", "%"], start=1):
        c = ws.cell(5, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BORDA

    linhas = [
        ("DESPESA BRUTA COM PESSOAL (I)", bruta, h["DESPESA BRUTA"], True, None),
        ("  Vencimentos, Vantagens e Outras Despesas Variáveis", L["vencimentos"], h["VENCIMENTOS"], False, "linha"),
        ("  Obrigações Patronais", L["patronal"], h["PATRONAIS"], False, "linha"),
        ("  Aposentadorias, Reserva e Reformas", L["aposentadorias"], h["APOSENTADORIAS"], False, "linha"),
        ("  Pensões", L["pensoes"], h["PENSOES"], False, "linha"),
        ("  Outras Despesas de Pessoal de Terceirização", L["terceirizacao"], h["TERCEIRIZACAO"], False, "linha"),
        ("  Despesa com Pessoal não Executada Orçamentariamente", ne, h["NAO_EXECUTADA"], False, "linha"),
        ("DESPESAS NÃO COMPUTADAS (II)", deducao, h["DEDUCOES"], True, None),
        ("  Decorrentes de Decisão Judicial", L["judiciais"], h["JUDICIAIS"], False, "linha"),
        ("  Despesas de Exercícios Anteriores", L["exercicios_anteriores"], h["EX_ANTERIORES"], False, "linha"),
        ("  Indenizações por Demissão e Incentivos", L["indenizacoes"], h["INDENIZACOES"], False, "linha"),
        ("  Inativos e Pensionistas com Recursos Vinculados", vinculados, h["VINCULADOS"], False, "linha"),
        ("  Parcela dedutível do piso do Enfermeiro", env["deducao"], h["PISO_ENFERMEIRO"], False, "linha"),
        ("DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)", liquida, h["LIQUIDA"], True, None),
    ]

    lin = 6
    for rotulo, apurado, oficial, negrito, tipo in linhas:
        _txt(ws, lin, 1, rotulo, negrito)
        _num(ws, lin, 2, apurado, negrito)
        _num(ws, lin, 3, oficial, negrito)
        dif = apurado - oficial
        _num(ws, lin, 4, dif, negrito)
        pct = (dif / oficial) if oficial else 0
        _num(ws, lin, 5, pct, negrito, formato="0.0%")
        if tipo is None:
            for j in range(1, 6):
                ws.cell(lin, j).fill = CAB
        cor = OK if abs(pct) <= 0.07 else (ATENCAO if abs(pct) <= 0.15 else RUIM)
        ws.cell(lin, 5).fill = cor
        lin += 1

    lin += 1
    _txt(ws, lin, 1, "APURAÇÃO DO LIMITE", negrito=True, tamanho=10)
    lin += 1
    for rotulo, valor, fmt in (("Receita Corrente Líquida — 12 meses", RCL, FMT),
                               ("% da despesa líquida sobre a RCL", liquida / RCL, "0.00%"),
                               ("Limite legal (60% da RCL)", RCL * 0.60, FMT),
                               ("Folga / (excesso)", RCL * 0.60 - liquida, FMT)):
        _txt(ws, lin, 1, rotulo)
        _num(ws, lin, 2, valor, negrito=True, formato=fmt)
        lin += 1

    lin += 1
    pct = liquida / RCL
    _txt(ws, lin, 1, f"Situação: {'ACIMA' if pct > 0.60 else 'DENTRO'} do limite de 60%",
         negrito=True, tamanho=10,
         fill=RUIM if pct > 0.60 else OK)

    # aba de POs
    ws2 = wb.create_sheet("POs e origens")
    ws2.sheet_view.showGridLines = False
    _txt(ws2, 1, 1, "DESPESA DE PESSOAL LIQUIDADA POR PO", negrito=True, tamanho=11)
    _txt(ws2, 3, 1, "PO", negrito=True, fill=CAB)
    _txt(ws2, 3, 2, "Descrição", negrito=True, fill=CAB)
    _txt(ws2, 3, 3, "Liquidado", negrito=True, fill=CAB)
    nomes = {"10111": "Poder Executivo – Governo Estadual",
             "10112": "Poder Executivo – RPPS Estadual",
             "60611": "Defensoria Pública Estadual"}
    lin = 4
    for po, valor in sorted(r.por_po().items(), key=lambda x: -x[1]):
        _txt(ws2, lin, 1, po)
        _txt(ws2, lin, 2, nomes.get(po, "outro poder (fora do recorte)"))
        _num(ws2, lin, 3, valor)
        if po not in M.PO_EXECUTIVO:
            ws2.cell(lin, 2).fill = ATENCAO
        lin += 1
    ws2.column_dimensions["A"].width = 12
    ws2.column_dimensions["B"].width = 44
    ws2.column_dimensions["C"].width = 20

    ws.column_dimensions["A"].width = 58
    for j in "BCDE":
        ws.column_dimensions[j].width = 20

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino
