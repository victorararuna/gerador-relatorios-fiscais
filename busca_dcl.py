# -*- coding: utf-8 -*-
"""Busca de subconjunto: quais contas reproduzem cada bloco do Anexo 2?

Usa meet-in-the-middle com valores em centavos (inteiros), tolerância zero.
"""
from __future__ import annotations

import itertools
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"

ALVOS = {
    "precatorios": 559_540_150_777,
    "contratual": 320_426_402_897,
    "outras": 94_192_619_762,
}


def centavos(v: float) -> int:
    return int(round(v * 100))


def busca(itens, alvo, limite=3, min_itens=1):
    """Subconjuntos de ``itens`` (lista de (nome, centavos)) que somam alvo."""
    n = len(itens)
    meio = n // 2
    esq, dir_ = itens[:meio], itens[meio:]

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

    es = somas(esq)
    di = somas(dir_)
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
    saldo = {}
    for r in acervo.ler(2025, 12, classe=2, tipo_valor="ending_balance"):
        c = r.conta
        if c.startswith("23") or c.startswith("27"):
            continue
        saldo[c] = saldo.get(c, 0.0) + r.liquido

    prec = [(c, centavos(v)) for c, v in saldo.items() if c.startswith("2211")]
    outr = [(c, centavos(v)) for c, v in saldo.items() if c.startswith("218")]
    contr = [(c, centavos(v)) for c, v in saldo.items()
             if c.startswith(("2221", "2222", "2231", "2241"))]

    for nome, itens, alvo in (("precatorios", prec, ALVOS["precatorios"]),
                              ("outras", outr, ALVOS["outras"]),
                              ("contratual", contr, ALVOS["contratual"])):
        print(f"\n=== {nome}: {len(itens)} contas, alvo {alvo / 100:,.2f}")
        if len(itens) > 30:
            print("   (muitas contas; limitando às 30 maiores)")
            itens = sorted(itens, key=lambda x: -abs(x[1]))[:30]
        achados = busca(itens, alvo)
        if not achados:
            print("   nenhum subconjunto exato")
        for combo in achados:
            total = sum(v for c, v in itens if c in combo)
            print(f"   {total / 100:,.2f}  <- {sorted(combo)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
