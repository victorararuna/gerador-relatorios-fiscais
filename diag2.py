# -*- coding: utf-8 -*-
"""Diagnostico: MSC 2025 (dez) x RGF 2025 Q3 oficial, por Poder e por elemento."""
from __future__ import annotations

import csv
import os
from collections import defaultdict

MSC = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn_msc\2025\MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_ending_balance.csv")
RGFDIR = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn\RGF\2025")

CONTAS = {"622130300", "622130400", "622130700"}
PO_EXEC = {"10111", "10112", "60611"}

LINHA = {
    "319001": "aposentadorias",
    "319003": "pensoes",
    "319011": "vencimentos", "319012": "vencimentos", "319016": "vencimentos",
    "319017": "vencimentos", "319004": "vencimentos", "319007": "vencimentos",
    "319013": "patronal", "319113": "patronal",
    "319091": "judiciais",
    "319092": "exerc_ant", "319192": "exerc_ant", "319096": "exerc_ant",
    "319094": "indenizacoes",
}
ORDEM = ["vencimentos", "patronal", "aposentadorias", "pensoes", "terceirizacao",
         "exerc_ant", "judiciais", "indenizacoes"]


def apurar():
    por_po = defaultdict(lambda: defaultdict(float))
    terceir = defaultdict(float)
    with open(MSC, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["conta_contabil"] not in CONTAS:
                continue
            po, nd, v = r["poder_orgao"], r["natureza_despesa"], float(r["valor"])
            por_po[po]["_total"] += v
            if not nd:
                por_po[po]["_sem_nd"] += v
                continue
            if nd.startswith("33"):
                if nd[:6] == "339034" or nd.endswith("34"):
                    terceir[po] += v
                continue
            por_po[po][LINHA.get(nd[:6], "vencimentos")] += v
    return por_po, terceir


def oficial(arquivo):
    linhas = {}
    poderes = set()
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            poderes.add(r["co_poder"])
            if r["coluna"] != "TOTAL (ÚLTIMOS 12 MESES) (a)":
                continue
            linhas[r["conta"]] = float(r["valor"])
    return linhas, poderes


def main():
    por_po, terceir = apurar()

    print(f"{'PO':<7} " + " ".join(f"{k[:9]:>13}" for k in ORDEM) + f" {'TOTAL':>15}")
    for po in sorted(por_po):
        v = por_po[po]
        print(f"{po:<7} " + " ".join(f"{v[k]:>13,.0f}" for k in ORDEM) + f" {v['_total']:>15,.0f}")

    print()
    print("Soma dos Poderes (todos os POs):")
    for k in ORDEM:
        print(f"   {k:<15} {sum(v[k] for v in por_po.values()):>18,.2f}")
    print(f"   {'terceirizacao':<15} {sum(terceir.values()):>18,.2f}")

    print()
    print("=" * 110)
    arq = os.path.join(RGFDIR, "RGF_24_2025_quad3_anexo01.csv")
    lin, poderes = oficial(arq)
    print(f"co_poder no arquivo oficial: {sorted(poderes)}")
    print(f"{'linha oficial':<58} {'oficial':>18} {'MSC exec':>18} {'dif':>14}")
    exec_ = {k: sum(v[k] for p, v in por_po.items() if p in PO_EXEC) for k in ORDEM}
    exec_["terceirizacao"] = sum(v for p, v in terceir.items() if p in PO_EXEC)
    mapa = {
        "Vencimentos, Vantagens e Outras Despesas Variáveis": "vencimentos",
        "Obrigações Patronais": "patronal",
        "Aposentadorias, Reserva e Reformas": "aposentadorias",
        "Pensões": "pensoes",
        "Outras Despesas de Pessoal decorrentes de Contratos de Terceirizados": "terceirizacao",
        "Indenizações por Demissão e Incentivos à Demissão Voluntária": "indenizacoes",
        "Decorrentes de Decisão Judicial de Período Anterior ao da Apuração": "judiciais",
        "Despesas de Exercícios Anteriores de Período Anterior ao da Apuração": "exerc_ant",
    }
    for rotulo, chave in mapa.items():
        of = lin.get(rotulo, float("nan"))
        ms = exec_[chave]
        print(f"{rotulo[:56]:<58} {of:>18,.2f} {ms:>18,.2f} {ms - of:>14,.2f}")

    tot = lin.get("DESPESA BRUTA COM PESSOAL (I)", float("nan"))
    msc_total = sum(exec_.values())
    print(f"{'DESPESA BRUTA (I)':<58} {tot:>18,.2f} {msc_total:>18,.2f} "
          f"{msc_total - tot:>14,.2f}")
    print(f"{'desvio %':<58} {'':>18} {'':>18} {(msc_total/tot-1)*100:>13.2f}%")


if __name__ == "__main__":
    main()
