# -*- coding: utf-8 -*-
"""Trava de regressão: os anexos que fecham não podem voltar a abrir.

Se alguém mexer numa regra e uma célula que era exata virar divergente, este
teste falha — antes de o relatório ser gerado.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "app"))
sys.path.insert(0, RAIZ)

import verificacao as V  # noqa: E402


class TestAnexosFechados(unittest.TestCase):
    """Cada grupo conferido aqui tem de estar 100% exato."""

    def _todos_exatos(self, linhas, rotulo):
        divergentes = [l for l in linhas if not l["ok"]]
        self.assertTrue(linhas, f"{rotulo} não retornou células")
        self.assertEqual(
            [], [(l["item"], l["desvio"]) for l in divergentes],
            f"{rotulo} voltou a divergir")

    def test_anexo13_saldos(self):
        self._todos_exatos(V.anexo13(), "RREO Anexo 13")

    def test_anexo13_projecoes(self):
        self._todos_exatos(V.anexo13_projecoes(), "RREO Anexo 13 projeções")

    def test_anexo9(self):
        self._todos_exatos(V.anexo9(), "RREO Anexo 9")

    def test_limites(self):
        self._todos_exatos(V.limites_anexo1(), "limites do Anexo 1")

    def test_anexo5(self):
        self._todos_exatos(V.anexo5(), "RGF Anexo 5")


class TestDivergenciasDocumentadas(unittest.TestCase):
    """Toda divergência conhecida precisa ter causa escrita."""

    CONHECIDAS = (
        "Abril — I", "Abril — III", "Demais Dívidas Contratuais",
        "Disponibilidade de Caixa Bruta", "Restos a Pagar Processados",
        "Depósitos Restitu", "Demais Haveres",
        "Aposentadorias civis", "Pensões por morte civis",
    )

    def test_cada_conhecida_tem_causa(self):
        for item in self.CONHECIDAS:
            causa = V._causa(item)
            self.assertNotEqual(causa, "sem causa identificada", item)

    def test_item_desconhecido_nao_inventa_causa(self):
        self.assertEqual(V._causa("linha inventada"), "sem causa identificada")


if __name__ == "__main__":
    unittest.main()
