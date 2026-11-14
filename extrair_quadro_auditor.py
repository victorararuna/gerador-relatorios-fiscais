# -*- coding: utf-8 -*-
"""Extrai a aba QUADRO do auditor — a fonte estruturada de 2025 (rodada 152).

O `Mapeamento` e a memoria de calculo, mas tem linhas de total que nao sao a soma
das parcelas (a II soma 4,86 bi contra 4,48 publicados). A aba **`Quadro`** e o
demonstrativo pronto, com uma linha por item e o valor de cada mes — e os tres
totais fecham ao centavo contra o publicado.

Uso:
    python extrair_quadro_auditor.py "caminho\\do\\RGF 2025_Q3_01 ....xlsx"
"""
from __future__ import annotations

import json
import os
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_2025_quadro.json")
ABA = "Quadro"
MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

#: linha do quadro -> chave
LINHAS = {
    17: "I",
    18: "ativo",
    19: "vencimentos",
    20: "patronal",
    21: "inativo",
    22: "aposentadorias",
    23: "pensoes",
    24: "terceirizacao",
    25: "nao_executada",
    26: "II",
    27: "indenizacoes",
    28: "judiciais",
    30: "inativos_vinculados",
    31: "acs_ace",
    32: "enfermagem",
    34: "III",
}


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python extrair_quadro_auditor.py <arquivo.xlsx>")
        return 2

    wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
    ws = wb[ABA]

    dados = {"fonte": os.path.basename(sys.argv[1]), "aba": ABA,
             "meses": list(MESES), "linhas": {}}
    for linha, chave in LINHAS.items():
        rotulo = ws.cell(linha, 1).value
        valores = [ws.cell(linha, c).value for c in range(2, 14)]
        dados["linhas"][chave] = {
            "rotulo": str(rotulo or "").strip(),
            "meses": [v if isinstance(v, (int, float)) else None for v in valores],
        }

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)

    print(f"{len(dados['linhas'])} linhas do QUADRO gravadas")
    for chave in ("I", "II", "III"):
        total = sum(v for v in dados["linhas"][chave]["meses"] if v is not None)
        print(f"   {chave:<4}{total:>20,.2f}")
    print(f"\nok -> {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
