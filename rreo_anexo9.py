# -*- coding: utf-8 -*-
"""RREO Anexo 9 — Operações de Crédito: o lado da despesa de capital.

As linhas de despesa do demonstrativo são o **empenhado** das contas 6.2.2.1.3
(soma de todas as 62213*), agrupado por natureza:

    44 -> Investimentos
    45 -> Inversões Financeiras
    46 -> Amortização da Dívida

O lado da receita (operações de crédito realizadas) não fecha: o demonstrativo
declara R$ 2.491.012,67 e a matriz tem R$ 6,70 bi brutos na natureza 17115001 —
a diferença é refinanciamento, que os demonstrativos não computam.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RREO = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn\RREO\2025\RREO_24_2025_bim6_anexo09.csv")
COLUNA = "DESPESAS EMPENHADAS (e)"

LINHAS = {
    "investimentos": "Investimentos",
    "inversoes": "Inversões Financeiras",
    "amortizacao": "Amortização da Dívida",
    "capital": "DESPESAS DE CAPITAL",
}

GRUPO = {"investimentos": "44", "inversoes": "45", "amortizacao": "46"}


def oficial() -> dict:
    valores = {}
    with open(RREO, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] != COLUNA:
                continue
            for chave, nome in LINHAS.items():
                if r["conta"] == nome and chave not in valores:
                    valores[chave] = float(r["valor"])
    return valores


def matriz() -> dict:
    acervo = M.Acervo(MSC)
    emp = Counter()
    for r in acervo.ler(2025, 12, classe=6, tipo_valor="ending_balance"):
        if r.conta.startswith("62213") and r.nd:
            emp[r.nd[:2]] += r.liquido
    saida = {chave: emp[grupo] for chave, grupo in GRUPO.items()}
    saida["capital"] = sum(saida.values())
    return saida


def main() -> int:
    of, ms = oficial(), matriz()
    print(f"{'linha':<26}{'oficial':>18}{'MSC':>18}{'dif':>10}")
    for chave in LINHAS:
        o, v = of.get(chave, 0.0), ms.get(chave, 0.0)
        print(f"{chave:<26}{o:>18,.2f}{v:>18,.2f}{v - o:>10,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
