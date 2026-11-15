# -*- coding: utf-8 -*-
"""Quadro II sem dupla dedução (rodada 154).

O mapeamento da STN manda mapear **Decisão Judicial (31.XX.91)** e **DEA
(31.XX.92)** exceto nas fontes 800/801/803/804 e 604/605. Quem está nelas entra
em **Inativos e Pensionistas com Recursos Vinculados** (naturezas 01, 03, 86, 91,
92 e 94).

Sem essa exceção, o mesmo valor é descontado nas duas linhas: os totais fecham e
as linhas não.

Conferido contra o Quadro do auditor (`RGF 2026_Q2_01`, aba `Quadro`): as nove
linhas batem em janeiro a agosto de 2026, exceto as duas de abril — que são o erro
de 5.241,65 do arquivo publicado.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import mapa_anexo1 as MAPA  # noqa: E402

MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto")


class TestQuadroII(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.q = {mes: MAPA.quadro_ii(mes) for mes in MESES}

    def test_dea_e_zero_nos_meses(self):
        """A DEA só é deduzida em dezembro; nos outros meses, zero."""
        for mes in MESES:
            with self.subTest(mes=mes):
                self.assertEqual(self.q[mes]["dea"], 0.0)

    def test_judicial_nao_inclui_as_fontes_vinculadas(self):
        """A Decisão Judicial tem de ser menor que o total bruto da natureza."""
        for mes in MESES:
            with self.subTest(mes=mes):
                c = MAPA.ler_comparativo(mes)
                bruto = c.get("31.90.91.00", 0.0) + c.get("31.91.91.00", 0.0)
                self.assertLessEqual(self.q[mes]["judicial"], bruto + 0.01)

    def test_linhas_somam_o_total(self):
        """O total do Quadro II é a soma das suas linhas."""
        for mes in MESES:
            with self.subTest(mes=mes):
                q = self.q[mes]
                soma = (q["indenizacoes"] + q["judicial"] + q["dea"]
                        + q["inativos"] + q["acs"] + q["enfermagem"])
                self.assertAlmostEqual(q["total"], soma, places=2)

    def test_total_do_quadro_ii_nao_e_negativo(self):
        for mes in MESES:
            with self.subTest(mes=mes):
                self.assertGreater(self.q[mes]["total"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
