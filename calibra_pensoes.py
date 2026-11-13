# -*- coding: utf-8 -*-
"""Pensões: qual desdobramento, se excluído, fecha as três janelas?"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF_DIR = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
           r"\siconfi_rn\RGF")
CASOS = [(2025, 3), (2026, 1), (2026, 2)]


def oficial_pensoes(ano, quad):
    arq = os.path.join(RGF_DIR, str(ano), f"RGF_24_{ano}_quad{quad}_anexo01.csv")
    with open(arq, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["conta"] == "Pensões" and r["coluna"].startswith("TOTAL"):
                return float(r["valor"])
    return float("nan")


def main() -> int:
    acervo = M.Acervo(MSC)
    por_janela = {}
    for ano, quad in CASOS:
        pares = M.periodos_janela(ano, M.MES_DO_QUADRIMESTRE[quad])
        por_se = defaultdict(float)
        for a, m in pares:
            for r in acervo.ler(a, m):
                if (r.conta in M.CONTAS_LIQUIDACAO and r.po in M.PO_EXECUTIVO
                        and M._classificar(r.nd) == "pensoes"):
                    por_se[r.nd] += r.liquido
        por_janela[(ano, quad)] = por_se

    se = sorted({k for d in por_janela.values() for k in d})
    print(f"{'desdobramento':<14}" + "".join(f"{f'{a}Q{q}':>18}" for a, q in CASOS))
    for k in se:
        print(f"{k:<14}" + "".join(f"{por_janela[c].get(k, 0.0):>18,.2f}" for c in CASOS))

    print(f"\n{'cenário':<26}" + "".join(f"{f'{a}Q{q}':>16}" for a, q in CASOS))
    cenarios = [("integral", ())]
    cenarios += [(f"sem {k}", (k,)) for k in se]
    for nome, excluir in cenarios:
        linha = ""
        for c in CASOS:
            total = sum(v for k, v in por_janela[c].items() if k not in excluir)
            of = oficial_pensoes(*c)
            linha += f"{(total / of - 1) * 100:>15.2f}%"
        print(f"{nome:<26}{linha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
