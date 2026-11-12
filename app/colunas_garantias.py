# -*- coding: utf-8 -*-
"""Valores por data para os Anexos 3 (garantias) e 5 (disponibilidade e RP).

As colunas do Anexo 3 são os saldos das garantias em quatro datas; como o Estado
não concedeu garantias em nenhuma delas, todas as linhas do quadro ficam zeradas
e apenas a RCL e os limites variam.

O Anexo 5 cruza a disponibilidade de caixa com os restos a pagar, por fonte de
recurso — estrutura do MDF, tópico 04.05.
"""
from __future__ import annotations

# Anexo 3 — RCL e limites por data
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
COLUNA_DA_DATA = {"2023-12": 2, "2024-04": 3, "2024-08": 4, "2024-12": 5}


def colunas_garantias() -> dict:
    """{campo: {coluna: valor}} para o Anexo 3."""
    campos = {}
    for data, col in COLUNA_DA_DATA.items():
        rcl = RCL_POR_DATA[data]
        rcl_aj = rcl - EMENDAS_POR_DATA[data]
        valores = {
            "gar_estados": 0.0, "gar_estados_ext": 0.0, "gar_estados_int": 0.0,
            "gar_municipios": 0.0, "gar_municipios_ext": 0.0, "gar_municipios_int": 0.0,
            "gar_controladas": 0.0, "gar_controladas_ext": 0.0,
            "gar_controladas_int": 0.0,
            "gar_fundos": 0.0, "gar_total": 0.0,
            "rcl": rcl,
            "gar_emendas": EMENDAS_POR_DATA[data],
            "gar_rcl_ajustada": rcl_aj,
            "gar_pct": 0.0,
            "gar_limite": rcl_aj * 0.22,
            "gar_limite_alerta": rcl_aj * 0.22 * 0.90,
            "contra_estados": 0.0, "contra_estados_ext": 0.0, "contra_estados_int": 0.0,
            "contra_municipios": 0.0, "contra_municipios_ext": 0.0,
            "contra_municipios_int": 0.0,
            "contra_controladas": 0.0, "contra_controladas_ext": 0.0,
            "contra_controladas_int": 0.0,
            "contra_fundos": 0.0, "contra_total": 0.0,
        }
        for campo, valor in valores.items():
            campos.setdefault(campo, {})[col] = valor
    return campos
