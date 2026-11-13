# -*- coding: utf-8 -*-
"""Testes do Anexo 3 / leitura da RCL."""
from __future__ import annotations

import os
import shutil
import sys
import unittest
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from app.anexo3_msc import (ler_rcl, linhas_anexo3,  # noqa: E402
                            PERCENTUAL_ALERTA, PERCENTUAL_GARANTIAS)


class TestRCL(unittest.TestCase):
    def setUp(self):
        self._base = os.path.join(RAIZ, ".tmp_tests")
        os.makedirs(self._base, exist_ok=True)
        self.pasta = os.path.join(self._base, f"r{uuid.uuid4().hex[:12]}")
        os.makedirs(self.pasta)
        self.arquivo = os.path.join(self.pasta, "RREO_anexo03.csv")
        with open(self.arquivo, "w", encoding="utf-8", newline="") as fh:
            fh.write("exercicio;periodo;periodicidade;instituicao;cod_ibge;uf;"
                     "co_poder;populacao;anexo;esfera;rotulo;coluna;cod_conta;"
                     "conta;valor\n")
            linhas = [
                ("RECEITA CORRENTE LÍQUIDA (III) = (I - II)", "1000"),
                ("RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES "
                 "DE ENDIVIDAMENTO (V)", "900"),
                ("RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES "
                 "DA DESPESA COM PESSOAL (VI)", "880"),
            ]
            for conta, valor in linhas:
                fh.write(f"2025;6;B;Ente;24;RN;E;1;RREO-Anexo 03;E;Padrão;"
                         f"TOTAL (ÚLTIMOS 12 MESES);x;{conta};{valor}\n")

    def tearDown(self):
        shutil.rmtree(self.pasta, ignore_errors=True)

    def test_deriva_transferencias(self):
        rcl = ler_rcl(self.arquivo)
        self.assertEqual(rcl.rcl, 1000.0)
        self.assertEqual(rcl.ajustada_endividamento, 900.0)
        self.assertEqual(rcl.transferencias, 100.0)  # 1000 - 900

    def test_limites(self):
        rcl = ler_rcl(self.arquivo)
        limite, alerta = rcl.limites_garantias()
        self.assertAlmostEqual(limite, 900.0 * PERCENTUAL_GARANTIAS)
        self.assertAlmostEqual(alerta, limite * PERCENTUAL_ALERTA)

    def test_cinco_linhas(self):
        self.assertEqual(len(linhas_anexo3(ler_rcl(self.arquivo))), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
