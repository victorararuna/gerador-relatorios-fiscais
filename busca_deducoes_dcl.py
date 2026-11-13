# -*- coding: utf-8 -*-
"""Anexo 2 (DCL): busca de subconjunto exato para as DEDUÇÕES.

As deduções do Anexo 2 (disponibilidade de caixa + haveres) são R$ 269.314.515,89.
Se algum subconjunto de contas da classe 1 reproduzir esse valor, temos a
composição — e, por consequência, a DC = DCL + deduções.
"""
from __future__ import annotations

import os
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
ALVO = 269_314_515.89


def centavos(v: float) -> int:
    return int(round(v * 100))


def busca(itens, alvo, limite=3):
    n = len(itens)
    meio = n // 2

    def somas(parte):
        d = {0: ()}
        for nome, v in parte:
            novo = {}
            for s, combo in d.items():
                t = s + v
                if t not in d and t not in novo:
                    novo[t] = combo + (nome,)
            d.update(novo)
        return d

    es, di = somas(itens[:meio]), somas(itens[meio:])
    achados = []
    for s, combo in es.items():
        falta = alvo - s
        if falta in di:
            achados.append(combo + di[falta])
            if len(achados) >= limite:
                break
    return achados


def main() -> int:
    acervo = M.Acervo(MSC)
    saldo = Counter()
    for r in acervo.ler(2025, 12, classe=1, tipo_valor="ending_balance"):
        if r.conta.startswith(("111", "112", "113")):
            saldo[r.conta] += -r.liquido

    itens = [(c, centavos(v)) for c, v in saldo.items() if abs(v) > 100_000]
    itens.sort(key=lambda x: -abs(x[1]))
    print(f"contas candidatas: {len(itens)}")
    if len(itens) > 34:
        print("limitando às 34 maiores")
        itens = itens[:34]

    achados = busca(itens, centavos(ALVO))
    if not achados:
        print("nenhum subconjunto exato")
        return 0
    for combo in achados:
        soma = sum(v for c, v in itens if c in combo)
        print(f"\nencontrado {soma / 100:,.2f}:")
        for c in sorted(combo):
            print(f"   {c}  {next(v for x, v in itens if x == c) / 100:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
