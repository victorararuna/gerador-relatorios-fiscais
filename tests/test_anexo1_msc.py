# -*- coding: utf-8 -*-
"""Testes do de-para do Anexo 1 (app/anexo1_msc.py)."""
from __future__ import annotations

import os
import shutil
import sys
import unittest
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from app.anexo1_msc import (  # noqa: E402
    MES_DO_QUADRIMESTRE,
    _classificar,
    apurar,
    deducoes,
    nao_executada,
    periodos_janela,
)
from app.leitor_msc import Acervo  # noqa: E402

CABECALHO = [
    "tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil", "poder_orgao",
    "ano_fonte_recursos", "fonte_recursos", "funcao", "subfuncao", "exercicio",
    "mes_referencia", "educacao_saude", "data_referencia", "entrada_msc",
    "natureza_despesa", "ano_inscricao", "natureza_receita", "valor",
    "natureza_conta", "tipo_valor", "complemento_fonte",
]


class TestClassificacao(unittest.TestCase):
    def test_vencimentos(self):
        for nd in ("31901100", "31901200", "31901600", "31900700"):
            self.assertEqual(_classificar(nd), "vencimentos", nd)

    def test_patronal(self):
        self.assertEqual(_classificar("31901301"), "patronal")
        self.assertEqual(_classificar("31911300"), "patronal")
        self.assertEqual(_classificar("31919213"), "patronal")
        self.assertEqual(_classificar("31900400"), "contratacao_temporaria")

    def test_inativo(self):
        self.assertEqual(_classificar("31900101"), "aposentadorias")
        self.assertEqual(_classificar("31900301"), "pensoes")

    def test_terceirizacao(self):
        self.assertEqual(_classificar("33903400"), "terceirizacao")
        self.assertEqual(_classificar("33909134"), "terceirizacao")
        self.assertIsNone(_classificar("33903900"))

    def test_desdobramento_92(self):
        self.assertEqual(_classificar("31909201"), "vencimentos")
        self.assertEqual(_classificar("31909203"), "pensoes")
        self.assertEqual(_classificar("31909211"), "exerc_ant")
        self.assertEqual(_classificar("31900305"), None)
        self.assertEqual(_classificar("31901302"), None)

    def test_fora_do_pessoal(self):
        self.assertIsNone(_classificar("44905100"))
        self.assertIsNone(_classificar("46907100"))
        self.assertIsNone(_classificar("33903900"))

    def test_sem_natureza(self):
        self.assertIsNone(_classificar(""))


class TestJanela(unittest.TestCase):
    def test_janela_dentro_do_ano(self):
        p = periodos_janela(2025, 12)
        self.assertEqual(len(p), 12)
        self.assertEqual(p[0], (2025, 1))
        self.assertEqual(p[-1], (2025, 12))

    def test_janela_atravessa_ano(self):
        p = periodos_janela(2026, 2)
        self.assertEqual(p[0], (2025, 3))
        self.assertEqual(p[-1], (2026, 2))
        self.assertEqual(len(p), 12)

    def test_mes_de_referencia_do_quadrimestre(self):
        self.assertEqual(MES_DO_QUADRIMESTRE, {1: 4, 2: 8, 3: 12})


class TestApuracao(unittest.TestCase):
    def setUp(self):
        self._base = os.path.join(RAIZ, ".tmp_tests")
        os.makedirs(self._base, exist_ok=True)
        self.pasta = os.path.join(self._base, f"a{uuid.uuid4().hex[:12]}")
        self.d2025 = os.path.join(self.pasta, "2025")
        os.makedirs(self.d2025)

    def tearDown(self):
        shutil.rmtree(self.pasta, ignore_errors=True)

    def _escrever(self, nome, linhas, classe="orcamentaria", cab=CABECALHO):
        caminho = os.path.join(self.d2025, nome)
        with open(caminho, "w", encoding="utf-8", newline="") as fh:
            fh.write(";".join(cab) + "\n")
            for l in linhas:
                fh.write(";".join(str(l.get(c, "")) for c in cab) + "\n")

    def _linha(self, **campos):
        base = {c: "" for c in CABECALHO}
        base.update({"tipo_matriz": "MSCC", "cod_ibge": "24", "classe_conta": "6",
                     "conta_contabil": "622130400", "poder_orgao": "10111",
                     "fonte_recursos": "1500", "exercicio": "2025",
                     "mes_referencia": "1", "valor": "0",
                     "natureza_conta": "C", "tipo_valor": "period_change"})
        base.update(campos)
        return base

    def test_apura_por_linha_e_ignora_nao_pessoal(self):
        self._escrever("MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            self._linha(natureza_despesa="31901100", valor="100"),
            self._linha(natureza_despesa="31901301", valor="50"),
            self._linha(natureza_despesa="33903400", valor="70"),
            self._linha(natureza_despesa="44905100", valor="999"),   # fora
            self._linha(natureza_despesa="33903900", valor="888"),   # fora
        ])
        acervo = Acervo(self.pasta)
        res = apurar(acervo, 2025, [1])
        self.assertEqual(res.get("vencimentos"), 100.0)
        self.assertEqual(res.get("patronal"), 50.0)
        self.assertEqual(res.get("terceirizacao"), 70.0)
        self.assertEqual(res.pessoal, 220.0)
        self.assertEqual(res.ignorados["44"], 999.0)
        self.assertEqual(res.ignorados["33"], 888.0)

    def test_debito_reduz(self):
        self._escrever("MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            self._linha(natureza_despesa="31901100", valor="100"),
            self._linha(natureza_despesa="31901100", valor="30", natureza_conta="D"),
        ])
        res = apurar(Acervo(self.pasta), 2025, [1])
        self.assertEqual(res.get("vencimentos"), 70.0)

    def test_recorte_por_poder(self):
        self._escrever("MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            self._linha(natureza_despesa="31901100", valor="100"),
            self._linha(natureza_despesa="31901100", valor="40", poder_orgao="30390"),
        ])
        acervo = Acervo(self.pasta)
        self.assertEqual(apurar(acervo, 2025, [1]).get("vencimentos"), 100.0)
        self.assertEqual(apurar(acervo, 2025, [1], pos=("30390",)).get("vencimentos"), 40.0)

    def test_nao_executada_classe8(self):
        self._escrever("MSC_24_2025_m01_MSCC_msc_controle_classe8_period_change.csv", [
            self._linha(classe_conta="8", conta_contabil="863310000", valor="25",
                        natureza_despesa=""),
        ], classe="controle")
        self.assertEqual(nao_executada(Acervo(self.pasta), [(2025, 1)]), 25.0)

    def test_deducoes(self):
        self._escrever("MSC_24_2025_m01_MSCC_msc_orcamentaria_classe6_period_change.csv", [
            self._linha(natureza_despesa="31900101", valor="200", fonte_recursos="1800",
                        complemento_fonte="1111"),
            self._linha(natureza_despesa="31901100", valor="100", fonte_recursos="1605"),
        ])
        d = deducoes(Acervo(self.pasta), [(2025, 1)])
        self.assertEqual(d["vinculados"], 200.0)
        self.assertEqual(d["enfermagem_percentual"], 0.80)  # EC 127/2022: 2023 100, 2024 90, 2025 80, 2026 72
        self.assertAlmostEqual(d["enfermagem"], 80.0)   # 100 x 0,80


if __name__ == "__main__":
    unittest.main(verbosity=2)








