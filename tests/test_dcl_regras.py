# -*- coding: utf-8 -*-
"""Regras do Anexo 2 (DCL) pelo mapeamento da STN — e a prova da ausencia.

O mapeamento oficial do RGF Anexo 2 diz, para cada linha, as contas contabeis:

  Outras Dividas  = 8.5.3.7.0.00.00 + 8.6.3.2.1.00.00 + 8.6.3.2.2.00.00
                  + 2.1.8.9.1.01.05 + 2.1.8.9.1.01.08 + 2.1.8.9.3.01.05
                  + 2.1.8.9.4.01.05 + 2.1.8.9.5.01.05
                  + 2.2.8.2.1.00.00 + 2.2.8.2.3.00.00 + 2.2.8.2.4.00.00
                  + 2.2.8.2.5.00.00;  EXCETO PO 10112/10122/10132

  (-) Restos a Pagar Processados
                  = [6.2.2.1.3.07 + 6.3.1.3.0 + 6.3.2.1.0;
                     ND 3.1 + 3.3 + 4.4 + 4.5; TODAS FR EXCETO 800/801/802]
                  - 8.6.3.2.2.00.00

A linha "Outras Dividas" publica 941.926.197,62 e a conta 8.6.3.2.2 e a que
carrega os 942.052.222,15 do RP inscrito sem disponibilidade de caixa (Nota 4).

**Teste de ausencia:** essa conta nao existe na MSC de 2025. Nenhuma classe, em
nenhum tipo de valor. Por isso o Anexo 2 nao fecha pela matriz, e nao por erro de
apuracao.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

#: contas da linha "Outras Dividas" (mapeamento, celula C45)
CONTAS_OUTRAS_DIVIDAS = {
    "853700000", "863210000", "863220000",
    "218910105", "218910108", "218930105", "218940105", "218950105",
    "228210000", "228230000", "228240000", "228250000",
}

#: contas da linha "(-) Restos a Pagar Processados" (mapeamento, celula C53)
CONTAS_RP = {"622130700", "631300000", "632100000"}
CONTROLE_RP = "863220000"

#: POs excluidos nas linhas do Anexo 2
PO_EXCLUIDOS = {"10112", "10122", "10132"}


def _acervo(ano: int, mes: int, classe: int, tipo: str):
    from acervo import Acervo
    return Acervo(os.path.join(RAIZ, "dados", "acervo")).ler(
        ano, mes, classe=classe, tipo_valor=tipo)


class TestRegrasDcl(unittest.TestCase):

    def test_conta_de_controle_do_rp_nao_existe_na_matriz(self):
        """8.6.3.2.2.00.00 nao esta na MSC — e o que trava o Anexo 2."""
        encontrada = []
        for classe in range(1, 9):
            for r in _acervo(2025, 12, classe, "ending_balance"):
                if (r.conta or "") == CONTROLE_RP:
                    encontrada.append((classe, r.liquido))
        self.assertEqual(
            encontrada, [],
            f"a conta {CONTROLE_RP} apareceu na MSC: {encontrada} — se isso "
            "mudar, o Anexo 2 passa a ser apuravel pela matriz")

    def test_outras_dividas_so_tem_o_8632_1_na_matriz(self):
        """Das contas de 'Outras Dividas', so a 8.6.3.2.1 tem saldo."""
        achadas = {}
        for classe in (2, 8):
            for r in _acervo(2025, 12, classe, "ending_balance"):
                if (r.conta or "") in CONTAS_OUTRAS_DIVIDAS:
                    achadas[r.conta] = achadas.get(r.conta, 0.0) + r.liquido
        self.assertEqual(list(achadas), ["863210000"])
        self.assertAlmostEqual(achadas["863210000"], 36_600.82, places=2)

    def test_contas_do_rp_existem_na_matriz(self):
        """As contas do RP existem: o que falta e o controle, nao a base."""
        achadas = set()
        for r in _acervo(2025, 12, 6, "ending_balance"):
            if (r.conta or "") in CONTAS_RP:
                achadas.add(r.conta)
        self.assertTrue(achadas, "nenhuma conta de RP encontrada na classe 6")


if __name__ == "__main__":
    unittest.main(verbosity=2)
