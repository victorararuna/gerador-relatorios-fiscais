# -*- coding: utf-8 -*-
"""RGF Anexo 6 (Demonstrativo Simplificado) — bloco da despesa com pessoal.

Os três limites do bloco são percentuais fixos da RCL ajustada para despesa com
pessoal (LRF, arts. 19, 20 e 22, e art. 59, § 1º, II):
    49,00%  limite máximo
    46,55%  limite prudencial (95% do máximo)
    44,10%  limite de alerta  (90% do máximo)
"""
from __future__ import annotations

import csv
import os
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anexo3_msc import RCL  # noqa: E402

LIMITE_MAXIMO = 0.49
LIMITE_PRUDENCIAL = 0.4655
LIMITE_ALERTA = 0.4410

ROTULOS = {
    "maximo": "Limite Máximo (incisos I, II e III art. 20 da LRF)",
    "prudencial": "Limite Prudencial (parágrafo único art. 22 da LRF)",
    "alerta": "Limite de Alerta (inciso II do §1º do art. 59 da LRF)",
}


def limites(rcl: RCL) -> Dict[str, float]:
    base = rcl.ajustada_pessoal
    return {"maximo": base * LIMITE_MAXIMO,
            "prudencial": base * LIMITE_PRUDENCIAL,
            "alerta": base * LIMITE_ALERTA}


def percentual(dtp: float, rcl: RCL) -> float:
    return dtp / rcl.ajustada_pessoal * 100


def conferir(valores: Dict[str, float], caminho_rgf: str) -> List[Tuple[str, float, float]]:
    oficiais: Dict[str, float] = {}
    with open(caminho_rgf, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"].startswith("VALOR"):
                oficiais.setdefault(r["conta"], float(r["valor"]))
    saida = []
    for chave, rotulo in ROTULOS.items():
        of = next((v for c, v in oficiais.items() if c.startswith(rotulo[:38])),
                  float("nan"))
        saida.append((rotulo, of, valores[chave]))
    return saida


def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Anexo 6 — bloco da despesa com pessoal.")
    ap.add_argument("--rreo", required=True)
    ap.add_argument("--rgf", required=True)
    ap.add_argument("--dtp", type=float, help="DTP apurado; sem ele usa o do Anexo 6")
    args = ap.parse_args()

    from anexo3_msc import ler_rcl

    rcl = ler_rcl(args.rreo)
    vals = limites(rcl)
    print(f"RCL ajustada (pessoal): {rcl.ajustada_pessoal:,.2f}\n")
    for rotulo, of, ms in conferir(vals, args.rgf):
        print(f"{rotulo[:56]:<58}{of:>18,.2f}{ms:>18,.2f}"
              f"{(ms / of - 1) * 100:>8.2f}%")

    if args.dtp:
        print(f"\n% DTP apurado: {percentual(args.dtp, rcl):.2f}%  "
              f"(limite {LIMITE_MAXIMO * 100:.2f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
