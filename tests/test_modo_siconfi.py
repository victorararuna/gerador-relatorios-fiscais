# -*- coding: utf-8 -*-
"""O modo Siconfi do Anexo 1 (rodada 150).

Abril/2026 tem uma diferenca de 5.241,65 que e **erro do arquivo publicado**:
subacao 408801 do TJRN, ND 31.90.92.03, fonte 0.5.00 — o arquivo somou o
empenhado (86.852,54) com o liquidado de outra fonte (29.377,60), quando o
correto seria 92.094,19 + 29.377,60 = 121.471,79.

O `modo_siconfi_q2` reproduz esse erro para que o numero bata com o publicado.
Fica **desligado por padrao**: quem publica numero errado e o gestor, nao o motor.

Este teste garante que:
1. o modo padrao continua tecnicamente correto;
2. o modo Siconfi muda abril em exatamente 5.241,65;
3. o modo Siconfi nao afeta nenhum outro mes.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import mapa_anexo1 as MAPA  # noqa: E402


class TestModoSiconfi(unittest.TestCase):

    def test_padrao_nao_aplica_o_ajuste(self):
        """Sem o modo, abril fica 5.241,65 abaixo do publicado."""
        padrao = MAPA.secoes("Abril")["pensoes"]
        siconfi = MAPA.secoes("Abril", modo_siconfi_q2=True)["pensoes"]
        self.assertAlmostEqual(
            siconfi - padrao, MAPA.DIFERENCA_EMPENHADO_LIQUIDADO_ABRIL_2026, places=2)

    def test_modo_siconfi_fecha_abril(self):
        """Com o modo, a pensao de abril bate com o publicado."""
        v = MAPA.secoes("Abril", modo_siconfi_q2=True)
        self.assertAlmostEqual(v["pensoes"], 76_129_972.89, places=2)

    def test_modo_siconfi_nao_afeta_outros_meses(self):
        """O ajuste e so de abril; os outros meses nao podem mudar."""
        for mes in ("Janeiro", "Fevereiro", "Março", "Maio"):
            with self.subTest(mes=mes):
                self.assertAlmostEqual(
                    MAPA.secoes(mes)["pensoes"],
                    MAPA.secoes(mes, modo_siconfi_q2=True)["pensoes"], places=2)

    def test_diferenca_e_o_empenho_de_marco(self):
        """5.241,65 = empenhado de marco (5.241,65) liquidado em abril."""
        self.assertAlmostEqual(
            MAPA.DIFERENCA_EMPENHADO_LIQUIDADO_ABRIL_2026, 5_241.65, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
