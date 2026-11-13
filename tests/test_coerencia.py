# -*- coding: utf-8 -*-
"""Coerência entre o README e o livro de verificação.

O README é o ponto de entrada: se ele disser um número e a planilha outro, quem
abrir o repositório duvida dos dois. Este teste compara os dois.

Rode `python verificacao.py` antes — o teste confere o que está publicado, não o
que o código faria se rodasse agora.
"""
import os
import re
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
