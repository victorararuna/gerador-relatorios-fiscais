# -*- coding: utf-8 -*-
"""RGF Anexo 4 (Operações de Crédito): limites calculados a partir da RCL.

O bloco de operações realizadas depende de identificar, na receita, o que é
operação nova e o que é refinanciamento — a matriz traz R$ 6,7 bi na natureza
`17115001` contra R$ 2,49 mi declarados como operações no Anexo 4. O bloco de
limites, porém, sai direto da RCL e fecha ao centavo.
"""
from __future__ import annotations

import csv
import os
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anexo3_msc import RCL  # noqa: E402

#: Resolução do Senado 43/2001 e 98/2010
PERCENTUAL_ARO = 0.07          # operações por antecipação da receita orçamentária
PERCENTUAL_GERAL = 0.16        # operações de crédito internas e externas
PERCENTUAL_ALERTA = 0.90

ROTULOS = {
    "aro": "LIMITE DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL PARA AS OPERAÇÕES "
           "DE CRÉDITO POR ANTECIPAÇÃO DA RECEITA ORÇAMENTÁRIA",
    "geral": "LIMITE GERAL DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL PARA AS "
             "OPERAÇÕES DE CRÉDITO INTERNAS E EXTERNAS",
    "alerta": "LIMITE DE ALERTA (inciso III do § 1º do art. 59 da LRF)",
}


def limites(rcl: RCL) -> Dict[str, float]:
    """Os três limites do Anexo 4, todos sobre a RCL ajustada de endividamento."""
    base = rcl.ajustada_endividamento
    geral = base * PERCENTUAL_GERAL
    return {
        "aro": base * PERCENTUAL_ARO,
        "geral": geral,
        "alerta": geral * PERCENTUAL_ALERTA,
    }


def conferir(valores: Dict[str, float], caminho_rgf: str,
             coluna: str = "VALOR") -> List[Tuple[str, float, float]]:
    oficiais: Dict[str, float] = {}
    with open(caminho_rgf, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == coluna:
                oficiais.setdefault(r["conta"], float(r["valor"]))
    saida = []
    for chave, rotulo in ROTULOS.items():
        of = next((v for c, v in oficiais.items() if c.startswith(rotulo[:40])),
                  float("nan"))
        saida.append((rotulo, of, valores[chave]))
    return saida
