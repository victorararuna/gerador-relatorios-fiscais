# -*- coding: utf-8 -*-
"""Transcreve o mapa de fontes do Anexo 5 para JSON (rodada 163).

A aba `MAPEAMENTO` da planilha da equipe tem duas coisas:

1. os **titulos das colunas** do demonstrativo (posicao 4 a 9, linha 16);
2. a **tabela de linhas**: nome da linha e o filtro de fonte de recurso
   (linhas 19 a 45) — por exemplo "FR Pos. inicial = 1; Tamanho = 2; Lista = 10".

Era a ultima coisa que prendia o Anexo 5 a uma planilha externa. Transcrita para
`dados/mapeamentos/anexo5_mapeamento.json`, o gerador passa a rodar sozinho.

Uso:
    python extrair_mapa_anexo5.py
"""
from __future__ import annotations

import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

DESTINO = os.path.join(RAIZ, "dados", "mapeamentos", "anexo5_mapeamento.json")


def main() -> int:
    import rgf_anexo5_disp as D

    if not os.path.exists(D.PLANILHA):
        print(f"planilha nao encontrada: {D.PLANILHA}")
        return 2

    colunas, linhas = D.ler_mapeamento(D.PLANILHA)
    dados = {
        "fonte": os.path.basename(D.PLANILHA),
        "aba": "MAPEAMENTO",
        "colunas": colunas,
        "linhas": [[nome, filtro] for nome, filtro in linhas],
    }
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)

    print(f"{len(colunas)} colunas, {len(linhas)} linhas")
    for nome, filtro in linhas[:8]:
        print(f"   {nome[:44]:<46} {filtro[:40]}")
    print(f"\nok -> {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
