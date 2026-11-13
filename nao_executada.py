# -*- coding: utf-8 -*-
"""MAPA linha 251 — Despesa com Pessoal Não Executada Orçamentariamente.

Regra do manual: `Movimento Credor − Movimento Devedor` das contas
`8.6.3.3.1.01.00.00` (Salários) e `8.6.3.3.1.02.00.00` (13º).

No movimento de baixa do 13º em abril/2026 há R$ 1.337.759,24 de encargos
patronais dos demais Poderes (subelementos .71/.72/.73/.75) que já entram
expurgados na despesa bruta — por isso são devolvidos aqui, para não deduzir
duas vezes.

Fonte: relatórios `Relatorio_13112026*.pdf` (Consolidado da conta).
"""
from __future__ import annotations

import glob
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

BASE = r"C:\Users\victo\Downloads\Arquivos etonjones"
MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")
#: devolução da baixa do 13º dos demais Poderes em abril/2026
EXPURGO_ABRIL = 1_337_759.24
NUM = r"-?\d{1,3}(?:\.\d{3})*,\d{2}"


def _num(t: str) -> float:
    return float(t.replace(".", "").replace(",", "."))


def ler_movimentos() -> dict:
    """(conta, mês) -> (movimento devedor, movimento credor)."""
    import leitor_pdf as LP

    saida = {}
    for arq in sorted(glob.glob(os.path.join(BASE, "Relatorio_13112026*.pdf"))):
        texto = re.sub(r"\s+", " ", " ".join(p.texto() for p in LP.ler_pdf(arq)))
        m_conta = re.search(r"Conta Contábil\s*(8\.6\.3\.3\.1\.\d\d\.00\.00)", texto)
        m_mes = re.search(r"M[êe]s Refer[êe]ncia\s+(" + "|".join(MESES) + r")", texto)
        if not m_conta or not m_mes:
            continue  # relatórios de abertura
        m = re.search(r"Saldo\s+(" + NUM + r")\s+(" + NUM + r")\s+(" + NUM + r")", texto)
        if not m:
            continue
        saida[(m_conta.group(1), m_mes.group(1))] = (_num(m.group(1)), _num(m.group(2)))
    return saida


def valores() -> dict:
    """mês -> valor da MAPA linha 251."""
    mov = ler_movimentos()
    saida = {}
    for mes in MESES:
        saldo = 0.0
        for conta in ("8.6.3.3.1.01.00.00", "8.6.3.3.1.02.00.00"):
            if (conta, mes) not in mov:
                continue
            devedor, credor = mov[(conta, mes)]
            saldo += credor - devedor
        if mes == "Abril":
            saldo += EXPURGO_ABRIL
        saida[mes] = saldo
    return saida


def main() -> int:
    v = valores()
    print(f"{'mês':<12}{'linha 251':>18}")
    for mes in MESES:
        if v[mes]:
            print(f"{mes:<12}{v[mes]:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
