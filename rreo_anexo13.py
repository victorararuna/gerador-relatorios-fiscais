# -*- coding: utf-8 -*-
"""RREO Anexo 13 — Parcerias Público-Privadas.

Não depende de cadastro de contratos: os saldos vêm da matriz contábil e a
despesa do contrato, da execução orçamentária.

Quadro I (saldos, `ending_balance`):

    Ativos Constituídos pela SPE ............ 8.9.1.2.2.*        (89122)
    Obrigações decorrentes dos ativos ....... 2.1.8.6.1.01 + 2.2.8.6.1.01
    Provisões de PPP ........................ 2.1.7.6 + 2.2.7.6
    Outros passivos ......................... 2.1.8.6.1.02/03/99 + 2.2.8.6.1.02/03/99
    Garantias concedidas .................... 8.1.2.1.1.01.22    (812110122)
    Obrigações contratuais .................. 8.1.2.3.1.08.01
    Riscos não provisionados ................ 8.1.2.3.1.08.03
    Outros passivos contingentes ............ 8.1.2.3.1.08.05

Quadro II (despesa do contrato, por modalidade 67):

    1º ao 5º bimestre: 6.2.2.1.1* + 6.2.2.1.2.02* + 6.2.2.1.3*
    6º bimestre:       SÓ 6.2.2.1.3*

A regra muda no último bimestre — e é justamente o do fechamento do exercício.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

ACERVO = os.path.join(AQUI, "dados", "acervo")

#: (linha do quadro I, classe, prefixos)
SALDOS = {
    "ativos_spe": (8, ("89122",)),
    "obrigacoes_spe": (2, ("2186101", "2286101")),
    "provisoes": (2, ("2176", "2276")),
    "outros_passivos": (2, ("2186102", "2186103", "2186199",
                            "2286102", "2286103", "2286199")),
    "garantias": (8, ("812110122",)),
    "obrigacoes_contratuais": (8, ("812310801",)),
    "riscos": (8, ("812310803",)),
    "outros_contingentes": (8, ("812310805",)),
}

#: prefixos das contas de despesa do contrato, por bloco de bimestre
DESPESA_ATE_5 = ("62211", "6221202", "62213")
DESPESA_6 = ("62213",)
#: modalidade 67 (PPP) nas naturezas 33, 44 e 45
MODALIDADE_PPP = ("3367", "4467", "4567")


def _acervo():
    from acervo import Acervo

    return Acervo(ACERVO)


def saldos(ano: int, mes: int) -> dict:
    """Quadro I — saldos das contas de PPP."""
    ac = _acervo()
    cache = {}
    saida = {}
    for chave, (classe, prefixos) in SALDOS.items():
        if classe not in cache:
            cache[classe] = list(ac.ler(ano, mes, classe=classe,
                                        tipo_valor="ending_balance"))
        total = 0.0
        for r in cache[classe]:
            if any(r.conta.startswith(p) for p in prefixos):
                total += r.liquido
        saida[chave] = total
    saida["total_ativos"] = saida["ativos_spe"]
    saida["total_passivos"] = (saida["obrigacoes_spe"] + saida["provisoes"]
                               + saida["outros_passivos"])
    saida["atos_potenciais"] = (saida["obrigacoes_contratuais"] + saida["riscos"]
                                + saida["garantias"] + saida["outros_contingentes"])
    return saida


def despesa_contrato(ano: int, mes: int, sexto_bimestre: bool = False) -> float:
    """Quadro II — dotação/despesa do contrato, filtrando a modalidade 67."""
    ac = _acervo()
    prefixos = DESPESA_6 if sexto_bimestre else DESPESA_ATE_5
    total = 0.0
    for r in ac.ler(ano, mes, classe=6, tipo_valor="ending_balance"):
        if not r.conta.startswith(prefixos):
            continue
        if not (r.nd or "").startswith(MODALIDADE_PPP):
            continue
        total += r.liquido
    return total


def main() -> int:
    from openpyxl import load_workbook

    planilha = (r"C:\Users\victo\Downloads\Arquivos etonjones"
                r"\Quadro_e_Mapa_Janeiro_a_Outubro_2026.xlsx")
    _ = planilha  # a planilha da equipe nao cobre o Anexo 13

    print("RREO Anexo 13 — PPP")
    print("\nQuadro I — saldos (31/12/2025 e 31/08/2026):")
    anterior = saldos(2025, 12)
    atual = saldos(2026, 8)
    rotulos = {
        "total_ativos": ("TOTAL DE ATIVOS", 400_000_000.00, 400_000_000.00),
        "total_passivos": ("TOTAL DE PASSIVOS", 215_455_288.93, 196_757_187.16),
        "atos_potenciais": ("ATOS POTENCIAIS PASSIVOS", 38_506_744.29, 413_225_632.16),
    }
    for chave, (nome, of_ant, of_atu) in rotulos.items():
        print(f"  {nome:<26}{anterior[chave]:>18,.2f}{atual[chave]:>18,.2f}"
              f"   oficial {of_ant:,.2f} / {of_atu:,.2f}")
    print(f"\nQuadro II — despesa do contrato: {despesa_contrato(2026, 8):>18,.2f}"
          f"   oficial 102.811.000,00")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
