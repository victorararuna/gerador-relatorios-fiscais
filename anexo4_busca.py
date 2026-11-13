# -*- coding: utf-8 -*-
"""Anexo 4: onde estão as operações de crédito de 2025 na matriz?"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
ALVO_ANO = 2_491_012.67
ALVO_QUAD = 1_913_445.77


def main() -> int:
    acervo = M.Acervo(MSC)
    por_mes = defaultdict(lambda: defaultdict(float))
    for mes in range(1, 13):
        for r in acervo.ler(2025, mes, classe=5, tipo_valor="period_change"):
            if not r.receita:
                continue
            por_mes[r.receita][mes] += r.liquido

    print(f"{'natureza':<12}{'ano':>18}{'m09-m12':>18}")
    candidatos = []
    for nat, serie in por_mes.items():
        ano = sum(serie.values())
        quad = sum(v for m, v in serie.items() if m >= 9)
        if abs(ano - ALVO_ANO) < 5_000 or abs(quad - ALVO_QUAD) < 5_000:
            candidatos.append((nat, ano, quad))
    for nat, ano, quad in sorted(candidatos):
        print(f"{nat:<12}{ano:>18,.2f}{quad:>18,.2f}  <== candidato")

    print("\nreceitas 17xx com maior valor anual:")
    linhas = sorted(por_mes.items(), key=lambda kv: -abs(sum(kv[1].values())))
    for nat, serie in linhas:
        if not nat.startswith("17"):
            continue
        ano = sum(serie.values())
        quad = sum(v for m, v in serie.items() if m >= 9)
        print(f"{nat:<12}{ano:>18,.2f}{quad:>18,.2f}")
        if ano < 0.001:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
