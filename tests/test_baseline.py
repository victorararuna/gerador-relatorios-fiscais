# -*- coding: utf-8 -*-
"""Auditoria da régua: os valores esperados têm de existir no arquivo publicado.

A maioria dos erros deste projeto não foi de apuração — foi de **referência**:
comparar contra a planilha da equipe em vez do homologado, ou contra uma linha
que não existe no anexo. Este teste lê o DCL publicado e confere, linha a linha,
que o `OFICIAL` do módulo carrega o valor do arquivo.

Se alguém trocar um valor esperado no código, o teste acusa.
"""
import os
import sys
import csv
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import rgf_anexo2_dcl as D  # noqa: E402

CSV_DCL = os.path.join(RAIZ, "dados", "siconfi", "rgf", "RGF_RGF-Anexo_02_24_2025_p3.csv")
COLUNA = "Até o 3º Quadrimestre"

#: nome da seção (aba Base) -> nome da linha no DCL publicado
ALIAS = {
    "Empréstimos Internos": "Internos",
    "Empréstimos Externos": "Externos",
    "Reestruturação da Dívida de Estados e Municípios":
        "Reestruturação da Dívida de Estados e Municípios",
    "De Tributos": "De Tributos",
    "De Contribuições Previdenciárias": "De Contribuições Previdenciárias",
    "Com Instituição Não financeira": "Com Instituição Não Financeira",
    "Precatórios Posteriores a 05/05/2000":
        "Precatórios Posteriores a 05/05/2000 (inclusive) Vencidos e Não Pagos",
    "PASSIVO ATUARIAL": "Passivo Atuarial",
    "DÍVIDA CONTRATUAL DE PPP": "Dívida Contratual de PPP",
    "Disponibilidade de Caixa Bruta": "Disponibilidade de Caixa Bruta",
    "(-) Restos a Pagar Processados (Exceto Precatórios)":
        "(-) Restos a Pagar Processados",
    "(-) Depósitos Restituíves e Valores Vinculados":
        "(-) Depósitos Restituíveis e Valores Vinculados",
    "Demais Haveres Financeiros": "Demais Haveres Financeiros",
    "Outras Dívidas": "Outras Dívidas",
}


class TestBaselineDCL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(CSV_DCL):
            raise unittest.SkipTest("DCL publicado ausente")
        cls.publicado = {}
        with open(CSV_DCL, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                if r["coluna"] == COLUNA:
                    cls.publicado[r["conta"].strip()] = float(r["valor"])

    def test_todo_esperado_vem_do_publicado(self):
        """Casa por prefixo: `ler_base` trunca os nomes das seções."""
        divergentes = []
        for prefixo, linha in ALIAS.items():
            chaves = [k for k in D.OFICIAL if k.startswith(prefixo)]
            if not chaves:
                continue
            valor = D.OFICIAL[chaves[0]]
            if not valor:
                continue
            self.assertIn(linha, self.publicado, f"linha {linha!r} não está no DCL")
            if abs(self.publicado[linha] - valor) >= 0.01:
                divergentes.append((chaves[0], valor, self.publicado[linha]))
        self.assertEqual([], divergentes,
                         "valor esperado diferente do DCL publicado")

    def test_todas_as_secoes_mapeadas(self):
        sem_mapa = [s for s, v in D.OFICIAL.items()
                    if v and not any(s.startswith(p) for p in ALIAS)]
        self.assertEqual([], sem_mapa,
                         "seção com valor esperado sem correspondência no DCL")


class TestBaselinePPP(unittest.TestCase):
    """Os saldos de referencia do Anexo 13 tem de vir do CSV publicado."""

    ARQUIVOS = (
        (1, "RREO_RREO-Anexo_13_24_2025_p6.csv", "SALDO FINAL ATÉ O BIMESTRE"),
        (2, "RREO_RREO-Anexo_13_24_2026_p4.csv", "SALDO FINAL ATÉ O BIMESTRE"),
    )

    def test_referencias_batem(self):
        import verificacao as V

        for indice, nome, coluna in self.ARQUIVOS:
            arq = os.path.join(RAIZ, "dados", "siconfi", "rreo", nome)
            if not os.path.exists(arq):
                continue
            with open(arq, encoding="utf-8-sig", newline="") as fh:
                valores = {}
                for r in csv.DictReader(fh, delimiter=";"):
                    if r["coluna"] == coluna:
                        valores[r["conta"].strip()] = float(r["valor"])
            for chave, (rotulo, ref25, ref26) in V.ANEXO13_REF.items():
                esperado = ref25 if indice == 1 else ref26
                self.assertIn(rotulo, valores, f"{rotulo} ausente em {nome}")
                self.assertAlmostEqual(
                    esperado, valores[rotulo], places=2,
                    msg=f"Anexo 13 {rotulo} em {nome}: codigo {esperado:,.2f} "
                        f"vs publicado {valores[rotulo]:,.2f}")


class TestBaselinePrevidenciario(unittest.TestCase):
    """As quatro linhas do Anexo 4 tem de vir do CSV publicado.

    "Pensões" aparece duas vezes no arquivo: a primeira no bloco de beneficios
    mantidos pelo Tesouro, a segunda no bloco militar. A linha do anexo e a
    segunda.
    """

    #: chave em rreo_anexo4_blocos.OFICIAL -> (nome da linha, usar a ultima?)
    MAPA = {
        "apos_civil": ("Aposentadorias", False),
        "pens_civil": ("Pensões por Morte", False),
        "inat_mil": ("Inatividade", False),
        "pens_mil": ("Pensões", True),
    }

    def test_linhas_batem(self):
        import rreo_anexo4_blocos as A4

        arq = os.path.join(RAIZ, "dados", "siconfi", "rreo",
                           "RREO_RREO-Anexo_04_24_2025_p6.csv")
        if not os.path.exists(arq):
            self.skipTest("Anexo 4 publicado ausente")
        coluna = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (e)"
        with open(arq, encoding="utf-8-sig", newline="") as fh:
            valores = {}
            for r in csv.DictReader(fh, delimiter=";"):
                if r["coluna"] == coluna:
                    valores.setdefault(r["conta"].strip(), []).append(float(r["valor"]))
        for chave, (nome, ultima) in self.MAPA.items():
            self.assertIn(nome, valores, f"{nome} ausente no CSV")
            publicado = valores[nome][-1] if ultima else valores[nome][0]
            esperado = A4.OFICIAL[chave][1]
            self.assertAlmostEqual(
                esperado, publicado, places=2,
                msg=f"Anexo 4 {chave}: codigo {esperado:,.2f} vs publicado {publicado:,.2f}")


if __name__ == "__main__":
    unittest.main()
