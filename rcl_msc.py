# -*- coding: utf-8 -*-
"""RCL construida a partir da MSC, pelo mapeamento do MDF 15a edicao.

Ate a rodada 129 a RCL era **lida** do arquivo publicado. O mapeamento oficial
(`dados/mapeamentos/rreo/.../RREO - ANEXO 03 - RCL ... - MSC 2026.xlsx`) mostra
que ela e calculavel: a receita realizada fica na **classe 6**, na conta
`6.2.1.2.0.00.00`, e as deducoes na `6.2.1.3.x` e em naturezas de receita.

Estrutura (Tabela 3.1 do MDF, Estados):

    RECEITAS CORRENTES (I)  = 6.2.1.2.x com NR comecando em 1
    DEDUCOES (II)           = 6.2.1.3.1.01.00  (FUNDEB)
                            + 6.2.1.3.1.02.00  (transferencias constitucionais)
                            + NR 1.2.1.5.x     (contribuicao do servidor)
                            + NR 1.9.9.9.03    (compensacao entre regimes)
                            + NR 1.3.2.1.04    (rendimentos previdenciarios)
    RCL (III)               = I - II

A janela e de **12 meses** (MR-11 a MR), nao o mes isolado.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "app"))

ACERVO = os.path.join(AQUI, "dados", "acervo")

#: contas de deducao na classe 6
CONTA_FUNDEB = "621310100"
CONTA_TRANSF = "621310200"

#: naturezas de receita que tambem sao deduzidas
NR_DEDUCOES = {
    "contrib_servidor": "1215",
    "compensacao": "199903",
    "rend_prev": "132104",
}


def _acervo():
    from acervo import Acervo
    return Acervo(ACERVO)


def janela(ano: int, mes: int, meses: int = 12) -> list[tuple[int, int]]:
    """Os meses da janela de 12 meses que termina em (ano, mes)."""
    saida = []
    a, m = ano, mes
    for _ in range(meses):
        saida.append((a, m))
        m -= 1
        if m == 0:
            a, m = a - 1, 12
    return list(reversed(saida))


def apurar(ano: int, mes: int) -> dict:
    """Constroi a RCL e as duas ajustadas para a janela de 12 meses."""
    ac = _acervo()
    receita = 0.0
    fundeb = 0.0
    transf = 0.0
    deducoes_nr = dict.fromkeys(NR_DEDUCOES, 0.0)

    for a, m in janela(ano, mes):
        for r in ac.ler(a, m, classe=6, tipo_valor="period_change"):
            conta = r.conta or ""
            nr = r.nr or ""
            if conta.startswith("6212") and nr.startswith("1"):
                receita += r.liquido
                # as tres naturezas abaixo estao DENTRO da receita e tambem sao
                # deduzidas: entram em I e saem em II
                for nome, prefixo in NR_DEDUCOES.items():
                    if nr.startswith(prefixo):
                        deducoes_nr[nome] += r.liquido
                        break
            elif conta == CONTA_FUNDEB:
                fundeb += r.liquido
            elif conta == CONTA_TRANSF:
                transf += r.liquido

    # as contas de deducao sao credoras: o valor vem negativo
    fundeb = -fundeb
    transf = -transf
    deducoes = fundeb + transf + sum(deducoes_nr.values())
    rcl = receita - deducoes

    return {
        "receitas_correntes": receita,
        "fundeb": fundeb,
        "transferencias": transf,
        **deducoes_nr,
        "deducoes": deducoes,
        "rcl": rcl,
    }


if __name__ == "__main__":
    for ano, mes in ((2025, 12), (2026, 8)):
        v = apurar(ano, mes)
        print(f"\n=== {ano}-{mes:02d} (janela de 12 meses)")
        for k, x in v.items():
            print(f"   {k:<22}{x:>20,.2f}")
