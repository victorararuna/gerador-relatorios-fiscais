# -*- coding: utf-8 -*-
"""Baixa as matrizes de cinco estados para teste de generalizacao (rodada 166).

O gerador foi construido sobre o Rio Grande do Norte. Este script baixa as
mesmas matrizes de outros cinco entes, sorteados com semente fixa, para
responder a pergunta que importa: **o sistema funciona fora do RN?**

Sorteio (semente 2026): RR (14), MA (21), RN (24), MG (31), PR (41).

Uso:
    python baixar_matrizes_teste.py
    python baixar_matrizes_teste.py --ano 2026 --mes 9
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import time
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "teste_estados")
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"
MATRIZ = "MSCC"
LIMITE = 5000
TIPOS = ("ending_balance", "period_change")

ESTADOS = {11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
           21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
           28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR",
           42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF"}

ENDPOINT = {1: "msc_patrimonial", 2: "msc_patrimonial", 3: "msc_patrimonial",
            4: "msc_patrimonial", 5: "msc_orcamentaria", 6: "msc_orcamentaria",
            7: "msc_controle", 8: "msc_controle"}

COLUNAS = ("tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil",
           "poder_orgao", "ano_fonte_recursos", "fonte_recursos", "funcao",
           "subfuncao", "exercicio", "mes_referencia", "educacao_saude",
           "data_referencia", "entrada_msc", "natureza_despesa",
           "ano_inscricao", "natureza_receita", "valor", "natureza_conta",
           "tipo_valor", "complemento_fonte", "fonte_sigef", "fonte_programa",
           "destinacao")


def baixar(ente: int, ano: int, mes: int, classe: int, tipo: str) -> list[dict]:
    linhas: list[dict] = []
    offset = 0
    while True:
        params = urllib.parse.urlencode({
            "an_referencia": ano, "me_referencia": mes,
            "co_tipo_matriz": MATRIZ, "id_ente": ente,
            "classe_conta": classe, "id_tv": tipo,
            "limit": LIMITE, "offset": offset,
        })
        url = BASE + ENDPOINT[classe] + "?" + params
        with urllib.request.urlopen(url, timeout=180) as r:
            dados = json.loads(r.read().decode("utf-8"))
        itens = dados.get("items", [])
        linhas.extend(itens)
        if not dados.get("hasMore") or not itens:
            break
        offset += LIMITE
        time.sleep(0.2)
    return linhas


def main() -> int:
    ap = argparse.ArgumentParser(description="Baixa matrizes de teste")
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--mes", type=int, default=9)
    ap.add_argument("--semente", type=int, default=2026)
    args = ap.parse_args()

    random.seed(args.semente)
    escolhidos = random.sample(sorted(ESTADOS), 5)
    print("estados sorteados:", ", ".join(f"{ESTADOS[e]} ({e})" for e in escolhidos))

    falhas = 0
    for ente in escolhidos:
        uf = ESTADOS[ente]
        pasta = os.path.join(DESTINO, uf)
        os.makedirs(pasta, exist_ok=True)
        print(f"\n--- {uf} ({ente})")
        for classe in range(1, 9):
            for tipo in TIPOS:
                try:
                    linhas = baixar(ente, args.ano, args.mes, classe, tipo)
                except Exception as e:
                    falhas += 1
                    print(f"   classe{classe} {tipo}: ERRO {type(e).__name__} {str(e)[:50]}")
                    continue
                if not linhas:
                    continue
                caminho = os.path.join(
                    pasta, f"{uf}_{args.ano}_{args.mes:02d}_classe{classe}_{tipo}.csv")
                with open(caminho, "w", encoding="utf-8", newline="") as fh:
                    esc = csv.DictWriter(fh, fieldnames=COLUNAS, extrasaction="ignore")
                    esc.writeheader()
                    for item in linhas:
                        esc.writerow(item)
                print(f"   classe{classe} {tipo:<14} {len(linhas):>6} linhas")
    print(f"\nfalhas: {falhas}")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
