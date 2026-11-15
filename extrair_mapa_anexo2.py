# -*- coding: utf-8 -*-
"""Transcreve o mapa de contas do Anexo 2 para JSON (rodada 162).

A aba `Anexo 2 - RGF BASE` da planilha da equipe lista, secao por secao, as
contas contabeis que compoem a Divida Consolidada e as Deducoes. O gerador lia
essa aba em tempo de execucao — o que o prendia a uma planilha externa.

Este script le a aba **uma vez** e grava o mapa em
`dados/mapeamentos/anexo2_contas.json`. A partir dai o gerador le o JSON, que e
versionado no repositorio: o mapa fica auditavel e a planilha deixa de ser
dependencia.

Uso:
    python extrair_mapa_anexo2.py
"""
from __future__ import annotations

import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

DESTINO = os.path.join(RAIZ, "dados", "mapeamentos", "anexo2_contas.json")


def main() -> int:
    import rgf_anexo2_dcl as D

    if not os.path.exists(D.PLANILHA):
        print(f"planilha nao encontrada: {D.PLANILHA}")
        return 2

    secoes = D.ler_base(D.PLANILHA)
    dados = {
        "fonte": os.path.basename(D.PLANILHA),
        "aba": "Anexo 2 - RGF BASE",
        "secoes": [
            {"nome": nome, "contas": [[c, s] for c, s in contas]}
            for nome, contas in secoes.items()
        ],
    }
    # as secoes apuradas na MSC leem contas de OUTRA aba: transcreve tambem
    from openpyxl import load_workbook
    wb = load_workbook(D.PLANILHA, data_only=True)
    abas = {}
    for secao, (aba, _classe, _po) in D.SECOES_MSC.items():
        if aba not in wb.sheetnames:
            continue
        ws = wb[aba]
        contas = []
        for r in range(1, ws.max_row + 1):
            c = ws.cell(r, 1).value
            if isinstance(c, str) and c[:1].isdigit() and c.count(".") >= 6:
                chave = c.replace(".", "")[:9]
                contas.append(D.EQUIVALENTES.get(chave, chave))
        abas[aba] = sorted(set(contas))
    dados["abas"] = abas

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)

    total = sum(len(s["contas"]) for s in dados["secoes"])
    print(f"{len(dados['secoes'])} secoes, {total} contas")
    for s in dados["secoes"]:
        if s["contas"]:
            print(f"   {s['nome'][:58]:<60} {len(s['contas']):>3} contas")
    print(f"\nok -> {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
