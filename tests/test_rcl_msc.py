# -*- coding: utf-8 -*-
"""A RCL construida pela MSC, conferida contra o publicado (rodada 130).

Ate aqui a RCL era lida do arquivo do Siconfi. O mapeamento oficial do MDF
mostra as contas: a receita realizada fica na 6.2.1.2.0.00.00 (classe 6) e as
deducoes na 6.2.1.3.x e em naturezas de receita.

O modulo `rcl_msc` constroi a RCL. Este teste garante que ela continua dentro de
0,02% do publicado — e documenta a diferenca residual.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import rcl_msc  # noqa: E402

#: RCL publicada (TOTAL ULTIMOS 12 MESES do Anexo 3)
PUBLICADA = {
    (2025, 12): 19_513_846_659.98,
    (2026, 8): 20_966_424_987.22,
}


class TestRclConstruida(unittest.TestCase):

    def test_rcl_dentro_de_dois_decimos_por_cento(self):
        """A RCL apurada pela matriz tem de ficar a menos de 0,02% da publicada."""
        for (ano, mes), esperado in PUBLICADA.items():
            with self.subTest(periodo=f"{ano}-{mes:02d}"):
                v = rcl_msc.apurar(ano, mes)["rcl"]
                desvio = abs(v - esperado) / esperado
                self.assertLess(
                    desvio, 0.0002,
                    f"RCL {ano}-{mes:02d}: apurada {v:,.2f} contra publicada "
                    f"{esperado:,.2f} — desvio {desvio:.4%}")

    def test_receitas_correntes_contem_as_deducoes_de_receita(self):
        """As tres naturezas deduzidas estao dentro de I e tambem em II."""
        v = rcl_msc.apurar(2025, 12)
        for chave in ("contrib_servidor", "compensacao", "rend_prev"):
            self.assertGreater(v[chave], 0.0, f"{chave} deveria ser positiva")
        # I - II = RCL, pela propria definicao
        self.assertAlmostEqual(
            v["rcl"], v["receitas_correntes"] - v["deducoes"], places=2)

    def test_fundeb_e_transferencias_batem_ao_centavo(self):
        """As duas deducoes que saem de conta propria fecham exatamente."""
        v = rcl_msc.apurar(2025, 12)
        self.assertAlmostEqual(v["fundeb"], 3_175_469_290.58, places=2)
        self.assertAlmostEqual(v["transferencias"], 2_733_005_621.51, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
