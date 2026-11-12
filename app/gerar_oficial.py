# -*- coding: utf-8 -*-
"""Gera os demonstrativos do RGF no layout oficial do Siconfi, com aba de
verificações.

Cada anexo reproduz a estrutura do arquivo homologado: bloco de identificação,
grupo/quadro/rótulo, subtítulo, cabeçalho de colunas, linhas do quadro e, no
Anexo 1, o quadro de apuração do limite.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import layout_stn as L

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF7F7F7F")] * 4)
CAB = PatternFill("solid", fgColor="FFD9E1F2")
SEC = PatternFill("solid", fgColor="FFF2F2F2")
TOT = PatternFill("solid", fgColor="FFFFF2CC")
TIT = PatternFill("solid", fgColor="FFBDD7EE")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
PCT = {"pct_dc", "pct_dcl", "limite", "limite_alerta"}


def _cabecalho_ident(ws, ncols: int) -> int:
    lin = 1
    for rotulo, valor in L.IDENTIFICACAO:
        c = ws.cell(lin, 1, rotulo)
        c.font = Font(name="Arial", size=8, bold=True)
        v = ws.cell(lin, 2, valor)
        v.font = Font(name="Arial", size=8)
        if rotulo == "RGF":
            c.font = Font(name="Arial", size=10, bold=True)
            v.font = Font(name="Arial", size=10, bold=True)
        lin += 1
    return lin + 1


def _bloco_titulo(ws, anexo: dict, lin: int, ncols: int) -> int:
    for texto, negrito in ((anexo["grupo"], False), (anexo["quadro"], False),
                           (anexo["rotulo"], False)):
        c = ws.cell(lin, 1, texto)
        c.font = Font(name="Arial", size=8, italic=not negrito)
        lin += 1
    c = ws.cell(lin, 1, anexo["titulo"])
    c.font = Font(name="Arial", size=10, bold=True)
    c.fill = TIT
    c.alignment = Alignment(horizontal="center")
    ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=ncols)
    lin += 1
    c = ws.cell(lin, 1, f"{anexo['subtitulo']}   ·   {anexo['unidade']}")
    c.font = Font(name="Arial", size=9, bold=True)
    c.alignment = Alignment(horizontal="center")
    ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=ncols)
    return lin + 2


def _cabecalho_colunas(ws, anexo: dict, lin: int) -> int:
    for j, (rotulo, largura) in enumerate(anexo["colunas"], start=1):
        c = ws.cell(lin, j, rotulo)
        c.font = Font(name="Arial", size=8, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA
        ws.column_dimensions[get_column_letter(j)].width = largura
    ws.row_dimensions[lin].height = 40
    return lin + 1


def _linha_quadro(ws, lin: int, tipo: str, rotulo: str, valor,
                  nivel: int, ncols: int, coluna_valor: int,
                  formato_pct: bool = False) -> int:
    negrito = tipo == "total"
    c = ws.cell(lin, 1, rotulo)
    c.font = Font(name="Arial", size=8, bold=negrito)
    c.alignment = Alignment(horizontal="left", vertical="center",
                            indent=nivel * 2, wrap_text=True)
    c.border = BORDA
    if negrito:
        c.fill = SEC
    if valor is not None:
        valor = round(valor, 2)
        cel = ws.cell(lin, coluna_valor, valor)
        cel.number_format = "0.00%" if formato_pct else FMT
        cel.font = Font(name="Arial", size=8, bold=negrito)
        cel.border = BORDA
        cel.fill = TOT if negrito else SEC
    if negrito:
        for j in range(1, ncols + 1):
            if ws.cell(lin, j).fill.fgColor.rgb != TOT.fgColor.rgb:
                ws.cell(lin, j).fill = SEC
    ws.row_dimensions[lin].height = 24 if len(rotulo) > 58 else 14
    return lin + 1


def _aba_anexo(wb: Workbook, anexo: dict, valores: Dict[str, float],
               nome_aba: str, colunas_extra: Dict[str, Dict[int, float]] | None = None) -> None:
    ws = wb.create_sheet(nome_aba)
    ws.sheet_view.showGridLines = False
    ncols = len(anexo["colunas"])
    col = anexo["coluna_valor"]

    lin = _cabecalho_ident(ws, ncols)
    lin = _bloco_titulo(ws, anexo, lin, ncols)
    lin = _cabecalho_colunas(ws, anexo, lin)

    for tipo, rotulo, campo, nivel in anexo["linhas"]:
        valor = valores.get(campo) if campo else None
        lin = _linha_quadro(ws, lin, tipo, rotulo, valor, nivel, ncols, col,
                            campo in PCT)
        # demais colunas (quadrimestres) - anexos patrimoniais
        if campo and colunas_extra and campo in colunas_extra:
            for c, v in colunas_extra[campo].items():
                if c == col:
                    continue
                cel = ws.cell(lin - 1, c, round(v, 2))
                cel.number_format = "0.00%" if campo in PCT else FMT
                cel.font = Font(name="Arial", size=8, bold=(tipo == "total"))
                cel.border = BORDA
                cel.fill = TOT if tipo == "total" else SEC

    # quadro de apuracao do limite (apenas Anexo 1)
    if anexo.get("limite_linhas"):
        lin += 2
        c = ws.cell(lin, 1, anexo["limite_titulo"])
        c.font = Font(name="Arial", size=9, bold=True)
        lin += 1
        for tipo, rotulo, campo, nivel in anexo["limite_linhas"]:
            valor = valores.get(campo) if campo else None
            lin = _linha_quadro(ws, lin, tipo, rotulo, valor, nivel, ncols, col,
                                campo in PCT)

    lin += 1
    nota = ws.cell(lin, 1,
                   "Fonte: Matriz de Saldos Contábeis (Siconfi). As colunas mensais "
                   "não são preenchidas porque a matriz utilizada traz o saldo acumulado "
                   "do exercício, não o movimento mês a mês.")
    nota.font = Font(name="Arial", size=7, italic=True, color="FF666666")
    nota.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=lin, start_column=1, end_row=lin, end_column=ncols)
    ws.row_dimensions[lin].height = 24


def _aba_verificacoes(wb: Workbook, dados: List[tuple]) -> None:
    ws = wb.create_sheet("Verificações")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "VERIFICAÇÕES — APURAÇÃO (MSC) x RGF HOMOLOGADO (Siconfi)"
    ws["A1"].font = Font(name="Arial", size=12, bold=True)
    ws["A2"] = ("Conferência linha a linha. Verde: desvio até 2%; amarelo: até 10%; "
                "vermelho: acima.")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, t in enumerate(["Anexo", "Linha", "Apurado (MSC)", "Homologado",
                           "Diferença", "%", "Situação"], start=1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BORDA

    lin = 5
    total_ok = 0
    for anexo, rotulo, apurado, referencia in dados:
        ws.cell(lin, 1, anexo).font = Font(name="Arial", size=8)
        ws.cell(lin, 2, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((3, round(apurado, 2)), (4, round(referencia, 2))):
            c = ws.cell(lin, j, v)
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        dif = round(apurado, 2) - round(referencia, 2)
        c = ws.cell(lin, 5, dif)
        c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        pct = (dif / referencia) if referencia else 0
        c = ws.cell(lin, 6, pct)
        c.number_format = "0.000%"
        c.font = Font(name="Arial", size=8)
        if abs(pct) <= 0.02:
            situacao, cor = "confere", OK
            total_ok += 1
        elif abs(pct) <= 0.10:
            situacao, cor = "atenção", ATEN
        else:
            situacao, cor = "divergente", RUIM
        c = ws.cell(lin, 7, situacao)
        c.font = Font(name="Arial", size=8, bold=situacao != "confere")
        for j in range(1, 8):
            ws.cell(lin, j).border = BORDA
            ws.cell(lin, j).fill = cor
        lin += 1

    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 52
    for col in "CDEFG":
        ws.column_dimensions[col].width = 17
    lin += 1
    ws.cell(lin, 1, f"Linhas que conferem (até 2%): {total_ok} de {len(dados)}"
            ).font = Font(name="Arial", size=9, bold=True)


ROTULOS_VERIFICACAO = [
    ("Anexo 1", "bruta", "Despesa Bruta com Pessoal (I)"),
    ("Anexo 1", "vencimentos", "Vencimentos, Vantagens e Outras Desp. Variáveis"),
    ("Anexo 1", "patronal", "Obrigações Patronais"),
    ("Anexo 1", "aposentadorias", "Aposentadorias, Reserva e Reformas"),
    ("Anexo 1", "pensoes", "Pensões"),
    ("Anexo 1", "terceirizacao", "Terceirização"),
    ("Anexo 1", "nao_executada", "Despesa não Executada Orçamentariamente"),
    ("Anexo 1", "deducoes", "Despesas não Computadas (II)"),
    ("Anexo 1", "judiciais", "Decisões Judiciais"),
    ("Anexo 1", "exercicios_anteriores", "Exercícios Anteriores"),
    ("Anexo 1", "indenizacoes", "Indenizações por Demissão"),
    ("Anexo 1", "vinculados", "Inativos e Pensionistas Vinculados"),
    ("Anexo 1", "piso_enfermagem", "Piso do Enfermeiro"),
    ("Anexo 1", "liquida", "Despesa Líquida (III)"),
    ("Anexo 1", "rcl_ajustada", "RCL Ajustada (VI)"),
    ("Anexo 1", "dtp", "Despesa Total com Pessoal (DTP)"),
    ("Anexo 2", "divida", "Dívida Consolidada (I)"),
    ("Anexo 2", "deducoes_dcl", "Deduções (II)"),
    ("Anexo 2", "dcl", "Dívida Consolidada Líquida (III)"),
    ("Anexo 3", "gar_total", "Total das Garantias Concedidas (V)"),
    ("Anexo 3", "gar_rcl_ajustada", "RCL Ajustada (VIII)"),
    ("Anexo 3", "gar_limite", "Limite das Garantias (22%)"),
    ("Anexo 3", "contra_total", "Total das Contragarantias Recebidas (XIII)"),
    ("Anexo 4", "oc_total", "Total das Operações de Crédito (III)"),
    ("Anexo 4", "oc_considerado", "Total considerado para o limite (VIII)"),
    ("Anexo 4", "oc_limite", "Limite geral (16% da RCL ajustada)"),
    ("Anexo 5", "a5_nao_vinculados", "Recursos Não Vinculados (I)"),
    ("Anexo 5", "a5_rpps", "Recursos Vinculados ao RPPS (III)"),
    ("Anexo 6", "a6_oc", "Anexo 6 — Operações de Crédito"),
    ("Anexo 6", "a6_rp", "Anexo 6 — Restos a Pagar Empenhados"),
]


def gerar(destino: str, valores1: Dict[str, float], valores2: Dict[str, float],
          valores3: Dict[str, float] | None = None,
          colunas2: Dict[str, Dict[int, float]] | None = None,
          valores4: Dict[str, float] | None = None,
          mensais1: Dict[str, Dict[int, float]] | None = None,
          colunas3: Dict[str, Dict[int, float]] | None = None,
          colunas4: Dict[str, Dict[int, float]] | None = None,
          valores5: Dict[str, float] | None = None,
          valores6: Dict[str, float] | None = None) -> str:
    wb = Workbook()
    wb.remove(wb.active)
    _aba_anexo(wb, L.ANEXO1, valores1, "RGF-Anexo 01", mensais1)
    _aba_anexo(wb, L.ANEXO2, valores2, "RGF-Anexo 02", colunas2)
    if valores3 is not None:
        _aba_anexo(wb, L.ANEXO3, valores3, "RGF-Anexo 03", colunas3)
    if valores4 is not None:
        _aba_anexo(wb, L.ANEXO4, valores4, "RGF-Anexo 04", colunas4)
    if valores5 is not None:
        _aba_anexo(wb, L.ANEXO5, valores5, "RGF-Anexo 05")
    if valores6 is not None:
        _aba_anexo(wb, L.ANEXO6, valores6, "RGF-Anexo 06")

    mapa = {"Anexo 1": valores1, "Anexo 2": valores2, "Anexo 3": valores3 or {},
            "Anexo 4": valores4 or {}, "Anexo 5": valores5 or {},
            "Anexo 6": valores6 or {}}
    dados = []
    for anexo, campo, rotulo in ROTULOS_VERIFICACAO:
        valores = mapa[anexo]
        ref = L.REFERENCIA[anexo].get(campo)
        if ref is not None:
            dados.append((anexo, rotulo, valores.get(campo, 0.0), ref))
    _aba_verificacoes(wb, dados)

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino
