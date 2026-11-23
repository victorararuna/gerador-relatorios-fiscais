# -*- coding: utf-8 -*-
"""Renderiza um anexo do RREO no layout oficial preservando as linhas (rodada 178).

O renderizador antigo (`rreo_layout._montar_aba`) guardava as linhas num `dict`,
o que **colapsava os rotulos repetidos** — o Anexo 1 tem os grupos de despesa em
dois blocos (exceto intra e intra) e o resultado saia com uma linha so.

Este renderizador le o template como **lista ordenada**, conta a ocorrencia de
cada (conta, coluna) e preenche `{(conta, coluna, ocorrencia): valor}`.
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict


def ler_template(caminho: str):
    """(colunas, linhas) — uma linha por conta, na ordem do template.

    O template oficial repete as contas em blocos (exceto intra, intra, total).
    Como o valor de cada conta ja e o total do bloco calculado, a versao limpa
    mostra uma linha por conta. A ocorrencia fica disponivel no dicionario de
    celulas para quem quiser separar os blocos.
    """
    colunas = []
    vistos_col = set()
    linhas = []
    vistos = set()
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            conta = r["conta"]
            coluna = r["coluna"]
            if coluna not in vistos_col:
                vistos_col.add(coluna)
                colunas.append(coluna)
            if conta not in vistos and not conta.startswith(
                    ("DESPESAS (EXCETO", "DESPESAS (INTRA", "TOTAL (III)")):
                vistos.add(conta)
                linhas.append(conta)
    return colunas, linhas


def renderizar(destino: str, template: str, celulas: dict, titulo: str,
               nota: str | None = None, ocorrencia_por_conta: bool = True):
    """Grava o XLSX no layout do template, preenchendo por ocorrencia."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    colunas, linhas = ler_template(template)
    wb = Workbook()
    ws = wb.active
    ws.title = "Anexo"

    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=12)
    if nota:
        ws["A2"] = nota
        ws["A2"].font = Font(italic=True, size=8, color="666666")

    cinza = PatternFill("solid", fgColor="EDEDED")
    ws.cell(row=4, column=1, value="CONTA").font = Font(bold=True)
    ws.cell(row=4, column=1).fill = cinza
    for j, col in enumerate(colunas, start=2):
        c = ws.cell(row=4, column=j, value=col)
        c.font = Font(bold=True)
        c.fill = cinza
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

    ocorr = defaultdict(int)
    # linhas que o calculo cobre (tem alguma celula): as demais colunas sao 0
    linhas_cobertas = {(c, o) for (c, _col, o) in celulas}
    preenchidas = total = 0
    for i, conta in enumerate(linhas, start=5):
        ws.cell(row=i, column=1, value=conta)
        occ = ocorr[conta] if ocorrencia_por_conta else 0
        ocorr[conta] += 1
        cobre = (conta, occ) in linhas_cobertas
        for j, col in enumerate(colunas, start=2):
            total += 1
            v = celulas.get((conta, col, occ))
            if v is None and ocorrencia_por_conta:
                v = celulas.get((conta, col, 0))
            if v is None:
                if not cobre:
                    v = 0.0      # linha do template sem movimento: zero
                else:
                    v = 0.0      # linha calculada: coluna nao prevista = zero
            cel = ws.cell(row=i, column=j, value=v)
            cel.number_format = "#,##0.00"
            preenchidas += 1

    ws.column_dimensions["A"].width = 60
    largura = max(13, min(20, int(150 / max(len(colunas), 1))))
    for j in range(2, len(colunas) + 2):
        ws.column_dimensions[get_column_letter(j)].width = largura
    ws.freeze_panes = "B5"

    # aba de cobertura
    cob = wb.create_sheet("Cobertura")
    cob["A1"] = "Cobertura do layout"
    cob["A1"].font = Font(bold=True, size=12)
    cob["A3"], cob["B3"] = "Preenchidas", "No molde"
    cob["A4"], cob["B4"] = preenchidas, total
    cob["A5"], cob["B5"] = "Cobertura", f"{preenchidas / total * 100:.1f}%" if total else "0%"
    cob.column_dimensions["A"].width = 16
    cob.column_dimensions["B"].width = 16

    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    wb.save(destino)
    return preenchidas, total
