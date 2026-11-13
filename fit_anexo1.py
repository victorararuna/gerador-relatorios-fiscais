# -*- coding: utf-8 -*-
"""Decomposição por elemento e por complemento_fonte — insumo do de-para."""
from __future__ import annotations

import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_msc import Acervo  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
PO_EXEC = {"10111", "10112", "60611"}
CONTAS = ("622130300", "622130400", "622130700")


def main() -> int:
    acervo = Acervo(MSC)
    meses = acervo.meses(2025, 6, "period_change")

    por_elem = defaultdict(float)
    por_elem_po = defaultdict(float)
    compl = defaultdict(lambda: defaultdict(float))

    for mes in meses:
        for r in acervo.ler(2025, mes):
            if r.conta not in CONTAS or r.po not in PO_EXEC:
                continue
            e = r.elemento or "(sem ND)"
            por_elem[e] += r.liquido
            por_elem_po[(e, r.po)] += r.liquido
            compl[e][r.compl or "(vazio)"] += r.liquido

    print("Executivo — por elemento (natureza da despesa):")
    for e, v in sorted(por_elem.items(), key=lambda x: -abs(x[1])):
        if abs(v) < 1_000_000:
            continue
        print(f"   {e:<10} {v:>18,.2f}")
    print(f"   {'TOTAL':<10} {sum(por_elem.values()):>18,.2f}")

    print("\npor elemento e Poder (elementos de pessoal):")
    for e in sorted(por_elem_po):
        if not e[0].startswith("31"):
            continue
        print(f"   {e[0]:<10} {e[1]:<7} {por_elem_po[e]:>18,.2f}")

    for alvo in ("319001", "319003", "319011", "319113", "319092", "319091"):
        print(f"\n{alvo} — por complemento_fonte:")
        for c, v in sorted(compl[alvo].items(), key=lambda x: -x[1]):
            print(f"   {c:<10} {v:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
