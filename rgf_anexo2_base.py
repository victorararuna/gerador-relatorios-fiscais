# -*- coding: utf-8 -*-
"""RGF Anexo 2 (DCL) a partir da base de contas da planilha da equipe.

A aba "Anexo 2 - RGF BASE" dos XLSX de trabalho lista, seção por seção, as
contas que compõem cada linha do demonstrativo. Contas prefixadas com "(-)" são
deduções (encargos, ajustes de perdas).

Sinal: passivo (classe 2) entra pelo saldo credor; ativo (classe 1) entra
negativo, porque a disponibilidade deduz da dívida.
"""
from __future__ import annotations

import os
import re
import sys
from collections import OrderedDict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

MSC = os.path.join(AQUI, "dados", "acervo")
PLANILHA = (r"C:\Users\victo\Downloads\RELATÓRIOS CONTAG\Demonstrativos Fiscais 2025"
            r"\RGF 2025\3º QUADRIMESTRE\PRONTOS\EXCEL"
            r"\RGF 2025_3Q_02 - DEMONSTRATIVO DA DÍVIDA CONSOLIDADA LÍQUIDA.xlsx")

RE_CONTA = re.compile(r"^\d(\.\d+)+$")


def ler_base(caminho: str) -> "OrderedDict[str, list]":
    """Seções na ordem; cada conta com o sinal (1 ou -1)."""
    from openpyxl import load_workbook

    ws = load_workbook(caminho, data_only=True)["Anexo 2 - RGF BASE"]
    secoes: "OrderedDict[str, list]" = OrderedDict()
    atual = "(início)"
    for r in range(1, ws.max_row + 1):
        a = ws.cell(r, 1).value
        if not isinstance(a, str):
            continue
        texto = a.strip()
        sinal = 1
        if texto.startswith("(-)"):
            texto = texto[3:].strip()
            sinal = -1
        if RE_CONTA.match(texto):
            secoes.setdefault(atual, []).append((texto, sinal))
        elif texto:
            atual = a.strip()
            secoes.setdefault(atual, [])
    return secoes


def apurar(ano: int, mes: int, contas: list) -> float:
    from acervo import Acervo

    alvo = {c.replace(".", ""): s for c, s in contas}
    acervo = Acervo(MSC)
    total = 0.0
    for classe in (1, 2):
        try:
            leitor = acervo.ler(ano, mes, classe=classe, tipo_valor="ending_balance")
        except FileNotFoundError:
            continue
        for r in leitor:
            s = alvo.get(r.conta)
            if s is None:
                continue
            # classe 2: credor é positivo; classe 1: devedor é positivo
            v = r.liquido if classe == 2 else -r.liquido
            total += s * v
    return total


def main() -> int:
    ano = int(sys.argv[1]) if len(sys.argv) > 1 else 2025
    mes = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    secoes = ler_base(PLANILHA)
    com_contas = {k: v for k, v in secoes.items() if v}
    print(f"{len(com_contas)} seções com contas | ano {ano} mês {mes}\n")
    for nome, contas in com_contas.items():
        v = apurar(ano, mes, contas)
        print(f"{nome[:50]:<52}{len(contas):>3}{v:>20,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
