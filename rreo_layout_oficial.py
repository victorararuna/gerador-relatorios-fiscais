# -*- coding: utf-8 -*-
"""Renderiza um anexo do RREO no layout oficial, com os blocos separados.

O template do Siconfi repete as contas em blocos:

    DESPESAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)   -> ocorrencia 0
    DESPESAS (INTRA-ORÇAMENTÁRIAS) (II)         -> ocorrencia 1
    TOTAL (III) = (I + II)                      -> ocorrencia 2

`ler_template` devolve cada conta com o **tipo de bloco** em que ela aparece,
e `renderizar` preenche `{(conta, coluna, bloco): valor}`.

O molde pode ser o proprio arquivo publicado do ente (estrutura identica a que
o Siconfi espera); os valores vem do dicionario de celulas, nunca do molde.
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict

CABECALHOS = {
    "DESPESAS (EXCETO INTRA": 0,
    "RECEITAS (EXCETO INTRA": 0,
    "DESPESAS (INTRA": 1,
    "RECEITAS (INTRA": 1,
    "TOTAL (III)": 2,
    "SUBTOTAL DAS RECEITAS": 2,
    "TOTAL DAS RECEITAS": 2,
}


def _bloco(conta: str) -> int | None:
    for prefixo, bloco in CABECALHOS.items():
        if conta.startswith(prefixo):
            return bloco
    return None


def ler_template(caminho: str):
    """(colunas, [(conta, bloco), ...]) na ordem do molde.

    O arquivo publicado vem ordenado por **coluna**: dentro de cada coluna as
    contas aparecem uma vez, na ordem dos blocos. A estrutura e lida da
    **primeira coluna**, que preserva as repeticoes de uma mesma conta entre os
    blocos (I = 0, II = 1, III = 2).
    """
    colunas = []
    vistos_col = set()
    por_coluna = defaultdict(list)
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            conta = r["conta"]
            coluna = r["coluna"]
            if coluna not in vistos_col:
                vistos_col.add(coluna)
                colunas.append(coluna)
            por_coluna[coluna].append(conta)

    if not colunas:
        return [], []
    # a coluna com mais linhas e a que traz todos os blocos (inclusive o intra)
    coluna_base = max(colunas, key=lambda c: len(por_coluna[c]))
    primeira = por_coluna[coluna_base]
    linhas = []
    bloco_atual = 0
    for conta in primeira:
        b = _bloco(conta)
        if b is not None:
            bloco_atual = b
        linhas.append((conta, bloco_atual))
    return colunas, linhas


def renderizar(destino: str, template: str, celulas: dict, titulo: str,
               nota: str | None = None):
    """Grava o XLSX no layout do molde, preenchendo por (conta, coluna, bloco)."""
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

    preenchidas = total = 0
    for i, (conta, bloco) in enumerate(linhas, start=5):
        cel = ws.cell(row=i, column=1, value=conta)
        if conta.isupper():
            cel.font = Font(bold=True)
        for j, col in enumerate(colunas, start=2):
            total += 1
            v = celulas.get((conta, col, bloco))
            if v is None:
                v = celulas.get((conta, col, 0), 0.0)
            c = ws.cell(row=i, column=j, value=v)
            c.number_format = "#,##0.00"
            preenchidas += 1

    ws.column_dimensions["A"].width = 62
    largura = max(13, min(20, int(150 / max(len(colunas), 1))))
    for j in range(2, len(colunas) + 2):
        ws.column_dimensions[get_column_letter(j)].width = largura
    ws.freeze_panes = "B5"

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
