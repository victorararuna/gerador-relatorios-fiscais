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

#: coluna -> (prefixos de conta, classe, sinal, exclusões)
#: (a) classe 1 com sinal D-C, excluindo a conta-espelho 111120000
#: (e) contas de CONTROLE da classe 8 - a pratica do RN (notas 3 e 4 do anexo),
#:     que diverge do template da STN (2.1.8.9.1.01.05/.08)
COLUNAS = {
    "a": (("111",), 1, -1, ("111120000",)),
    "b": (("6321", "6313"), 6, 1, ()),
    "c": (("6327",), 6, 1, ()),
    "d": (("6311", "6312"), 6, 1, ()),
    "e": (("821130200", "821130300"), 8, 1, ()),
    "h": (("6317",), 6, 1, ()),
}

#: acrescimo proprio do ente na coluna (e), so na linha de recursos nao vinculados
CONTA_NAO_EXECUTADA = "863310000"
LINHA_NAO_VINCULADOS = "Recursos Não Vinculados de Impostos"

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


def apurar(ano: int, mes: int, prefixos, fr, classe: int = 6, sinal: int = 1,
           excluir=()) -> float:
    """Soma a coluna. Filtra por conta, por fonte e pelo Poder Executivo.

    O filtro `po` começando por "10" é o que separa o Executivo dos demais
    Poderes — sem ele, seis células do anexo somavam os outros Poderes.
    """
    from acervo import Acervo

    pos, tam, lista = fr
    acervo = Acervo(MSC)
    total = 0.0
    for r in acervo.ler(ano, mes, classe=classe, tipo_valor="ending_balance"):
        if not r.conta.startswith(prefixos):
            continue
        if r.conta in excluir:
            continue
        if not (r.po or "").startswith("10"):
            continue
        if ((r.fr or "")[pos - 1:pos - 1 + tam]) not in lista:
            continue
        total += sinal * r.liquido
    return total


def apurar_nao_executada(ano: int, mes: int, fr) -> float:
    """Acréscimo da conta 8.6.3.3.1 na coluna (e), linha de não vinculados."""
    from acervo import Acervo

    pos, tam, _ = fr
    acervo = Acervo(MSC)
    total = 0.0
    for r in acervo.ler(ano, mes, classe=8, tipo_valor="ending_balance"):
        if not r.conta.startswith(CONTA_NAO_EXECUTADA):
            continue
        if not (r.po or "").startswith("10"):
            continue
        total += r.liquido
    return total


def main() -> int:
    filtros, oficial = ler_planilha(PLANILHA)
    # a fonte 759 aparece em "Recursos Vinculados a Fundos" e em "Outras
    # Vinculações Legais"; o anexo a atribui somente à primeira.
    if "Outras Vinculações Legais" in filtros:
        pos, tam, lista = filtros["Outras Vinculações Legais"]
        filtros["Outras Vinculações Legais"] = (
            pos, tam, [f for f in lista if f != "759"])
    print(f"{len(filtros)} linhas com filtro de fonte\n")
    print(f"{'linha':<46}{'col':<4}{'nosso':>16}{'oficial':>16}{'dif':>12}")
    acertos = total = 0
    for nome, fr in filtros.items():
        valores = oficial.get(nome)
        if not valores:
            continue
        for i, (chave, (prefixos, classe, sinal, excluir)) in enumerate(COLUNAS.items()):
            if i >= len(valores):
                continue
            of = valores[i]
            if of is None:
                continue
            v = apurar(2025, 12, prefixos, fr, classe=classe, sinal=sinal,
                       excluir=excluir)
            if chave == "e" and nome == LINHA_NAO_VINCULADOS:
                v += apurar_nao_executada(2025, 12, fr)
            total += 1
            ok = abs(v - of) < 1.0
            acertos += ok
            if not ok:
                print(f"{nome[:44]:<46}{chave:<4}{v:>16,.2f}{of:>16,.2f}{v - of:>12,.0f}")
    print(f"\n{acertos} de {total} células exatas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


