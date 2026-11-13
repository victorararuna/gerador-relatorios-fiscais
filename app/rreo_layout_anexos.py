# -*- coding: utf-8 -*-
"""Adaptadores: da apuração da matriz para as células do layout oficial.

Cada função devolve um dicionário (conta, coluna) -> valor, usando exatamente os
rótulos do arquivo do Siconfi (o molde). O que não é apurado simplesmente não
entra — a célula fica em branco.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rreo_gerador import GRUPOS, ApuracaoRREO  # noqa: E402

Celulas = Dict[Tuple[str, str], float]

#: colunas de despesa no Anexo 1 do RREO
COL_EMPENHADA = "DESPESAS EMPENHADAS ATÉ O BIMESTRE (f)"
COL_LIQUIDADA = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)"
COL_PAGA = "DESPESAS PAGAS ATÉ O BIMESTRE (j)"
COL_EMP_BIM = "DESPESAS EMPENHADAS NO BIMESTRE"
COL_LIQ_BIM = "DESPESAS LIQUIDADAS NO BIMESTRE"

#: agregados do Anexo 1
AGREGADOS_1 = {
    "DESPESAS CORRENTES": ("31", "32", "33"),
    "DESPESAS DE CAPITAL": ("44", "45", "46"),
}


def anexo14(res: ApuracaoRREO) -> Celulas:
    """Simplificado: três linhas, uma coluna."""
    col = "Até o Bimestre"
    return {
        ("Despesas Empenhadas", col): res.empenhado,
        ("Despesas Liquidadas", col): res.liquidado,
        ("Despesas Pagas", col): res.pago,
    }


def anexo9(res: ApuracaoRREO) -> Celulas:
    """Operações de crédito: despesa de capital empenhada."""
    col = "DESPESAS EMPENHADAS (e)"
    cel: Celulas = {}
    for chave, pref in (("Investimentos", "44"),
                        ("Inversões Financeiras", "45"),
                        ("Amortização da Dívida", "46")):
        g = res.grupos.get(pref)
        if g:
            cel[(chave, col)] = g["empenhado"]
    capital = sum(res.grupos.get(p, {}).get("empenhado", 0.0)
                  for p in ("44", "45", "46"))
    for conta in ("DESPESAS DE CAPITAL", "DESPESA DE CAPITAL LÍQUIDA (II)"):
        cel[(conta, col)] = capital
    return cel


def anexo7(res: ApuracaoRREO) -> Celulas:
    """Restos a pagar: só as linhas de TOTAL (o detalhe por Poder exige recorte)."""
    total = "TOTAL (III) = (I + II)"
    cel: Celulas = {}
    pares = {
        "Pagos (c)": "rpp_pagos",
        "Cancelados (d)": "rpp_cancelados",
        "Saldo e = (a + b) - (c + d)": "rpp_saldo",
        "Pagos (i)": "rpn_pagos",
        "Cancelados (j)": "rpn_cancelados",
    }
    for coluna, chave in pares.items():
        v = res.restos.get(chave)
        if v is not None:
            cel[(total, coluna)] = v
    return cel


def anexo1(res: ApuracaoRREO, ocorrencia: int = 0) -> Celulas:
    """Balanço: despesa por grupo. Só as colunas de despesa.

    O layout repete o mesmo rótulo nos blocos 'exceto intra', 'intra' e 'total'.
    Como a matriz não separa intra, o preenchimento deve escolher **um** bloco —
    o adaptador devolve as três colunas e o renderizador aplica na ocorrência
    indicada.
    """
    cel: Celulas = {}
    for pref, nome in GRUPOS.items():
        g = res.grupos.get(pref)
        if not g:
            continue
        cel[(nome, COL_EMPENHADA)] = g["empenhado"]
        cel[(nome, COL_LIQUIDADA)] = g["liquidado"]
        cel[(nome, COL_PAGA)] = g["pago"]
        gb = res.grupos_bimestre.get(pref)
        if gb:
            cel[(nome, COL_EMP_BIM)] = gb["empenhado"]
            cel[(nome, COL_LIQ_BIM)] = gb["liquidado"]
    for nome, prefixos in AGREGADOS_1.items():
        cel[(nome, COL_EMPENHADA)] = sum(
            res.grupos.get(p, {}).get("empenhado", 0.0) for p in prefixos)
        cel[(nome, COL_LIQUIDADA)] = sum(
            res.grupos.get(p, {}).get("liquidado", 0.0) for p in prefixos)
        cel[(nome, COL_PAGA)] = sum(
            res.grupos.get(p, {}).get("pago", 0.0) for p in prefixos)
        cel[(nome, COL_EMP_BIM)] = sum(
            res.grupos_bimestre.get(p, {}).get("empenhado", 0.0) for p in prefixos)
        cel[(nome, COL_LIQ_BIM)] = sum(
            res.grupos_bimestre.get(p, {}).get("liquidado", 0.0) for p in prefixos)
    for nome in ("SUBTOTAL DAS DESPESAS (X) = (VIII + IX)",
                 "TOTAL DAS DESPESAS (XII) = (X + XI)"):
        cel[(nome, COL_EMPENHADA)] = res.empenhado
        cel[(nome, COL_LIQUIDADA)] = res.liquidado
        cel[(nome, COL_PAGA)] = res.pago
    return cel

