# -*- coding: utf-8 -*-
"""Extrai o MAPA do auditor — 340 linhas x 12 meses (rodada 145).

A aba `Mapeamento` do `RGF 2025_Q3_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.xlsx`
e o **MAPA do auditor**: a memoria de calculo linha a linha, com o valor de cada
mes. E o gabarito completo do Anexo 1 — nao so os totais, mas cada linha.

Estrutura:
    coluna B -> rotulo da linha
    coluna C -> descricao
    colunas D a O -> janeiro a dezembro
    coluna P -> total

Uso:
    python extrair_mapa_auditor.py "caminho\\do\\RGF 2025_Q3_01 ....xlsx"
"""
from __future__ import annotations

import json
import os
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_2025_mapa.json")
ABA = "Mapeamento"
MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python extrair_mapa_auditor.py <arquivo.xlsx>")
        return 2

    wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
    ws = wb[ABA]

    linhas = []
    for r in range(1, ws.max_row + 1):
        rotulo = ws.cell(r, 2).value
        if rotulo is None or not str(rotulo).strip():
            continue
        valores = [ws.cell(r, c).value for c in range(4, 16)]   # D a O
        numeros = [v if isinstance(v, (int, float)) else None for v in valores]
        if not any(v is not None for v in numeros):
            continue
        total = ws.cell(r, 16).value
        linhas.append({
            "linha": r,
            "rotulo": str(rotulo).strip(),
            "descricao": str(ws.cell(r, 3).value or "").strip(),
            "meses": numeros,
            "total": total if isinstance(total, (int, float)) else None,
        })

    dados = {
        "fonte": os.path.basename(sys.argv[1]),
        "aba": ABA,
        "meses": list(MESES),
        "linhas": linhas,
    }
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)

    print(f"{len(linhas)} linhas com valor gravadas")
    for chave in ("DESPESA BRUTA COM PESSOAL", "Vencimentos, Vantagens",
                  "Obrigações Patronais", "Inativos e Pensionistas com Recursos"):
        encontrada = next(
            (x for x in linhas if x["rotulo"].startswith(chave[:28])), None)
        if encontrada:
            soma = sum(v for v in encontrada["meses"] if v is not None)
            print(f"   {encontrada['rotulo'][:52]:<54}{soma:>18,.2f}")
    print(f"\nok -> {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
