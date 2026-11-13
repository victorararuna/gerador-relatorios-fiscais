# -*- coding: utf-8 -*-
"""Testes dos limites do RGF (Anexos 4 e 6) calculados sobre a RCL."""
from __future__ import annotations

import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import app.anexo4_msc as A4  # noqa: E402
import app.anexo6_msc as A6  # noqa: E402
from app.anexo3_msc import RCL  # noqa: E402

# RCL do RN em 2025 (RREO B6) — valores homologados
RCL_RN_2025 = RCL(rcl=19_513_846_659.98,
                  transferencias=4_499_856.06,
                  ajustada_endividamento=19_509_346_803.92,
                  ajustada_pessoal=19_507_449_078.52)


class TestAnexo4(unittest.TestCase):
    def test_limites_homologados(self):
        v = A4.limites(RCL_RN_2025)
        self.assertAlmostEqual(v["aro"], 1_365_654_276.27, places=2)
        self.assertAlmostEqual(v["geral"], 3_121_495_488.63, places=2)
        self.assertAlmostEqual(v["alerta"], 2_809_345_939.76, places=2)

    def test_alerta_e_90_por_cento_do_geral(self):
        v = A4.limites(RCL_RN_2025)
        self.assertAlmostEqual(v["alerta"], v["geral"] * 0.90, places=2)

    def test_base_e_a_rcl_de_endividamento(self):
        v = A4.limites(RCL_RN_2025)
        self.assertAlmostEqual(v["geral"],
                               RCL_RN_2025.ajustada_endividamento * 0.16, places=2)


class TestAnexo6(unittest.TestCase):
    def test_limites_homologados(self):
        v = A6.limites(RCL_RN_2025)
        self.assertAlmostEqual(v["maximo"], 9_558_650_048.47, places=2)
        self.assertAlmostEqual(v["prudencial"], 9_080_717_546.05, places=2)
        # o homologado traz 8.602.785.043,62; o cálculo dá ,63 (1 centavo)
        self.assertAlmostEqual(v["alerta"], 8_602_785_043.62, delta=0.01)

    def test_relacoes_entre_limites(self):
        v = A6.limites(RCL_RN_2025)
        self.assertAlmostEqual(v["prudencial"], v["maximo"] * (46.55 / 49), places=2)
        self.assertAlmostEqual(v["alerta"], v["maximo"] * (44.10 / 49), places=2)

    def test_percentual_dtp(self):
        # DTP homologada do Anexo 6
        self.assertAlmostEqual(A6.percentual(11_004_331_905.62, RCL_RN_2025),
                               56.41, places=2)

    def test_base_e_a_rcl_de_pessoal(self):
        v = A6.limites(RCL_RN_2025)
        self.assertAlmostEqual(v["maximo"],
                               RCL_RN_2025.ajustada_pessoal * 0.49, places=2)


class TestBasesDiferentes(unittest.TestCase):
    def test_rcl_de_endividamento_nao_e_a_de_pessoal(self):
        self.assertNotAlmostEqual(RCL_RN_2025.ajustada_endividamento,
                                  RCL_RN_2025.ajustada_pessoal, places=2)

    def test_ajustada_e_rcl_menos_emendas(self):
        self.assertAlmostEqual(
            RCL_RN_2025.rcl - RCL_RN_2025.transferencias,
            RCL_RN_2025.ajustada_endividamento, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

