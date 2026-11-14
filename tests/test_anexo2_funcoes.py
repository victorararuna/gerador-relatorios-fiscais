# -*- coding: utf-8 -*-
"""RREO Anexo 2 — as 23 funções (rodada 143).

Cada função aparece **duas vezes** no arquivo publicado: uma no bloco "exceto
intra-orçamentárias" e outra no bloco "intra-orçamentárias", com o mesmo nome e
valores diferentes.

O total da função é a **soma das duas**. Foi o que faltava: lendo só a primeira
ocorrência, 19 das 23 funções pareciam divergentes.

Somando, as 23 fecham ao centavo.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import verificacao as V  # noqa: E402
import rreo_anexo2 as R2  # noqa: E402


class TestAnexo2Funcoes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.linhas = V.anexo2_funcoes()

    def test_vinte_e_tres_funcoes(self):
        self.assertEqual(len(self.linhas), 23)

    def test_todas_exatas(self):
        divergentes = [x for x in self.linhas if not x["ok"]]
        self.assertEqual(
            divergentes, [],
            "funcoes divergentes: " + ", ".join(
                f"{x['item']} ({x['desvio']:,.2f})" for x in divergentes))

    def test_soma_das_funcoes_e_o_total_publicado(self):
        """As 23 funções somam o total liquidado do Balanço Orçamentário."""
        total = sum(x["apurado"] for x in self.linhas)
        self.assertAlmostEqual(total, 23_361_499_529.63, places=2)

    def test_toda_funcao_tem_par(self):
        """Nenhuma função do módulo ficou sem referência no arquivo."""
        itens = [x["item"] for x in self.linhas]
        for nome in R2.FUNCOES.values():
            if nome in ("Defesa Nacional", "Relações Exteriores", "Urbanismo",
                        "Saneamento", "Organização Agrária"):
                continue      # funcoes sem execucao no RN
            with self.subTest(funcao=nome):
                self.assertTrue(any(nome in i for i in itens),
                                f"{nome} nao esta entre as linhas conferidas")


if __name__ == "__main__":
    unittest.main(verbosity=2)
