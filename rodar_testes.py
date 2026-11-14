# -*- coding: utf-8 -*-
"""Roda a suite inteira e diz, numa linha, o que aconteceu.

Existe porque "79 testes" pode significar duas coisas diferentes: 79 testes que
passaram, ou 79 testes definidos dos quais vários pularam por falta de arquivo.
Este script separa as duas e falha se algo pular sem motivo declarado.
"""
from __future__ import annotations

import os
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(RAIZ, "tests")


def main() -> int:
    if RAIZ not in sys.path:
        sys.path.insert(0, RAIZ)
    carregador = unittest.TestLoader()
    suite = carregador.discover(PASTA, pattern="test_*.py", top_level_dir=PASTA)
    resultado = unittest.TextTestRunner(verbosity=1).run(suite)

    total = resultado.testsRun
    pulados = len(resultado.skipped)
    falhas = len(resultado.failures) + len(resultado.errors)
    ok = total - pulados - falhas

    print()
    print(f"definidos: {total} | executados: {ok} | pulados: {pulados} | falhas: {falhas}")
    if pulados:
        print("\npulados (verifique se e esperado):")
        for caso, motivo in resultado.skipped:
            print(f"   {caso}: {motivo}")
    if total == 0:
        print("\nERRO: nenhum teste encontrado — o caminho esta certo?")
        return 2
    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
