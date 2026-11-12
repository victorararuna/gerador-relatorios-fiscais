# -*- coding: utf-8 -*-
"""Apuração do RGF Anexo 1 (Despesa com Pessoal) a partir das fontes primárias.

Gera uma planilha de trabalho com:
  - Quadro 1 no formato do MDF 14ª edição (2024), 12 colunas mensais;
  - a RCL apurada no RREO Anexo 3 (6º bimestre de 2024);
  - o mapa de subelementos de obrigações patronais por poder;
  - cenários de dedução (inativos vinculados x inativos dos outros poderes).

Não substitui o demonstrativo oficial: mostra a origem de cada número e o efeito
de cada critério de dedução, para que a decisão fique explícita.
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

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF999999")] * 4)
CAB = PatternFill("solid", fgColor="FFDDEBF7")
PEND = PatternFill("solid", fgColor="FFFFF2CC")
OK = PatternFill("solid", fgColor="FFE2EFDA")


def _cab(ws, linha: int, textos: List[str]) -> None:
    for j, t in enumerate(textos, start=1):
        c = ws.cell(linha, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA
    ws.row_dimensions[linha].height = 30


def _moeda(ws, linha: int, col: int, valor: Optional[float], negrito: bool = False) -> None:
    c = ws.cell(linha, col, valor)
    c.number_format = FMT
    c.font = Font(name="Arial", size=9, bold=negrito)
    c.border = BORDA


# subelementos de 31.91.13 que identificam cada poder (lidos das planilhas por poder)
SUBS_PODER = {
    "ALRN": ["31.91.13.22", "31.91.13.43", "31.91.13.49"],
    "TCERN": ["31.91.13.23", "31.91.13.44", "31.91.13.50"],
    "TJRN": ["31.91.13.24", "31.91.13.45", "31.91.13.51"],
    "MPRN": ["31.91.13.25", "31.91.13.48", "31.91.13.53"],
    "DPRN": ["31.91.13.13", "31.91.13.43", "31.91.13.46"],
}

RCL_2024 = 17259989216.73


def patronal_outros_poderes(res: F.Resultado) -> Dict[str, float]:
    saida: Dict[str, float] = {}
    for poder, subs in SUBS_PODER.items():
        total = 0.0
        for sub in subs:
            s = res.por_natureza.get(sub)
            if s:
                total += s.total()
        saida[poder] = total
    return saida


def gerar(pasta_entrada: str, destino: str, rcl: Optional[float] = RCL_2024,
          exercicio: int = 2024) -> str:
    res = F.ler_comparativos(pasta_entrada)
    linhas = F.quadro1(res)
    t = F.totais(linhas)
    pat = patronal_outros_poderes(res)
    wb = Workbook()

    # ---------------------------------------------------------------- Quadro 1
    ws = wb.active
    ws.title = "Quadro 1 (MDF)"
    ws.sheet_view.showGridLines = False
    ws["A1"] = "DEMONSTRATIVO DA DESPESA COM PESSOAL — RGF Anexo 1"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A2"] = (f"Governo do Estado do Rio Grande do Norte · Poder Executivo · exercício {exercicio} · "
                "3º quadrimestre (últimos 12 meses: jan a dez)")
    ws["A2"].font = Font(name="Arial", size=9)
    ws["A3"] = "MDF 14ª edição (vigente em 2024) · valores LIQUIDADOS · R$ 1,00"
    ws["A3"].font = Font(name="Arial", size=9, italic=True)

    _cab(ws, 5, ["DISCRIMINAÇÃO", "ORIGEM (natureza da despesa)"] +
         [f"MR{-11 + i}" if i < 11 else "MR" for i in range(12)] + ["TOTAL (12 meses)", "SITUAÇÃO"])

    lin = 6
    for item in linhas:
        s = item["serie"]
        grupo = item["pendente"] and not item["detalhe"]
        c = ws.cell(lin, 1, item["rotulo"])
        c.font = Font(name="Arial", size=9, bold=grupo)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True,
                                indent=0 if grupo else 2)
        ws.cell(lin, 2, item["detalhe"] or "—").font = Font(name="Arial", size=8)
        for i in range(12):
            cel = ws.cell(lin, 3 + i, s.liquidada[i])
            cel.number_format = FMT
            cel.font = Font(name="Arial", size=8)
        _moeda(ws, lin, 15, s.total() if not item["pendente"] else None, negrito=True)
        sit = ws.cell(lin, 16, "pendente de definição" if item["pendente"] else "apurado")
        sit.font = Font(name="Arial", size=9, bold=item["pendente"],
                        color="FFC00000" if item["pendente"] else "FF375623")
        for j in range(1, 17):
            ws.cell(lin, j).border = BORDA
            if item["pendente"]:
                ws.cell(lin, j).fill = PEND
        lin += 1

    lin += 1
    for rotulo, valor, negrito in (
            ("DESPESA BRUTA COM PESSOAL (I)", t["bruta"], True),
            ("DESPESAS NÃO COMPUTADAS (II) — parcela apurada", t["deducao"], False),
            ("DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)", t["liquida"], True)):
        c = ws.cell(lin, 1, rotulo)
        c.font = Font(name="Arial", size=10 if negrito else 9, bold=negrito)
        c.alignment = Alignment(horizontal="left", vertical="center")
        _moeda(ws, lin, 15, valor, negrito=negrito)
        if negrito:
            ws.cell(lin, 1).fill = OK
            ws.cell(lin, 15).fill = OK
        lin += 1

    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 30
    for j in range(3, 15):
        ws.column_dimensions[get_column_letter(j)].width = 15
    ws.column_dimensions["O"].width = 18
    ws.column_dimensions["P"].width = 21
    ws.freeze_panes = "C6"

    # ---------------------------------------------------------------- RCL e limite
    ws2 = wb.create_sheet("RCL e limite")
    ws2.sheet_view.showGridLines = False
    ws2["A1"] = "RECEITA CORRENTE LÍQUIDA E APURAÇÃO DO LIMITE"
    ws2["A1"].font = Font(name="Arial", size=13, bold=True)
    ws2["A2"] = ("RCL apurada no RREO Anexo 3 (LRF, art. 53, I) — 6º bimestre de 2024, coluna dos "
                 "últimos 12 meses. Limite: art. 20, III, 'c', da LRF (60% para os Estados).")
    ws2["A2"].font = Font(name="Arial", size=9, italic=True)
    ws2["A2"].alignment = Alignment(wrap_text=True)
    ws2.merge_cells("A2:D2")
    ws2.row_dimensions[2].height = 28

    _cab(ws2, 4, ["Item", "Valor", "% da RCL", "Observação"])
    lin = 5
    limite = rcl * 0.6 if rcl else None
    dados_rcl = [
        ("Receita Corrente Líquida (III)", rcl, None, "RREO Anexo 3, linha 'RCL (III)'"),
        ("Despesa líquida com pessoal (III)", t["liquida"],
         (t["liquida"] / rcl if rcl else None), "Quadro 1 (sem as deduções pendentes)"),
        ("Limite legal — 60% da RCL", limite, 0.6, "art. 20, III, 'c', da LRF"),
        ("Excedente / (folga)", (t["liquida"] - limite if limite else None), None,
         "negativo indica folga"),
    ]
    for nome, valor, pct, obs in dados_rcl:
        ws2.cell(lin, 1, nome).font = Font(name="Arial", size=9, bold=True)
        _moeda(ws2, lin, 2, valor)
        if pct is not None:
            c = ws2.cell(lin, 3, pct)
            c.number_format = "0.0%"
            c.font = Font(name="Arial", size=9, bold=True,
                          color="FFC00000" if pct > 0.6 else "FF375623")
            c.border = BORDA
        ws2.cell(lin, 4, obs).font = Font(name="Arial", size=8)
        lin += 1
    ws2.column_dimensions["A"].width = 44
    ws2.column_dimensions["B"].width = 20
    ws2.column_dimensions["C"].width = 14
    ws2.column_dimensions["D"].width = 40

    # ---------------------------------------------------------------- deduções
    ws3 = wb.create_sheet("Deduções")
    ws3.sheet_view.showGridLines = False
    ws3["A1"] = "DEDUÇÕES — O QUE JÁ ESTÁ APURADO E O QUE DEPENDE DE CRITÉRIO"
    ws3["A1"].font = Font(name="Arial", size=13, bold=True)

    lin = 3
    ws3.cell(lin, 1, "1. Obrigações patronais dos outros poderes (dedução pelo subelemento de 31.91.13)").font = Font(name="Arial", size=10, bold=True)
    lin += 1
    _cab(ws3, lin, ["Poder", "Subelementos", "Valor liquidado 2024"])
    lin += 1
    for poder, valor in pat.items():
        ws3.cell(lin, 1, poder).font = Font(name="Arial", size=9)
        ws3.cell(lin, 2, ", ".join(SUBS_PODER[poder])).font = Font(name="Arial", size=8)
        _moeda(ws3, lin, 3, valor)
        lin += 1
    c = ws3.cell(lin, 1, "Subtotal")
    c.font = Font(name="Arial", size=9, bold=True)
    _moeda(ws3, lin, 3, sum(pat.values()), negrito=True)
    lin += 3

    ws3.cell(lin, 1, "2. Cenários para a despesa líquida").font = Font(name="Arial", size=10, bold=True)
    lin += 1
    _cab(ws3, lin, ["Critério", "Dedução de inativos/pensionistas", "Despesa líquida", "% da RCL"])
    lin += 1
    ap = res.por_natureza.get("31.90.01.00")
    pe = res.por_natureza.get("31.90.03.00")

    def _soma(s, prefixos):
        if not s:
            return 0.0
        return sum(v for f, v in s.por_fonte.items() if any(f.startswith(p) for p in prefixos))

    base_ded = t["deducao"] + sum(pat.values())
    cenarios = [
        ("Só outros poderes (sem dedução de vinculados)", 0.0),
        ("+ dedução da fonte 0.8 (RPPS)", _soma(ap, ["0.8"]) + _soma(pe, ["0.8"])),
        ("+ dedução de todas as fontes (inativos integrais)",
         _soma(ap, ["0.8", "0.5", "0.6", "1.0", "0.7"]) + _soma(pe, ["0.8", "0.5", "0.6", "1.0", "0.7"])),
    ]
    for nome, vinc in cenarios:
        liq = t["bruta"] - base_ded - vinc
        ws3.cell(lin, 1, nome).font = Font(name="Arial", size=9)
        _moeda(ws3, lin, 2, vinc)
        _moeda(ws3, lin, 3, liq, negrito=True)
        if rcl:
            c = ws3.cell(lin, 4, liq / rcl)
            c.number_format = "0.0%"
            c.font = Font(name="Arial", size=9, bold=True,
                          color="FFC00000" if liq / rcl > 0.6 else "FF375623")
            c.border = BORDA
        for j in range(1, 5):
            ws3.cell(lin, j).fill = PEND
            ws3.cell(lin, j).border = BORDA
        lin += 1

    lin += 1
    ws3.cell(lin, 1, "A escolha do critério é do gestor. A LRF (art. 19, § 2º) permite deduzir as "
                     "despesas com inativos e pensionistas custeadas com recursos vinculados ao RPPS.").font = Font(name="Arial", size=9, italic=True)
    ws3.column_dimensions["A"].width = 52
    ws3.column_dimensions["B"].width = 30
    ws3.column_dimensions["C"].width = 20
    ws3.column_dimensions["D"].width = 14

    # ---------------------------------------------------------------- séries
    ws4 = wb.create_sheet("Séries mensais")
    ws4.sheet_view.showGridLines = False
    _cab(ws4, 1, ["Natureza"] + [F.MESES[i][:3].title() for i in range(12)] + ["Total"])
    lin = 2
    for nat in sorted(res.por_natureza):
        s = res.por_natureza[nat]
        ws4.cell(lin, 1, nat).font = Font(name="Arial", size=8)
        for i in range(12):
            c = ws4.cell(lin, 2 + i, s.liquidada[i])
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        _moeda(ws4, lin, 14, s.total())
        lin += 1
    ws4.column_dimensions["A"].width = 15
    for j in range(2, 15):
        ws4.column_dimensions[get_column_letter(j)].width = 14
    ws4.freeze_panes = "B2"

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino


if __name__ == "__main__":
    entrada = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\victo\AppData\Local\Temp"
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saida", "RGF_2024_Q3_Anexo1_APURACAO.xlsx")
    print(gerar(entrada, saida))
