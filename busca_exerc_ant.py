# -*- coding: utf-8 -*-
"""A linha 'Exercícios Anteriores' do Anexo 1: algum subconjunto da matriz
reproduz exatamente os R$ 248.732.357,39 que o homologado repete em três
janelas diferentes?
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
ALVO = 248_732_357.39
CONTAS = ("622130300", "622130400", "622130700")


def centavos(v: float) -> int:
    return int(round(v * 100))


def busca(itens, alvo, limite=2):
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
    comp = defaultdict(float)
    for mes in range(1, 13):
        for r in acervo.ler(2025, mes):
            if r.conta not in CONTAS or not r.nd:
                continue
            if r.nd[:6] in ("319092", "319192", "319096", "319196"):
                if r.po in ("10111", "10112", "60611"):
                    comp[(r.nd, r.po)] += r.liquido

    itens = [(f"{nd}/{po}", centavos(v)) for (nd, po), v in comp.items()]
    itens.sort(key=lambda x: -abs(x[1]))
    if len(itens) > 26:
        print(f"AVISO: {len(itens)} componentes; usando os 26 maiores")
        itens = itens[:26]
    total = sum(v for _, v in itens)
    print(f"componentes 92/192/96: {len(itens)}  soma {total / 100:,.2f}")
    print(f"alvo (homologado) .... {ALVO:,.2f}")

    achados = busca(itens, centavos(ALVO))
    if not achados:
        print("\nnenhum subconjunto exato")
        return 0
    for combo in achados:
        soma = sum(v for c, v in itens if c in combo)
        print(f"\nencontrado: {soma / 100:,.2f} com {len(combo)} componentes")
        for c in sorted(combo):
            print(f"   {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


