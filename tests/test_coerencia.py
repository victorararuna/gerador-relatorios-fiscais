# -*- coding: utf-8 -*-
"""Coerência entre o README e o livro de verificação.

O README é o ponto de entrada: se ele disser um número e a planilha outro, quem
abrir o repositório duvida dos dois. Este teste compara os dois.

Rode `python verificacao.py` antes — o teste confere o que está publicado, não o
que o código faria se rodasse agora.
"""
import os
import re
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
README = os.path.join(RAIZ, "README.md")
LIVRO = os.path.join(RAIZ, "saida", "verificacao_anexos.xlsx")


def _numeros_do_readme():
    with open(README, encoding="utf-8") as fh:
        texto = fh.read()
    m = re.search(r"(\d+) de (\d+) células exatas", texto)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _numeros_do_livro():
    from openpyxl import load_workbook

    ws = load_workbook(LIVRO, data_only=True)["RESUMO"]
    total = exatas = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or row[0] == "TOTAL":
            continue
        total += row[1] or 0
        exatas += row[2] or 0
    return exatas, total


class TestCoerencia(unittest.TestCase):
    def test_livro_existe(self):
        self.assertTrue(os.path.exists(LIVO) if (LIVO := LIVRO) else False,
                        "rode verificacao.py antes: o livro é o que se publica")

    def test_readme_igual_ao_livro(self):
        doc = _numeros_do_readme()
        self.assertIsNotNone(doc, "o README precisa declarar 'N de M células exatas'")
        livro = _numeros_do_livro()
        self.assertEqual(doc, livro,
                         f"README diz {doc[0]} de {doc[1]}; a planilha diz "
                         f"{livro[0]} de {livro[1]} — atualize o README")

    def test_divergencias_igual_ao_livro(self):
        """O .md, o console e a planilha tem de dizer o mesmo numero.

        O gerador do DIVERGENCIAS.md ja somou os grupos duas vezes uma vez e
        anunciou 303 de 306 quando o livro dizia 307 de 310. Este teste fecha
        essa porta: os tres artefatos passam a ser comparados.
        """
        import re

        caminho_md = os.path.join(RAIZ, "docs", "DIVERGENCIAS.md")
        if not os.path.exists(caminho_md):
            self.skipTest("DIVERGENCIAS.md ausente")
        with open(caminho_md, encoding="utf-8") as fh:
            texto = fh.read()
        m = re.search(r"\*\*(\d+) de (\d+) células exatas\*\*", texto)
        self.assertIsNotNone(m, "o .md precisa declarar a contagem")
        md = (int(m.group(1)), int(m.group(2)))
        livro = _numeros_do_livro()
        self.assertEqual(md, livro,
                         f"DIVERGENCIAS.md diz {md[0]} de {md[1]}; "
                         f"a planilha diz {livro[0]} de {livro[1]}")

    def test_readme_conta_do_anexo2(self):
        """O "15 de 16" do README tem de bater com a apuracao do Anexo 2.

        As travas anteriores comparam numeros do livro. Esta amarra a **prosa**:
        se o README anunciar uma contagem que o modulo nao produz, ela falha.
        """
        import re
        import rgf_anexo2_dcl as D

        with open(README, encoding="utf-8") as fh:
            texto = fh.read()
        m = re.search(r"Anexo 2\*\* — DCL \| \*\*(\d+) de (\d+)", texto)
        if not m:
            self.skipTest("README nao declara a contagem do Anexo 2")
        declarado = (int(m.group(1)), int(m.group(2)))

        saldo = D.ler_balancete(D.BALANCETE)
        secoes = D.ler_base(D.PLANILHA)
        exatas = comparadas = 0
        for nome, contas in secoes.items():
            oficial = D.OFICIAL.get(nome)
            if not contas or oficial is None:
                continue
            if nome.startswith("Disponibilidade de Caixa Bruta"):
                v = D.disponibilidade()
            elif nome.startswith("(-) Depósitos"):
                v = D.depositos()
            elif nome in D.SECOES_MSC:
                aba, classe, po = D.SECOES_MSC[nome]
                v = D.apurar_msc(aba, classe, po)
            else:
                v = D.apurar_secao(saldo, contas)
            comparadas += 1
            exatas += abs(v - oficial) < 0.01
        self.assertEqual(declarado, (exatas, comparadas),
                         f"README diz {declarado[0]} de {declarado[1]}; "
                         f"a apuracao da {exatas} de {comparadas}")

    def test_toda_divergencia_tem_causa(self):
        from openpyxl import load_workbook

        wb = load_workbook(LIVRO, data_only=True)
        sem_causa = []
        for nome in wb.sheetnames:
            if nome == "RESUMO":
                continue
            for row in wb[nome].iter_rows(min_row=2, values_only=True):
                if row[4] == "DIVERGENTE" and not row[5]:
                    sem_causa.append((nome, row[0]))
        self.assertEqual([], sem_causa, "divergência sem causa escrita na planilha")


if __name__ == "__main__":
    unittest.main()
