# -*- coding: utf-8 -*-
"""O que muda entre 2025 e 2026: média mensal por natureza."""
from __future__ import annotations

import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"


def main() -> int:
    acervo = M.Acervo(MSC)
    totais = {2025: defaultdict(float), 2026: defaultdict(float)}
    meses = {2025: range(1, 13), 2026: range(1, 10)}
    for ano, ms in meses.items():
        for m in ms:
            for r in acervo.ler(ano, m):
                if r.conta in M.CONTAS_LIQUIDACAO and r.po in M.PO_EXECUTIVO:
                    totais[ano][r.nd] += r.liquido

    n = {2025: 12, 2026: 9}
    print(f"{'ND':<10}{'2025/mês':>18}{'2026/mês':>18}{'dif/mês':>18}{'linha':<16}")
    linhas = []
    for nd in set(totais[2025]) | set(totais[2026]):
        a = totais[2025].get(nd, 0.0) / n[2025]
        b = totais[2026].get(nd, 0.0) / n[2026]
        if abs(a) < 100_000 and abs(b) < 100_000:
            continue
        linhas.append((b - a, nd, a, b))
    linhas.sort(reverse=True)
    for dif, nd, a, b in linhas[:15]:
        print(f"{nd:<10}{a:>18,.2f}{b:>18,.2f}{dif:>18,.2f}"
              f"{str(M._classificar(nd)):<16}")
    print("\nmaiores quedas:")
    for dif, nd, a, b in linhas[-10:]:
        print(f"{nd:<10}{a:>18,.2f}{b:>18,.2f}{dif:>18,.2f}"
              f"{str(M._classificar(nd)):<16}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
