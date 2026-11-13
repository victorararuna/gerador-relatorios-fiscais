# -*- coding: utf-8 -*-
"""Onde nasce o desvio: compara dezembro com a média dos outros meses.

Procura lançamentos de encerramento (concentrados em dezembro) nas contas de
liquidação do Executivo.
"""
from __future__ import annotations

import os
import statistics
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_msc import Acervo  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
PO_EXEC = {"10111", "10112", "60611"}
CONTAS = ("622130300", "622130400", "622130700")


def main() -> int:
    acervo = Acervo(MSC)
    meses = acervo.meses(2025, 6, "period_change")

    total_mes = {}
    por_chave = defaultdict(dict)   # (conta, elemento) -> {mes: valor}

    for mes in meses:
        s = 0.0
        for r in acervo.ler(2025, mes):
            if r.conta not in CONTAS or r.po not in PO_EXEC:
                continue
            s += r.liquido
            chave = (r.conta, r.elemento or "(sem ND)")
            por_chave[chave][mes] = por_chave[chave].get(mes, 0.0) + r.liquido
        total_mes[mes] = s

    print("total do Executivo por mês:")
    for mes in meses:
        print(f"   m{mes:02d}  {total_mes[mes]:>18,.2f}")

    print("\nlançamentos cujo dezembro destoa da média (jan-nov):")
    print(f"{'conta':<12}{'elem':<10}{'média jan-nov':>18}{'dezembro':>18}"
          f"{'excesso':>16}{'n meses':>9}")
    linhas = []
    for (conta, elem), serie in por_chave.items():
        outros = [serie.get(m, 0.0) for m in meses if m != 12]
        media = statistics.mean(outros) if outros else 0.0
        dez = serie.get(12, 0.0)
        linhas.append((dez - media, conta, elem, media, dez, len(serie)))
    linhas.sort(reverse=True)
    for excesso, conta, elem, media, dez, n in linhas[:20]:
        print(f"{conta:<12}{elem:<10}{media:>18,.2f}{dez:>18,.2f}"
              f"{excesso:>16,.2f}{n:>9}")

    print("\nmaiores quedas em dezembro:")
    for excesso, conta, elem, media, dez, n in linhas[-8:]:
        print(f"{conta:<12}{elem:<10}{media:>18,.2f}{dez:>18,.2f}"
              f"{excesso:>16,.2f}{n:>9}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
