# -*- coding: utf-8 -*-
"""Limites da LRF do Anexo 1 — e a trava da janela."""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "app"))
sys.path.insert(0, RAIZ)

import mapa_anexo1 as MAPA  # noqa: E402

RCL = 20_958_175_998.75       # RCL ajustada para pessoal, 2026 Q2
DTP_12M = 11_563_398_205.71   # DTP de 12 meses (set/2025 a ago/2026)
DTP_10M = 9_288_694_215.97    # DTP de jan a out/2026 (janela errada)


class TestLimites(unittest.TestCase):
    def test_percentual_publicado(self):
        r = MAPA.limites(RCL, DTP_12M)
        self.assertAlmostEqual(r["percentual"], 55.17, places=2)

    def test_limites_em_reais(self):
        r = MAPA.limites(RCL, DTP_12M)
        self.assertAlmostEqual(r["limite_maximo"], 10_269_506_239.39, places=2)
        self.assertAlmostEqual(r["limite_prudencial"], 9_756_030_927.42, places=2)
        self.assertAlmostEqual(r["limite_alerta"], 9_242_555_615.45, places=2)

    def test_janela_mista_da_o_numero_errado(self):
        """10 meses de despesa sobre 12 de receita produz 44,32% — o erro do painel."""
        r = MAPA.limites(RCL, DTP_10M)
        self.assertAlmostEqual(r["percentual"], 44.32, places=2)
        self.assertNotAlmostEqual(r["percentual"], 55.17, places=1)

    def test_rcl_zerada(self):
        with self.assertRaises(ValueError):
            MAPA.limites(0.0, DTP_12M)


if __name__ == "__main__":
    unittest.main()
