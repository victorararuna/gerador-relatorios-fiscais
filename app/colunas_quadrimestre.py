# -*- coding: utf-8 -*-
"""Preenche as colunas de quadrimestre dos anexos patrimoniais (Anexo 2 e 3)
a partir das várias Matrizes de Saldos Contábeis.

Cada coluna do RGF corresponde a uma data de saldo:

    col 2  Saldo do exercício anterior   -> MSC de dezembro do ano anterior
    col 3  Até o 1º quadrimestre         -> MSC de abril
    col 4  Até o 2º quadrimestre         -> MSC de agosto
    col 5  Até o 3º quadrimestre         -> MSC de dezembro
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import msc_dcl

RCL_POR_DATA = {
    "2023-12": 16215892205.45,
    "2024-04": 17146660625.01,
    "2024-08": 17296766377.43,
    "2024-12": 17259892416.73,
}
EMENDAS_POR_DATA = {
    "2023-12": 25988263.30,
    "2024-04": 25173738.30,
    "2024-08": 27742808.98,
    "2024-12": 4802839.15,
}


def colunas_dcl(arquivos: dict) -> dict:
    """Devolve {campo: {coluna: valor}} para o Anexo 2.

    arquivos: {"2023-12": caminho, "2024-04": caminho, ...}
    """
    coluna_da_data = {"2023-12": 2, "2024-04": 3, "2024-08": 4, "2024-12": 5}
    campos = {}
    for data, caminho in arquivos.items():
        if not caminho or not os.path.exists(caminho):
            continue
        r = msc_dcl.ler_msc(caminho)
        d = msc_dcl.apurar(caminho)
        col = coluna_da_data[data]
        rcl = RCL_POR_DATA.get(data, 0.0)
        rcl_aj = rcl - EMENDAS_POR_DATA.get(data, 0.0)

        def soma(*contas):
            return sum(r.divida.get(c, 0.0) for c in contas)

        valores = {
            "divida": d["divida"],
            "divida_mobiliaria": 0.0,
            "divida_contratual": soma("222210200", "222110298"),
            "emprestimos": soma("222210200", "222110298"),
            "emprestimos_internos": soma("222110298"),
            "emprestimos_externos": soma("222210200"),
            "reestruturacao": 0.0,
            "parcelamentos": soma("223110402", "223110403"),
            "parc_tributos": 0.0,
            "parc_previdenciarias": soma("223110402"),
            "parc_inst_financeira": soma("223110403"),
            "precatorios": soma("221110302", "221110303"),
            "outras_dividas": soma("218910106", "218810110", "218911400", "211439800"),
            "deducoes_dcl": d["deducoes"],
            "disp_caixa": 0.0,
            "disp_bruta": 0.0,
            "rp_processados": 0.0,
            "depositos": 0.0,
            "haveres": d["deducoes"],
            "dcl": d["dcl"],
            "rcl": rcl,
            "emendas_dcl": EMENDAS_POR_DATA.get(data, 0.0),
            "rcl_ajustada_dcl": rcl_aj,
            "pct_dc": (d["divida"] / rcl_aj) if rcl_aj else 0.0,
            "pct_dcl": (d["dcl"] / rcl_aj) if rcl_aj else 0.0,
            "limite": rcl_aj * 2.0,
            "limite_alerta": rcl_aj * 1.8,
        }
        for campo, valor in valores.items():
            campos.setdefault(campo, {})[col] = valor
    return campos
