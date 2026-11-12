# -*- coding: utf-8 -*-
"""Apuração do Anexo 2 do RGF — Dívida Consolidada Líquida — a partir da MSC.

Estrutura conforme o MDF 14ª edição, tópico 04.02 (páginas 505 a 534):

    DÍVIDA CONSOLIDADA (I) = Dívida Mobiliária + Dívida Contratual +
                             Precatórios + Operações de crédito +
                             Parcelamento e renegociação
    DEDUÇÕES (II)          = Disponibilidade de caixa + Aplicações +
                             Demais haveres
    DÍVIDA CONSOLIDADA LÍQUIDA (III) = (I - II)
    % da DCL sobre a RCL

O Anexo 2 do Executivo **abrange todos os Poderes** (MDF, p. 505) — não se
aplica o recorte por PO usado no Anexo 1.

Contas identificadas por reconciliação contra o RGF homologado (o mapeamento
oficial de contas do Anexo 2 não é publicado no MDF — está nos arquivos de
mapeamento da STN, indisponíveis).
"""
from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CONTAS_DIVIDA = {
    # 2.2.1.1 - obrigacoes com precatorios
    "221110302": "Precatórios - RPPS",
    "221110303": "Precatórios - demais",
    # 2.2.2.1 / 2.2.2.2 - divida contratual
    "222110298": "Dívida contratual - interna",
    "222210200": "Dívida contratual - externa",
    # 2.2.3.1.1 - parcelamentos e renegociacoes
    "223110402": "Parcelamento - previdenciário",
    "223110403": "Parcelamento - demais",
    # 2.1.8.9 / 2.1.8.8 / 2.1.1.4 - demais obrigacoes
    "218910106": "Demais obrigações - longo prazo",
    "218810110": "Demais obrigações - curto prazo",
    "218911400": "Demais obrigações - ajustes",
    "211439800": "Empréstimos - outras",
}

CONTAS_DEDUCAO = {
    "121119905": "Créditos a receber - dedução",
    "121119700": "Créditos a receber - dedução",
    "113811100": "Aplicações financeiras",
    "113510400": "Disponibilidade",
}

RCL_2024 = 17259989216.73


@dataclass
class ResultadoDCL:
    divida: Dict[str, float] = field(default_factory=dict)
    deducoes: Dict[str, float] = field(default_factory=dict)

    @property
    def total_divida(self) -> float:
        return sum(self.divida.values())

    @property
    def total_deducoes(self) -> float:
        return sum(self.deducoes.values())

    @property
    def dcl(self) -> float:
        return self.total_divida - self.total_deducoes


def ler_msc(caminho: str) -> ResultadoDCL:
    r = ResultadoDCL()
    with open(caminho, encoding="utf-8", errors="replace", newline="") as f:
        f.readline()
        rd = csv.reader(f, delimiter=";")
        next(rd)
        for row in rd:
            if len(row) != 16 or row[14] != "ending_balance":
                continue
            conta = row[0]
            if conta in CONTAS_DIVIDA:
                try:
                    r.divida[conta] = r.divida.get(conta, 0.0) + abs(float(row[13].replace(",", ".")))
                except ValueError:
                    pass
            elif conta in CONTAS_DEDUCAO:
                try:
                    r.deducoes[conta] = r.deducoes.get(conta, 0.0) + abs(float(row[13].replace(",", ".")))
                except ValueError:
                    pass
    return r


def apurar(caminho: str, rcl: float = RCL_2024) -> Dict[str, float]:
    r = ler_msc(caminho)
    return {
        "divida": r.total_divida,
        "deducoes": r.total_deducoes,
        "dcl": r.dcl,
        "rcl": rcl,
        "pct_dc": r.total_divida / rcl if rcl else 0.0,
        "pct_dcl": r.dcl / rcl if rcl else 0.0,
    }
