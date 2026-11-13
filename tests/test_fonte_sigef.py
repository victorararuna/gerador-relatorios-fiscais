# -*- coding: utf-8 -*-
"""Testes da identificação de exercício e mês dos relatórios do SIGEF/RN."""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "app"))

from fonte_sigef import ErroFonte, ler_cabecalho, validar  # noqa: E402

CABECALHO_IEO = ("ESTADO DO RIO GRANDE DO NORTE Imprimir Execução Orçamentária - IEO "
                 "por Subação/ Fonte Recurso/ Elemento Despesa Ano Base: 2026 "
                 "Unidade Gestora 162233 Fundo Financeiro do Estado do Rio Grande do Norte")
MES_IEO = "Mês Referência Setembro Valores Consulta No mês"

CABECALHO_COMP = ("Comparativo Despesa Autorizada, Empenhada, Liquidada e Paga "
                  "Ano Base: 2026 Poder Executivo Mês Referência Outubro")


class TestCabecalho(unittest.TestCase):
    def test_ano_e_mes_do_ieo(self):
        ano, mes = ler_cabecalho(CABECALHO_IEO + " " + MES_IEO)
        self.assertEqual(ano, 2026)
        self.assertEqual(mes, "Setembro")

    def test_ano_e_mes_do_comparativo(self):
        ano, mes = ler_cabecalho(CABECALHO_COMP)
        self.assertEqual(ano, 2026)
        self.assertEqual(mes, "Outubro")

    def test_sem_ano(self):
        ano, _ = ler_cabecalho("documento sem cabeçalho")
        self.assertIsNone(ano)


class TestValidar(unittest.TestCase):
    def test_exercicio_e_mes_corretos(self):
        validar(2026, "Setembro", 2026, "Setembro")  # não levanta

    def test_exercicio_errado(self):
        with self.assertRaises(ErroFonte) as ctx:
            validar(2025, "Setembro", 2026, "Setembro")
        self.assertIn("exercício errado", str(ctx.exception))

    def test_mes_errado(self):
        with self.assertRaises(ErroFonte) as ctx:
            validar(2026, "Agosto", 2026, "Setembro")
        self.assertIn("mês errado", str(ctx.exception))

    def test_ano_ausente(self):
        with self.assertRaises(ErroFonte):
            validar(None, "Setembro", 2026, "Setembro")

    def test_mes_ausente_quando_exigido(self):
        with self.assertRaises(ErroFonte):
            validar(2026, None, 2026, "Setembro")

    def test_mes_nao_exigido(self):
        validar(2026, None, 2026)


if __name__ == "__main__":
    unittest.main()
