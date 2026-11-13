# -*- coding: utf-8 -*-
"""Leitor do Balancete Consolidado do SIAFEM/RN.

O balancete é o relatório de **encerramento** e traz todas as classes contábeis,
inclusive a **classe 8** (controles credores) — onde ficam as contas que a MSC
publicada não expõe:

    8.6.3.3.1.00.00.00   Controles da Despesa Não Executada Orçamentariamente
    8.2.1.7.4.01.00.00   Disponibilidade por Fonte a Utilizar

Formato (aba Sheet1):

    linha 8     Tipo Consolidação: Consolidado Geral
    linha 9     Mês Referência: Encerramento
    linha 11    Conta Contábil
    linha 13    Saldo Exercício Anterior | Movimento Até Mês Anterior | ...

Para cada conta:

    linha N     "8.6.3.3.1.00.00.00 Controles da Despesa Não Executada..."
    linha N+1   os valores: c3 = saldo anterior, c6 = movimento D,
                c9 = movimento C, c12 = saldo final

Os valores vêm como texto no padrão brasileiro com sufixo D/C
(``454.943.101,05 C``).
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import leitor_xls as LX

RE_CONTA = re.compile(r"^(\d+(?:\.\d+)+)\s+(.*)$")
RE_VALOR = re.compile(r"^(-?[\d.]+,\d{2})\s*([DC]?)$")


@dataclass
class Conta:
    codigo: str
    descricao: str
    saldo_anterior: float
    nat_anterior: str
    mov_debito: float
    mov_credito: float
    saldo_final: float
    nat_final: str

    @property
    def valor(self) -> float:
        """Movimento líquido: créditos − débitos."""
        return self.mov_credito - self.mov_debito


def _num(v) -> tuple:
    """('454.943.101,05 C') -> (454943101.05, 'C')."""
    if v is None:
        return 0.0, ""
    t = str(v).strip().replace("C", " C").replace("D", " D")
    m = RE_VALOR.match(t)
    if not m:
        # sem sufixo
        try:
            return float(t.replace(".", "").replace(",", ".")), ""
        except ValueError:
            return 0.0, ""
    bruto, nat = m.group(1), m.group(2)
    try:
        return float(bruto.replace(".", "").replace(",", ".")), nat
    except ValueError:
        return 0.0, ""


def ler(caminho: str) -> Dict[str, Conta]:
    """{codigo: Conta} do balancete."""
    wb = LX.ler_xls(caminho)
    aba = wb.aba(wb.nomes[0])
    contas: Dict[str, Conta] = {}

    lin = 1
    while lin <= aba.max_lin:
        bruto = aba.valor(lin, 3)
        if not isinstance(bruto, str):
            lin += 1
            continue
        m = RE_CONTA.match(bruto.strip())
        if not m:
            lin += 1
            continue
        codigo, descricao = m.group(1), m.group(2).strip()
        # os valores estão na linha seguinte
        prox = lin + 1
        saldo_ant, nat_ant = _num(aba.valor(prox, 3))
        mov_dev, _ = _num(aba.valor(prox, 6))
        mov_cre, _ = _num(aba.valor(prox, 9))
        saldo_fin, nat_fin = _num(aba.valor(prox, 12))
        contas[codigo] = Conta(codigo=codigo, descricao=descricao,
                               saldo_anterior=saldo_ant, nat_anterior=nat_ant,
                               mov_debito=mov_dev, mov_credito=mov_cre,
                               saldo_final=saldo_fin, nat_final=nat_fin)
        lin += 2
    return contas


def nao_executada(caminho: str, usar_movimento: bool = True) -> float:
    """Despesa com Pessoal não Executada Orçamentariamente (conta 8.6.3.3.1).

    A conta **zera no encerramento**: o saldo anterior é a despesa não executada
    do exercício anterior e o saldo final é zero. A despesa do exercício corrente
    é o **movimento líquido** (créditos − débitos).

    Conferido: no balancete de 2025, o movimento é R$ 168.849.452,03 — o mesmo
    valor apurado pela MSC.
    """
    c = ler(caminho)
    for codigo in ("8.6.3.3.1.00.00.00", "8.6.3.3.1.00.00"):
        if codigo in c:
            conta = c[codigo]
            return conta.valor if usar_movimento else conta.saldo_anterior
    total = 0.0
    for k, v in c.items():
        if k.startswith("8.6.3.3.1.") and k.count(".") == 6 and k.endswith("00.00"):
            total += v.valor if usar_movimento else v.saldo_anterior
    return total


def disponibilidade_por_fonte(caminho: str) -> float:
    """Disponibilidade por Fonte a Utilizar (conta 8.2.1.7.4.01)."""
    c = ler(caminho)
    for codigo in ("8.2.1.7.4.01.00.00", "8.2.1.7.4.01.00", "8.2.1.7.4.01"):
        if codigo in c:
            return c[codigo].saldo_anterior or c[codigo].valor
    return 0.0


def ano_base(caminho: str) -> str:
    """Ano Base do balancete (cabeçalho)."""
    wb = LX.ler_xls(caminho)
    aba = wb.aba(wb.nomes[0])
    for lin in range(1, 12):
        for col in range(1, aba.max_col + 1):
            v = aba.valor(lin, col)
            if isinstance(v, str) and "ano base" in v.lower():
                m = re.search(r"(\d{4})", v)
                if m:
                    return m.group(1)
    return ""


def resumo(caminho: str) -> dict:
    c = ler(caminho)
    return {
        "ano_base": ano_base(caminho),
        "contas": len(c),
        "classe8": sum(1 for k in c if k.startswith("8.")),
        "nao_executada": nao_executada(caminho),
        "nao_executada_anterior": nao_executada(caminho, usar_movimento=False),
        "disponibilidade_fonte": disponibilidade_por_fonte(caminho),
    }


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else \
        r"C:\Users\victo\Downloads\Imprimir Balancete Consolidado.xls"
    r = resumo(caminho)
    print(f"ano base ............ {r['ano_base']}")
    print(f"contas .............. {r['contas']}")
    print(f"contas classe 8 ..... {r['classe8']}")
    print(f"nao executada ....... {r['nao_executada']:,.2f} (movimento do exercicio)")
    print(f"nao executada ant ... {r['nao_executada_anterior']:,.2f} (saldo anterior)")
    print(f"disponib. por fonte . {r['disponibilidade_fonte']:,.2f}")
