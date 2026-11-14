# -*- coding: utf-8 -*-
"""RREO Anexo 4 — contribuições dos segurados (rodada 141).

A natureza de receita 1.2.1.5.x separa o segurado por situação:

| natureza | quem é |
|---|---|
| `1.2.1.5.01.11` | ativo civil |
| `1.2.1.5.01.21` | inativo civil |
| `1.2.1.5.01.31` | pensionista civil |
| `1.2.1.5.52.11` | militar ativo |
| `1.2.1.5.52.21` | militar inativo |
| `1.2.1.5.52.31` | militar pensionista |

Três linhas militares e a de pensionista civil fecham ao centavo contra o
publicado de 2025.

**Duas armadilhas deste arquivo:**

1. a linha "Pensionista" aparece **duas vezes** (fundo em capitalização e
   benefícios mantidos pelo Tesouro), com valores diferentes — vale a primeira;
2. o **TOTAL (XX) publicado não é a soma das suas três linhas**: dá 201.138.636,57
   contra 201.130.480,24, diferença de 8.156,33.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import verificacao as V  # noqa: E402

#: soma das tres linhas militares, do proprio publicado
SOMA_MILITARES = 201_130_480.24
#: total publicado na linha (XX) — difere da soma em 8.156,33
TOTAL_PUBLICADO_XX = 201_138_636.57


class TestAnexo4Contribuicoes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.linhas = V.anexo4_contribuicoes()

    def test_quatro_linhas_conferidas(self):
        self.assertEqual(len(self.linhas), 4)

    def test_todas_exatas(self):
        for x in self.linhas:
            with self.subTest(item=x["item"]):
                self.assertTrue(
                    x["ok"],
                    f"{x['item']}: {x['apurado']:,.2f} contra {x['referencia']:,.2f}")

    def test_militares_somam_as_tres_linhas_do_publicado(self):
        """A soma das três linhas militares — não o total (XX), que está errado."""
        total = sum(x["apurado"] for x in self.linhas if "Militares" in x["item"])
        self.assertAlmostEqual(total, SOMA_MILITARES, places=2)

    def test_total_publicado_nao_e_a_soma_das_linhas(self):
        """Registra a inconsistência do arquivo: 8.156,33 de diferença."""
        self.assertNotAlmostEqual(TOTAL_PUBLICADO_XX, SOMA_MILITARES, places=2)
        self.assertAlmostEqual(
            TOTAL_PUBLICADO_XX - SOMA_MILITARES, 8_156.33, places=2)

    def test_pensionista_civil_e_a_primeira_ocorrencia(self):
        """A linha 'Pensionista' aparece duas vezes; vale a primeira."""
        linha = next(x for x in self.linhas if "Pensionistas (civil)" in x["item"])
        self.assertAlmostEqual(linha["apurado"], 26_547_985.82, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
