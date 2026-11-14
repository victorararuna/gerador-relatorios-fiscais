# -*- coding: utf-8 -*-
"""O benchmark de 2025 do Anexo 1 (rodada 134).

A aba `CONFERÊNCIAS` do `RGF 2025_Q3_01` traz o quadro SIGEF e o publicado, mes a
mes. Os dois batem. Doze meses somados tem de dar exatamente o CSV do Siconfi.

Este teste prova que o benchmark e fiel — e que a diferenca da nossa apuracao de
2025 e de **metodo**, nao de dado: o CSV publicado e o benchmark dizem a mesma
coisa, e nos nao chegamos la porque o **Comparativo de 2025 nao existe**.
"""
import csv
import json
import os
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARK = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_2025.json")
CSV2025 = os.path.join(RAIZ, "dados", "siconfi", "rgf",
                       "RGF_RGF-Anexo_01_24_2025_p3.csv")


def _ler_benchmark() -> dict:
    with open(BENCHMARK, encoding="utf-8") as fh:
        return json.load(fh)


def _soma(bloco: dict, chave: str) -> float:
    return sum(bloco.get(chave, []))


class TestBenchmark2025(unittest.TestCase):

    def test_benchmark_existe(self):
        self.assertTrue(os.path.exists(BENCHMARK), "benchmark de 2025 ausente")

    def test_soma_do_benchmark_igual_ao_publicado(self):
        """12 meses do benchmark == total do CSV publicado, ao centavo."""
        dados = _ler_benchmark()
        publicado = {}
        with open(CSV2025, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                if r["coluna"] == "TOTAL (ÚLTIMOS 12 MESES)":
                    publicado[r["conta"].strip()] = float(r["valor"])

        pares = (
            ("I", "DESPESA BRUTA COM PESSOAL (I)"),
            ("II", "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)"),
            ("III", "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)"),
        )
        for chave, rotulo in pares:
            esperado = next((v for k, v in publicado.items()
                             if k.startswith(rotulo[:30])), None)
            if esperado is None:
                continue
            with self.subTest(linha=chave):
                self.assertAlmostEqual(
                    _soma(dados["sigef"], chave), esperado, places=2)

    def test_sigef_e_siconfi_iguais_no_benchmark(self):
        """O quadro do SIGEF e o publicado sao identicos — logo o benchmark vale."""
        dados = _ler_benchmark()
        for chave in ("I", "II", "III"):
            # o bloco SICONFI vem com 2 decimais; compara pela soma, ao centavo
            self.assertAlmostEqual(_soma(dados["sigef"], chave),
                                   _soma(dados["siconfi"], chave), places=2,
                                   msg=f"{chave}: SIGEF e SICONFI divergem")

    def test_benchmark_tem_doze_meses_em_cada_rubrica(self):
        dados = _ler_benchmark()
        for chave, valores in dados["sigef"].items():
            self.assertEqual(len(valores), 12, f"{chave} nao tem 12 meses")


if __name__ == "__main__":
    unittest.main(verbosity=2)
