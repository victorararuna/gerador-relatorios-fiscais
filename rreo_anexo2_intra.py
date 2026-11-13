# -*- coding: utf-8 -*-
"""RREO Anexo 2: o total por função (MSC) menos o 'exceto intra' (oficial)
deveria ser exatamente a despesa intra-orçamentária de cada função.

Se todos os deltas forem positivos e a soma fechar com os R$ 2.664.925.314,43
declarados no Anexo 1, o atributo ``funcao`` da matriz está correto e a
diferença é a intra que o Siconfi não publica por função.
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from rreo_anexo2 import COLUNA, FUNCOES, RREO, nosso_por_funcao  # noqa: E402

INTRA_RREO = 2_664_925_314.43
EXCETO_RREO = 20_696_574_215.20


def oficial_exceto():
    bloco = 0
    bruto = {}
    with open(RREO, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            c = r["conta"]
            if c.startswith("DESPESAS (EXCETO INTRA"):
                bloco = 1
                continue
            if c.startswith("DESPESAS (INTRA"):
                bloco = 2
                continue
            if c.startswith("TOTAL (III)"):
                bloco = 3
                continue
            if bloco != 1 or r["coluna"] != COLUNA:
                continue
            if c in FUNCOES.values():
                bruto[c] = bruto.get(c, 0.0) + float(r["valor"])
    return bruto


def main() -> int:
    of = oficial_exceto()
    ms = nosso_por_funcao()
    print(f"{'função':<26}{'exceto intra':>18}{'MSC total':>18}{'delta':>18}")
    negativos = []
    total_of = total_ms = 0.0
    for cod, nome in FUNCOES.items():
        o = of.get(nome, 0.0)
        v = ms.get(cod, 0.0)
        if not o and not v:
            continue
        total_of += o
        total_ms += v
        delta = v - o
        if delta < -1:
            negativos.append((nome, delta))
        print(f"{nome:<26}{o:>18,.2f}{v:>18,.2f}{delta:>18,.2f}")
    print("-" * 80)
    print(f"{'TOTAL':<26}{total_of:>18,.2f}{total_ms:>18,.2f}"
          f"{total_ms - total_of:>18,.2f}")
    print(f"\nexceto intra (homologado): {total_of:,.2f}  "
          f"(arquivo: {EXCETO_RREO:,.2f})")
    print(f"intra (homologado) ....... {INTRA_RREO:,.2f}")
    print(f"delta total .............. {total_ms - total_of:,.2f}")
    if negativos:
        print(f"\nfunções com delta negativo ({len(negativos)}):")
        for nome, d in negativos:
            print(f"   {nome:<24}{d:>18,.2f}")
    else:
        print("\ntodas as funções com delta >= 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
