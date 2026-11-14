# -*- coding: utf-8 -*-
"""RREO Anexo 11 — Alienação de Ativos (rodada 137).

O anexo e apurado pela regra do mapeamento da STN: natureza de receita 2.2.1 /
8.2.1 / 1.9.4.1 / 7.9.4.1 (bens móveis), os equivalentes .2 e .3, os rendimentos
de aplicação 1.3.2.1.01/.02/.03/.05/.99, e as despesas de capital ND 4.4 e 4.5 —
todas restritas às fontes 755, 756 e 762.

Conferido contra o publicado de 2025 ao centavo, nas cinco linhas com valor.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import rreo_anexo11 as A11  # noqa: E402

#: valores publicados no CSV do Siconfi (2025, 6o bimestre)
PUBLICADO_2025 = {
    "moveis": 1_284_564.22,
    "rendimentos": 33_593.57,
    "receitas_alienacao": 1_318_157.79,
    "investimentos": 55_800.00,
    "valor": 1_262_357.79,
}


class TestAnexo11(unittest.TestCase):

    def test_2025_bate_ao_centavo(self):
        v = A11.linhas(2025)
        for chave, esperado in PUBLICADO_2025.items():
            with self.subTest(linha=chave):
                self.assertAlmostEqual(v[chave], esperado, places=2)

    def test_imoveis_e_intangiveis_zerados_em_2025(self):
        v = A11.linhas(2025)
        self.assertEqual(v["imoveis"], 0.0)
        self.assertEqual(v["intangiveis"], 0.0)

    def test_valor_e_receita_menos_aplicacao(self):
        v = A11.linhas(2025)
        self.assertAlmostEqual(
            v["valor"], v["receitas_alienacao"] - v["aplicacao"], places=2)

    def test_soma_das_linhas_de_receita_e_o_total(self):
        v = A11.linhas(2025)
        self.assertAlmostEqual(
            v["receitas_alienacao"],
            v["moveis"] + v["imoveis"] + v["intangiveis"] + v["rendimentos"],
            places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
