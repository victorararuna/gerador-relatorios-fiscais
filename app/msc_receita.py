# -*- coding: utf-8 -*-
"""Leitura do Comparativo da Receita Orçada com a Arrecadada (SIAFEM/RN).

O arquivo traz, para cada rubrica de receita, a previsão orçada, a arrecadação
do mês e a receita acumulada no exercício.

Formato do arquivo (aba Sheet1):

    linha 13   cabeçalho: Descrição | Orçada | Arrecadada no mês | Acumulada | Diferença
    linha N    código da rubrica em C3 e descrição em C6
    linha N+2  os valores, nas colunas 5 (orçada), 7 (mês), 9 (acumulada), 11 (diferença)

Os valores vêm como texto no padrão brasileiro (1.234.567,89).

A classificação completa começa em 4.: 4.1 receitas correntes, 4.2 receitas de
capital. As operações de crédito estão em 4.2.1.
"""
from __future__ import annotations

import os
import re
import sys
from typing import Dict, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import leitor_xls as LX

COL_CODIGO = 3
COL_DESCRICAO = 6
COL_ORCADA = 5
COL_MES = 7
COL_ACUMULADA = 9
COL_DIFERENCA = 11
LINHA_INICIAL = 13


def _num(v) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip()
    if not t:
        return None
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def ler_comparativo(caminho: str) -> Dict[str, Tuple[Optional[str], float, float]]:
    """{codigo: (descricao, orcada, acumulada)}."""
    wb = LX.ler_xls(caminho)
    aba = wb.aba(wb.nomes[0])
    saida: Dict[str, Tuple[Optional[str], float, float]] = {}

    for lin in range(LINHA_INICIAL, aba.max_lin + 1):
        codigo = aba.valor(lin, COL_CODIGO)
        if not isinstance(codigo, str) or not codigo.strip():
            continue
        codigo = codigo.strip()
        if not re.match(r"^\d+(\.\d+)*$", codigo):
            continue
        descricao = aba.valor(lin, COL_DESCRICAO)
        descricao = descricao.strip() if isinstance(descricao, str) else None
        # os valores ficam duas linhas abaixo da descricao
        orcada = _num(aba.valor(lin + 2, COL_ORCADA))
        acumulada = _num(aba.valor(lin + 2, COL_ACUMULADA))
        saida[codigo] = (descricao, orcada or 0.0, acumulada or 0.0)

    return saida


def operacoes_credito(receitas: Dict[str, Tuple[Optional[str], float, float]]) -> dict:
    """Operações de crédito do exercício (rubrica 4.2.1)."""
    bruto = receitas.get("4.2.1", (None, 0.0, 0.0))[2]
    # 4.2.1.2 = mercado externo; 4.2.1.1 = mercado interno
    interno = receitas.get("4.2.1.1", (None, 0.0, 0.0))[2]
    externo = receitas.get("4.2.1.2", (None, 0.0, 0.0))[2]
    return {"total": bruto, "interno": interno, "externo": externo}


def receitas_correntes(receitas: Dict[str, Tuple[Optional[str], float, float]]) -> float:
    return receitas.get("4.1", (None, 0.0, 0.0))[2]


def receitas_capital(receitas: Dict[str, Tuple[Optional[str], float, float]]) -> float:
    return receitas.get("4.2", (None, 0.0, 0.0))[2]


def apurar(caminho: str) -> dict:
    r = ler_comparativo(caminho)
    oc = operacoes_credito(r)
    return {
        "operacoes_credito": oc["total"],
        "operacoes_interno": oc["interno"],
        "operacoes_externo": oc["externo"],
        "receitas_correntes": receitas_correntes(r),
        "receitas_capital": receitas_capital(r),
        "rubricas": len(r),
    }


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else \
        r"C:\Users\victo\Downloads\Comparativo da Receita Orçada com a Arrecadada.xls"
    print(apurar(caminho))
