# -*- coding: utf-8 -*-
"""Receita realizada de RR pela MSC, sem gabarito (rodada 175 — Opcao A).

A receita arrecadada esta na **classe 5** (receita orcamentaria), conta com
natureza da receita (NR). O acumulado do exercicio e o `ending_balance` do mes
de referencia; o movimento do bimestre e o `period_change` dos dois ultimos meses.

Agrupando pela origem (NR[:2]) obtem-se as categorias do Anexo 1:

    11 impostos/taxas   12 contribuicoes   13 patrimonial   16 servicos
    17 transferencias correntes   19 outras correntes
    21 operacoes de credito   22 alienacao   24 transferencias de capital
    7x intra-orcamentarias

As colunas de **previsao/dotacao** (LOA) NAO vem da matriz — ficam em branco.
Preenchemos so a receita REALIZADA ("Ate o Bimestre (c)" e "No Bimestre (b)").
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "app"))

#: origem (NR[:2]) -> rotulo da categoria no Anexo 1
CATEGORIAS = {
    "11": "IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA",
    "12": "CONTRIBUIÇÕES",
    "13": "RECEITA PATRIMONIAL",
    "14": "RECEITA AGROPECUÁRIA",
    "15": "RECEITA INDUSTRIAL",
    "16": "RECEITA DE SERVIÇOS",
    "17": "TRANSFERÊNCIAS CORRENTES",
    "19": "OUTRAS RECEITAS CORRENTES",
    "21": "OPERAÇÕES DE CRÉDITO",
    "22": "ALIENAÇÃO DE BENS",
    "23": "AMORTIZAÇÕES DE EMPRÉSTIMOS",
    "24": "TRANSFERÊNCIAS DE CAPITAL",
    "29": "OUTRAS RECEITAS DE CAPITAL",
}
COL_ATE = "Até o Bimestre (c)"
COL_NO = "No Bimestre (b)"


def _acervo(raiz: str):
    from acervo import Acervo
    return Acervo(raiz)


def por_origem(raiz: str, ano: int, mes_fim: int,
               tipo: str = "ending_balance", meses=None) -> dict:
    """Receita por origem (NR[:2]). ending_balance acumula; period_change soma meses."""
    ac = _acervo(raiz)
    por = defaultdict(float)
    lista = meses if meses is not None else [mes_fim]
    for m in lista:
        try:
            regs = ac.ler(ano, m, classe=5, tipo_valor=tipo)
        except Exception:
            continue
        for r in regs:
            nr = r.nr or ""
            if not nr:
                continue
            por[nr[:2]] += -r.liquido      # receita e devedora na matriz
    return dict(por)


def _agregados(por: dict) -> dict:
    correntes = sum(v for k, v in por.items() if k.startswith("1"))
    capital = sum(v for k, v in por.items() if k.startswith("2"))
    intra = sum(v for k, v in por.items() if k.startswith("7"))
    exceto = correntes + capital
    return {
        "RECEITAS CORRENTES": correntes,
        "RECEITAS DE CAPITAL": capital,
        "RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)": exceto,
        "RECEITAS (INTRA-ORÇAMENTÁRIAS) (II)": intra,
        "SUBTOTAL DAS RECEITAS (III) = (I + II)": exceto + intra,
        "TOTAL DAS RECEITAS (V) = (III + IV)": exceto + intra,
    }


def celulas_anexo1(raiz: str, ano: int, bimestre: int) -> dict:
    """Celulas (conta, coluna) da receita REALIZADA do Anexo 1."""
    mes_fim = 2 * bimestre
    acum = por_origem(raiz, ano, mes_fim, "ending_balance")
    bim = por_origem(raiz, ano, mes_fim, "period_change",
                     meses=[mes_fim - 1, mes_fim])
    cel = {}
    for origem, valor in acum.items():
        if origem in CATEGORIAS:
            cel[(CATEGORIAS[origem], COL_ATE)] = valor
    for rotulo, valor in _agregados(acum).items():
        cel[(rotulo, COL_ATE)] = valor
    for origem, valor in bim.items():
        if origem in CATEGORIAS:
            cel[(CATEGORIAS[origem], COL_NO)] = valor
    for rotulo, valor in _agregados(bim).items():
        cel[(rotulo, COL_NO)] = valor
    return cel


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default=os.path.join(RAIZ, "dados", "rr_msc"))
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=5)
    a = ap.parse_args()
    acum = por_origem(a.raiz, a.ano, 2 * a.bimestre)
    print("Receita realizada por origem (acumulado):")
    for k in sorted(acum):
        print(f"   {k} {CATEGORIAS.get(k, '?')[:40]:<42}{acum[k]:>18,.2f}")
    print("\nAgregados:")
    for k, v in _agregados(acum).items():
        print(f"   {k[:48]:<50}{v:>18,.2f}")
