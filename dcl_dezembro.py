# -*- coding: utf-8 -*-
"""Anexo 2: o que cresceu na dívida entre agosto e dezembro de 2025."""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"


def saldos(acervo, mes):
    s = {}
    for r in acervo.ler(2025, mes, classe=2, tipo_valor="ending_balance"):
        c = r.conta
        if c.startswith("23") or c.startswith("27"):
            continue
        s[c] = s.get(c, 0.0) + r.liquido
    return s


def main() -> int:
    acervo = M.Acervo(MSC)
    ago, dez = saldos(acervo, 8), saldos(acervo, 12)

    linhas = []
    for c in set(ago) | set(dez):
        d = dez.get(c, 0.0) - ago.get(c, 0.0)
        if abs(d) > 20_000_000:
            linhas.append((d, c, ago.get(c, 0.0), dez.get(c, 0.0)))
    linhas.sort(reverse=True)

    print(f"{'conta':<12}{'ago':>18}{'dez':>18}{'variação':>18}")
    for d, c, a, z in linhas:
        print(f"{c:<12}{a:>18,.2f}{z:>18,.2f}{d:>18,.2f}")
    print(f"\nsoma das variações: {sum(x[0] for x in linhas):,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
