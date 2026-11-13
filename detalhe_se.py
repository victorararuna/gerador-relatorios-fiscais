# -*- coding: utf-8 -*-
"""Detalhe por natureza completa (elemento + desdobramento) e por CO."""
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
ALVOS = ("319003", "319092", "319094", "319013", "319001", "319091")


def main() -> int:
    acervo = Acervo(MSC)
    meses = acervo.meses(2025, 6, "period_change")
    nd = defaultdict(float)
    co = defaultdict(lambda: defaultdict(float))
    for r in (r for m in meses for r in acervo.ler(2025, m)):
        if r.conta not in CONTAS or r.po not in PO_EXEC or not r.nd:
            continue
        if r.nd[:6] in ALVOS:
            nd[r.nd] += r.liquido
            co[r.nd[:6]][r.compl or "(vazio)"] += r.liquido

    for elem in ALVOS:
        print(f"\n{elem}")
        for k, v in sorted(nd.items()):
            if k[:6] == elem:
                print(f"   {k:<10} {v:>18,.2f}")
        print("   por CO:")
        for c, v in sorted(co[elem].items(), key=lambda x: -abs(x[1])):
            print(f"      {c:<8} {v:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
