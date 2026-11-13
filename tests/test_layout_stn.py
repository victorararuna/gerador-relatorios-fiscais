# -*- coding: utf-8 -*-
"""Trava contra o uso silencioso dos valores fixos de 2024 no layout STN."""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "app"))

import layout_stn  # noqa: E402


class TestReferencia(unittest.TestCase):
    def test_2024_permitido(self):
        self.assertIsInstance(layout_stn.referencia(2024), dict)

    def test_2026_barrado(self):
        with self.assertRaises(ValueError) as ctx:
            layout_stn.referencia(2026)
        self.assertIn("Anexo 3", str(ctx.exception))

    def test_outro_exercicio_barrado(self):
        with self.assertRaises(ValueError):
            layout_stn.referencia(2025)


if __name__ == "__main__":
    unittest.main()
