# -*- coding: utf-8 -*-
"""A linha 251 pela matriz — crédito − débito (rodada 135).

A "Despesa com Pessoal não Executada Orçamentariamente" sai das contas
`8.6.3.3.1.01.00.00` (salários) e `8.6.3.3.1.02.00.00` (13º), pelo movimento
**credor menos devedor**. Antes o módulo lia PDFs; agora apura pela MSC.

Dois pontos que só apareceram ao conferir:

1. **O valor pode ser negativo.** Em janeiro/2025 é −252.032.455,16: o débito
   (a folha de dezembro do exercício anterior sendo executada) supera o crédito
   novo. Quem soma só o crédito erra a linha por centenas de milhões.

2. **O expurgo de 1.337.759,24 tem sinal.** É a patronal do 13º dos demais
   Poderes. Em dezembro/2025 ela está no **crédito** (nova inscrição) e sai; em
   abril/2026 está no **débito** (baixa) e volta.
"""
import csv
import json
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import nao_executada as NE  # noqa: E402

BENCHMARK = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_2025.json")
CSV2026 = os.path.join(RAIZ, "dados", "siconfi", "rgf",
                       "RGF_RGF-Anexo_01_24_2026_p2.csv")


class TestNaoExecutada(unittest.TestCase):

    def test_2025_bate_com_o_gabarito_do_auditor(self):
        """Doze meses de 2025, ao centavo, contra a aba CONFERÊNCIAS."""
        with open(BENCHMARK, encoding="utf-8") as fh:
            alvo = json.load(fh)["sigef"]["nao_executada"]
        v = NE.valores_msc(2025)
        for i, mes in enumerate(NE.MESES):
            with self.subTest(mes=mes):
                self.assertAlmostEqual(v[mes], alvo[i], places=2,
                                       msg=f"{mes}: {v[mes]:,.2f} contra {alvo[i]:,.2f}")

    def test_2026_bate_com_o_publicado(self):
        """Janeiro a maio de 2026, ao centavo, contra o CSV do Siconfi."""
        publicado = {}
        with open(CSV2026, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                if r["conta"].strip().startswith("Despesa com Pessoal não Execut"):
                    publicado[r["coluna"]] = float(r["valor"])
        v = NE.valores_msc(2026)
        for i, mes in enumerate(NE.MESES[:5]):
            coluna = "<MR>" if i == 7 else f"<MR-{7 - i}>"
            if coluna not in publicado:
                continue
            with self.subTest(mes=mes):
                self.assertAlmostEqual(v[mes], publicado[coluna], places=2)

    def test_abril_de_2026_e_negativo_e_bate_com_o_manual(self):
        """A baixa do 13º em abril/2026, já com o expurgo devolvido."""
        v = NE.valores_msc(2026)
        self.assertAlmostEqual(v["Abril"], -624_713_040.31, places=2)

    def test_dezembro_de_2025_e_positivo_e_bate_com_o_manual(self):
        """A inscrição do 13º em dezembro/2025, já com o expurgo retirado."""
        v = NE.valores_msc(2025)
        self.assertAlmostEqual(v["Dezembro"], 622_454_793.84, places=2)

    def test_janeiro_de_2025_e_negativo(self):
        """O sinal sozinho: quem soma só o crédito erra 252 milhões."""
        v = NE.valores_msc(2025)
        self.assertLess(v["Janeiro"], 0)
        self.assertAlmostEqual(v["Janeiro"], -252_032_455.16, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
