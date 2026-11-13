# -*- coding: utf-8 -*-
"""Teste de viabilidade: da nova MSC (2025/2026) para o Anexo 1 do RGF.

Compara a apuracao pela matriz de dezembro/2025 com o RGF 2025 Q3 oficial.
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict

MSC = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn_msc\2025\MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_ending_balance.csv")
RGF = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn\RGF\2025\RGF_24_2025_quad3_anexo01.csv")

CONTAS = {"622130300", "622130400", "622130700"}
PO_EXEC = {"10111", "10112", "60611"}


def ler_msc(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter=";")
        for r in rd:
            if r["conta_contabil"] not in CONTAS:
                continue
            yield r


def main():
    por_po = defaultdict(lambda: {"rows": 0, "c": 0.0, "d": 0.0, "sem_nd": 0,
                                  "sem_fr": 0, "sem_co": 0})
    contas = defaultdict(int)
    comp_fonte = defaultdict(float)
    nds = defaultdict(float)

    for r in ler_msc(MSC):
        po = r["poder_orgao"]
        v = float(r["valor"])
        s = por_po[po]
        s["rows"] += 1
        if r["natureza_conta"] == "C":
            s["c"] += v
        else:
            s["d"] += v
        if not r["natureza_despesa"]:
            s["sem_nd"] += 1
        if not r["fonte_recursos"]:
            s["sem_fr"] += 1
        if not r["complemento_fonte"]:
            s["sem_co"] += 1
        contas[r["conta_contabil"]] += 1
        comp_fonte[r["complemento_fonte"] or "(vazio)"] += v
        nds[r["natureza_despesa"][:6] or "(vazio)"] += v

    print("CONTAS presentes:", dict(contas))
    print()
    print(f"{'PO':<7} {'linhas':>7} {'creditos':>18} {'debitos':>18} "
          f"{'liquido':>18} {'sem ND':>7} {'sem FR':>7} {'sem compl':>9}")
    tot_c = tot_d = 0.0
    exec_c = 0.0
    for po in sorted(por_po):
        s = por_po[po]
        print(f"{po:<7} {s['rows']:>7} {s['c']:>18,.2f} {s['d']:>18,.2f} "
              f"{s['c'] - s['d']:>18,.2f} {s['sem_nd']:>7} {s['sem_fr']:>7} {s['sem_co']:>9}")
        tot_c += s["c"]
        tot_d += s["d"]
        if po in PO_EXEC:
            exec_c += s["c"] - s["d"]
    print("-" * 100)
    print(f"{'TOTAL':<7} {'':>7} {tot_c:>18,.2f} {tot_d:>18,.2f} {tot_c - tot_d:>18,.2f}")
    print(f"Executivo (10111+10112+60611) liquido: {exec_c:,.2f}")
    print()
    print("complemento_fonte (soma liquida de todos os POs):")
    for k, v in sorted(comp_fonte.items(), key=lambda x: -abs(x[1])):
        print(f"   {k:<10} {v:>18,.2f}")
    print()
    print("natureza_despesa (elemento) — soma de creditos:")
    for k, v in sorted(nds.items(), key=lambda x: -x[1])[:20]:
        print(f"   {k:<10} {v:>18,.2f}")

    # ---- oficial ----
    print()
    print("=" * 100)
    print("RGF 2025 Q3 oficial — linhas de total")
    with open(RGF, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter=";")
        for r in rd:
            if r["coluna"] in ("TOTAL (ÚLTIMOS 12 MESES) (a)",):
                print(f"   {r['conta'][:60]:<62} {float(r['valor']):>18,.2f}")


if __name__ == "__main__":
    main()
