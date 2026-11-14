# -*- coding: utf-8 -*-
"""Resolve os caminhos das pastas de dados.

As pastas do auditor e da equipe ja mudaram de lugar tres vezes nesta sessao:
`Downloads`, `workspace` e `workspace/Antigravity`. Em vez de fixar um caminho,
cada modulo pede a pasta pelo nome e este modulo procura.

Ordem de busca:
    1. `C:\\Users\\<usuario>\\Downloads\\<pasta>`
    2. `<workspace>/<pasta>`
    3. `<workspace>/Antigravity/<pasta>`
    4. `<repo>/<pasta>`
"""
from __future__ import annotations

import os

AQUI = os.path.dirname(os.path.abspath(__file__))
_ACIMA = os.path.dirname(AQUI)
_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

ARQUIVOS_ETONJONES = "Arquivos etonjones"
RELATORIOS_CONTAG = "RELATÓRIOS CONTAG"


def _candidatos(nome: str) -> tuple[str, ...]:
    return (
        os.path.join(_DOWNLOADS, nome),
        os.path.join(_ACIMA, nome),
        os.path.join(_ACIMA, "Antigravity", nome),
        os.path.join(AQUI, nome),
        os.path.join(_ACIMA, "..", "Antigravity", nome),
    )


def pasta(nome: str, padrao: str | None = None) -> str:
    """Primeiro caminho que existe para a pasta `nome`."""
    for caminho in _candidatos(nome):
        if os.path.exists(caminho):
            return os.path.abspath(caminho)
    return padrao or _candidatos(nome)[0]


def arquivos_etonjones() -> str:
    """Pasta com os PDFs do SIGEF (Comparativo, IEO, balancetes)."""
    return pasta(ARQUIVOS_ETONJONES)


def relatorios_contag() -> str:
    """Pasta com as planilhas da equipe (Demonstrativos Fiscais)."""
    return pasta(RELATORIOS_CONTAG)


if __name__ == "__main__":
    print("Arquivos etonjones :", arquivos_etonjones())
    print("RELATORIOS CONTAG  :", relatorios_contag())
