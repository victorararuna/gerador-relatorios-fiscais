# -*- coding: utf-8 -*-
"""Trava do RGF Anexo 2: as 11 linhas que fecham não podem voltar a abrir.

Cada linha é conferida contra o valor da aba "Base" da planilha da equipe (que
espelha o publicado). As três que ainda não fecham estão nomeadas em
`PENDENTES`, com o motivo — se alguma passar a fechar, o teste avisa para
atualizar a lista.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "app"))
sys.path.insert(0, RAIZ)

import rgf_anexo2_dcl as D  # noqa: E402

#: linhas que ainda não fecham, com o motivo
PENDENTES = {
    "(-) Restos a Pagar Processados (Exceto Precatórios)":
        "exige o relatório por fonte (bloco de RP) por Poder",
}


def _comparar():
    saldo = D.ler_balancete(D.BALANCETE)
    secoes = D.ler_base(D.PLANILHA)
    saida = {}
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
        saida[nome] = (v, oficial)
    return saida


class TestAnexo2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.linhas = _comparar()

    def test_linhas_exatas(self):
        esperadas = {n: (v, o) for n, (v, o) in self.linhas.items()
                     if n not in PENDENTES}
        self.assertTrue(esperadas, "nenhuma linha comparada")
        divergentes = {n: v - o for n, (v, o) in esperadas.items() if abs(v - o) >= 0.01}
        self.assertEqual({}, divergentes, "linha que fechava voltou a divergir")

    def test_pendentes_continuam_pendentes(self):
        """Se uma pendente fechar, a lista precisa ser atualizada."""
        fechadas = [n for n in PENDENTES
                    if n in self.linhas and abs(self.linhas[n][0] - self.linhas[n][1]) < 0.01]
        self.assertEqual([], fechadas, "linha saiu de PENDENTES: atualize a lista")

    def test_contagem(self):
        exatas = sum(1 for n, (v, o) in self.linhas.items()
                     if n not in PENDENTES and abs(v - o) < 0.01)
        self.assertEqual(15, exatas, f"esperava 15 linhas exatas, achei {exatas}")


if __name__ == "__main__":
    unittest.main()
