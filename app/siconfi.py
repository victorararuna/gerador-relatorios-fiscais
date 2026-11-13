# -*- coding: utf-8 -*-
"""Coleta de dados do Siconfi.

O Siconfi expõe três caminhos distintos, e cada um serve a um propósito:

1. **API de dados abertos** (`apidatalake.tesouro.gov.br/ords/siconfi/tt`)
   funciona para o cadastro de entes; os endpoints de RGF e RREO responderam
   vazios nas tentativas de 2026-11.

2. **Arquivos de declaração** (`.xls`) — RGF e RREO — são baixados da área
   pública de consulta.

3. **Matriz de Saldos Contábeis** — não há URL estável de download em massa. O
   Siconfi entrega por consulta interativa, um arquivo por classe, mês e tipo de
   saldo. Quando o acervo já existe em disco, `Acervo` o indexa direto.

Este módulo:
- baixa o cadastro de entes (funciona);
- tenta os endpoints de declaração e informa o que respondeu;
- **normaliza um acervo local** no padrão que o `acervo.Acervo` espera;
- monta um plano de coleta com o que falta.

Uso:

    python siconfi.py --entes
    python siconfi.py --acervo "D:\\...\\MSC_RN_2021_2026_06" --destino dados/acervo
    python siconfi.py --diagnostico
"""
from __future__ import annotations

import json
import os
import re
import shutil
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
      "Accept": "application/json"}

API = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
CONSULTA = "https://siconfi.tesouro.gov.br/siconfi/pages/public"

COD_IBGE_RN = 24


def _get_json(url: str, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as z:
        return json.loads(z.read())


def _status(url: str, timeout: int = 45) -> str:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as z:
            return f"{z.status} ({z.headers.get('Content-Type', '')[:40]})"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {str(e)[:50]}"


# ---------------------------------------------------------------------------
# 1. Entes
# ---------------------------------------------------------------------------
def baixar_entes() -> List[dict]:
    """Cadastro de entes da federação (funciona)."""
    todos: List[dict] = []
    offset = 0
    while True:
        d = _get_json(f"{API}/entes?offset={offset}")
        itens = d.get("items", [])
        todos.extend(itens)
        if not d.get("hasMore") or not itens:
            break
        offset += len(itens)
    return todos


def ente_rn() -> Optional[dict]:
    for e in baixar_entes():
        if int(e.get("cod_ibge", 0)) == COD_IBGE_RN:
            return e
    return None


# ---------------------------------------------------------------------------
# 2. Diagnóstico dos endpoints
# ---------------------------------------------------------------------------
def diagnostico() -> Dict[str, str]:
    """Estado atual de cada caminho de coleta."""
    alvos = {
        "entes": f"{API}/entes?limit=1",
        "rgf": f"{API}/rgf?an_exercicio=2024&nr_periodo=3&id_ente=24",
        "rreo": f"{API}/rreo?an_exercicio=2024&nr_periodo=6&id_ente=24",
        "msc": f"{API}/msc?an_exercicio=2024&nr_periodo=12",
        "consulta_rgf": f"{CONSULTA}/consulta_rgf_filtro.jsf",
        "consulta_rreo": f"{CONSULTA}/consulta_rreo_filtro.jsf",
        "consulta_msc": f"{CONSULTA}/consulta_matriz_filtro.jsf",
    }
    return {k: _status(u) for k, u in alvos.items()}


# ---------------------------------------------------------------------------
# 3. Normalização de acervo local
# ---------------------------------------------------------------------------
#: aceita RN_2024_12_classe6_period_change.csv e o padrão oficial
_RE_RN = re.compile(r"^\w+_(\d{4})_(\d{2})_classe(\d)_(ending_balance|period_change)\.csv$",
                    re.I)
_RE_MSC = re.compile(
    r"^MSC_(\d+)_(\d{4})_m(\d{2})_(MSCC|MSCE)_msc_"
    r"(orcamentaria|patrimonial|controle)_classe(\d)_"
    r"(ending_balance|period_change)\.csv$", re.I)


def classificar_nome(nome: str) -> Optional[str]:
    """Devolve o nome normalizado ``RN_<ano>_<mm>_classe<n>_<tipo>.csv``."""
    m = _RE_RN.match(nome)
    if m:
        return f"RN_{m.group(1)}_{m.group(2)}_classe{m.group(3)}_{m.group(4).lower()}.csv"
    m = _RE_MSC.match(nome)
    if m:
        return (f"RN_{m.group(2)}_{m.group(3)}_classe{m.group(6)}_"
                f"{m.group(7).lower()}.csv")
    return None


def normalizar(origem: str, destino: str, copiar: bool = False) -> Dict[str, int]:
    """Organiza um acervo no padrão esperado por ``acervo.Acervo``.

    Percorre a origem recursivamente, renomeia cada CSV reconhecido e grava em
    ``destino/<ano>/``. Não sobrescreve: se o destino já tem o arquivo, conta
    como existente.
    """
    os.makedirs(destino, exist_ok=True)
    contagem = {"novos": 0, "existentes": 0, "ignorados": 0}
    for raiz, _, arquivos in os.walk(origem):
        for nome in arquivos:
            if not nome.lower().endswith(".csv"):
                continue
            novo = classificar_nome(nome)
            if not novo:
                contagem["ignorados"] += 1
                continue
            ano = novo.split("_")[1]
            pasta = os.path.join(destino, ano)
            os.makedirs(pasta, exist_ok=True)
            alvo = os.path.join(pasta, novo)
            if os.path.exists(alvo):
                contagem["existentes"] += 1
                continue
            origem_arq = os.path.join(raiz, nome)
            if copiar:
                shutil.copyfile(origem_arq, alvo)
            else:
                try:
                    os.link(origem_arq, alvo)
                except OSError:
                    shutil.copyfile(origem_arq, alvo)
            contagem["novos"] += 1
    return contagem


# ---------------------------------------------------------------------------
# 4. Plano de coleta
# ---------------------------------------------------------------------------
PENDENTES = [
    ("MSC — Matriz de Saldos Contábeis",
     "consulta interativa do Siconfi (um arquivo por classe/mês/saldo); "
     "não há URL estável de download em massa",
     "acervo local normalizado com --acervo"),
    ("RGF — declaração (.xls)",
     "área pública de consulta do Siconfi",
     "download manual em Consulta > RGF > Exportar"),
    ("RREO — declaração (.xls)",
     "área pública de consulta do Siconfi",
     "download manual em Consulta > RREO > Exportar"),
    ("Comparativo da Receita",
     "SIAFEM/RN — não é publicado no Siconfi",
     "arquivo do sistema estadual"),
]


def plano() -> str:
    linhas = ["PENDÊNCIAS DE COLETA", ""]
    for nome, onde, como in PENDENTES:
        linhas.append(f"- {nome}")
        linhas.append(f"    origem: {onde}")
        linhas.append(f"    solução: {como}")
        linhas.append("")
    return "\n".join(linhas)


def _cli() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Coleta de dados do Siconfi.")
    ap.add_argument("--entes", action="store_true", help="baixa o cadastro de entes")
    ap.add_argument("--acervo", help="pasta de origem de um acervo MSC local")
    ap.add_argument("--destino", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "acervo"))
    ap.add_argument("--copiar", action="store_true", help="copia em vez de criar link")
    ap.add_argument("--diagnostico", action="store_true", help="testa os endpoints")
    ap.add_argument("--plano", action="store_true", help="mostra o plano de coleta")
    args = ap.parse_args()

    if args.entes:
        e = ente_rn()
        print("ente RN:", e)
    if args.acervo:
        r = normalizar(args.acervo, args.destino, copiar=args.copiar)
        print(f"acervo normalizado em {args.destino}")
        print(f"   novos: {r['novos']} | existentes: {r['existentes']} | "
              f"ignorados: {r['ignorados']}")
    if args.diagnostico:
        print("DIAGNÓSTICO DOS ENDPOINTS")
        for k, v in diagnostico().items():
            print(f"   {k:16} {v}")
    if args.plano:
        print(plano())
    if not any((args.entes, args.acervo, args.diagnostico, args.plano)):
        ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
