# -*- coding: utf-8 -*-
"""Checagens finas da nova MSC: contas 62213, debitos, MSCE e complemento_fonte."""
from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict

BASE = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn_msc\2025")


def ler(nome):
    return os.path.join(BASE, nome)


def contas_62213(arquivo):
    c = Counter()
    dc = Counter()
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["conta_contabil"].startswith("62213"):
                c[r["conta_contabil"]] += 1
                dc[r["natureza_conta"]] += 1
    return c, dc


def compl_por_nd(arquivo):
    """complemento_fonte x elemento, para as contas de liquidacao."""
    tab = defaultdict(Counter)
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["conta_contabil"] not in ("622130300", "622130400", "622130700"):
                continue
            nd = (r["natureza_despesa"] or "(vazio)")[:6]
            tab[nd][r["complemento_fonte"] or "(vazio)"] += float(r["valor"])
    return tab


def main():
    eb = ler("MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_ending_balance.csv")
    pc = ler("MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_period_change.csv")
    mscE = ler("MSC_24_2025_m12_MSCE_msc_orcamentaria_classe6_ending_balance.csv")

    for rot, arq in (("ENDING_BALANCE", eb), ("PERIOD_CHANGE", pc)):
        c, dc = contas_62213(arq)
        print(f"{rot}: contas 62213* = {dict(sorted(c.items()))}  natureza_conta={dict(dc)}")
    print()

    print("complemento_fonte por elemento (contas de liquidacao, todos os POs):")
    tab = compl_por_nd(eb)
    for nd in sorted(tab, key=lambda k: -sum(tab[k].values()))[:10]:
        total = sum(tab[nd].values())
        detalhe = ", ".join(f"{k}={v/1e6:,.1f}mi" for k, v in tab[nd].most_common(5))
        print(f"   {nd:<10} {total/1e6:>10,.1f} mi   {detalhe}")
    print()

    print("MSCE (matriz do ente?) — classe 6:")
    with open(mscE, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter=";")
        pos = Counter()
        n = 0
        total = 0.0
        for r in rd:
            n += 1
            pos[r["poder_orgao"]] += 1
            total += float(r["valor"])
        print(f"   linhas={n} POs={dict(pos)} soma={total:,.2f}")


if __name__ == "__main__":
    main()
