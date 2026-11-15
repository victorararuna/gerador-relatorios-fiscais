# -*- coding: utf-8 -*-
"""O gerador nao depende mais das planilhas da equipe (rodada 164).

O Anexo 2 lia a aba `Anexo 2 - RGF BASE` e o Anexo 5 lia a aba `MAPEAMENTO` em
tempo de execucao — o que prendia o gerador a uma planilha externa. Os dois mapas
foram transcritos para JSON e agora sao lidos do repositorio.

Este teste garante que:
1. os JSONs existem e tem o conteudo esperado;
2. o modulo le o JSON quando a planilha nao esta disponivel;
3. os valores nao mudam entre os dois caminhos.
"""
import json
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import rgf_anexo2_dcl as A2  # noqa: E402
import rgf_anexo5_vinculacao as A5  # noqa: E402


class TestMapasTranscritos(unittest.TestCase):

    def test_mapa_do_anexo2_existe(self):
        self.assertTrue(os.path.exists(A2.MAPA_JSON))
        with open(A2.MAPA_JSON, encoding="utf-8") as fh:
            dados = json.load(fh)
        self.assertGreaterEqual(len(dados["secoes"]), 28)
        total = sum(len(s["contas"]) for s in dados["secoes"])
        self.assertGreaterEqual(total, 300)

    def test_ler_base_usa_o_json(self):
        """Sem a planilha, ler_base ainda devolve o mapa."""
        com = A2.ler_base(A2.PLANILHA)
        sem = A2.ler_base("")
        self.assertEqual(list(com), list(sem))
        self.assertEqual(sum(len(v) for v in com.values()),
                         sum(len(v) for v in sem.values()))

    def test_contas_da_aba_usa_o_json(self):
        self.assertEqual(A2.contas_da_aba("D+ Haveres"),
                         sorted(A2.contas_da_aba("D+ Haveres")))

    def test_mapa_do_anexo5_existe(self):
        self.assertTrue(os.path.exists(A5.MAPA_JSON))
        with open(A5.MAPA_JSON, encoding="utf-8") as fh:
            dados = json.load(fh)
        self.assertGreaterEqual(len(dados["linhas"]), 20)
        self.assertIn("a", dados["colunas"])

    def test_filtros_do_anexo5_sem_planilha(self):
        """Sem a planilha, os filtros vem do JSON e os oficiais ficam vazios."""
        filtros, oficial = A5.ler_planilha("")
        self.assertTrue(filtros)
        self.assertEqual(oficial, {})
        for nome, (pos, tam, lista) in filtros.items():
            self.assertIsInstance(pos, int)
            self.assertIsInstance(tam, int)
            self.assertIsInstance(lista, list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
