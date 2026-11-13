# -*- coding: utf-8 -*-
"""Quantas linhas de debito existem no ending_balance e em que contas."""
import collections
import csv

P = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
     r"\siconfi_rn_msc\2025\MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_ending_balance.csv")

c = collections.Counter()
d = collections.Counter()
with open(P, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        (c if r["natureza_conta"] == "C" else d)[r["conta_contabil"]] += 1

print("linhas C:", sum(c.values()), " linhas D:", sum(d.values()))
print("contas com D:", dict(list(d.items())[:15]))
