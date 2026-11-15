# -*- coding: utf-8 -*-
"""Aposentadorias somam TODOS os CO (rodada 168).

O `msc_pessoal.apurar` filtravam as naturezas 31.90.01 e 31.90.03 por
`complemento_fonte`, mantendo so vazio/1111/1151/2111/2151. O filtro cortava
R$ 953 milhoes das aposentadorias do RN:

    2211  614.960.748,14
    1131  150.994.803,21
    1121  123.164.829,08
    1122   57.406.865,05
    1141    7.321.996,16

Com o filtro, aposentadorias dava 4.268.008.067,90 contra 5.281.577.891,79
publicados (−19,19%). Sem ele, 5.263.258.798,60 (−0,35%).

O ganho se repetiu nos cinco estados testados. Na despesa bruta (I):

    RN  −10,21%  ->  −1,73%
    MG  −18,73%  ->  −1,98%
    MA  −15,45%  ->  −5,75%
    PR   −8,52%  ->  +3,16%
    RR   −6,99%  ->  −6,99%

MG passou a fechar aposentadorias ao centavo (−0,00%).
"""
import inspect
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import msc_pessoal as M  # noqa: E402


class TestSemFiltroDeCO(unittest.TestCase):

    def test_apurar_nao_filtra_por_co(self):
        """O codigo de `apurar` nao pode voltar a filtrar 319001/319003 por CO."""
        fonte = inspect.getsource(M.apurar)
        self.assertNotIn('l.co not in', fonte,
                         "o filtro de CO cortava R$ 953 mi das aposentadorias")

    def test_apurar_tem_as_linhas_do_anexo1(self):
        fonte = inspect.getsource(M.apurar)
        for campo in ("vencimentos", "patronal", "aposentadorias", "pensoes"):
            self.assertIn(campo, fonte)

    def test_elemento_de_aposentadoria_esta_mapeado(self):
        """319001 tem de continuar indo para aposentadorias."""
        self.assertEqual(M.LINHA_POR_ELEMENTO.get("319001"), "aposentadorias")

    def test_elemento_de_pensao_esta_mapeado(self):
        self.assertEqual(M.LINHA_POR_ELEMENTO.get("319003"), "pensoes")


if __name__ == "__main__":
    unittest.main(verbosity=2)
