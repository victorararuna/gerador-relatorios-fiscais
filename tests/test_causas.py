# -*- coding: utf-8 -*-
"""Toda divergencia tem de ter causa declarada (rodada 140).

O `DIVERGENCIAS.md` e gerado do motor: quando uma celula nao bate, ele procura a
causa na tabela `CAUSAS` e, se nao acha, escreve "sem causa identificada".

Esse texto e um sinal de trabalho pela metade. Este teste garante que ele nao
aparece em nenhuma das 26 divergencias — nem hoje, nem quando uma nova aparecer.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import verificacao as V  # noqa: E402


class TestCausasDasDivergencias(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.grupos = V._grupos()
        cls.divergentes = [
            (nome, item)
            for nome, itens in cls.grupos.items()
            for item in itens if not item["ok"]
        ]

    def test_existe_alguma_divergencia(self):
        """Se nao houver divergencia, o teste seguinte nao prova nada."""
        self.assertGreater(len(self.divergentes), 0)

    def test_nenhuma_divergencia_sem_causa(self):
        sem = [(nome, item["item"]) for nome, item in self.divergentes
               if V._causa(item["item"]) == "sem causa identificada"]
        self.assertEqual(
            sem, [],
            "divergencias sem causa declarada:\n" +
            "\n".join(f"   {n} / {i}" for n, i in sem))

    def test_causa_nao_e_muito_curta(self):
        """Causa de uma linha nao explica nada — exige-se ao menos 60 caracteres."""
        curtas = [(nome, item["item"], V._causa(item["item"]))
                  for nome, item in self.divergentes
                  if len(V._causa(item["item"])) < 60]
        self.assertEqual(curtas, [],
                         "causas curtas demais: " +
                         ", ".join(f"{i} ({len(c)} chars)" for _, i, c in curtas))

    def test_divergencia_tem_valor_e_referencia(self):
        """Toda divergencia traz o valor apurado e o de referencia."""
        for nome, item in self.divergentes:
            with self.subTest(item=item["item"][:40]):
                self.assertIn("apurado", item)
                self.assertIn("referencia", item)
                self.assertNotEqual(item["apurado"], item["referencia"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
