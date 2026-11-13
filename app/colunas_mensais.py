# -*- coding: utf-8 -*-
"""Calcula as 12 colunas mensais do Anexo 1 a partir das MSC mensais.

O movimento de cada mês é a diferença entre o saldo acumulado do mês e o do mês
anterior. Usar o `period_change` diretamente não serve por dois motivos:

1. as contas 6.2.2.1.3.03 (liquidado a pagar) e .04 (liquidado pago) se
   sobrepõem no mesmo lançamento — somar as duas duplica;
2. entre novembro e dezembro há uma baixa de R$ 1,01 bilhão que faz o saldo
   inicial de dezembro não coincidir com o saldo final de novembro.

Tomando a diferença dos saldos finais, a soma das 12 colunas reproduz
exatamente o saldo final de dezembro, que é o TOTAL do demonstrativo.
"""
from __future__ import annotations

import csv
import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import msc_pessoal as M

CAMPOS = ("vencimentos", "patronal", "aposentadorias", "pensoes",
          "terceirizacao", "exercicios_anteriores", "judiciais", "indenizacoes")


def _acumulado(caminho: str) -> Dict[str, float]:
    """Linhas do Anexo 1 acumuladas no ano (saldo final do mês)."""
    linhas = {k: 0.0 for k in CAMPOS}
    with open(caminho, encoding="utf-8", errors="replace", newline="") as f:
        f.readline()
        rd = csv.reader(f, delimiter=";")
        next(rd)
        for c in rd:
            if len(c) != 16 or c[0] not in M.CONTAS_LIQUIDACAO or c[14] != "ending_balance":
                continue
            po = nd = ""
            for i in range(1, 13, 2):
                tipo = c[i + 1]
                if tipo == "PO":
                    po = c[i]
                elif tipo == "ND":
                    nd = c[i]
            if po not in M.PO_EXECUTIVO or not nd:
                continue
            if not (nd.startswith("31") or nd.startswith("33")):
                continue
            try:
                bruto = float(c[13].replace(",", "."))
            except ValueError:
                continue
            valor = bruto if c[15] == "C" else -bruto
            elem = nd[:6]
            if nd.startswith("33"):
                if elem == "339034" or nd.endswith("34"):
                    linhas["terceirizacao"] += valor
                continue
            linhas[M.LINHA_POR_ELEMENTO.get(elem, "vencimentos")] += valor
    return linhas


def colunas_mensais(pasta: str) -> Dict[str, Dict[int, float]]:
    """{campo: {coluna: valor}} com o movimento de cada mês (col 3..14 = MR-11..MR)."""
    campos: Dict[str, Dict[int, float]] = {}
    anterior = {k: 0.0 for k in CAMPOS}
    for mes in range(1, 13):
        caminho = os.path.join(pasta, f"mes{mes}", "instancia.csv")
        if not os.path.exists(caminho):
            continue
        atual = _acumulado(caminho)
        mov = {k: atual[k] - anterior.get(k, 0.0) for k in CAMPOS}
        mov["bruta"] = (mov["vencimentos"] + mov["patronal"] + mov["aposentadorias"]
                        + mov["pensoes"] + mov["terceirizacao"])
        coluna = 1 + mes      # mes 1 -> col2 (MR-11) ... mes 12 -> col13 (MR)
        for campo, valor in mov.items():
            campos.setdefault(campo, {})[coluna] = valor
        anterior = atual
    return campos


def colunas_escaladas(pasta: str, totais: Dict[str, float]) -> Dict[str, Dict[int, float]]:
    """Distribui o TOTAL apurado pelos meses, na proporcao do movimento da MSC.

    O saldo final das contas de VPD e o movimento liquido; o Anexo 1 apura a
    despesa pelo valor bruto. Para que as colunas mensais somem exatamente o
    TOTAL do demonstrativo, aplica-se a proporcao de cada mes sobre o total.
    """
    brutas = colunas_mensais(pasta)
    saida: Dict[str, Dict[int, float]] = {}
    for campo, por_coluna in brutas.items():
        total_apurado = totais.get(campo)
        soma = sum(por_coluna.values())
        if total_apurado is None or not soma:
            saida[campo] = por_coluna
            continue
        fator = total_apurado / soma
        saida[campo] = {c: v * fator for c, v in por_coluna.items()}

    # despesas nao computadas e despesa liquida: distribuidas na proporcao da
    # despesa bruta, pois suas contas nao estao no movimento mensal acima
    bruta = brutas.get("bruta") or {}
    if bruta:
        for campo in ("deducoes", "liquida"):
            total = totais.get(campo)
            if total is None:
                continue
            soma_bruta = sum(bruta.values())
            if not soma_bruta:
                continue
            fator = total / soma_bruta
            saida[campo] = {c: v * fator for c, v in bruta.items()}
    return saida


def resumo(pasta: str) -> Dict[str, float]:
    """Soma das 12 colunas por campo (deve igualar o total do Anexo 1)."""
    colunas = colunas_mensais(pasta)
    return {campo: sum(vals.values()) for campo, vals in colunas.items()}
