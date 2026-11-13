# -*- coding: utf-8 -*-
"""Fevereiro/2025: que natureza explica a troca de ~131 mi entre vencimentos e aposentadorias."""
from __future__ import annotations

import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
PO_EXEC = M.PO_EXECUTIVO


def main() -> int:
    acervo = M.Acervo(MSC)

    por_mes_nd = defaultdict(lambda: defaultdict(float))
    por_po = defaultdict(float)
    for mes in range(1, 13):
        for r in acervo.ler(2025, mes):
            if r.conta not in M.CONTAS_LIQUIDACAO or r.po not in PO_EXEC or not r.nd:
                continue
            linha = M._classificar(r.nd)
            if linha is None:
                continue
            por_mes_nd[r.nd][mes] += r.liquido
            if r.nd.startswith("31909201"):
                por_po[(r.po, mes)] += r.liquido

    print("31909201 (exercícios anteriores de vencimentos) por PO e mês:")
    for (po, mes), v in sorted(por_po.items()):
        print(f"   {po:<7} m{mes:02d} {v:>18,.2f}")

    print("\nFevereiro: naturezas muito acima da média dos outros meses")
    print(f"{'ND':<10}{'média jan-nov':>18}{'fev':>18}{'excesso':>16}{'linha':<14}")
    linhas = []
    for nd, serie in por_mes_nd.items():
        outros = [serie.get(m, 0.0) for m in range(1, 13) if m != 2]
        media = sum(outros) / len(outros)
        fev = serie.get(2, 0.0)
        linhas.append((fev - media, nd, media, fev))
    linhas.sort(reverse=True)
    for excesso, nd, media, fev in linhas[:12]:
        print(f"{nd:<10}{media:>18,.2f}{fev:>18,.2f}{excesso:>16,.2f}"
              f"{M._classificar(nd):<14}")
    print("\n... e as maiores quedas:")
    for excesso, nd, media, fev in linhas[-6:]:
        print(f"{nd:<10}{media:>18,.2f}{fev:>18,.2f}{excesso:>16,.2f}"
              f"{M._classificar(nd):<14}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
