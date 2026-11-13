# -*- coding: utf-8 -*-
"""RGF Anexo 5 — disponibilidade por vinculação, a partir do MAPEAMENTO da equipe.

A aba MAPEAMENTO do arquivo de trabalho dá as duas dimensões:

* **coluna** — critério de conta (a) a (f), sempre Ending_Balance;
* **linha** — filtro por PO e pela fonte de recursos (posição 2, tamanho 3).

Este módulo lê esse mapeamento, aplica na MSC e compara com o QUADRO PRINCIPAL.
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

#: totais oficiais do QUADRO PRINCIPAL (linha 39), 2025 Q3
OFICIAL = {
    "a": 1_088_399_547.00,
    "b": 472_988_715.32,
    "c": 1_405_948_478.02,
    "d": 11_871_954.46,
    "e": 2_230_614_991.10,
    "f": 0.0,
    "g": -3_033_024_591.90,
}

RE_LISTA = re.compile(r"(?:Lista\)?\s*[:=]?\s*)([\d,\s]+)")


def _lista(texto: str) -> list:
    trecho = texto.split(":")[-1] if ":" in texto else texto
    return [t.strip() for t in re.split(r"[,\s]+", trecho) if t.strip().isdigit()]


def ler_mapeamento(caminho: str):
    from openpyxl import load_workbook

    ws = load_workbook(caminho, data_only=True)["MAPEAMENTO"]
    colunas = {}
    for c, chave in ((4, "a"), (5, "b"), (6, "c"), (7, "d"), (8, "e"), (9, "f")):
        colunas[chave] = ws.cell(16, c).value or ""
    linhas = []
    for r in range(19, 46):
        nome = ws.cell(r, 1).value
        filtro = ws.cell(r, 2).value
        if isinstance(nome, str) and nome.strip():
            linhas.append((nome.strip(), str(filtro or "")))
    return colunas, linhas


def _filtro_fr(texto: str):
    """(posição, tamanho, lista) do filtro de FR, se houver."""
    m = re.search(r"FR\s+Pos\.?\s*inicial\s*=\s*(\d+)\s*;?\s*Tamanho\s*=\s*(\d+)"
                  r"(?:\s*;\s*Lista\s*=)?\s*([\d,\s]+)?", texto, re.I)
    if not m:
        return None
    pos, tam = int(m.group(1)), int(m.group(2))
    itens = [t.strip() for t in re.split(r"[,\s]+", m.group(3) or "") if t.strip()]
    return pos, tam, itens


def apurar(ano: int, mes: int, contas_prefixos: list, fr_filtro) -> float:
    from acervo import Acervo

    acervo = Acervo(MSC)
    total = 0.0
    if not acervo.tem(ano, mes, classe=1, tipo_valor="ending_balance"):
        return 0.0
    for classe in (1, 2, 6):
        try:
            leitor = acervo.ler(ano, mes, classe=classe, tipo_valor="ending_balance")
        except FileNotFoundError:
            continue
        for r in leitor:
            if not any(r.conta.startswith(p) for p in contas_prefixos):
                continue
            if fr_filtro:
                pos, tam, itens = fr_filtro
                pedaco = (r.fr or "")[pos - 1:pos - 1 + tam]
                if itens and pedaco not in itens:
                    continue
            total += r.liquido
    return total


def main() -> int:
    colunas, linhas = ler_mapeamento(PLANILHA)
    print("critérios de conta:")
    for k, v in colunas.items():
        print(f"   ({k}) {str(v)[:64]}")
    print(f"\nlinhas de vinculação: {len(linhas)}")
    amostra = linhas[:3]
    for nome, filtro in amostra:
        print(f"   {nome[:46]:<48} {filtro[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
