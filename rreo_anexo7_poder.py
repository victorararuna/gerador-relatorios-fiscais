# -*- coding: utf-8 -*-
"""RREO Anexo 7 por Poder — valida o recorte de PO contra os arquivos oficiais.

Os arquivos `RREO_24_<ano>_bim<n>_anexo07_<P>.csv` trazem o demonstrativo de
cada Poder. Aqui comparamos as linhas de restos a pagar do Poder com o que as
contas 6.3.1/6.3.2 da matriz produzem para os POs correspondentes.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict
from typing import Dict, Tuple

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_completo\MSC"
RREO = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_completo\RREO"

#: co_poder -> POs da matriz
PODERES = {
    "E": ("10111", "10112"),
    "L": ("20211", "20212"),
    "J": ("30390",),
    "M": ("50511",),
    "D": ("60611",),
}

CONTAS = {
    "rpp_pagos": "632200000",
    "rpp_cancelados": "632910000",
    "rpp_saldo": "632100000",
    "rpn_pagos": "631400000",
    "rpn_cancelados": "631990000",
}

COLUNAS = {
    "rpp_pagos": "Pagos (c)",
    "rpp_cancelados": "Cancelados (d)",
    "rpp_saldo": "Saldo e = (a + b) - (c + d)",
    "rpn_pagos": "Pagos (i)",
    "rpn_cancelados": "Cancelados (j)",
}

TOTAL = "TOTAL (III) = (I + II)"


def oficial(arquivo: str) -> Dict[str, float]:
    valores = {}
    if not os.path.exists(arquivo):
        return valores
    with open(arquivo, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["conta"] != TOTAL:
                continue
            for chave, coluna in COLUNAS.items():
                if r["coluna"] == coluna:
                    valores[chave] = float(r["valor"])
    return valores


def matriz(ano: int, bimestre: int, pos: Tuple[str, ...]) -> Dict[str, float]:
    acervo = M.Acervo(MSC)
    meses = list(range(1, 2 * bimestre + 1))
    saida = defaultdict(float)
    for mes in meses:
        for r in acervo.ler(ano, mes, classe=6):
            if r.po not in pos:
                continue
            for chave, conta in CONTAS.items():
                if r.conta == conta:
                    saida[chave] += r.liquido
    # saldo é estoque: usa o saldo do mês de referência
    try:
        for r in acervo.ler(ano, meses[-1], classe=6, tipo_valor="ending_balance"):
            if r.po in pos and r.conta == CONTAS["rpp_saldo"]:
                saida["rpp_saldo"] = saida.get("rpp_saldo", 0.0) + r.liquido
    except Exception:  # noqa: BLE001
        pass
    return saida


def main() -> int:
    ano = int(sys.argv[1]) if len(sys.argv) > 1 else 2025
    bim = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    print(f"RREO Anexo 7 — {ano} B{bim} — por Poder\n")
    total_ok = total = 0
    for poder, pos in PODERES.items():
        of = oficial(os.path.join(RREO, str(ano),
                                  f"RREO_24_{ano}_bim{bim}_anexo07_{poder}.csv"))
        ms = matriz(ano, bim, pos)
        if not of:
            continue
        print(f"[{poder}] POs {', '.join(pos)}")
        for chave in CONTAS:
            o, v = of.get(chave, 0.0), ms.get(chave, 0.0)
            ok = abs(v - o) <= 0.01
            total += 1
            total_ok += ok
            print(f"   {chave:<16}{v:>18,.2f}{o:>18,.2f}"
                  f"{'  OK' if ok else '  dif'}")
    print(f"\n{total_ok} de {total} linhas exatas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
