# -*- coding: utf-8 -*-
"""Gera o Anexo 1 por Poder (7 POs) e o consolidado, em um único XLSX.

    python gerar_anexo1_poderes.py --ano 2025 --quadrimestre 3
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402
from app.relatorio_anexo1 import linhas_anexo1  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
SAIDA = os.path.join(AQUI, "saida")

#: Poder/Órgão -> nome
PODERES = {
    "10111": "Executivo — Governo",
    "10112": "Executivo — RPPS",
    "60611": "Defensoria Pública",
    "20211": "Legislativo — Assembleia",
    "20212": "Legislativo — Tribunal de Contas",
    "30390": "Judiciário",
    "50511": "Ministério Público",
}


def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Anexo 1 por Poder.")
    ap.add_argument("--raiz", default=MSC)
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--quadrimestre", type=int, default=3)
    args = ap.parse_args()

    acervo = M.Acervo(args.raiz)
    mes_fim = M.MES_DO_QUADRIMESTRE[args.quadrimestre]
    pares = M.periodos_janela(args.ano, mes_fim)

    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    wb.remove(wb.active)

    consolidado = {}
    for po, nome in PODERES.items():
        res = M.apurar_janela(acervo, args.ano, mes_fim, (po,))
        ded = M.deducoes(acervo, pares, (po,))
        ne = M.nao_executada(acervo, pares, (po,))
        linhas = linhas_anexo1(res, ded, ne)
        for ln in linhas:
            consolidado[ln.chave] = consolidado.get(ln.chave, 0.0) + ln.valor

        ws = wb.create_sheet(nome[:31])
        ws["A1"] = f"RGF — Anexo 1 — {nome} ({po}) — {args.ano} Q{args.quadrimestre}"
        ws["A1"].font = Font(bold=True, size=12)
        ws["A3"] = "Descrição"
        ws["B3"] = "Valor apurado"
        for c in ("A3", "B3"):
            ws[c].font = Font(bold=True)
            ws[c].fill = PatternFill("solid", fgColor="EDEDED")
        for i, ln in enumerate(linhas, start=4):
            ws.cell(row=i, column=1, value=("    " * ln.nivel) + ln.descricao)
            cel = ws.cell(row=i, column=2, value=ln.valor)
            cel.number_format = "#,##0.00"
            if ln.total:
                ws.cell(row=i, column=1).font = Font(bold=True)
                ws.cell(row=i, column=2).font = Font(bold=True)
        ws.column_dimensions["A"].width = 72
        ws.column_dimensions["B"].width = 22

    ws = wb.create_sheet("Consolidado")
    ws["A1"] = f"RGF — Anexo 1 — Estado (7 POs) — {args.ano} Q{args.quadrimestre}"
    ws["A1"].font = Font(bold=True, size=12)
    todos = tuple(PODERES)
    res = M.apurar_janela(acervo, args.ano, mes_fim, todos)
    ded = M.deducoes(acervo, pares, todos)
    ne = M.nao_executada(acervo, pares, todos)
    linhas = linhas_anexo1(res, ded, ne)
    ws["A3"] = "Descrição"
    ws["B3"] = "Valor apurado"
    ws["C3"] = "Soma dos Poderes"
    ws["D3"] = "Diferença"
    for c in ("A3", "B3", "C3", "D3"):
        ws[c].font = Font(bold=True)
        ws[c].fill = PatternFill("solid", fgColor="EDEDED")
    for i, ln in enumerate(linhas, start=4):
        ws.cell(row=i, column=1, value=("    " * ln.nivel) + ln.descricao)
        ws.cell(row=i, column=2, value=ln.valor).number_format = "#,##0.00"
        ws.cell(row=i, column=3, value=consolidado.get(ln.chave, 0.0)).number_format = "#,##0.00"
        ws.cell(row=i, column=4,
                value=ln.valor - consolidado.get(ln.chave, 0.0)).number_format = "#,##0.00"
    ws.column_dimensions["A"].width = 72
    for col in ("B", "C", "D"):
        ws.column_dimensions[col].width = 22

    destino = os.path.join(SAIDA, f"RGF_{args.ano}_Q{args.quadrimestre}_Anexo01_Poderes.xlsx")
    os.makedirs(SAIDA, exist_ok=True)
    wb.save(destino)

    print(f"{'Poder':<32}{'Despesa Bruta (I)':>22}{'Despesa Líquida':>22}")
    for po, nome in PODERES.items():
        res = M.apurar_janela(acervo, args.ano, mes_fim, (po,))
        ded = M.deducoes(acervo, pares, (po,))
        ne = M.nao_executada(acervo, pares, (po,))
        v = {ln.chave: ln.valor for ln in linhas_anexo1(res, ded, ne)}
        print(f"{nome:<32}{v['I']:>22,.2f}{v['III']:>22,.2f}")
    v = {ln.chave: ln.valor for ln in linhas}
    print(f"{'CONSOLIDADO':<32}{v['I']:>22,.2f}{v['III']:>22,.2f}")
    print(f"\n-> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

