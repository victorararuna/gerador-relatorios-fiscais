# -*- coding: utf-8 -*-
"""Completa o Anexo 1 com as linhas que se replicam do ultimo RREO publicado.

O RREO e cumulativo: algumas linhas do Anexo 1 **nao mudam** ao longo do ano e
devem ser replicadas do ultimo RREO publicado, enquanto a execucao
(empenhada/liquidada/paga) vem da matriz do bimestre.

Linhas replicadas do publicado:
    SALDOS DE EXERCICIOS ANTERIORES
    Superavit Financeiro Utilizado para Creditos Adicionais
    RESERVA DE CONTINGENCIA (dotacao)
    PREVISAO INICIAL / PREVISAO ATUALIZADA (receita)
    DOTACAO INICIAL (despesa)

O resto (execucao, %, saldos, totais) e apurado na matriz.

Uso:
    python rreo_completar_publicado.py --publicado dados/rr_rreo_pub/2026/RREO_14_2026_bim4_anexo01.csv
"""
from __future__ import annotations

import csv
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

#: linhas que se replicam do publicado (nao mudam no exercicio)
FIXAS = (
    "SALDOS DE EXERCÍCIOS ANTERIORES",
    "Superávit Financeiro Utilizado para Créditos Adicionais",
    "RESERVA DE CONTINGÊNCIA",
    "DÉFICIT (VI)",
    "TOTAL COM DÉFICIT (VII) = (V + VI)",
    "TOTAL COM SUPERÁVIT (XIV) = (XII + XIII)",
)
#: colunas que se replicam para as linhas de saldo
COLS_FIXAS = ("Até o Bimestre (c)", "No Bimestre (b)")


def ler_publicado(caminho: str) -> dict:
    """{(conta, coluna): valor} do publicado."""
    pub = {}
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            pub.setdefault((r["conta"], r["coluna"]), float(r["valor"]))
    return pub


def replicar(cel: dict, publicado: dict) -> int:
    """Sobrepõe as linhas fixas no dict de celulas, todas as colunas."""
    n = 0
    for (conta, coluna), valor in publicado.items():
        if any(conta.startswith(f) for f in FIXAS):
            cel[(conta, coluna, 0)] = valor
            n += 1
    return n
