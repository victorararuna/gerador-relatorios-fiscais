# -*- coding: utf-8 -*-
"""RREO Anexo 11 — Alienação de Ativos e Aplicação dos Recursos.

Regra do mapeamento da STN (`RREO - ANEXO 11 - Alienação de Ativos ... MSC 2026`):

  Receita de Alienação de Bens Móveis
      NR: 2.2.1 + 8.2.1 + 1.9.4.1 + 7.9.4.1   ·   FR: 755, 756, 762
  Receita de Alienação de Bens Imóveis
      NR: 2.2.2 + 8.2.2 + 1.9.4.2 + 7.9.4.2
  Receita de Alienação de Bens Intangíveis
      NR: 2.2.3 + 8.2.3 + 1.9.4.3 + 7.9.4.3
  Receita de Rendimentos de Aplicações Financeiras
      NR: 1.3.2.1.01 + .02 + .03 + .05 + .99
  Investimentos          -> ND 4.4 · FR 755, 756, 762, sobre 6.2.2.1.3
  Inversões Financeiras  -> ND 4.5 · FR 755, 756, 762, sobre 6.2.2.1.3

A receita sai de `6.2.1.2.0.00.00` (classe 6) e a despesa de `6.2.2.1.3.00.00`.
O valor da linha (III) e a receita menos as despesas de capital custeadas.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "app"))

ACERVO = os.path.join(AQUI, "dados", "acervo")

#: fontes de recursos que custeiam a alienacao
FONTES = {"755", "756", "762"}

#: naturezas de receita, por linha
NR_RECEITAS = {
    "moveis": ("221", "821", "1941", "7941"),
    "imoveis": ("222", "822", "1942", "7942"),
    "intangiveis": ("223", "823", "1943", "7943"),
    "rendimentos": ("132101", "132102", "132103", "132105", "132999"),
}


def _fonte(registro) -> str:
    """Os tres ultimos digitos da fonte (X.755 -> 755)."""
    return (registro.fr or "")[1:4]


def linhas(ano: int, meses: int = 12) -> dict:
    """Apuura as seis linhas do Anexo 11 para o acumulado do exercicio."""
    from acervo import Acervo

    ac = Acervo(ACERVO)
    receitas = dict.fromkeys(NR_RECEITAS, 0.0)
    investimentos = inversoes = 0.0

    for mes in range(1, meses + 1):
        try:
            registros = list(ac.ler(ano, mes, classe=6, tipo_valor="period_change"))
        except FileNotFoundError:
            continue          # mes ainda nao publicado na matriz
        for r in registros:
            conta = r.conta or ""
            if _fonte(r) not in FONTES:
                continue
            if conta.startswith("6212"):
                nr = r.nr or ""
                for chave, prefixos in NR_RECEITAS.items():
                    if nr.startswith(prefixos):
                        receitas[chave] += r.liquido
                        break
            elif conta.startswith("62213"):
                nd = (r.nd or "").replace(".", "")
                if nd.startswith("44"):
                    investimentos += r.liquido
                elif nd.startswith("45"):
                    inversoes += r.liquido

    total_receita = sum(receitas.values())
    aplicacao = investimentos + inversoes
    return {
        **receitas,
        "receitas_alienacao": total_receita,
        "investimentos": investimentos,
        "inversoes": inversoes,
        "aplicacao": aplicacao,
        "valor": total_receita - aplicacao,
    }


if __name__ == "__main__":
    for ano in (2025, 2026):
        v = linhas(ano)
        print(f"\n=== {ano}")
        for k, x in v.items():
            print(f"   {k:<20}{x:>16,.2f}")
