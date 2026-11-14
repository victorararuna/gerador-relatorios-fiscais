# -*- coding: utf-8 -*-
"""Extrai o benchmark de 2025 do Anexo 1 (rodada 134).

A aba `CONFERÊNCIAS` do `RGF 2025_Q3_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.xlsx`
traz, mes a mes, o quadro SIGEF e o quadro publicado no Siconfi — e os dois batem.

Doze meses somados dao exatamente o publicado no CSV do Siconfi:
  I  = 15.478.621.265,08   III = 11.001.153.864,38

Como o Comparativo da Despesa de 2025 **nao existe** (a pasta so tem os de 2026),
esse benchmark e a unica referencia mensal de 2025. Grava-se aqui para que a
apuracao de 2025 possa ser comparada sem depender de arquivo fora do repositorio.

Uso:
    python extrair_benchmark_2025.py "caminho\\do\\RGF 2025_Q3_01 ....xlsx"
"""
from __future__ import annotations

import json
import os
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_2025.json")
ABA = "CONFERÊNCIAS"
MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

#: rotulo na planilha -> chave
LINHAS = {
    "DESPESA BRUTA COM PESSOAL (I)": "I",
    "Vencimentos, Vantagens e Out": "vencimentos",
    "Obrigações Patronais": "patronal",
    "Aposentadorias, Reserva e Re": "aposentadorias",
    "Pensões": "pensoes",
    "Outras Despesas de Pessoal Dec": "terceirizacao",
    "Despesa com Pessoal não Execut": "nao_executada",
    "DESPESAS NÃO COMPUTADAS (II)": "II",
    "Indenizações por Demissão e Incent": "indenizacoes",
    "Decorrentes de Decisão Judicial de": "judiciais",
    "Inativos e Pensionistas com Recurs": "inativos_vinculados",
    "Agentes Comunitários de Saúde e de": "acs_ace",
    "Parcela dedutível referente ao pis": "enfermagem",
    "DESPESA LÍQUIDA COM PESSOAL (III)": "III",
}


def _bloco(ws, inicio: int) -> dict:
    """Le um bloco (SIGEF ou SICONFI) a partir da linha de titulo das rubricas."""
    saida = {}
    for r in range(inicio, inicio + 30):
        rotulo = ws.cell(r, 1).value
        if not isinstance(rotulo, str):
            continue
        for prefixo, chave in LINHAS.items():
            if rotulo.strip().startswith(prefixo) and chave not in saida:
                valores = [ws.cell(r, c).value for c in range(2, 14)]
                saida[chave] = [v if isinstance(v, (int, float)) else 0.0
                                for v in valores]
                break
    return saida


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python extrair_benchmark_2025.py <arquivo.xlsx>")
        return 2
    wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
    ws = wb[ABA]

    # localiza os dois blocos pelos titulos
    inicio_sigef = inicio_siconfi = None
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if not isinstance(v, str):
            continue
        if v.strip().startswith("QUADRO PARA PUBLICAÇÃO"):
            inicio_sigef = r + 1
        elif v.strip().startswith("QUADRO PUBLICADO NO SICONFI"):
            inicio_siconfi = r + 1

    dados = {
        "fonte": os.path.basename(sys.argv[1]),
        "aba": ABA,
        "meses": list(MESES),
        "sigef": _bloco(ws, inicio_sigef) if inicio_sigef else {},
        "siconfi": _bloco(ws, inicio_siconfi) if inicio_siconfi else {},
    }

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2)

    print(f"blocos: SIGEF na linha {inicio_sigef}, SICONFI na {inicio_siconfi}")
    for bloco in ("sigef", "siconfi"):
        print(f"\n{bloco}:")
        for chave in ("I", "II", "III"):
            if chave in dados[bloco]:
                print(f"   {chave:<4}{sum(dados[bloco][chave]):>20,.2f}")
    print(f"\nok -> {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
