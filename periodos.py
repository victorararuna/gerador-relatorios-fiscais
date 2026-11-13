# -*- coding: utf-8 -*-
"""Os totais do Anexo 1 são janela móvel de 12 meses ou acumulado do ano?"""
from __future__ import annotations

import csv
import glob
import os

BASE = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn\RGF")

ALVO = "DESPESA BRUTA COM PESSOAL (I)"


def main() -> int:
    for arq in sorted(glob.glob(os.path.join(BASE, "*", "*anexo01.csv"))):
        with open(arq, encoding="utf-8-sig", newline="") as fh:
            linhas = list(csv.DictReader(fh, delimiter=";"))
        cols = []
        for r in linhas:
            if r["conta"] == ALVO and r["coluna"] not in cols:
                cols.append(r["coluna"])
        total = next((float(r["valor"]) for r in linhas
                      if r["conta"] == ALVO
                      and r["coluna"].startswith("TOTAL")), float("nan"))
        print(f"{os.path.basename(arq)}")
        print(f"   colunas ({len(cols)}): {cols[:3]} ... {cols[-3:]}")
        print(f"   total 12 meses: {total:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
