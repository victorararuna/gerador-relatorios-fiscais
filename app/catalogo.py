# -*- coding: utf-8 -*-
"""Catálogo de rótulos dos anexos que o Siconfi exporta sem rótulos.

Os anexos RREO 3, 4, 6, 7 e 13 chegam do Siconfi apenas com valores. Os rótulos
oficiais foram minerados das planilhas de trabalho do Estado (caminho 3 da
Fase 2) por `ferramentas/descobrir_rotulos.py`, que casa as sequências de
valores — quadro a quadro — para descobrir a aba e a coluna corretas, e grava um
JSON por anexo com a lista de rótulos de cada quadro.

Este módulo só carrega esses JSONs e os aplica às linhas do rascunho, na ordem,
quadro a quadro. Nada aqui inventa rótulo: se o catálogo não cobrir exatamente o
número de linhas de um quadro, aquele quadro fica sem aplicação e a geração
avisa.
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from modelo import Anexo

PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "dados", "catalogo")

_cache: Dict[str, Optional[dict]] = {}


def caminho_json(anexo: Anexo) -> str:
    return os.path.join(PASTA, f"rotulos_{anexo.documento}_{anexo.numero:02d}.json")


def carregar(anexo: Anexo) -> Optional[dict]:
    chave = anexo.chave
    if chave in _cache:
        return _cache[chave]
    dados = None
    caminho = caminho_json(anexo)
    if os.path.exists(caminho):
        try:
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
        except (OSError, json.JSONDecodeError):
            dados = None
    _cache[chave] = dados
    return dados


def disponivel(anexo: Anexo) -> bool:
    return carregar(anexo) is not None


def _aplicar_quadro(bloco, rotulos: List[dict]) -> bool:
    linhas = list(bloco.linhas)
    if not linhas or len(rotulos) != len(linhas):
        return False
    aplicou = False
    for linha, rot in zip(linhas, rotulos):
        texto = (rot.get("texto") or "").strip()
        if not texto:
            continue
        linha.rotulo = texto
        linha.nivel = int(rot.get("nivel") or 0)
        linha.total = bool(rot.get("total"))
        linha.negrito = linha.total
        aplicou = True
    return aplicou


def aplicar(anexo: Anexo) -> int:
    """Aplica o catálogo; devolve quantos quadros receberam rótulos."""
    dados = carregar(anexo)
    if not dados:
        return 0
    aplicados = 0
    for item in dados.get("blocos", []):
        idx = item.get("indice")
        if idx is None or idx >= len(anexo.blocos):
            continue
        if _aplicar_quadro(anexo.blocos[idx], item.get("rotulos", [])):
            aplicados += 1
    return aplicados


def cobertura(anexo: Anexo) -> float:
    """Fração das linhas com valores que possuem rótulo (0..1)."""
    linhas = [l for b in anexo.blocos for l in b.linhas if l.valores]
    if not linhas:
        return 0.0
    return sum(1 for l in linhas if l.rotulo.strip()) / len(linhas)


def quadros_cobertos(anexo: Anexo) -> int:
    return sum(1 for b in anexo.blocos
               if b.linhas and sum(1 for l in b.linhas if l.rotulo.strip()) / len(b.linhas) >= 0.5)


def aplicar_em(anexos: List[Anexo]) -> int:
    total = 0
    for anexo in anexos:
        total += aplicar(anexo)
    return total
