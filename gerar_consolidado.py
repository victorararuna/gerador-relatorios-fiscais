# -*- coding: utf-8 -*-
"""RGF Anexo 1 — consolidado do Estado combinando matriz e arquivos por Poder.

O Executivo é **apurado na matriz** (validado contra o homologado). Os demais
Poderes vêm dos arquivos oficiais `RGF_..._anexo01_<P>.csv`, porque a matriz
registra a folha deles na unidade executora (Tesouro/RPPS), não no Poder de
origem — o vínculo do servidor não está no dado contábil.

    python gerar_consolidado.py --ano 2025 --quadrimestre 3
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402
from app.relatorio_anexo1 import ler_oficiais, linhas_anexo1  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_completo\MSC"
RGF = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_completo\RGF"
SAIDA = os.path.join(AQUI, "saida")

#: a Defensoria (60611) integra o Executivo — confirmado: o "Pessoal Ativo" do
#: arquivo E é igual à nossa soma 10111+10112+60611 com desvio de 0,01%
PODERES = {"E": ("10111", "10112", "60611"), "L": ("20211", "20212"),
           "J": ("30390",), "M": ("50511",)}
NOMES = {"E": "Executivo (c/ Defensoria)", "L": "Legislativo",
         "J": "Judiciário", "M": "Ministério Público"}


def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Anexo 1 consolidado do Estado.")
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--quadrimestre", type=int, default=3)
    args = ap.parse_args()

    acervo = M.Acervo(MSC)
    mes_fim = M.MES_DO_QUADRIMESTRE[args.quadrimestre]
    pares = M.periodos_janela(args.ano, mes_fim)

    # Executivo: matriz
    pos_e = PODERES["E"]
    res = M.apurar_janela(acervo, args.ano, mes_fim, pos_e)
    nosso = {ln.descricao: ln.valor
             for ln in linhas_anexo1(res, M.deducoes(acervo, pares, pos_e),
                                     M.nao_executada(acervo, pares, pos_e))}

    pasta = os.path.join(RGF, str(args.ano))
    oficiais = {}
    for poder in PODERES:
        arq = os.path.join(pasta, f"RGF_24_{args.ano}_quad{args.quadrimestre}_anexo01_{poder}.csv")
        oficiais[poder] = ler_oficiais(arq) if os.path.exists(arq) else {}

    # ordem das linhas: a do arquivo oficial do Executivo
    ordem = [c for c in oficiais["E"]] or list(nosso)

    colunas = {p: dict(oficiais[p]) for p in PODERES}
    colunas["E"] = {**colunas["E"], **nosso}     # matriz prevalece no Executivo

    # ---- XLSX
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "Consolidado"
    ws["A1"] = (f"RGF Anexo 1 — consolidado do Estado — {args.ano} "
                f"Q{args.quadrimestre}")
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Executivo apurado na MSC; demais Poderes dos arquivos oficiais "
                "(a matriz não identifica o Poder do inativo).")
    ws["A2"].font = Font(italic=True, size=8, color="666666")

    cabecalho = ["Linha"] + [NOMES[p] for p in PODERES] + ["TOTAL"]
    for j, nome in enumerate(cabecalho, start=1):
        c = ws.cell(row=4, column=j, value=nome)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")

    for i, linha in enumerate(ordem, start=5):
        ws.cell(row=i, column=1, value=linha)
        soma = 0.0
        for j, poder in enumerate(PODERES, start=2):
            v = colunas[poder].get(linha)
            if v is not None:
                ws.cell(row=i, column=j, value=v).number_format = "#,##0.00"
                soma += v
        ws.cell(row=i, column=len(PODERES) + 2, value=soma).number_format = "#,##0.00"

    ws.column_dimensions["A"].width = 64
    for j in range(2, len(PODERES) + 3):
        ws.column_dimensions[chr(64 + j)].width = 20

    # ---- conferência do Executivo
    ws2 = wb.create_sheet("Conferência Executivo")
    ws2["A1"] = "Executivo — matriz × homologado"
    ws2["A1"].font = Font(bold=True, size=12)
    for j, nome in enumerate(["Linha", "Matriz", "Homologado", "Diferença", "%"], start=1):
        c = ws2.cell(row=3, column=j, value=nome)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")
    r = 4
    for linha in ordem:
        m = nosso.get(linha)
        o = oficiais["E"].get(linha)
        if m is None or o is None:
            continue
        ws2.cell(row=r, column=1, value=linha)
        ws2.cell(row=r, column=2, value=m).number_format = "#,##0.00"
        ws2.cell(row=r, column=3, value=o).number_format = "#,##0.00"
        ws2.cell(row=r, column=4, value=m - o).number_format = "#,##0.00"
        ws2.cell(row=r, column=5, value=(m / o - 1) if o else 0).number_format = "0.00%"
        r += 1
    ws2.column_dimensions["A"].width = 64
    for col in ("B", "C", "D", "E"):
        ws2.column_dimensions[col].width = 20

    # ---- limites por Poder (Anexo 6 de cada um)
    import app.anexo3_msc as A3

    rcl = A3.ler_rcl(os.path.join(
        r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_completo\RREO\2025",
        "RREO_24_2025_bim6_anexo03_E.csv"))
    dtp_poder = {}
    for poder in PODERES:
        arq6 = os.path.join(pasta, f"RGF_24_{args.ano}_quad{args.quadrimestre}_anexo06_{poder}.csv")
        if not os.path.exists(arq6):
            continue
        dtp = limite = pct = None
        with open(arq6, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                if r["conta"].startswith("Despesa Total com Pessoal") and r["coluna"] in ("Apuração do Valor", "VALOR"):
                    dtp = float(r["valor"])
                if r["conta"].startswith("Limite Máximo") and r["coluna"] in ("Apuração do Valor", "VALOR"):
                    limite = float(r["valor"])
                if r["conta"].startswith("Limite Máximo") and "%" in r["coluna"]:
                    pct = float(r["valor"])
        dtp_poder[poder] = (dtp, limite, pct)

    ws3 = wb.create_sheet("Limites")
    ws3["A1"] = f"Limites de pessoal por Poder — {args.ano} Q{args.quadrimestre}"
    ws3["A1"].font = Font(bold=True, size=12)
    for j, nome in enumerate(["Poder", "DTP", "% sobre RCL", "Limite (%)",
                              "Limite (R$)", "Folga/Excesso"], start=1):
        c = ws3.cell(row=3, column=j, value=nome)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")
    total_dtp = 0.0
    for i, poder in enumerate(PODERES, start=4):
        dtp, limite, pct = dtp_poder.get(poder, (None, None, None))
        if dtp is None:
            continue
        total_dtp += dtp
        ws3.cell(row=i, column=1, value=NOMES[poder])
        ws3.cell(row=i, column=2, value=dtp).number_format = "#,##0.00"
        ws3.cell(row=i, column=3, value=dtp / rcl.ajustada_pessoal).number_format = "0.00%"
        ws3.cell(row=i, column=4, value=(pct or 0) / 100).number_format = "0.00%"
        if limite:
            ws3.cell(row=i, column=5, value=limite).number_format = "#,##0.00"
            ws3.cell(row=i, column=6, value=limite - dtp).number_format = "#,##0.00"
    ws3.cell(row=len(PODERES) + 5, column=1, value="ESTADO").font = Font(bold=True)
    c = ws3.cell(row=len(PODERES) + 5, column=2, value=total_dtp)
    c.number_format = "#,##0.00"
    c.font = Font(bold=True)
    c = ws3.cell(row=len(PODERES) + 5, column=3,
                 value=total_dtp / rcl.ajustada_pessoal)
    c.number_format = "0.00%"
    c.font = Font(bold=True)
    ws3.column_dimensions["A"].width = 30
    for col in ("B", "C", "D", "E", "F"):
        ws3.column_dimensions[col].width = 20

    destino = os.path.join(SAIDA, f"RGF_{args.ano}_Q{args.quadrimestre}_Anexo01_Consolidado.xlsx")
    os.makedirs(SAIDA, exist_ok=True)
    wb.save(destino)

    print(f"{'Poder':<20}{'Despesa Bruta (I)':>22}")
    for poder in PODERES:
        v = colunas[poder].get("DESPESA BRUTA COM PESSOAL (I)", 0.0)
        marca = " (matriz)" if poder == "E" else " (oficial)"
        print(f"{NOMES[poder] + marca:<20}{v:>22,.2f}")
    total = sum(colunas[p].get("DESPESA BRUTA COM PESSOAL (I)", 0.0) for p in PODERES)
    print(f"{'CONSOLIDADO':<20}{total:>22,.2f}")
    print(f"\n-> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())



