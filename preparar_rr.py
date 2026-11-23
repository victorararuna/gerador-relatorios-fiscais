# -*- coding: utf-8 -*-
"""Prepara a MSC de Roraima para gerar o RREO sem gabarito (rodada 174).

O usuario forneceu outubro/2026 no formato de instancia (`14EX;2026-10`). A API
do Siconfi tem RR de janeiro a setembro/2026. Este script:

1. baixa RR 2026 meses 1-9, classes 1-8, ending_balance e period_change;
2. converte o arquivo de outubro (instancia -> longo);
3. grava tudo no formato antigo `MSC_14_2026_mNN_MSCC_msc_<grupo>_classe<n>_<tipo>`
   em `dados/rr_msc/2026`, que o `app/leitor_msc.py` le.

Uso:
    python preparar_rr.py --outubro "C:\\...\\MSC14EX202610.csv"
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "rr_msc", "2026")
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"
ENTE = 14
GRUPO = {1: "patrimonial", 2: "patrimonial", 3: "patrimonial", 4: "patrimonial",
         5: "orcamentaria", 6: "orcamentaria", 7: "controle", 8: "controle"}
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
MAPA_ATRIB = {"PO": "poder_orgao", "FR": "fonte_recursos", "CO": "complemento_fonte",
              "ND": "natureza_despesa", "NR": "natureza_receita", "AI": "ano_inscricao",
              "FS": "fonte_sigef", "FP": "ano_fonte_recursos", "DC": "destinacao"}


def nome_antigo(mes: int, classe: int, tipo: str) -> str:
    return (f"MSC_{ENTE}_2026_m{mes:02d}_MSCC_msc_{GRUPO[classe]}"
            f"_classe{classe}_{tipo}.csv")


def gravar(mes: int, classe: int, tipo: str, linhas: list[dict]) -> int:
    if not linhas:
        return 0
    os.makedirs(DESTINO, exist_ok=True)
    caminho = os.path.join(DESTINO, nome_antigo(mes, classe, tipo))
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=COLUNAS, delimiter=";", extrasaction="ignore")
        esc.writeheader()
        esc.writerows(linhas)
    return len(linhas)


def baixar_api(mes: int, classe: int, tipo: str) -> list[dict]:
    linhas, off = [], 0
    while True:
        p = {"an_referencia": 2026, "me_referencia": mes, "co_tipo_matriz": "MSCC",
             "id_ente": ENTE, "classe_conta": classe, "id_tv": tipo,
             "limit": 5000, "offset": off}
        url = BASE + ENDPOINT[classe] + "?" + urllib.parse.urlencode(p)
        with urllib.request.urlopen(url, timeout=180) as r:
            d = json.loads(r.read().decode())
        it = d.get("items", [])
        linhas.extend(it)
        if not d.get("hasMore") or not it:
            break
        off += 5000
        time.sleep(0.15)
    return linhas


def converter_outubro(caminho: str) -> int:
    """Instancia (14EX) -> formato antigo, todas as classes e tipos."""
    por_chave: dict = {}
    with open(caminho, encoding="utf-8", errors="replace", newline="") as fh:
        fh.readline()                       # 14EX;2026-10
        rd = csv.reader(fh, delimiter=";")
        next(rd)                            # cabecalho
        for c in rd:
            if len(c) != 16:
                continue
            conta = c[0].strip()
            if not conta:
                continue
            try:
                valor = float(c[13].replace(",", "."))
            except ValueError:
                continue
            tipo = c[14].strip().lower()
            if tipo not in ("ending_balance", "period_change"):
                continue
            reg = {k: "" for k in COLUNAS}
            reg.update({"tipo_matriz": "MSCC", "cod_ibge": str(ENTE),
                        "classe_conta": conta[0], "conta_contabil": conta,
                        "exercicio": "2026", "mes_referencia": "10",
                        "valor": f"{valor:.2f}", "natureza_conta": c[15].strip().upper()[:1],
                        "tipo_valor": tipo})
            for i in range(6):
                ic, t = c[2 * i + 1].strip(), c[2 * i + 2].strip().upper()
                if ic and t and t in MAPA_ATRIB:
                    reg[MAPA_ATRIB[t]] = ic
            por_chave.setdefault((int(conta[0]), tipo), []).append(reg)
    total = 0
    for (classe, tipo), regs in por_chave.items():
        total += gravar(10, classe, tipo, regs)
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepara a MSC de RR")
    ap.add_argument("--outubro", required=True)
    ap.add_argument("--classes", default="1,2,3,4,5,6,7,8")
    args = ap.parse_args()

    classes = [int(x) for x in args.classes.split(",")]
    feitos = 0
    for mes in range(1, 10):
        for classe in classes:
            for tipo in ("ending_balance", "period_change"):
                destino = os.path.join(DESTINO, nome_antigo(mes, classe, tipo))
                if os.path.exists(destino) and os.path.getsize(destino) > 200:
                    continue
                try:
                    linhas = baixar_api(mes, classe, tipo)
                except Exception as e:
                    print(f"  {mes:02d} c{classe} {tipo}: ERRO {str(e)[:50]}", flush=True)
                    continue
                n = gravar(mes, classe, tipo, linhas)
                if n:
                    feitos += 1
                    print(f"  {mes:02d} c{classe} {tipo:<14} {n:>6}", flush=True)
    n_out = converter_outubro(args.outubro)
    print(f"\nAPI: {feitos} arquivos | outubro convertido: {n_out} linhas")
    print(f"destino: {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
