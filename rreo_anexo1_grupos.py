# -*- coding: utf-8 -*-
"""RREO Anexo 1 (Balanço Orçamentário) — despesa por grupo de natureza.

Mesmo teste do Anexo 2: o total da MSC por grupo menos o "exceto intra"
homologado deve ser positivo em todos os grupos e somar exatamente a
intra-orçamentária declarada (R$ 2.664.925.314,43).
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
        r"\siconfi_rn\RREO\2025\RREO_24_2025_bim6_anexo01.csv")
COLUNA = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)"
INTRA = 2_664_925_314.43

#: prefixo da natureza -> (rótulo oficial, grupo)
GRUPOS = {
    "31": "PESSOAL E ENCARGOS SOCIAIS",
    "32": "JUROS E ENCARGOS DA DÍVIDA",
    "33": "OUTRAS DESPESAS CORRENTES",
    "44": "INVESTIMENTOS",
    "45": "INVERSÕES FINANCEIRAS",
    "46": "AMORTIZAÇÃO DA DÍVIDA",
}


def oficial():
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
            if bloco != 1 or r["coluna"] != COLUNA:
                continue
            if c in GRUPOS.values():
                bruto[c] = float(r["valor"])
    return bruto


def nosso():
    acervo = M.Acervo(MSC)
    por_grupo = {}
    for r in acervo.ler(2025, 12, tipo_valor="ending_balance"):
        if r.conta not in M.CONTAS_LIQUIDACAO or not r.nd:
            continue
        g = r.nd[:2]
        por_grupo[g] = por_grupo.get(g, 0.0) + r.liquido
    return por_grupo


def main() -> int:
    of = oficial()
    ms = nosso()
    print(f"{'grupo':<30}{'exceto intra':>18}{'MSC total':>18}{'intra':>18}")
    total_of = total_ms = 0.0
    negativos = []
    for pref, nome in GRUPOS.items():
        o = of.get(nome, 0.0)
        v = ms.get(pref, 0.0)
        total_of += o
        total_ms += v
        d = v - o
        if d < -1:
            negativos.append((nome, d))
        print(f"{nome:<30}{o:>18,.2f}{v:>18,.2f}{d:>18,.2f}")
    print("-" * 84)
    print(f"{'TOTAL':<30}{total_of:>18,.2f}{total_ms:>18,.2f}"
          f"{total_ms - total_of:>18,.2f}")
    print(f"\nintra declarada no Anexo 1: {INTRA:,.2f}")
    print(f"delta apurado ............. {total_ms - total_of:,.2f}")
    print("todos os grupos com delta >= 0" if not negativos
          else f"grupos negativos: {negativos}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

