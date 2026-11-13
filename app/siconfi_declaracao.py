# -*- coding: utf-8 -*-
"""Leitura das declarações do Siconfi baixadas pela API.

Formato longo: uma linha por (conta, coluna), com `rotulo`, `coluna`, `conta`,
`cod_conta` e `valor`.

**Atenção à escala.** O Anexo 1 do RGF vem em reais; os Anexos 2 a 6 vêm em
**centavos**. Conferido:

    Anexo 1  15478621265.08   (R$ 15,48 bi)
    Anexo 4  19513846659.98   (R$ 19,51 bi — RCL)
    Anexo 6  11004331905.62   (R$ 11,00 bi — DTP)

**Todos em reais, no formato americano** (ponto decimal, sem separador de
milhar). O parser precisa distinguir: se houver vírgula, é formato brasileiro;
sem vírgula, o ponto é decimal.
"""
from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "dados", "siconfi")

#: Todos os anexos vêm em reais, no formato americano (ponto decimal).
#: A hipótese de "centavos" veio de um bug no parser numérico que removia o
#: ponto decimal e inflava os valores em 100 vezes.
ANEXOS_CENTAVOS: set = set()


def num(v) -> Optional[float]:
    """Converte o valor do CSV.

    A API entrega em **formato americano** (``15478621265.08``), não brasileiro.
    Se houver vírgula, é formato brasileiro; sem vírgula, o ponto é decimal.
    """
    if v is None:
        return None
    t = str(v).strip()
    if not t:
        return None
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        try:
            return float(t.replace(",", ""))
        except ValueError:
            return None


def _arquivo(tipo: str, anexo: str, ano: int, periodo: int,
             ente: int = 24) -> str:
    nome = f"{tipo.upper()}_{anexo.replace(' ', '_')}_{ente}_{ano}_p{periodo}.csv"
    return os.path.join(BASE, tipo.lower(), nome)


@dataclass
class Declaracao:
    tipo: str
    anexo: str
    ano: int
    periodo: int
    linhas: List[dict]

    def valor(self, conta: str, coluna: str, prefixo: bool = False) -> Optional[float]:
        """Valor normalizado (em reais) de uma conta/coluna.

        Com ``prefixo=True`` aceita o começo do nome — as contas do Anexo 1 têm
        nomes longos que o Siconfi trunca.
        """
        bruto = None
        for r in self.linhas:
            nome = r.get("conta") or ""
            bate = nome.startswith(conta) if prefixo else nome == conta
            if bate and r.get("coluna") == coluna:
                bruto = num(r.get("valor"))
                break
        if bruto is None:
            return None
        return bruto / 100 if self.anexo in ANEXOS_CENTAVOS else bruto

    def valores(self, conta: str) -> Dict[str, float]:
        saida: Dict[str, float] = {}
        escala = 100 if self.anexo in ANEXOS_CENTAVOS else 1
        for r in self.linhas:
            if r.get("conta") != conta:
                continue
            v = num(r.get("valor"))
            if v is None:
                continue
            saida[r.get("coluna", "")] = v / escala
        return saida

    def contas(self) -> List[str]:
        vistos: List[str] = []
        for r in self.linhas:
            c = r.get("conta", "")
            if c and c not in vistos:
                vistos.append(c)
        return vistos

    def total_12_meses(self, conta: str, prefixo: bool = False) -> Optional[float]:
        return self.valor(conta, "TOTAL (ÚLTIMOS 12 MESES) (a)", prefixo)

    def busca(self, prefixo: str) -> List[Tuple[str, Dict[str, float]]]:
        """Todas as contas que começam com o prefixo, com seus valores."""
        escala = 100 if self.anexo in ANEXOS_CENTAVOS else 1
        saida: Dict[str, Dict[str, float]] = {}
        for r in self.linhas:
            nome = r.get("conta") or ""
            if not nome.startswith(prefixo):
                continue
            v = num(r.get("valor"))
            if v is None:
                continue
            saida.setdefault(nome, {})[r.get("coluna", "")] = v / escala
        return list(saida.items())


def ler(tipo: str, anexo: str, ano: int, periodo: int,
        ente: int = 24) -> Declaration:  # noqa: F821
    caminho = _arquivo(tipo, anexo, ano, periodo, ente)
    if not os.path.exists(caminho):
        raise FileNotFoundError(caminho)
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        linhas = list(csv.DictReader(fh, delimiter=";"))
    return Declaracao(tipo=tipo, anexo=anexo, ano=ano, periodo=periodo,
                      linhas=linhas)


#: atalhos
def rgf(anexo: str, ano: int = 2025, periodo: int = 3) -> Declaracao:
    return ler("RGF", anexo, ano, periodo)


def rreo(anexo: str, ano: int = 2025, periodo: int = 6) -> Declaracao:
    return ler("RREO", anexo, ano, periodo)


# ---------------------------------------------------------------------------
# valores de referência do RGF 2025 Q3 (homologado)
# ---------------------------------------------------------------------------
def referencia_rgf(ano: int = 2025, periodo: int = 3) -> Dict[str, float]:
    a1 = rgf("RGF-Anexo 01", ano, periodo)
    a4 = rgf("RGF-Anexo 04", ano, periodo)
    a6 = rgf("RGF-Anexo 06", ano, periodo)
    return {
        "bruta": a1.total_12_meses("DESPESA BRUTA COM PESSOAL (I)"),
        "vencimentos": a1.total_12_meses("Vencimentos, Vantagens e Outras Despesas Variáveis"),
        "patronal": a1.total_12_meses("Obrigações Patronais"),
        "aposentadorias": a1.total_12_meses("Aposentadorias, Reserva e Reformas"),
        "pensoes": a1.total_12_meses("Pensões"),
        "terceirizacao": a1.total_12_meses("Outras Despesas de Pessoal decorrentes de Contratos de Terceirização", prefixo=True),
        "nao_executada": a1.total_12_meses("Despesa com Pessoal não Executada Orçamentariamente"),
        "deducoes": a1.total_12_meses("DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)"),
        "liquida": a1.total_12_meses("DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)"),
        "vinculados": a1.total_12_meses("Inativos e Pensionistas com Recursos Vinculados", prefixo=True),
        "enfermagem": a1.total_12_meses("Parcela dedutível referente ao piso salarial do Enfermeiro", prefixo=True),
        "rcl": a4.valor("RECEITA CORRENTE LÍQUIDA - RCL (IV)", "VALOR"),
        "oc_total": a4.valor("TOTAL (III)", "Até o Quadrimestre de Referência (a)"),
        "oc_limite": a4.valor("LIMITE GERAL DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL PARA AS OPERAÇÕES DE CRÉDITO INTERNAS E EXTERNAS", "VALOR"),
        "dtp": a6.valor("Despesa Total com Pessoal - DTP", "VALOR"),
        "dtp_limite": a6.valor("Limite Máximo (incisos I, II e III art. 20 da LRF)", "VALOR"),
    }


if __name__ == "__main__":
    import json
    r = referencia_rgf()
    for k, v in r.items():
        print(f"   {k:18} {v if v is None else format(v, ',.2f')}")
