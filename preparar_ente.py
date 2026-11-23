# -*- coding: utf-8 -*-
"""Prepara a MSC de um ente para gerar o RREO sem gabarito (rodada 182).

Faz o mesmo que o `preparar_rr.py`, mas parametrizado por ente:

1. baixa da API os meses do exercicio ate o mes anterior ao informado,
   classes 1-8, ending_balance e period_change;
2. converte o arquivo de instancia (`NNEX;AAAA-MM`) do mes informado;
3. baixa nov/dez do ano anterior (janela de 12 meses da RCL);
4. baixa o RREO publicado do ultimo bimestre fechado, para servir de molde.

Uso:
    python preparar_ente.py --ente 27 --ano 2026 --mes 10 \
        --instancia "C:\\...\\MSC_27EX_MENSAL_10_msc_csv.zip" --nome al
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
import urllib.parse
import urllib.request
import zipfile

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"
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

ENTE = 27
ANO = 2026
MES = 10
DESTINO = ""
PUBLICADO = ""


def nome(mes: int, classe: int, tipo: str, ano: int) -> str:
    return (f"MSC_{ENTE}_{ano}_m{mes:02d}_MSCC_msc_{GRUPO[classe]}"
            f"_classe{classe}_{tipo}.csv")


def gravar(pasta: str, ano: int, mes: int, classe: int, tipo: str,
           linhas: list[dict]) -> int:
    if not linhas:
        return 0
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome(mes, classe, tipo, ano))
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=COLUNAS, delimiter=";", extrasaction="ignore")
        esc.writeheader()
        esc.writerows(linhas)
    return len(linhas)


def baixar_api(ano: int, mes: int, classe: int, tipo: str) -> list[dict]:
    linhas, off = [], 0
    while True:
        p = {"an_referencia": ano, "me_referencia": mes, "co_tipo_matriz": "MSCC",
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


def converter(pasta: str, caminho: str) -> int:
    """Instancia (NNEX;AAAA-MM) -> formato antigo, todas as classes e tipos."""
    if caminho.lower().endswith(".zip"):
        with zipfile.ZipFile(caminho) as z:
            alvo = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
            z.extract(alvo, pasta)
            caminho = os.path.join(pasta, alvo)
    por_chave: dict = {}
    with open(caminho, encoding="utf-8", errors="replace", newline="") as fh:
        fh.readline()                       # NNEX;AAAA-MM
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
                        "exercicio": str(ANO), "mes_referencia": f"{MES:02d}",
                        "valor": f"{valor:.2f}", "natureza_conta": c[15].strip().upper()[:1],
                        "tipo_valor": tipo})
            for i in range(6):
                ic, t = c[2 * i + 1].strip(), c[2 * i + 2].strip().upper()
                if ic and t and t in MAPA_ATRIB:
                    reg[MAPA_ATRIB[t]] = ic
            por_chave.setdefault((int(conta[0]), tipo), []).append(reg)
    total = 0
    for (classe, tipo), regs in por_chave.items():
        total += gravar(os.path.join(pasta, str(ANO)), ANO, MES, classe, tipo, regs)
    return total


def baixar_publicado(ano: int, periodo: int, pasta: str) -> int:
    """Baixa o RREO publicado do ente (anexos 1,2,3,4,6,7,14)."""
    base = BASE + "rreo"
    os.makedirs(pasta, exist_ok=True)
    n = 0
    for anexo in (1, 2, 3, 4, 6, 7, 14):
        itens, off = [], 0
        while True:
            p = {"an_exercicio": ano, "nr_periodo": periodo,
                 "co_tipo_demonstrativo": "RREO", "no_anexo": f"RREO-Anexo {anexo:02d}",
                 "co_esfera": "E", "co_poder": "E", "in_periodicidade": "B",
                 "id_ente": ENTE, "limit": 5000, "offset": off}
            try:
                with urllib.request.urlopen(base + "?" + urllib.parse.urlencode(p),
                                            timeout=180) as r:
                    d = json.loads(r.read().decode())
            except Exception as e:
                print(f"   anexo {anexo:02d}: ERRO {str(e)[:40]}")
                break
            it = d.get("items", [])
            itens.extend(it)
            if not d.get("hasMore") or not it:
                break
            off += 5000
        if not itens:
            continue
        dest = os.path.join(pasta, f"RREO_{ENTE}_{ano}_bim{periodo}_anexo{anexo:02d}.csv")
        with open(dest, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(itens[0].keys()),
                               delimiter=";", extrasaction="ignore")
            w.writeheader()
            w.writerows(itens)
        n += len(itens)
        print(f"   anexo {anexo:02d}: {len(itens)} registros")
    return n


def main() -> int:
    global ENTE, ANO, MES, DESTINO, PUBLICADO
    ap = argparse.ArgumentParser(description="Prepara a MSC de um ente")
    ap.add_argument("--ente", type=int, required=True)
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--mes", type=int, required=True)
    ap.add_argument("--instancia", required=True)
    ap.add_argument("--nome", required=True, help="sigla da pasta (ex.: al)")
    args = ap.parse_args()

    ENTE, ANO, MES = args.ente, args.ano, args.mes
    DESTINO = os.path.join(RAIZ, "dados", f"{args.nome}_msc")
    PUBLICADO = os.path.join(RAIZ, "dados", f"{args.nome}_rreo_pub", str(ANO))
    pasta_mes = os.path.join(DESTINO, str(ANO))

    classes = (1, 2, 3, 4, 5, 6, 7, 8)
    feitos = 0
    for mes in range(1, MES):
        for classe in classes:
            for tipo in ("ending_balance", "period_change"):
                if os.path.exists(os.path.join(pasta_mes, nome(mes, classe, tipo, ANO))):
                    continue
                try:
                    linhas = baixar_api(ANO, mes, classe, tipo)
                except Exception as e:
                    print(f"  {mes:02d} c{classe} {tipo}: ERRO {str(e)[:40]}", flush=True)
                    continue
                n = gravar(pasta_mes, ANO, mes, classe, tipo, linhas)
                if n:
                    feitos += 1
    print(f"API {ANO} meses 1-{MES-1}: {feitos} arquivos")

    n_out = converter(DESTINO, args.instancia)
    print(f"instancia {MES:02d}/{ANO} convertida: {n_out} linhas")

    # nov/dez do ano anterior (janela de 12 meses da RCL)
    anterior = ANO - 1
    feitos = 0
    for mes in (11, 12):
        for classe in (5, 6):
            for tipo in ("ending_balance", "period_change"):
                if os.path.exists(os.path.join(DESTINO, str(anterior),
                                               nome(mes, classe, tipo, anterior))):
                    continue
                try:
                    linhas = baixar_api(anterior, mes, classe, tipo)
                except Exception as e:
                    print(f"  {mes:02d}/{anterior} c{classe}: ERRO {str(e)[:40]}")
                    continue
                n = gravar(os.path.join(DESTINO, str(anterior)), anterior,
                           mes, classe, tipo, linhas)
                if n:
                    feitos += 1
    print(f"API {anterior} nov/dez: {feitos} arquivos")

    periodo = MES // 2
    print(f"RREO publicado {ANO} bimestre {periodo}:")
    baixar_publicado(ANO, periodo, PUBLICADO)

    print(f"\nmatriz: {DESTINO}")
    print(f"publicado: {PUBLICADO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
