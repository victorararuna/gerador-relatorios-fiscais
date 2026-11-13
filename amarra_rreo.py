# -*- coding: utf-8 -*-
"""Amarração com o RREO: a MSC reproduz o total liquidado do Balanço Orçamentário?

RREO 2025 B6, Anexo 1, coluna 'DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)':
  DESPESAS (EXCETO INTRA) .......... 20.696.574.215,20
  DESPESAS (INTRA) .................  2.664.925.314,43
  TOTAL ............................ 23.361.499.529,63
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_msc import Acervo  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
CONTAS = ("622130300", "622130400", "622130700")

RREO_TOTAL = 23_361_499_529.63
RREO_EXCETO_INTRA = 20_696_574_215.20
RREO_INTRA = 2_664_925_314.43
RREO_PESSOAL_EXCETO = 14_997_034_125.53

RGF_BRUTA = 15_478_621_265.08


def main() -> int:
    acervo = Acervo(MSC)
    meses = acervo.meses(2025, 6, "period_change")

    total = pessoal = 0.0
    pessoal_po = {}
    for r in (r for m in meses for r in acervo.ler(2025, m)):
        if r.conta not in CONTAS:
            continue
        total += r.liquido
        if r.nd.startswith("31"):
            pessoal += r.liquido
            pessoal_po[r.po] = pessoal_po.get(r.po, 0.0) + r.liquido

    print(f"MSC, contas 62213*, todos os POs .... {total:>18,.2f}")
    print(f"RREO total liquidado ................ {RREO_TOTAL:>18,.2f}")
    print(f"diferença ........................... {total - RREO_TOTAL:>18,.2f}")
    print()
    print(f"MSC, ND 31 (pessoal), todos os POs .. {pessoal:>18,.2f}")
    print(f"RREO pessoal exceto intra ........... {RREO_PESSOAL_EXCETO:>18,.2f}")
    intra = pessoal - RREO_PESSOAL_EXCETO
    print(f"intra-orçamentária de pessoal ....... {intra:>18,.2f}")
    print(f"  (2024, investigação: 2.270.546.730,00)")
    print()
    print(f"RGF bruta (I) ....................... {RGF_BRUTA:>18,.2f}")
    print(f"MSC pessoal - intra ................. {pessoal - intra:>18,.2f}"
          f"   (dif {pessoal - intra - RGF_BRUTA:>14,.2f})")
    print(f"RGF - RREO exceto intra ............. {RGF_BRUTA - RREO_PESSOAL_EXCETO:>18,.2f}")
    print()
    print("pessoal por PO:")
    for po, v in sorted(pessoal_po.items()):
        print(f"   {po:<7} {v:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
