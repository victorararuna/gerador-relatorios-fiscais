# -*- coding: utf-8 -*-
"""RREO Anexo 14 — Demonstrativo Simplificado: as linhas de despesa.

As três linhas de despesa do simplificado saem direto das contas 6.2.2.1.3
da matriz:

    62213*  (01 a 07)  -> Despesas Empenhadas
    622130300/0400/0700 -> Despesas Liquidadas
    622130400           -> Despesas Pagas
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RREO = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn\RREO\2025\RREO_24_2025_bim6_anexo14.csv")
COLUNA = "Até o Bimestre"

LINHAS = {
    "empenhadas": "Despesas Empenhadas",
    "liquidadas": "Despesas Liquidadas",
    "pagas": "Despesas Pagas",
    "rcl": "Receita Corrente Líquida",
    "rcl_endividamento": ("Receita Corrente Líquida Ajustada para Cálculo "
                          "dos Limites de Endividamento"),
    "rcl_pessoal": ("Receita Corrente Líquida Ajustada para Cálculo "
                    "dos Limites da Despesa com Pessoal"),
}


def oficial(caminho: str | None = None) -> dict:
    valores = {}
    with open(caminho or RREO, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] != COLUNA:
                continue
            for chave, nome in LINHAS.items():
                if r["conta"] == nome and chave not in valores:
                    valores[chave] = float(r["valor"])
    return valores


def matriz(ano: int = 2025, mes: int = 12,
           anexo3: str | None = None) -> dict:
    acervo = M.Acervo(MSC)
    emp = liq = pago = 0.0
    for r in acervo.ler(ano, mes, classe=6, tipo_valor="ending_balance"):
        if not r.conta.startswith("62213"):
            continue
        emp += r.liquido
        if r.conta in ("622130300", "622130400", "622130700"):
            liq += r.liquido
        if r.conta == "622130400":
            pago += r.liquido

    import app.anexo3_msc as A3
    rcl = A3.ler_rcl(anexo3 or os.path.join(
        os.path.dirname(RREO), "RREO_24_2025_bim6_anexo03.csv"))
    return {"empenhadas": emp, "liquidadas": liq, "pagas": pago,
            "rcl": rcl.rcl,
            "rcl_endividamento": rcl.ajustada_endividamento,
            "rcl_pessoal": rcl.ajustada_pessoal}


def main() -> int:
    of, ms = oficial(), matriz()
    print(f"{'linha':<24}{'oficial':>18}{'MSC':>18}{'dif':>10}")
    for chave in LINHAS:
        o, v = of.get(chave, 0.0), ms.get(chave, 0.0)
        print(f"{chave:<24}{o:>18,.2f}{v:>18,.2f}{v - o:>10,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
