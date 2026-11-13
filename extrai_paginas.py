# -*- coding: utf-8 -*-
"""Imprime páginas específicas de um PDF usando o extrator do projeto.

    python extrai_paginas.py <arquivo.pdf> 28-34
"""
from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_pdf import ler_pdf  # noqa: E402


def main() -> int:
    caminho = sys.argv[1]
    faixa = sys.argv[2]
    ini, _, fim = faixa.partition("-")
    ini, fim = int(ini), int(fim or ini)

    paginas = ler_pdf(caminho)
    for p in paginas:
        if ini <= p.numero <= fim:
            texto = re.sub(r"[ \t]+", " ", p.texto())
            print(f"\n===== página {p.numero} =====")
            print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
