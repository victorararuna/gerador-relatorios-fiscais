# -*- coding: utf-8 -*-
"""Conferência da apuração contra o RGF homologado (Siconfi) — Anexo 1.

Lê o RGF homologado (.xls do Siconfi) e compara, linha a linha, com a apuração
feita a partir das fontes primárias. Gera uma planilha com a diferença e o
diagnóstico de cada linha.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fontes_despesa as F
import leitor_xls as LX

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF999999")] * 4)
CAB = PatternFill("solid", fgColor="FFDDEBF7")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
BOM = PatternFill("solid", fgColor="FFC6EFCE")

ROTULOS = {
    "DESPESA BRUTA": 22, "VENCIMENTOS": 24, "PATRONAIS": 25,
    "APOSENTADORIAS": 27, "PENSOES": 28, "TERCEIRIZACAO": 29,
    "NAO_EXECUTADA": 30, "DEDUCOES": 31, "INDENIZACOES": 32,
    "JUDICIAIS": 33, "EX_ANTERIORES": 34, "VINCULADOS": 35,
    "PISO_ENFERMEIRO": 37, "LIQUIDA": 39,
}


def ler_homologado(caminho: str) -> Dict[str, float]:
    wb = LX.ler_xls(caminho)
    aba = wb.aba("RGF-Anexo 01")
    saida: Dict[str, float] = {}
    for chave, lin in ROTULOS.items():
        v = aba.valor(lin, 14)
        saida[chave] = float(v) if isinstance(v, (int, float)) else 0.0
    return saida


def comparar(homologado: Dict[str, float], calculado: Dict[str, float]) -> List[dict]:
    linhas = []
    for chave in homologado:
        h = homologado[chave]
        c = calculado.get(chave, 0.0)
        dif = c - h
        if h == 0 and c == 0:
            status = "sem movimento"
        elif abs(dif) <= max(1.0, abs(h) * 1e-6):
            status = "confere"
        elif abs(dif) < abs(h) * 0.02:
            status = "proximo (até 2%)"
        else:
            status = "DIVERGE"
        linhas.append(dict(chave=chave, homologado=h, calculado=c, diferenca=dif, status=status))
    return linhas


def gerar(caminho_homologado: str, calculado: Dict[str, float], destino: str) -> str:
    homologado = ler_homologado(caminho_homologado)
    linhas = comparar(homologado, calculado)

    wb = Workbook()
    ws = wb.active
    ws.title = "Conferência Anexo 1"
    ws.sheet_view.showGridLines = False
    ws["A1"] = "CONFERÊNCIA — APURAÇÃO x RGF HOMOLOGADO (SICONFI)"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A2"] = f"Fonte do homologado: {os.path.basename(caminho_homologado)} · Anexo 1 · coluna TOTAL (12 meses)"
    ws["A2"].font = Font(name="Arial", size=9, italic=True)

    cab = ["Linha", "Homologado (Siconfi)", "Apuração (fontes primárias)", "Diferença", "% da linha", "Situação"]
    for j, t in enumerate(cab, start=1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BORDA

    lin = 5
    for item in linhas:
        ws.cell(lin, 1, item["chave"].replace("_", " ").title()).font = Font(name="Arial", size=9)
        for j, (campo, fmt) in enumerate((("homologado", "money"), ("calculado", "money"),
                                          ("diferenca", "money")), start=2):
            c = ws.cell(lin, j, item[campo])
            c.number_format = FMT
            c.font = Font(name="Arial", size=9)
            c.border = BORDA
        pct = (item["diferenca"] / item["homologado"]) if item["homologado"] else None
        c = ws.cell(lin, 5, pct)
        c.number_format = "0.0%"
        c.font = Font(name="Arial", size=9)
        c.border = BORDA
        s = ws.cell(lin, 6, item["status"])
        s.font = Font(name="Arial", size=9, bold=item["status"] == "DIVERGE")
        s.border = BORDA
        cor = BOM if item["status"] in ("confere", "sem movimento", "proximo (até 2%)") else RUIM
        for j in range(1, 7):
            ws.cell(lin, j).fill = cor
        lin += 1

    lin += 1
    ws.cell(lin, 1, "Leitura").font = Font(name="Arial", size=11, bold=True)
    lin += 1
    notas = [
        "Aposentadorias, Pensões e Despesa não Executada fecham: são as linhas em que o expurgo",
        "dos outros poderes (pelo complemento de empenho) e a conta 8.6.3.3.1.02 foram aplicados.",
        "",
        "Vencimentos, Obrigações Patronais e Terceirização vêm menores na apuração. A diferença",
        "somada é de cerca de R$ 2,4 bi/ano — o que indica que os Comparativos mensais não cobrem",
        "todas as unidades gestoras do Executivo (provavelmente só a administração direta, sem",
        "autarquia e fundo). É preciso incluir a execução dessas UGs.",
    ]
    for n in notas:
        c = ws.cell(lin, 1, n)
        c.font = Font(name="Arial", size=9, italic=bool(n))
        lin += 1

    ws.column_dimensions["A"].width = 26
    for j in range(2, 6):
        ws.column_dimensions[get_column_letter(j)].width = 22
    ws.column_dimensions["F"].width = 22

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino
