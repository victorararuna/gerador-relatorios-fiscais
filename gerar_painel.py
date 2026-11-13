# -*- coding: utf-8 -*-
"""Painel de verificação: reúne num único XLSX tudo o que fecha e o que não fecha.

    python gerar_painel.py --ano 2025 --quadrimestre 3
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402
import app.anexo3_msc as A3  # noqa: E402
import app.anexo4_msc as A4  # noqa: E402
import app.anexo6_msc as A6  # noqa: E402
from app.relatorio_anexo1 import ler_oficiais, linhas_anexo1  # noqa: E402
from rreo_anexo1_grupos import GRUPOS  # noqa: E402
from rreo_anexo2 import FUNCOES  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
BASE = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn"
SAIDA = os.path.join(AQUI, "saida")


def _cabecalho(ws, titulo, colunas):
    from openpyxl.styles import Font, PatternFill
    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=12)
    for i, nome in enumerate(colunas, start=1):
        cel = ws.cell(row=3, column=i, value=nome)
        cel.font = Font(bold=True)
        cel.fill = PatternFill("solid", fgColor="EDEDED")


def _autolargura(ws, larguras):
    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura


def main() -> int:
    from openpyxl import Workbook

    wb = Workbook()
    wb.remove(wb.active)
    resumo = []

    # ---------------------------------------------------------------- Anexo 1
    acervo = M.Acervo(MSC)
    mes_fim = 12
    pares = M.periodos_janela(2025, mes_fim)
    res = M.apurar_janela(acervo, 2025, mes_fim)
    ded = M.deducoes(acervo, pares)
    ne = M.nao_executada(acervo, pares)
    linhas = linhas_anexo1(res, ded, ne)
    oficial = ler_oficiais(os.path.join(BASE, r"RGF\2025\RGF_24_2025_quad3_anexo01.csv"))

    ws = wb.create_sheet("RGF-Anexo 01")
    _cabecalho(ws, "RGF Anexo 1 — Despesa com Pessoal — 2025 Q3",
               ["Descrição", "Apurado", "Homologado", "%"])
    for i, ln in enumerate(linhas, start=4):
        of = oficial.get(ln.descricao)
        ws.cell(row=i, column=1, value=("    " * ln.nivel) + ln.descricao)
        ws.cell(row=i, column=2, value=ln.valor).number_format = "#,##0.00"
        if of:
            ws.cell(row=i, column=3, value=of).number_format = "#,##0.00"
            ws.cell(row=i, column=4, value=ln.valor / of - 1).number_format = "0.00%"
    _autolargura(ws, {"A": 70, "B": 22, "C": 22, "D": 10})
    v = {ln.chave: ln.valor for ln in linhas}
    resumo.append(("RGF Anexo 1 — Despesa Bruta (I)", v["I"],
                   oficial.get("DESPESA BRUTA COM PESSOAL (I)")))
    resumo.append(("RGF Anexo 1 — Despesa Líquida (III)", v["III"],
                   oficial.get("DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)")))

    # ---------------------------------------------------------------- Anexo 3
    rcl = A3.ler_rcl(os.path.join(BASE, r"RREO\2025\RREO_24_2025_bim6_anexo03.csv"))
    ws = wb.create_sheet("RGF-Anexo 03")
    _cabecalho(ws, "RGF Anexo 3 — Garantias — 2025 Q3", ["Linha", "Apurado", "Homologado"])
    of3 = {}
    with open(os.path.join(BASE, r"RGF\2025\RGF_24_2025_quad3_anexo03.csv"),
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == "Até o 3º Quadrimestre":
                of3.setdefault(r["conta"], float(r["valor"]))
    for i, (rot, val) in enumerate(A3.linhas_anexo3(rcl), start=4):
        ws.cell(row=i, column=1, value=rot)
        ws.cell(row=i, column=2, value=val).number_format = "#,##0.00"
        of = next((x for c, x in of3.items() if c.startswith(rot[:40])), None)
        if of is not None:
            ws.cell(row=i, column=3, value=of).number_format = "#,##0.00"
    _autolargura(ws, {"A": 70, "B": 22, "C": 22})
    resumo.append(("RGF Anexo 3 — Limite do Senado (22%)",
                   A3.linhas_anexo3(rcl)[3][1], None))

    # ----------------------------------------------------------- limites 4 e 6
    ws = wb.create_sheet("Limites")
    _cabecalho(ws, "Limites calculados sobre a RCL — 2025 Q3",
               ["Demonstrativo", "Limite", "Apurado", "Homologado"])
    linhas_lim = []
    lim4 = A4.limites(rcl)
    for chave, rotulo in A4.ROTULOS.items():
        linhas_lim.append(("Anexo 4", rotulo, lim4[chave]))
    lim6 = A6.limites(rcl)
    for chave, rotulo in A6.ROTULOS.items():
        linhas_lim.append(("Anexo 6", rotulo, lim6[chave]))

    of4, of6 = {}, {}
    for arq, alvo in ((os.path.join(BASE, r"RGF\2025\RGF_24_2025_quad3_anexo04.csv"), of4),
                      (os.path.join(BASE, r"RGF\2025\RGF_24_2025_quad3_anexo06.csv"), of6)):
        with open(arq, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                if r["coluna"].startswith("VALOR"):
                    alvo.setdefault(r["conta"], float(r["valor"]))
    for i, (anexo, rotulo, val) in enumerate(linhas_lim, start=4):
        fonte = of4 if anexo == "Anexo 4" else of6
        of = next((x for c, x in fonte.items() if c.startswith(rotulo[:36])), None)
        ws.cell(row=i, column=1, value=anexo)
        ws.cell(row=i, column=2, value=rotulo)
        ws.cell(row=i, column=3, value=val).number_format = "#,##0.00"
        if of is not None:
            ws.cell(row=i, column=4, value=of).number_format = "#,##0.00"
    _autolargura(ws, {"A": 12, "B": 66, "C": 22, "D": 22})

    # ------------------------------------------------- RREO Anexo 1 (despesa)
    import rreo_anexo1_grupos as R1
    ofg, msg = R1.oficial(), R1.nosso()
    ws = wb.create_sheet("RREO-Anexo 01 despesa")
    _cabecalho(ws, "RREO Anexo 1 — despesa por grupo — 2025 B6",
               ["Grupo", "Exceto intra (oficial)", "MSC total", "Intra derivada"])
    for i, (pref, nome) in enumerate(GRUPOS.items(), start=4):
        o, m = ofg.get(nome, 0.0), msg.get(pref, 0.0)
        ws.cell(row=i, column=1, value=nome)
        ws.cell(row=i, column=2, value=o).number_format = "#,##0.00"
        ws.cell(row=i, column=3, value=m).number_format = "#,##0.00"
        ws.cell(row=i, column=4, value=m - o).number_format = "#,##0.00"
    _autolargura(ws, {"A": 32, "B": 24, "C": 24, "D": 20})

    # -------------------------------------------------- RREO Anexo 2 (função)
    import rreo_anexo2 as R2
    import rreo_anexo2_intra as R2I
    of2, ms2 = R2I.oficial_exceto(), R2.nosso_por_funcao()
    ws = wb.create_sheet("RREO-Anexo 02 função")
    _cabecalho(ws, "RREO Anexo 2 — despesa por função — 2025 B6",
               ["Função", "Exceto intra (oficial)", "MSC total", "Intra derivada"])
    for i, (cod, nome) in enumerate(FUNCOES.items(), start=4):
        o, m = of2.get(nome, 0.0), ms2.get(cod, 0.0)
        if not o and not m:
            continue
        ws.cell(row=i, column=1, value=nome)
        ws.cell(row=i, column=2, value=o).number_format = "#,##0.00"
        ws.cell(row=i, column=3, value=m).number_format = "#,##0.00"
        ws.cell(row=i, column=4, value=m - o).number_format = "#,##0.00"
    _autolargura(ws, {"A": 30, "B": 24, "C": 24, "D": 20})

    # ---------------------------------------------------------------- resumo
    ws = wb.create_sheet("Resumo", 0)
    _cabecalho(ws, "Painel de verificação — 2025 Q3 / B6",
               ["Item", "Apurado", "Homologado", "Desvio"])
    for i, (nome, nosso, of) in enumerate(resumo, start=4):
        ws.cell(row=i, column=1, value=nome)
        ws.cell(row=i, column=2, value=nosso).number_format = "#,##0.00"
        if of:
            ws.cell(row=i, column=3, value=of).number_format = "#,##0.00"
            ws.cell(row=i, column=4, value=nosso / of - 1).number_format = "0.00%"
    _autolargura(ws, {"A": 48, "B": 24, "C": 24, "D": 12})

    destino = os.path.join(SAIDA, "Painel_Verificacao_2025Q3.xlsx")
    os.makedirs(SAIDA, exist_ok=True)
    wb.save(destino)
    print(f"-> {destino}")
    print(f"abas: {wb.sheetnames}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
