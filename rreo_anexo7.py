# -*- coding: utf-8 -*-
"""RREO Anexo 7 — Restos a Pagar: as contas 6.3.1/6.3.2 da matriz.

Movimentos identificados por valor exato contra o homologado:
   632200000  RP processados pagos no exercício
   632910000  RP processados cancelados
   632100000  saldo de RP processados
   631400000  RP não processados pagos
   631990000  RP não processados cancelados
"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RREO = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn\RREO\2025\RREO_24_2025_bim6_anexo07.csv")

CONTAS = {
    "rpp_pagos": "632200000",
    "rpp_cancelados": "632910000",
    "rpp_saldo": "632100000",
    "rpn_pagos": "631400000",
    "rpn_cancelados": "631990000",
}

OFICIAL = {
    "rpp_pagos": ("Pagos (c)", "TOTAL (III) = (I + II)"),
    "rpp_cancelados": ("Cancelados (d)", "TOTAL (III) = (I + II)"),
    "rpp_saldo": ("Saldo e = (a + b) - (c + d)", "TOTAL (III) = (I + II)"),
    "rpn_pagos": ("Pagos (i)", "TOTAL (III) = (I + II)"),
    "rpn_cancelados": ("Cancelados (j)", "TOTAL (III) = (I + II)"),
}


def oficial(caminho: str | None = None) -> dict:
    saida = {}
    with open(caminho or RREO, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            for chave, (col, conta) in OFICIAL.items():
                if r["coluna"] == col and r["conta"] == conta:
                    saida[chave] = float(r["valor"])
    return saida


def matriz(ano: int = 2025, mes: int = 12) -> dict:
    acervo = M.Acervo(MSC)
    soma = defaultdict(float)
    for r in acervo.ler(ano, mes, classe=6, tipo_valor="ending_balance"):
        for chave, conta in CONTAS.items():
            if r.conta == conta:
                soma[chave] += r.liquido
    return soma


def main() -> int:
    of, ms = oficial(), matriz()
    print(f"{'linha':<44}{'oficial':>18}{'MSC':>18}{'dif':>10}")
    for chave in CONTAS:
        o = of.get(chave, 0.0)
        v = ms.get(chave, 0.0)
        print(f"{chave:<44}{o:>18,.2f}{v:>18,.2f}{v - o:>10,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
