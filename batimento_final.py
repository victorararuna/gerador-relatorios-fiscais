# -*- coding: utf-8 -*-
"""Batimento final de 2025 — apurado contra o homologado do Siconfi.

Compara:
  * RGF Anexo 1 — despesa com pessoal (acervo da MSC + balancete)
  * RGF Anexo 4 — operações de crédito (comparativo × Siconfi)
  * RGF Anexo 6 — limites (RCL)
  * RREO Anexo 3 — RCL

Gera `saida/BATIMENTO_2025.xlsx` com três abas: Resumo, RGF e RREO.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import balancete
import msc_receita
import siconfi_declaracao as S
from acervo import Acervo, janela_do_quadrimestre
from gerar_anexo1_acervo import apurar_com_mensal

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF808080")] * 4)
CAB = PatternFill("solid", fgColor="FFD9E1F2")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")
BALANCETE = r"C:\Users\victo\Downloads\Imprimir Balancete Consolidado.xls"
RECEITA_2025 = r"C:\Users\victo\Downloads\Comparativo da Receita Orçada com a Arrecadada (1).xls"

ANO, QUADRIMESTRE = 2026, 2


def classif(pct):
    if pct is None:
        return "não apurável", CINZA
    if abs(pct) <= 0.005:
        return "fecha", OK
    if abs(pct) <= 0.02:
        return "confere", OK
    if abs(pct) <= 0.10:
        return "atenção", ATEN
    return "divergente", RUIM


def apurar_2025():
    acervo = Acervo(ACERVO)
    janela = janela_do_quadrimestre(ANO, QUADRIMESTRE, acervo)
    r, _mensal = apurar_com_mensal(acervo, janela)
    # O balancete so serve se for do mesmo exercicio: a conta 8.6.3.3.1 zera no
    # encerramento e o movimento e a despesa nao executada do ano.
    ne = 0.0
    if os.path.exists(BALANCETE) and balancete.ano_base(BALANCETE) == str(ANO):
        ne = balancete.nao_executada(BALANCETE)
    r["nao_executada"] = ne
    r["bruta"] = (r["vencimentos"] + r.get("patronal", 0.0)
                  + r.get("aposentadorias", 0.0) + r.get("pensoes", 0.0)
                  + r.get("terceirizacao", 0.0) + ne)
    # deducoes e liquida ja vem calculadas pelo motor (incluem as judiciais)
    return r, janela


def main() -> int:
    r, janela = apurar_2025()
    ref = S.referencia_rgf(ANO, QUADRIMESTRE)

    linhas = [
        ("RGF A1", "Despesa Bruta com Pessoal (I)", r["bruta"], ref["bruta"]),
        ("RGF A1", "Vencimentos", r["vencimentos"], ref["vencimentos"]),
        ("RGF A1", "Obrigações Patronais", r.get("patronal", 0.0), ref["patronal"]),
        ("RGF A1", "Aposentadorias", r.get("aposentadorias", 0.0), ref["aposentadorias"]),
        ("RGF A1", "Pensões", r.get("pensoes", 0.0), ref["pensoes"]),
        ("RGF A1", "Terceirização", r.get("terceirizacao", 0.0), ref["terceirizacao"]),
        ("RGF A1", "Despesa não Executada", r["nao_executada"], ref["nao_executada"]),
        ("RGF A1", "Despesas não Computadas (II)", r["deducoes"], ref["deducoes"]),
        ("RGF A1", "Despesa Líquida (III)", r["liquida"], ref["liquida"]),
        ("RGF A1", "Inativos e Pensionistas Vinculados", r.get("vinculados", 0.0), ref["vinculados"]),
        ("RGF A1", "Piso do Enfermeiro", r.get("enfermagem", 0.0), ref["enfermagem"]),
    ]

    wb = Workbook()
    wb.remove(wb.active)

    # ---------- Resumo ----------
    ws = wb.create_sheet("Resumo")
    ws.sheet_view.showGridLines = False
    ws["A1"] = f"BATIMENTO {ANO} Q{QUADRIMESTRE} — apurado x homologado"
    ws["A1"].font = Font(name="Arial", size=14, bold=True)
    ws.merge_cells("A1:F1")
    ws["A2"] = ("Apurado: acervo da MSC (janela 12 meses, movimento líquido) + "
                "balancete de encerramento. Homologado: API do Siconfi.")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)
    ws.merge_cells("A2:F2")

    for j, t in enumerate(["Bloco", "Itens", "Fecham", "Atenção", "Divergem", "Situação"], 1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.border = BORDA
        c.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(j)].width = 22 if j == 1 else 12

    contagem = {}
    for bloco, rotulo, ap, of in linhas:
        if of is None or ap is None:
            continue
        pct = (ap - of) / of if of else 0.0
        _, cor = classif(pct)
        d = contagem.setdefault(bloco, [0, 0, 0])
        d[0] += 1
        if abs(pct) <= 0.02:
            d[1] += 1
        elif abs(pct) <= 0.10:
            d[2] += 1
        else:
            d[2] += 1

    lin = 5
    for bloco, (tot, ok, naook) in contagem.items():
        ws.cell(lin, 1, bloco).font = Font(name="Arial", size=9, bold=True)
        ws.cell(lin, 2, tot).font = Font(name="Arial", size=9)
        ws.cell(lin, 3, ok).font = Font(name="Arial", size=9)
        ws.cell(lin, 4, naook).font = Font(name="Arial", size=9)
        c = ws.cell(lin, 6, "fecha" if naook == 0 else "atenção")
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = OK if naook == 0 else ATEN
        for j in range(1, 7):
            ws.cell(lin, j).border = BORDA
        lin += 1

    # ---------- RGF ----------
    ws2 = wb.create_sheet("RGF")
    ws2.sheet_view.showGridLines = False
    ws2["A1"] = "RGF 2025 Q3 — Anexo 1, linha a linha"
    ws2["A1"].font = Font(name="Arial", size=12, bold=True)
    for j, t in enumerate(["Bloco", "Linha", "Apurado", "Homologado", "Diferença", "%", "Situação"], 1):
        c = ws2.cell(3, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.border = BORDA
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for j, w in ((1, 10), (2, 46), (3, 18), (4, 18), (5, 16), (6, 10), (7, 14)):
        ws2.column_dimensions[get_column_letter(j)].width = w

    lin = 4
    for bloco, rotulo, ap, of in linhas:
        pct = None
        if ap is not None and of:
            pct = (ap - of) / of
        sit, cor = classif(pct)
        ws2.cell(lin, 1, bloco).font = Font(name="Arial", size=8)
        ws2.cell(lin, 2, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((3, ap), (4, of)):
            c = ws2.cell(lin, j, round(v, 2) if v is not None else "—")
            if v is not None:
                c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        c = ws2.cell(lin, 5, round(ap - of, 2) if (ap is not None and of) else "—")
        if ap is not None and of:
            c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        c = ws2.cell(lin, 6, pct if pct is not None else "—")
        c.number_format = "0.00%"
        c.font = Font(name="Arial", size=8)
        c = ws2.cell(lin, 7, sit)
        c.font = Font(name="Arial", size=8, bold=sit not in ("fecha", "confere"))
        c.fill = cor
        for j in range(1, 8):
            ws2.cell(lin, j).border = BORDA
        lin += 1

    # ---------- Cruzamento entre relatórios ----------
    ws3 = wb.create_sheet("Cruzamento")
    ws3.sheet_view.showGridLines = False
    ws3["A1"] = "Cruzamento entre os relatórios"
    ws3["A1"].font = Font(name="Arial", size=12, bold=True)
    for j, t in enumerate(["Origem", "Item", "Valor", "Outra origem", "Valor", "Diferença", "Situação"], 1):
        c = ws3.cell(3, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.border = BORDA
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for j, w in ((1, 22), (2, 34), (3, 18), (4, 22), (5, 18), (6, 16), (7, 14)):
        ws3.column_dimensions[get_column_letter(j)].width = w

    oc_siconfi = S.rgf("RGF-Anexo 04", ANO, QUADRIMESTRE).valor(
        "TOTAL (III)", "Até o Quadrimestre de Referência (a)")
    oc_receita = msc_receita.apurar(RECEITA_2025)["operacoes_credito"] if os.path.exists(RECEITA_2025) else None
    rcl_ref = ref["rcl"]

    cruz = [
        ("RGF Anexo 4", "Operações de crédito (até o quadrimestre)", oc_siconfi,
         "Comparativo da Receita 4.2.1", oc_receita),
        ("RGF Anexo 4", "RCL (IV)", rcl_ref, "RREO Anexo 3 (RCL)", None),
        ("RGF Anexo 6", "Despesa Total com Pessoal (DTP)", ref["dtp"],
         "RGF Anexo 1 (III)", ref["liquida"]),
    ]

    lin = 4
    for origem, item, v1, origem2, v2 in cruz:
        ws3.cell(lin, 1, origem).font = Font(name="Arial", size=8)
        ws3.cell(lin, 2, item).font = Font(name="Arial", size=8)
        c = ws3.cell(lin, 3, round(v1, 2) if v1 is not None else "—")
        if v1 is not None:
            c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        ws3.cell(lin, 4, origem2).font = Font(name="Arial", size=8)
        c = ws3.cell(lin, 5, round(v2, 2) if v2 is not None else "—")
        if v2 is not None:
            c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        if v1 is not None and v2 is not None:
            dif = v1 - v2
            c = ws3.cell(lin, 6, round(dif, 2))
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
            pct = dif / v2 if v2 else None
            sit, cor = classif(pct)
        else:
            sit, cor = "sem par", CINZA
        c = ws3.cell(lin, 7, sit)
        c.font = Font(name="Arial", size=8, bold=True)
        c.fill = cor
        for j in range(1, 8):
            ws3.cell(lin, j).border = BORDA
        lin += 1

    destino = os.path.join(RAIZ, "saida", "BATIMENTO_2025.xlsx")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    wb.save(destino)
    print(f"gerado: {destino}")

    # console
    print()
    print(f"{'linha':40}{'apurado':>18}{'homologado':>18}{'%':>9}")
    print("-" * 86)
    for bloco, rotulo, ap, of in linhas:
        pct = (ap - of) / of if (ap is not None and of) else None
        s_ap = f"{ap:,.2f}" if ap is not None else "-"
        s_of = f"{of:,.2f}" if of is not None else "-"
        s_pct = f"{pct*100:+.2f}%" if pct is not None else "-"
        print(f"{rotulo[:40]:40}{s_ap:>18}{s_of:>18}{s_pct:>9}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
