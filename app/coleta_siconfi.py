#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coleta das declarações do Siconfi pela API de dados abertos.

Adaptado do extrator multiente `siconfi_brasil_completo.py` para o recorte deste
projeto: os demonstrativos do Rio Grande do Norte, RGF e RREO, de 2024 em diante.

A API exige o conjunto completo de parâmetros — foi o que faltava nas primeiras
tentativas, que retornavam zero:

    id_ente, an_exercicio, nr_periodo, in_periodicidade,
    co_tipo_demonstrativo, no_anexo, co_esfera, co_poder

Resposta: uma linha por (conta, coluna), com ``rotulo``, ``coluna``, ``conta`` e
``valor``. É a mesma estrutura do arquivo `.xls` de declaração, em formato longo.

Uso:

    python coleta_siconfi.py --ano 2025 --what rgf rreo
    python coleta_siconfi.py --ano 2025 --anexo "RGF-Anexo 01" --periodo 3
    python coleta_siconfi.py --diagnostico
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/"

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

UA = {"Accept": "application/json",
      "User-Agent": "gerador-relatorios-fiscais/1.0"}

LOG = logging.getLogger("coleta")

#: Rio Grande do Norte
ENTE_RN = 24
ESFERA_ESTADO = "E"

RGF_ANEXOS = [f"RGF-Anexo {i:02d}" for i in range(1, 7)]
RREO_ANEXOS = [f"RREO-Anexo {i:02d}" for i in (1, 2, 3, 4, 6, 7, 9, 10, 11, 13, 14)]


def _get(endpoint: str, params: Dict, timeout: int = 120) -> dict:
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as z:
        return json.loads(z.read())


def coletar(endpoint: str, params: Dict, timeout: int = 120,
            pausa: float = 0.3, tentativas: int = 3) -> List[dict]:
    """Coleta com paginação manual (a API devolve no máximo 5000 por página)."""
    linhas: List[dict] = []
    offset = 0
    while True:
        p = dict(params, offset=offset)
        for tentativa in range(tentativas):
            try:
                d = _get(endpoint, p, timeout)
                break
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if tentativa == tentativas - 1:
                    raise
                time.sleep(1.5 * (tentativa + 1))
        itens = d.get("items") or []
        linhas.extend(itens)
        if len(itens) < 5000:
            break
        offset += 5000
        time.sleep(pausa)
    return linhas


def params_anexo(anexo: str, ano: int, periodo: int, tipo: str,
                 ente: int = ENTE_RN, esfera: str = ESFERA_ESTADO,
                 poder: str = "E") -> Dict:
    return {
        "id_ente": ente,
        "an_exercicio": ano,
        "nr_periodo": periodo,
        "in_periodicidade": "Q" if tipo.upper() == "RGF" else "B",
        "co_tipo_demonstrativo": tipo.upper(),
        "no_anexo": anexo,
        "co_esfera": esfera,
        "co_poder": poder,
    }


def baixar_anexo(anexo: str, ano: int, periodo: int, tipo: str,
                 destino: Path, ente: int = ENTE_RN,
                 esfera: str = ESFERA_ESTADO, poder: str = "E",
                 sobrescrever: bool = False) -> Optional[Path]:
    """Baixa um anexo e grava em CSV. Devolve o caminho ou None."""
    nome = f"{tipo.upper()}_{anexo.replace(' ', '_')}_{ente}_{ano}_p{periodo}.csv"
    alvo = destino / tipo.lower() / nome
    if alvo.exists() and not sobrescrever:
        return alvo
    linha = coletar(tipo.lower(), params_anexo(anexo, ano, periodo, tipo,
                                               ente, esfera, poder))
    if not linha:
        return None
    alvo.parent.mkdir(parents=True, exist_ok=True)
    campos = list(dict.fromkeys(k for ln in linha for k in ln))
    with alvo.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(linha)
    LOG.info("   %-24s %5d linhas -> %s", anexo, len(linha), alvo.name)
    return alvo


def diagnostico() -> Dict[str, int]:
    """Quantas linhas cada anexo devolve para o RN."""
    saida: Dict[str, int] = {}
    for tipo, anexos, periodo in (("RGF", RGF_ANEXOS, 3), ("RREO", RREO_ANEXOS, 6)):
        for a in anexos:
            try:
                d = _get(tipo.lower(), params_anexo(a, 2024, periodo, tipo))
                saida[a] = d.get("count", 0)
            except Exception as e:  # noqa: BLE001
                saida[a] = -1
    return saida


def _cli() -> int:
    ap = argparse.ArgumentParser(description="Coleta RGF/RREO do Siconfi.")
    ap.add_argument("--anos", nargs="+", type=int, default=[2024, 2025])
    ap.add_argument("--ente", type=int, default=ENTE_RN)
    ap.add_argument("--esfera", default=ESFERA_ESTADO)
    ap.add_argument("--poder", default="E")
    ap.add_argument("--what", nargs="+", default=["rgf", "rreo"],
                    choices=("rgf", "rreo"))
    ap.add_argument("--periodo", type=int, help="período único (quadrimestre RGF ou bimestre RREO)")
    ap.add_argument("--anexo", help="anexo único, ex.: RGF-Anexo 01")
    ap.add_argument("--saida", default=str(Path(__file__).resolve().parent.parent / "dados" / "siconfi"))
    ap.add_argument("--sobrescrever", action="store_true")
    ap.add_argument("--diagnostico", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.diagnostico:
        for k, v in diagnostico().items():
            print(f"   {k:22} {v:>6} linhas")
        return 0

    destino = Path(args.saida)
    destino.mkdir(parents=True, exist_ok=True)

    for ano in args.anos:
        for tipo in args.what:
            periodos = [args.periodo] if args.periodo else (
                [1, 2, 3] if tipo == "rgf" else [1, 2, 3, 4, 5, 6])
            anexos = [args.anexo] if args.anexo else (
                RGF_ANEXOS if tipo == "rgf" else RREO_ANEXOS)
            LOG.info("=== %s %d ===", tipo.upper(), ano)
            for periodo in periodos:
                for anexo in anexos:
                    try:
                        baixar_anexo(anexo, ano, periodo, tipo, destino,
                                     args.ente, args.esfera, args.poder,
                                     args.sobrescrever)
                    except Exception as e:  # noqa: BLE001
                        LOG.warning("   %-24s ERRO %s", anexo, str(e)[:70])
                    time.sleep(0.3)
    LOG.info("concluído: %s", destino)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
