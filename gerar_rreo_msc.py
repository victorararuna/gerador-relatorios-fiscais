# -*- coding: utf-8 -*-
"""RREO de julho-agosto/2026 gerado da MSC — o que ela reproduz.

Testa as contas de controle da despesa (classe 6) e da receita (classe 5) contra
o RREO Anexo 1 homologado de 2026 B4.

Uso:

    python gerar_rreo_msc.py --ano 2026 --bimestre 4
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import siconfi_declaracao as S
from acervo import Acervo

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")

#: contas de controle da despesa e o que representam
#: A conta que reproduz a despesa liquidada do RREO Anexo 1 e a 622130400
#: (credito empenhado liquidado a pagar): +0,02% em 2026 B4. A 622920103
#: (despesa liquidada total) traz tambem o que ja foi pago e da +4,88%.
CONTAS_DESPESA = {
    "622130400": "Credito empenhado liquidado a pagar  <-- RREO A1",
    "622920103": "Despesa liquidada (total)",
    "622920104": "Liquidado a pagar (controle)",
    "622920101": "Empenhos a liquidar",
    "622920102": "Empenhos em liquidacao",
    "622130300": "Credito empenhado a liquidar",
    "622110000": "Credito empenhado",
}


def classif(pct):
    if pct is None:
        return "sem par", CINZA
    if abs(pct) <= 0.005:
        return "fecha", OK
    if abs(pct) <= 0.02:
        return "confere", OK
    if abs(pct) <= 0.05:
        return "até 5%", ATEN
    return "divergente", RUIM


def main(ano: int, bimestre: int) -> int:
    acervo = Acervo(ACERVO)
    meses = [m for m in range(1, bimestre * 2 + 1) if acervo.tem(ano, m)]
    print(f"acervo: {len(meses)} meses de {ano} ({meses[0]}..{meses[-1]})")

    # ---- totais das contas de controle
    totais = {}
    for conta in CONTAS_DESPESA:
        t = 0.0
        for mes in meses:
            for r in acervo.ler(ano, mes):
                if r.conta == conta:
                    t += r.liquido
        totais[conta] = t

    # ---- homologado
    r1 = S.rreo("RREO-Anexo 01", ano, bimestre)
    hom = {}
    for c in r1.contas():
        hom[c] = r1.valores(c)

    def h(conta, coluna):
        return hom.get(conta, {}).get(coluna)

    # ---- comparacoes
    comparacoes = [
        ("Despesa liquidada até o bimestre",
         totais.get("622130400"), h("TOTAL DAS DESPESAS (XII) = (X + XI)",
                                    "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)")),
        ("Referência: liquidada total",
         totais.get("622920103"), h("TOTAL DAS DESPESAS (XII) = (X + XI)",
                                    "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)")),
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = "RREO A1"
    ws.sheet_view.showGridLines = False
    ws["A1"] = f"RREO Anexo 1 — {ano} B{bimestre} (jul-ago)"
    ws["A1"].font = Font(name="Arial", size=14, bold=True)
    ws["A2"] = "Apurado da MSC (contas de controle) × homologado do Siconfi"
    ws["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, (t, w) in enumerate((("Item", 42), ("MSC", 20), ("Homologado", 20),
                                ("Diferença", 18), ("%", 10), ("Situação", 14)), 1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        ws.column_dimensions[chr(64 + j)].width = w

    lin = 5
    for rotulo, ap, of in comparacoes:
        pct = (ap - of) / of if (ap and of) else None
        sit, cor = classif(pct)
        ws.cell(lin, 1, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((2, ap), (3, of)):
            c = ws.cell(lin, j, round(v, 2) if v is not None else "—")
            if v is not None:
                c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        if pct is not None:
            c = ws.cell(lin, 4, round(ap - of, 2))
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 5, pct if pct is not None else "—")
        c.number_format = "0.00%"
        c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 6, sit)
        c.font = Font(name="Arial", size=8, bold=sit == "divergente")
        c.fill = cor
        print(f"   {rotulo:42} {ap:>18,.2f} {pct*100 if pct else 0:>+8.2f}%  {sit}")
        lin += 1

    # ---- todas as contas de controle
    lin += 2
    ws.cell(lin, 1, "CONTAS DE CONTROLE DA MSC (total do período)").font = \
        Font(name="Arial", size=10, bold=True)
    lin += 1
    for conta, desc in CONTAS_DESPESA.items():
        ws.cell(lin, 1, f"{conta} — {desc}").font = Font(name="Arial", size=8)
        c = ws.cell(lin, 2, round(totais[conta], 2))
        c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        lin += 1

    destino = os.path.join(RAIZ, "saida", f"RREO_{ano}_B{bimestre}_MSC.xlsx")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    wb.save(destino)
    print(f"\ngerado: {destino}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=4)
    a = ap.parse_args()
    raise SystemExit(main(a.ano, a.bimestre))
