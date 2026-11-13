# -*- coding: utf-8 -*-
"""Onde a curva se descola: comparação mês a mês das janelas móveis."""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF_DIR = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
           r"\siconfi_rn\RGF")
CASOS = [(2025, 3), (2026, 1), (2026, 2)]
COLUNAS = [f"<MR-{i}>" for i in range(11, 0, -1)] + ["<MR>"]
ALVO = "DESPESA BRUTA COM PESSOAL (I)"


def oficial_por_mes(ano, quad):
    arq = os.path.join(RGF_DIR, str(ano), f"RGF_24_{ano}_quad{quad}_anexo01.csv")
    valores = {}
    with open(arq, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["conta"] == ALVO and r["coluna"] in COLUNAS:
                valores[r["coluna"]] = float(r["valor"])
    return [valores.get(c, 0.0) for c in COLUNAS]


def nosso_por_mes(acervo, pares, filtrar_co=False):
    out = []
    for ano, mes in pares:
        res = M.apurar(acervo, ano, [mes], M.PO_EXECUTIVO, filtrar_co=filtrar_co)
        ne = M.nao_executada(acervo, [(ano, mes)], M.PO_EXECUTIVO)
        i = (res.get("vencimentos") + res.get("judiciais") + res.get("patronal")
             + res.get("aposentadorias") + res.get("pensoes")
             + res.get("terceirizacao") + ne)
        out.append(i)
    return out


def main() -> int:
    acervo = M.Acervo(MSC)
    for filtrar in (False, True):
        print("=" * 110)
        print(f"filtro de CO: {'SIM' if filtrar else 'NÃO'}")
        for ano, quad in CASOS:
            pares = M.periodos_janela(ano, M.MES_DO_QUADRIMESTRE[quad])
            of = oficial_por_mes(ano, quad)
            ms = nosso_por_mes(acervo, pares, filtrar)
            print(f"\n{ano} Q{quad}")
            print(f"{'mês':<9}{'oficial':>18}{'MSC':>18}{'dif':>16}{'%':>9}")
            for (a, m), o, v in zip(pares, of, ms):
                pct = (v / o - 1) * 100 if o else float("nan")
                print(f"{a}-{m:02d}  {o:>18,.2f}{v:>18,.2f}{v - o:>16,.2f}{pct:>8.2f}%")
            print(f"{'TOTAL':<9}{sum(of):>18,.2f}{sum(ms):>18,.2f}"
                  f"{sum(ms) - sum(of):>16,.2f}"
                  f"{(sum(ms) / sum(of) - 1) * 100:>8.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
