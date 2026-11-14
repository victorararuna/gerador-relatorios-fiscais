# -*- coding: utf-8 -*-
"""Extrai as regras do mapeamento oficial do RGF Anexo 1 (rodada 131).

O arquivo `RGF - ANEXO 1 ... - MSC 2026.xlsx` traz, para cada rubrica, duas
coisas: o **filtro do Siconfi** (coluna B) e o **criterio de contas** (coluna C).
Estao em texto livre, com listas longas de naturezas de despesa.

Este script le as celulas inteiras e grava um JSON com as listas, para que a
apuracao use a regra oficial em vez das listas montadas a mao.
"""
from __future__ import annotations

import json
import os
import re
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(RAIZ, "dados", "mapeamentos", "rgf",
                     "RGF - PARTE IV - MDF 15ª EDIÇÃO")
ABA = "Anexo 1- E, DF, M- 3Q- DemaisPO"

#: linha do mapeamento -> chave da rubrica
RUBRICAS = {
    27: "vencimentos",
    28: "patronal",
    30: "aposentadorias",
    31: "pensoes",
    32: "terceirizacao",
    33: "nao_executada",
}

#: linhas de despesas nao computadas
NAO_COMPUTADAS = {
    35: "indenizacoes",
    36: "judiciais",
    37: "exercicios_anteriores",
    38: "inativos_vinculados",
    39: "acs_ace",
}


def _listas(texto: str) -> list[str]:
    """Extrai as listas de naturezas de um texto do mapeamento.

    As listas aparecem como "Lista=30,70,80,90" ou como sequencias longas de
    codigos de 6 a 8 digitos separados por virgula.
    """
    if not texto:
        return []
    achados = []
    for bloco in re.findall(r"(?:Lista\s*=\s*)([0-9,\s/]+)", texto):
        for item in re.split(r"[,/\s]+", bloco):
            item = item.strip()
            if item and item not in achados:
                achados.append(item)
    # codigos longos soltos (ex.: 31909101)
    for codigo in re.findall(r"\b(3[0-9]{5,7})\b", texto):
        if codigo not in achados:
            achados.append(codigo)
    return achados


def main() -> int:
    arq = next(f for f in os.listdir(PASTA) if "ANEXO 1" in f)
    wb = openpyxl.load_workbook(os.path.join(PASTA, arq), data_only=True)
    ws = wb[ABA]

    saida = {"fonte": arq, "aba": ABA, "rubricas": {}, "nao_computadas": {}}

    for linha, chave in {**RUBRICAS, **NAO_COMPUTADAS}.items():
        filtro = ws.cell(linha, 2).value or ""
        contas = ws.cell(linha, 3).value or ""
        destino = ("rubricas" if linha in RUBRICAS else "nao_computadas")
        saida[destino][chave] = {
            "filtro_texto": str(filtro).strip(),
            "contas_texto": str(contas).strip(),
            "listas": _listas(str(filtro)),
            "contas": sorted(set(re.findall(r"\b6\.\d\.\d\.\d\.\d{2}\.\d{2}\b", str(contas)))),
            "nds": sorted(set(re.findall(r"\b3\.\d\.\d{2}\.\d{2}\.\d{2}\b", str(contas)))),
        }

    destino = os.path.join(RAIZ, "dados", "mapeamentos", "anexo1_regras.json")
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=2)

    for grupo in ("rubricas", "nao_computadas"):
        print(f"\n{grupo}:")
        for chave, v in saida[grupo].items():
            print(f"   {chave:<22}{len(v['nds']):>4} NDs  {len(v['contas']):>2} contas  "
                  f"{len(v['listas']):>4} listas")
    print(f"\nok -> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
