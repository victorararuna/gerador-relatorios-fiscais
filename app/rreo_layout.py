# -*- coding: utf-8 -*-
"""Renderiza os anexos do RREO no layout oficial.

O molde é o **próprio arquivo do Siconfi** de um período anterior (a estrutura é
estável): o renderizador mantém linhas e colunas na ordem oficial e preenche
apenas as células que sabemos apurar. O resto fica em branco, com a cobertura
reportada.

    from rreo_layout import gerar_workbook
    gerar_workbook(destino, [("Anexo 07", molde_csv, celulas, "título")])
"""
from __future__ import annotations

import csv
import os
from collections import OrderedDict
from typing import Dict, List, Optional, Sequence, Tuple

Celulas = Dict[Tuple[str, str], float]


def ler_template(caminho: str) -> Tuple[List[str], "OrderedDict[str, List[str]]"]:
    colunas: List[str] = []
    linhas: "OrderedDict[str, List[str]]" = OrderedDict()
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            col, conta = r["coluna"], r["conta"]
            if col not in colunas:
                colunas.append(col)
            linhas.setdefault(conta, [])
            if col not in linhas[conta]:
                linhas[conta].append(col)
    return colunas, linhas


def _montar_aba(ws, template: str, valores: Celulas, titulo: str,
                nota: Optional[str], colunas: Optional[Sequence[str]]):
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    colunas_tpl, linhas = ler_template(template)
    if colunas:
        colunas_tpl = [c for c in colunas_tpl if c in colunas]

    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=12)
    if nota:
        ws["A2"] = nota
        ws["A2"].font = Font(italic=True, size=8, color="666666")

    negrito = Font(bold=True)
    cinza = PatternFill("solid", fgColor="EDEDED")
    cab = ws.cell(row=4, column=1, value="CONTA")
    cab.font = negrito
    cab.fill = cinza
    for j, col in enumerate(colunas_tpl, start=2):
        c = ws.cell(row=4, column=j, value=col)
        c.font = negrito
        c.fill = cinza
        c.alignment = Alignment(wrap_text=True, vertical="center",
                                horizontal="center")

    preenchidas = total = 0
    for i, (conta, _cols) in enumerate(linhas.items(), start=5):
        ws.cell(row=i, column=1, value=conta)
        for j, col in enumerate(colunas_tpl, start=2):
            total += 1
            v = valores.get((conta, col))
            if v is None:
                continue
            cel = ws.cell(row=i, column=j, value=v)
            cel.number_format = "#,##0.00"
            preenchidas += 1

    ws.column_dimensions["A"].width = 58
    largura = max(14, min(22, int(150 / max(len(colunas_tpl), 1))))
    for j in range(2, len(colunas_tpl) + 2):
        ws.column_dimensions[get_column_letter(j)].width = largura
    ws.freeze_panes = "B5"
    return preenchidas, total


def gerar_workbook(destino: str, anexos: Sequence[Tuple[str, str, Celulas, str]],
                   nota: Optional[str] = None,
                   colunas: Optional[Sequence[str]] = None) -> str:
    """Gera um XLSX com uma aba por anexo, no layout do molde informado."""
    from openpyxl import Workbook
    from openpyxl.styles import Font

    wb = Workbook()
    wb.remove(wb.active)
    cobertura = []
    for nome_aba, template, valores, titulo in anexos:
        ws = wb.create_sheet(nome_aba[:31])
        p, t = _montar_aba(ws, template, valores, titulo, nota, colunas)
        cobertura.append((nome_aba, p, t))

    ws = wb.create_sheet("Cobertura", 0)
    ws["A1"] = "Cobertura do layout"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A3"] = "Aba"
    ws["B3"] = "Preenchidas"
    ws["C3"] = "No molde"
    ws["D3"] = "Cobertura"
    for c in ("A3", "B3", "C3", "D3"):
        ws[c].font = Font(bold=True)
    for i, (nome, p, t) in enumerate(cobertura, start=4):
        ws.cell(row=i, column=1, value=nome)
        ws.cell(row=i, column=2, value=p)
        ws.cell(row=i, column=3, value=t)
        ws.cell(row=i, column=4, value=f"{p / t * 100:.1f}%" if t else "0%")
    ws.column_dimensions["A"].width = 18
    for col in ("B", "C", "D"):
        ws.column_dimensions[col].width = 14
    ws.cell(row=len(cobertura) + 6, column=1,
            value="Células em branco são as que a matriz não apura "
                  "(receita, RCL, detalhe por Poder).").font = Font(italic=True, size=9)

    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    wb.save(destino)
    return destino
