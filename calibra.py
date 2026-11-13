# -*- coding: utf-8 -*-
"""Calibração: qual regra de CO (e em que Poder) fecha as três janelas?"""
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
PO_EXEC = M.PO_EXECUTIVO

CO_BENEFICIO = {"1111", "1151", "2111", "2151", "2211"}


def carregar():
    """(ano, mes, linha, po, co) -> valor; mais série mensal por linha."""
    acervo = M.Acervo(MSC)
    dados = defaultdict(float)
    meses = sorted({(a, m) for a in (2025, 2026) for m in range(1, 13)})
    for ano, mes in meses:
        try:
            linhas = list(acervo.ler(ano, mes))
        except M.ErroMSC:
            continue
        for r in linhas:
            if r.conta not in M.CONTAS_LIQUIDACAO or r.po not in PO_EXEC:
                continue
            linha = M._classificar(r.nd)
            if linha is None:
                continue
            dados[(ano, mes, linha, r.po, r.compl)] += r.liquido
    return dados


def total_janela(dados, pares, regra):
    total = 0.0
    for (ano, mes, linha, po, co), v in dados.items():
        if (ano, mes) not in pares:
            continue
        if regra["linhas"] and linha not in regra["linhas"]:
            continue
        if regra.get("pos") and po not in regra["pos"]:
            continue
        if regra.get("filtrar") and co not in CO_BENEFICIO:
            continue
        total += v
    return total


def principal(dados, pares, regra):
    """Total I: ativo + inativo + terceirização (sem não executada)."""
    venc = total_janela(dados, pares, {**regra, "linhas": {"vencimentos", "judiciais"},
                                       "filtrar": False})
    patr = total_janela(dados, pares, {**regra, "linhas": {"patronal"}, "filtrar": False})
    terc = total_janela(dados, pares, {**regra, "linhas": {"terceirizacao"}, "filtrar": False})
    inat = total_janela(dados, pares, {**regra, "linhas": {"aposentadorias", "pensoes"}})
    return venc + patr + terc + inat


def oficial(ano, quad):
    arq = os.path.join(RGF_DIR, str(ano), f"RGF_24_{ano}_quad{quad}_anexo01.csv")
    with open(arq, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["conta"] == "DESPESA BRUTA COM PESSOAL (I)" and r["coluna"].startswith("TOTAL"):
                return float(r["valor"])
    return float("nan")


def main() -> int:
    dados = carregar()
    regras = {
        "sem filtro": {"linhas": set(), "filtrar": False},
        "filtro total": {"linhas": set(), "filtrar": True},
        "filtro só 10112": {"linhas": set(), "filtrar": True, "pos": ("10112",)},
        "filtro só 10111": {"linhas": set(), "filtrar": True, "pos": ("10111",)},
        "filtro apos+pens, não 10112": {"linhas": {"aposentadorias", "pensoes"},
                                        "filtrar": True, "pos": ("10111", "60611")},
    }
    print(f"{'regra':<32}" + "".join(f"{f'{a}Q{q}':>16}" for a, q in CASOS) + f"{'pior':>9}")
    for nome, regra in regras.items():
        erros = []
        for ano, quad in CASOS:
            pares = set(M.periodos_janela(ano, M.MES_DO_QUADRIMESTRE[quad]))
            ne = M.nao_executada(M.Acervo(MSC), sorted(pares), PO_EXEC)
            nos = principal(dados, pares, regra) + ne
            of = oficial(ano, quad)
            erros.append((nos / of - 1) * 100)
        pior = max(abs(e) for e in erros)
        print(f"{nome:<32}" + "".join(f"{e:>15.2f}%" for e in erros) + f"{pior:>8.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

