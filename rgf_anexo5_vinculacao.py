# -*- coding: utf-8 -*-
"""RGF Anexo 5 — quebra por vinculação (as 27 linhas do MAPEAMENTO).

Cada linha do anexo é identificada por um filtro de **fonte de recursos**
(posição 2, tamanho variável, lista de valores). As colunas vêm do MAPEAMENTO:

    (a) disponibilidade   -> 8.2.1.7.4.01 + 1.1.1.1.1.01
    (b) RP liquidados     -> 6321, 6313
    (c) RP do exercício   -> 6327
    (d) RP não liquidados -> 6311, 6312
    (e) demais obrigações -> 8.2.1.1.3.02 e 03
    (f) insuficiência     -> 8535
    (g) = (a − (b+c+d+e) − f)

Este módulo apura as colunas (b), (c) e (d) por linha e compara com o QUADRO
PRINCIPAL.
"""
from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

MSC = os.path.join(AQUI, "dados", "acervo")
PLANILHA = (r"C:\Users\victo\Downloads\RELATÓRIOS CONTAG\Demonstrativos Fiscais 2025"
            r"\RGF 2025\3º QUADRIMESTRE\PRONTOS\EXCEL"
            r"\RGF 2025_Q3_05 -DEMONSTRATIVO DA DISPONIBILIDADE DE CAIXA E DOS RESTOS A PAGAR.xlsx")

#: coluna -> prefixos de conta
COLUNAS = {
    "b": ("6321", "6313"),
    "c": ("6327",),
    "d": ("6311", "6312"),
}

RE_FILTRO = re.compile(
    r"FR\s+Pos\.?\s*inicial\s*=\s*(\d+)\s*;\s*Tamanho\s*=\s*(\d+);?\s*Lista\s*=\s*([\d,]+)",
    re.I)


def ler_planilha(caminho: str):
    """(filtros por linha, valores oficiais por linha)."""
    from openpyxl import load_workbook

    wb = load_workbook(caminho, data_only=True)
    qm, qp = wb["MAPEAMENTO"], wb["QUADRO PRINCIPAL"]
    filtros = {}
    for r in range(19, 46):
        nome = qm.cell(r, 1).value
        texto = qm.cell(r, 2).value
        if not (isinstance(nome, str) and nome.strip() and texto):
            continue
        m = RE_FILTRO.search(str(texto))
        if m:
            filtros[nome.strip()] = (
                int(m.group(1)), int(m.group(2)),
                [x.strip() for x in m.group(3).split(",")])
    oficial = {}
    for r in range(13, 40):
        nome = qp.cell(r, 1).value
        if isinstance(nome, str) and nome.strip():
            oficial[nome.strip()] = tuple(qp.cell(r, c).value for c in range(2, 7))
    return filtros, oficial


def apurar(ano: int, mes: int, prefixos, fr) -> float:
    from acervo import Acervo

    pos, tam, lista = fr
    acervo = Acervo(MSC)
    total = 0.0
    for r in acervo.ler(ano, mes, classe=6, tipo_valor="ending_balance"):
        if not r.conta.startswith(prefixos):
            continue
        if ((r.fr or "")[pos - 1:pos - 1 + tam]) not in lista:
            continue
        total += r.liquido
    return total


def main() -> int:
    filtros, oficial = ler_planilha(PLANILHA)
    print(f"{len(filtros)} linhas com filtro de fonte\n")
    print(f"{'linha':<46}{'col':<4}{'nosso':>16}{'oficial':>16}{'dif':>12}")
    acertos = total = 0
    for nome, fr in filtros.items():
        valores = oficial.get(nome)
        if not valores:
            continue
        for i, (chave, prefixos) in enumerate(COLUNAS.items(), start=1):
            of = valores[i]
            if of is None:
                continue
            v = apurar(2025, 12, prefixos, fr)
            total += 1
            ok = abs(v - of) < 1.0
            acertos += ok
            if not ok:
                print(f"{nome[:44]:<46}{chave:<4}{v:>16,.2f}{of:>16,.2f}{v - of:>12,.0f}")
    print(f"\n{acertos} de {total} células exatas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
