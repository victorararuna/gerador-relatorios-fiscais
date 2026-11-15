# -*- coding: utf-8 -*-
"""Baixa as matrizes MSC do Siconfi para o acervo (rodada 158).

Os ultimos doze meses disponiveis vao de outubro/2025 a setembro/2026 — o
Siconfi publica com defasagem e outubro/2026 ainda nao saiu.

O acervo ja tinha 2025 inteiro e 2026 de janeiro a junho. Faltavam julho,
agosto e setembro de 2026 — e sao exatamente os meses que o Anexo 1 do 2o
quadrimestre usa.

Endpoints (conforme a documentacao da API):
    classes 1 a 4 -> msc_patrimonial
    classes 5 e 6 -> msc_orcamentaria
    classes 7 e 8 -> msc_controle

Uso:
    python baixar_msc.py                # so os meses faltando
    python baixar_msc.py --tudo         # os doze meses
    python baixar_msc.py --meses 2026-07,2026-08,2026-09
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
ACERVO = os.path.join(RAIZ, "dados", "acervo")
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"
ENTE = 24                      # IBGE do Rio Grande do Norte
MATRIZ = "MSCC"
LIMITE = 5000
TIPOS = ("ending_balance", "period_change")

#: classe -> endpoint
ENDPOINT = {1: "msc_patrimonial", 2: "msc_patrimonial",
            3: "msc_patrimonial", 4: "msc_patrimonial",
            5: "msc_orcamentaria", 6: "msc_orcamentaria",
            7: "msc_controle", 8: "msc_controle"}

#: ordem das colunas no CSV do acervo
COLUNAS = ("tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil",
           "poder_orgao", "ano_fonte_recursos", "fonte_recursos", "funcao",
           "subfuncao", "exercicio", "mes_referencia", "educacao_saude",
           "data_referencia", "entrada_msc", "natureza_despesa",
           "ano_inscricao", "natureza_receita", "valor", "natureza_conta",
           "tipo_valor", "complemento_fonte", "fonte_sigef", "fonte_programa",
           "destinacao")


def ultimos_doze(hoje: tuple[int, int]) -> list[tuple[int, int]]:
    """Os doze meses ate `hoje`, do mais antigo para o mais novo."""
    ano, mes = hoje
    meses = []
    for _ in range(12):
        meses.append((ano, mes))
        mes -= 1
        if mes == 0:
            ano, mes = ano - 1, 12
    return list(reversed(meses))


def baixar(ano: int, mes: int, classe: int, tipo: str) -> list[dict]:
    """Todas as linhas de uma classe/tipo, paginando."""
    endpoint = ENDPOINT[classe]
    linhas: list[dict] = []
    offset = 0
    while True:
        params = urllib.parse.urlencode({
            "an_referencia": ano, "me_referencia": mes,
            "co_tipo_matriz": MATRIZ, "id_ente": ENTE,
            "classe_conta": classe, "id_tv": tipo,
            "limit": LIMITE, "offset": offset,
        })
        with urllib.request.urlopen(BASE + endpoint + "?" + params, timeout=120) as r:
            dados = json.loads(r.read().decode("utf-8"))
        itens = dados.get("items", [])
        linhas.extend(itens)
        if not dados.get("hasMore") or not itens:
            break
        offset += LIMITE
        time.sleep(0.3)
    return linhas


def gravar(ano: int, mes: int, classe: int, tipo: str, linhas: list[dict]) -> str:
    pasta = os.path.join(ACERVO, str(ano))
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, f"RN_{ano}_{mes:02d}_classe{classe}_{tipo}.csv")
    with open(destino, "w", encoding="utf-8", newline="") as fh:
        escritor = csv.DictWriter(fh, fieldnames=COLUNAS, extrasaction="ignore")
        escritor.writeheader()
        for item in linhas:
            escritor.writerow(item)
    return destino


def completo(ano: int, mes: int) -> bool:
    for classe in range(1, 9):
        for tipo in TIPOS:
            caminho = os.path.join(ACERVO, str(ano),
                                   f"RN_{ano}_{mes:02d}_classe{classe}_{tipo}.csv")
            if not os.path.exists(caminho) or os.path.getsize(caminho) < 200:
                return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Baixa as MSC do Siconfi")
    ap.add_argument("--tudo", action="store_true", help="os doze meses")
    ap.add_argument("--meses", help="lista AAAA-MM separada por virgula")
    ap.add_argument("--hoje", default="2026-09", help="ultimo mes publicado")
    args = ap.parse_args()

    if args.meses:
        alvo = []
        for parte in args.meses.split(","):
            ano, mes = parte.strip().split("-")
            alvo.append((int(ano), int(mes)))
    else:
        ano, mes = args.hoje.split("-")
        alvo = ultimos_doze((int(ano), int(mes)))
        if not args.tudo:
            alvo = [m for m in alvo if not completo(*m)]

    if not alvo:
        print("nada a baixar: os doze meses ja estao completos")
        return 0

    print(f"{len(alvo)} mes(es) a baixar: "
          + ", ".join(f"{a}-{m:02d}" for a, m in alvo))
    falhas = 0
    for ano, mes in alvo:
        for classe in range(1, 9):
            for tipo in TIPOS:
                try:
                    linhas = baixar(ano, mes, classe, tipo)
                except Exception as e:
                    falhas += 1
                    print(f"  {ano}-{mes:02d} classe{classe} {tipo}: {type(e).__name__} {e}")
                    continue
                caminho = gravar(ano, mes, classe, tipo, linhas)
                print(f"  {ano}-{mes:02d} classe{classe} {tipo:<14} {len(linhas):>6} linhas"
                      f" -> {os.path.basename(caminho)}")
    print(f"\nfalhas: {falhas}")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
