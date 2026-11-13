# -*- coding: utf-8 -*-
"""RREO Anexo 1 — receita: as três bases lado a lado.

Compara, por origem da natureza da receita:
  * RREO Anexo 1 (líquido de deduções)
  * classe 5 da matriz
  * RREO Anexo 3 (bruto de deduções)

    python rreo_anexo1_receita.py
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
BASE = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn\RREO\2025")

ORIGENS = {
    "11": ("Impostos, taxas e contribuições de melhoria",
           "IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA",
           "Impostos, Taxas e Contribuições de Melhoria"),
    "12": ("Contribuições", "CONTRIBUIÇÕES", "Contribuições"),
    "13": ("Receita patrimonial", "RECEITA PATRIMONIAL", "Receita Patrimonial"),
    "15": ("Receita industrial", "RECEITA INDUSTRIAL", "Receita Industrial"),
    "16": ("Receita de serviços", "RECEITA DE SERVIÇOS", "Receita de Serviços"),
    "17": ("Transferências correntes", "TRANSFERÊNCIAS CORRENTES",
           "Transferências Correntes"),
    "19": ("Outras receitas correntes", "OUTRAS RECEITAS CORRENTES",
           "Outras Receitas Correntes"),
}


def _coluna(arquivo: str, coluna: str) -> dict:
    saida = {}
    with open(arquivo, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == coluna:
                saida.setdefault(r["conta"], float(r["valor"]))
    return saida


def matriz_por_origem() -> dict:
    acervo = M.Acervo(MSC)
    por_origem = {}
    for r in acervo.ler(2025, 12, classe=5, tipo_valor="ending_balance"):
        if not r.receita:
            continue
        por_origem[r.receita[:2]] = por_origem.get(r.receita[:2], 0.0) - r.liquido
    return por_origem


def main() -> int:
    anexo1 = _coluna(os.path.join(BASE, "RREO_24_2025_bim6_anexo01.csv"),
                     "Até o Bimestre (c)")
    anexo3 = _coluna(os.path.join(BASE, "RREO_24_2025_bim6_anexo03.csv"),
                     "TOTAL (ÚLTIMOS 12 MESES)")
    ms = matriz_por_origem()

    print(f"{'origem':<40}{'Anexo 1':>18}{'MSC':>18}{'Anexo 3':>18}"
          f"{'MSC-1':>14}")
    for pref, (nome, linha1, linha3) in ORIGENS.items():
        a1 = anexo1.get(linha1, 0.0)
        a3 = next((v for c, v in anexo3.items() if c.startswith(linha3)), 0.0)
        v = ms.get(pref, 0.0)
        print(f"{nome[:38]:<40}{a1:>18,.2f}{v:>18,.2f}{a3:>18,.2f}"
              f"{v - a1:>14,.2f}")

    capital_ms = sum(v for k, v in ms.items() if k.startswith("2"))
    capital_a1 = anexo1.get("RECEITAS DE CAPITAL", 0.0)
    intra_ms = sum(v for k, v in ms.items() if k.startswith("7"))
    intra_a1 = anexo1.get("RECEITAS (INTRA-ORÇAMENTÁRIAS) (II)", 0.0)
    print(f"{'Receitas de capital':<40}{capital_a1:>18,.2f}"
          f"{capital_ms:>18,.2f}{'':>18}{capital_ms - capital_a1:>14,.2f}")
    print(f"{'Receitas intra-orçamentárias':<40}{intra_a1:>18,.2f}"
          f"{intra_ms:>18,.2f}{'':>18}{intra_ms - intra_a1:>14,.2f}")
    print(f"{'TOTAL':<40}{sum(anexo1.get(l, 0.0) for _, l, _ in ORIGENS.values()) + capital_a1 + intra_a1:>18,.2f}"
          f"{sum(ms.values()):>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
