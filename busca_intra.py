# -*- coding: utf-8 -*-
"""Onde estão os ~R$ 499 mi de diferença? Quebra do pessoal do Executivo por fonte."""
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

    por_fr = defaultdict(float)
    por_fr_po = defaultdict(float)
    for r in (r for m in meses for r in acervo.ler(2025, m)):
        if r.conta not in CONTAS or not r.nd.startswith("31"):
            continue
        por_fr[r.fr or "(vazio)"] += r.liquido
        if r.po in PO_EXEC:
            por_fr_po[(r.po, r.fr or "(vazio)")] += r.liquido

    print("pessoal (ND 31), todos os POs, por fonte de recursos:")
    for fr, v in sorted(por_fr.items(), key=lambda x: -abs(x[1]))[:15]:
        print(f"   {fr:<10} {v:>18,.2f}")
    print(f"   {'TOTAL':<10} {sum(por_fr.values()):>18,.2f}")

    print("\nExecutivo — fontes 1.7xx / 2.7xx (candidatas a intra):")
    for (po, fr), v in sorted(por_fr_po.items()):
        if fr[:2] in ("17", "27") or fr.startswith("7"):
            print(f"   {po:<7} {fr:<8} {v:>18,.2f}")

    print("\nExecutivo — total por fonte (top 12):")
    agg = defaultdict(float)
    for (po, fr), v in por_fr_po.items():
        agg[fr] += v
    for fr, v in sorted(agg.items(), key=lambda x: -abs(x[1]))[:12]:
        print(f"   {fr:<10} {v:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
