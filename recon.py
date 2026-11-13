# -*- coding: utf-8 -*-
"""Reconhecimento das novas matrizes MSC do Siconfi (2025/2026) do RN."""
from __future__ import annotations

import csv
import os
from collections import Counter

BASE = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"

ARQUIVOS = [
    (2025, "m12", "MSCC", "classe6"),
    (2025, "m12", "MSCC", "classe8"),
    (2026, "m09", "MSCC", "classe6"),
    (2026, "m09", "MSCC", "classe5"),
]


def caminho(ano, mes, tipo, classe):
    return os.path.join(
        BASE, str(ano),
        f"MSC_24_{ano}_{mes}_{tipo}_msc_orcamentaria_{classe}_ending_balance.csv"
        if classe == "classe6" or classe == "classe5"
        else f"MSC_24_{ano}_{mes}_{tipo}_msc_controle_{classe}_ending_balance.csv")


def censo(caminho_arq):
    with open(caminho_arq, encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f, delimiter=";")
        cab = next(rd)
        vazios = Counter()
        valores = {c: Counter() for c in cab}
        n = 0
        for linha in rd:
            if len(linha) != len(cab):
                continue
            n += 1
            for c, v in zip(cab, linha):
                if v == "":
                    vazios[c] += 1
                elif len(valores[c]) < 4000:
                    valores[c][v] += 1
    return cab, n, vazios, valores


def resumo(ano, mes, tipo, classe):
    arq = caminho(ano, mes, tipo, classe)
    print("=" * 100)
    print(f"{ano} {mes} {tipo} {classe}")
    print(f"  arquivo: {os.path.basename(arq)}  ({os.path.getsize(arq)/1e6:.2f} MB)")
    cab, n, vazios, valores = censo(arq)
    print(f"  linhas: {n}  colunas: {len(cab)}")
    for c in cab:
        distintos = len(valores[c])
        amostra = ", ".join(list(valores[c])[:6])
        print(f"    {c:<22} vazios={vazios[c]:>7}  distintos={distintos:<5} ex: {amostra[:80]}")
    return cab, valores


if __name__ == "__main__":
    for ano, mes, tipo, classe in ARQUIVOS:
        resumo(ano, mes, tipo, classe)
