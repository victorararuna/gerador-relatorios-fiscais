# -*- coding: utf-8 -*-
"""Testa o RREO em todos os estados (rodada 172).

O RREO inteiro sai da matriz. A linha mais pesada e o **Anexo 2 — Despesa por
Funcao**, que acumula a liquidacao do exercicio. O modulo `rreo_anexo2` le a
classe 6 de **dezembro** (saldo acumulado): uma matriz por estado.

Este script:
1. baixa dezembro/2025, classe 6, ending_balance dos 27 estados;
2. busca o RREO Anexo 2 publicado (2025, 6o bimestre) de cada um;
3. compara funcao por funcao.

Uso:
    python teste_rreo_estados.py
    python teste_rreo_estados.py --ano 2025 --periodo 6
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "teste_rreo")
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"
ESTADOS = {11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
           21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
           28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR",
           42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF"}

COLUNAS = ("tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil",
           "poder_orgao", "ano_fonte_recursos", "fonte_recursos", "funcao",
           "subfuncao", "exercicio", "mes_referencia", "educacao_saude",
           "data_referencia", "entrada_msc", "natureza_despesa",
           "ano_inscricao", "natureza_receita", "valor", "natureza_conta",
           "tipo_valor", "complemento_fonte", "fonte_sigef", "fonte_programa",
           "destinacao")


def baixar_msc(ente: int, ano: int, mes: int) -> list[dict]:
    linhas, offset = [], 0
    while True:
        p = {"an_referencia": ano, "me_referencia": mes, "co_tipo_matriz": "MSCC",
             "id_ente": ente, "classe_conta": 6, "id_tv": "ending_balance",
             "limit": 5000, "offset": offset}
        with urllib.request.urlopen(BASE + "msc_orcamentaria?" +
                                    urllib.parse.urlencode(p), timeout=180) as r:
            d = json.loads(r.read().decode())
        it = d.get("items", [])
        linhas.extend(it)
        if not d.get("hasMore") or not it:
            break
        offset += 5000
        time.sleep(0.2)
    return linhas


def baixar_publicado(ente: int, ano: int, periodo: int) -> dict:
    itens, offset = [], 0
    while True:
        p = {"an_exercicio": ano, "nr_periodo": periodo,
             "co_tipo_demonstrativo": "RREO", "no_anexo": "RREO-Anexo 02",
             "co_esfera": "E", "co_poder": "E", "in_periodicidade": "B",
             "id_ente": ente, "limit": 5000, "offset": offset}
        with urllib.request.urlopen(BASE + "rreo?" +
                                    urllib.parse.urlencode(p), timeout=180) as r:
            d = json.loads(r.read().decode())
        it = d.get("items", [])
        itens.extend(it)
        if not d.get("hasMore") or not it:
            break
        offset += 5000
    # a linha de total e a liquidada ate o bimestre
    return {(x["conta"], x["coluna"]): x["valor"] for x in itens}


def total_liquidado(publicado: dict) -> float | None:
    """Total = bloco exceto intra (I) + bloco intra (II).

    O bloco intra aparece DUPLICADO no arquivo; somar as duas ocorrencias
    dobraria o valor. Usa-se uma vez so.
    """
    exceto = intra = None
    for (conta, coluna), v in publicado.items():
        if "LIQUIDADAS AT" not in coluna.upper():
            continue
        c = conta.upper()
        if "EXCETO INTRA" in c:
            exceto = v
        elif c.startswith("DESPESAS (INTRA") and intra is None:
            intra = v
    if exceto is None:
        return None
    return exceto + (intra or 0.0)


def main() -> int:
    ap = argparse.ArgumentParser(description="Testa o RREO nos 27 estados")
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--periodo", type=int, default=6)
    args = ap.parse_args()

    os.makedirs(DESTINO, exist_ok=True)
    import rreo_anexo2 as A2

    print(f"{'UF':<4}{'funcoes':>9}{'publicado':>20}{'nosso':>20}{'dif %':>9}")
    print("-" * 64)
    ok = total = 0
    for ente, uf in sorted(ESTADOS.items()):
        caminho = os.path.join(DESTINO, f"{uf}_classe6_{args.ano}_{args.periodo}.csv")
        if not os.path.exists(caminho):
            try:
                linhas = baixar_msc(ente, args.ano, 12)
            except Exception as e:
                print(f"{uf:<4}erro no download: {type(e).__name__}")
                continue
            if not linhas:
                print(f"{uf:<4}sem matriz")
                continue
            with open(caminho, "w", encoding="utf-8", newline="") as fh:
                esc = csv.DictWriter(fh, fieldnames=COLUNAS, extrasaction="ignore",
                                     delimiter=";")
                esc.writeheader()
                for item in linhas:
                    esc.writerow(item)

        # nosso: soma por funcao lendo o arquivo baixado
        nosso = {}
        with open(caminho, encoding="utf-8") as fh:
            cab = fh.readline(); fh.seek(0)
            sep = ";" if cab.count(";") > cab.count(",") else ","
            for reg in csv.DictReader(fh, delimiter=sep):
                if reg.get("conta_contabil") not in A2.CONTAS:
                    continue
                f = reg.get("funcao") or ""
                if not f:
                    continue
                nd = reg.get("natureza_conta") or ""
                v = float((reg.get("valor") or "0").replace(",", "."))
                nosso[f] = nosso.get(f, 0.0) + (v if nd == "C" else -v)

        try:
            publicado = baixar_publicado(ente, args.ano, args.periodo)
        except Exception as e:
            print(f"{uf:<4}erro no publicado: {type(e).__name__}")
            continue

        # o publicado tem uma linha por funcao; achamos a de total
        alvo = total_liquidado(publicado)
        soma_nosso = sum(nosso.values())
        if alvo is None:
            print(f"{uf:<4}{len(nosso):>9}{'(sem total)':>20}{soma_nosso:>20}")
            continue
        total += 1
        pct = (soma_nosso - alvo) / alvo * 100 if alvo else 0.0
        marca = " OK" if abs(pct) < 0.01 else ""
        if abs(pct) < 0.01:
            ok += 1
        print(f"{uf:<4}{len(nosso):>9}{alvo:>20,.2f}{soma_nosso:>20,.2f}{pct:>8.2f}%{marca}")
    print("-" * 64)
    print(f"{ok} de {total} estados com o total exato")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
