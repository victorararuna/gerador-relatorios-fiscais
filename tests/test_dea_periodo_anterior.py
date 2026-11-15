# -*- coding: utf-8 -*-
"""Quadro II do Anexo 1 — DEA de dezembro e dupla dedução (jan–out/2026).

Cobre duas regras do mapeamento STN (Anexo 1, Poder Executivo):

1. Decisão Judicial (31.XX.91) e DEA (31.XX.92) são mapeadas EXCETO nas fontes
   X.800, X.801, X.803, X.804, X.604 e X.605; a parcela do RPPS vai para
   "Inativos e Pensionistas com Recursos Vinculados". Sem isso o mesmo valor é
   deduzido duas vezes (oito células erradas em jan, mai, jun e out/2026).
2. A DEA de período anterior entra inteira na coluna de dezembro:
   R$ 61.416.717,30 em jan–out/2026.

Os valores esperados vêm do Quadro_Despesa_Pessoal_RGF_RN_2026.csv dos
auditores, que também coincide com o Siconfi publicado (jan–ago).
"""
import csv
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import mapa_anexo1 as M  # noqa: E402

QUADRO = os.path.join(RAIZ, "dados", "benchmarks",
                      "Quadro_Despesa_Pessoal_RGF_RN_2026.csv")
DEA_DEZEMBRO = 61_416_717.30


def _num(t: str) -> float:
    return float(t.replace(".", "").replace(",", "."))


def _quadro() -> dict:
    with open(QUADRO, encoding="utf-8-sig") as fh:
        return {int(r[0]): [_num(x) for x in r[2:12]]
                for r in csv.reader(fh, delimiter=";") if r[0].isdigit()}


def _tem_dados() -> bool:
    try:
        M.ler_comparativo("Janeiro")
        return os.path.exists(QUADRO)
    except Exception:
        return False


@unittest.skipUnless(_tem_dados(), "Comparativos do SIGEF ou quadro ausentes")
class TestQuadroII(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.quadro = _quadro()
        cls.meses = M.MESES_2026[:10]
        cls.q2 = [M.quadro_ii(m) for m in cls.meses]

    def test_dea_de_dezembro(self):
        self.assertAlmostEqual(M.dea_periodo_anterior(), DEA_DEZEMBRO, places=2)

    def test_judicial_e_dea_nao_duplicam_fonte_do_rpps(self):
        for i, q in enumerate(self.q2):
            self.assertAlmostEqual(q["judicial"], self.quadro[28][i], places=2,
                                   msg=f"judicial {self.meses[i]}")
            self.assertAlmostEqual(q["dea"], self.quadro[29][i], places=2,
                                   msg=f"DEA {self.meses[i]}")

    def test_inativos_recebe_a_parcela_vinculada(self):
        for i, q in enumerate(self.q2):
            self.assertAlmostEqual(q["inativos"], self.quadro[30][i], places=2,
                                   msg=f"inativos {self.meses[i]}")

    def test_total_nao_computadas(self):
        for i, q in enumerate(self.q2):
            self.assertAlmostEqual(q["total"], self.quadro[26][i], places=2,
                                   msg=f"total II {self.meses[i]}")


if __name__ == "__main__":
    unittest.main()
