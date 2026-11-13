# -*- coding: utf-8 -*-
"""Testes do leitor MSC (app/leitor_msc.py).

Rodar de RN_Fiscal:
    python -m unittest discover -s tests -v
"""
from __future__ import annotations

import os
import shutil
import sys
import unittest
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from app.leitor_msc import Acervo, ErroMSC  # noqa: E402

CABECALHO_6 = [
    "tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil", "poder_orgao",
    "ano_fonte_recursos", "fonte_recursos", "funcao", "subfuncao", "exercicio",
    "mes_referencia", "educacao_saude", "data_referencia", "entrada_msc",
    "natureza_despesa", "ano_inscricao", "natureza_receita", "valor",
    "natureza_conta", "tipo_valor", "complemento_fonte",
]

# classe 1 não tem natureza_despesa / funcao / receita
CABECALHO_1 = [
    "tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil", "poder_orgao",
    "financeiro_permanente", "ano_fonte_recursos", "fonte_recursos", "exercicio",
    "mes_referencia", "divida_consolidada", "data_referencia", "entrada_msc",
    "valor", "natureza_conta", "tipo_valor", "complemento_fonte",
]


def linha(**campos):
    base = {
        "tipo_matriz": "MSCC", "cod_ibge": "24", "classe_conta": "6",
        "conta_contabil": "622130400", "poder_orgao": "10111",
        "ano_fonte_recursos": "1", "fonte_recursos": "1500", "funcao": "",
        "subfuncao": "", "exercicio": "2025", "mes_referencia": "1",
        "educacao_saude": "", "data_referencia": "",
        "entrada_msc": "1", "natureza_despesa": "31901100",
        "ano_inscricao": "", "natureza_receita": "", "valor": "100",
        "natureza_conta": "C", "tipo_valor": "period_change",
        "complemento_fonte": "",
    }
    base.update(campos)
    return base


def escrever(pasta, nome, linhas, cabecalho=CABECALHO_6):
    caminho = os.path.join(pasta, nome)
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(";".join(cabecalho) + "\n")
        for l in linhas:
            fh.write(";".join(str(l.get(c, "")) for c in cabecalho) + "\n")
    return caminho


class Base(unittest.TestCase):
    def setUp(self):
        # o diretório temporário do sistema é somente leitura neste ambiente e
        # mkdtemp cria pastas com ACL restritiva; usamos pasta própria do repo
        self._base = os.path.join(RAIZ, ".tmp_tests")
        os.makedirs(self._base, exist_ok=True)
        self.pasta = os.path.join(self._base, f"t{uuid.uuid4().hex[:12]}")
        os.makedirs(self.pasta)
        self.d2025 = os.path.join(self.pasta, "2025")
        os.makedirs(self.d2025)

    def tearDown(self):
        shutil.rmtree(self.pasta, ignore_errors=True)


class TestIndice(Base):
    def test_meses_e_arquivo(self):
        escrever(self.d2025, "MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv",
                 [linha()])
        escrever(self.d2025, "MSC_24_2025_m03_MSCC_msc_orcamentaria_classe6_period_change.csv",
                 [linha()])
        escrever(self.d2025, "MSC_24_2025_m03_MSCC_msc_orcamentaria_classe6_ending_balance.csv",
                 [linha()])
        acervo = Acervo(self.pasta)
        self.assertEqual(acervo.anos, [2025])
        self.assertEqual(acervo.meses(2025), [3])
        self.assertEqual(acervo.meses(2025, tipo_valor="period_change"), [1, 3])
        self.assertTrue(acervo.arquivo(2025, 1).endswith("m01_MSCC_msc_orcamentaria_classe6_period_change.csv"))

    def test_arquivo_ausente_erro_claro(self):
        escrever(self.d2025, "MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv",
                 [linha()])
        acervo = Acervo(self.pasta)
        with self.assertRaises(ErroMSC) as ctx:
            acervo.arquivo(2025, 7)
        self.assertIn("ausente", str(ctx.exception))

    def test_pasta_sem_matriz(self):
        with self.assertRaises(ErroMSC):
            Acervo(self.pasta)

    def test_nome_fora_do_padrao_ignorado(self):
        escrever(self.d2025, "manifesto.csv", [linha()])
        with self.assertRaises(ErroMSC):
            Acervo(self.pasta)


class TestLeitura(Base):
    def test_sinal_credito_debito(self):
        escrever(self.d2025, "MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            linha(conta_contabil="622130400", valor="100", natureza_conta="C"),
            linha(conta_contabil="622130400", valor="30", natureza_conta="D"),
        ])
        acervo = Acervo(self.pasta)
        regs = list(acervo.ler(2025, 1))
        self.assertEqual(regs[0].liquido, 100.0)
        self.assertEqual(regs[1].liquido, -30.0)
        self.assertEqual(regs[0].elemento, "319011")

    def test_valor_invalido_erro(self):
        escrever(self.d2025, "MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv",
                 [linha(valor="abc")])
        acervo = Acervo(self.pasta)
        with self.assertRaises(ErroMSC):
            list(acervo.ler(2025, 1))

    def test_esquema_diferente_classe1(self):
        escrever(self.d2025, "MSC_24_2025_m12_MSCC_msc_patrimonial_classe1_ending_balance.csv", [
            {"tipo_matriz": "MSCC", "cod_ibge": "24", "classe_conta": "1",
             "conta_contabil": "112110000", "poder_orgao": "10111",
             "financeiro_permanente": "1", "fonte_recursos": "1500",
             "exercicio": "2025", "mes_referencia": "12", "valor": "1234.56",
             "natureza_conta": "D"},
        ], cabecalho=CABECALHO_1)
        acervo = Acervo(self.pasta)
        regs = list(acervo.ler(2025, 12, classe=1, tipo_valor="ending_balance"))
        self.assertEqual(len(regs), 1)
        self.assertEqual(regs[0].nd, "")
        self.assertEqual(regs[0].liquido, -1234.56)  # natureza D


class TestAgregacao(Base):
    def setUp(self):
        super().setUp()
        escrever(self.d2025, "MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            linha(conta_contabil="622130400", poder_orgao="10111", valor="100", natureza_conta="C"),
            linha(conta_contabil="622130400", poder_orgao="10111", valor="40", natureza_conta="D"),
            linha(conta_contabil="622130700", poder_orgao="10112", valor="50", natureza_conta="C"),
            linha(conta_contabil="622130700", poder_orgao="20211", valor="20", natureza_conta="C"),
            linha(conta_contabil="339030000", poder_orgao="10111", valor="999", natureza_conta="C"),
        ])
        self.acervo = Acervo(self.pasta)

    def test_filtro_por_prefixo_de_conta(self):
        total = self.acervo.total(2025, [1], contas=("62213",))
        self.assertAlmostEqual(total, 130.0)   # 100 - 40 + 50 + 20

    def test_agrupa_por_po(self):
        por_po = self.acervo.agregar(2025, [1], contas=("62213",), chave=("po",))
        self.assertAlmostEqual(por_po[("10111",)], 60.0)
        self.assertAlmostEqual(por_po[("10112",)], 50.0)
        self.assertAlmostEqual(por_po[("20211",)], 20.0)

    def test_filtro_por_po(self):
        total = self.acervo.total(2025, [1], contas=("62213",),
                                  filtro=lambda r: r.po == "10111")
        self.assertAlmostEqual(total, 60.0)

    def test_bruto_soma_absoluto(self):
        total = self.acervo.total(2025, [1], contas=("622130400",), bruto=True)
        self.assertAlmostEqual(total, 140.0)

    def test_contas_fora_do_filtro_ignoradas(self):
        total = self.acervo.total(2025, [1], contas=("6221304",))
        self.assertAlmostEqual(total, 60.0)


class TestAmarracao(Base):
    def _par(self, saldo):
        escrever(self.d2025, "MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            linha(conta_contabil="622130400", valor="100", natureza_conta="C"),
            linha(conta_contabil="622130400", valor="30", natureza_conta="D"),
        ])
        escrever(self.d2025, "MSC_24_2025_m02_MSCC_msc_orcamentaria_classe6_ending_balance.csv", [
            linha(conta_contabil="622130400", valor=str(saldo), natureza_conta="C"),
        ])

    def test_saldo_igual_fluxo(self):
        self._par(70)
        self.assertEqual(Acervo(self.pasta).conferir_fluxo_estoque(2025), [])

    def test_saldo_divergente_reportado(self):
        self._par(75)
        div = Acervo(self.pasta).conferir_fluxo_estoque(2025)
        self.assertEqual(len(div), 1)
        conta, fluxo, saldo, dif = div[0]
        self.assertEqual(conta, "622130400")
        self.assertAlmostEqual(fluxo, 70.0)
        self.assertAlmostEqual(saldo, 75.0)
        self.assertAlmostEqual(dif, -5.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

