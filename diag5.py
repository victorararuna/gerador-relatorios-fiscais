# -*- coding: utf-8 -*-
"""Hipotese: o total do exercicio e a soma dos period_change mensais (C - D).

Testa contra o ending_balance de dezembro e contra o RGF 2025 Q3 oficial.
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict

BASE = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn_msc\2025")

CONTAS = {"622130300", "622130400", "622130700"}
PO_EXEC = {"10111", "10112", "60611"}
OFICIAL = 15_478_621_265.08


def soma_periodo(mes, contas=CONTAS):
    arq = os.path.join(BASE, f"MSC_24_2025_m{mes:02d}_MSCC_msc_orcamentaria_classe6_period_change.csv")
    por_po = defaultdict(float)
    if not os.path.exists(arq):
        return por_po, False
    with open(arq, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["conta_contabil"] not in contas:
                continue
            v = float(r["valor"])
            por_po[r["poder_orgao"]] += v if r["natureza_conta"] == "C" else -v
    return por_po, True


def main():
    acumulado = defaultdict(float)
    print(f"{'mes':<5} {'Executivo':>18} {'Todos os POs':>18}")
    for mes in range(1, 13):
        por_po, ok = soma_periodo(mes)
        if not ok:
            print(f"{mes:<5} {'(arquivo ausente)':>18}")
            continue
        ex = sum(v for p, v in por_po.items() if p in PO_EXEC)
        for p, v in por_po.items():
            acumulado[p] += v
        print(f"{mes:<5} {ex:>18,.2f} {sum(por_po.values()):>18,.2f}")

    print("-" * 45)
    ex_ano = sum(v for p, v in acumulado.items() if p in PO_EXEC)
    print(f"{'ANO':<5} {ex_ano:>18,.2f} {sum(acumulado.values()):>18,.2f}")
    print()
    print(f"Oficial 2025 Q3 (Executivo, bruta) : {OFICIAL:,.2f}")
    print(f"MSC soma period_change (Executivo) : {ex_ano:,.2f}")
    print(f"desvio                              : {ex_ano - OFICIAL:,.2f} "
          f"({(ex_ano/OFICIAL-1)*100:+.2f}%)")
    print()
    print("por PO (ano):")
    for p in sorted(acumulado):
        print(f"   {p:<7} {acumulado[p]:>18,.2f}")


if __name__ == "__main__":
    main()
