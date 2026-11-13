# -*- coding: utf-8 -*-
"""Publica o projeto no GitHub pela API.

Uso:

    python subir.py --token ghp_xxx
    python subir.py --token ghp_xxx --repo gerador-relatorios-fiscais

O script:
1. cria o repositório (se não existir);
2. envia todos os arquivos de código e documentação;
3. aplica descrição e topics.

Ficam de fora: dados/, saida/, MDF_STN/, _repo_novo/, __pycache__/, .xlsx e .zip.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

RAIZ = os.path.dirname(os.path.abspath(__file__))

EXCLUIR_DIR = ("dados", "saida", "MDF_STN", "_repo_novo", "__pycache__", ".git")
EXCLUIR_EXT = (".pyc", ".zip", ".7z", ".log", ".xlsx", ".xls")
EXCLUIR_PREFIXO = ("~$", "_tmp")


def listar() -> list:
    saida = []
    for raiz, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in EXCLUIR_DIR]
        for a in arqs:
            if a.endswith(EXCLUIR_EXT) or a.startswith(EXCLUIR_PREFIXO):
                continue
            full = os.path.join(raiz, a)
            rel = os.path.relpath(full, RAIZ).replace("\\", "/")
            saida.append((rel, full))
    return sorted(saida)


class GH:
    def __init__(self, token: str):
        self.token = token
        self.base = "https://api.github.com"

    def api(self, url: str, method: str = "GET", data=None):
        req = urllib.request.Request(
            url, method=method,
            headers={"Authorization": f"token {self.token}",
                     "Accept": "application/vnd.github+json",
                     "User-Agent": "rn-fiscal",
                     "Content-Type": "application/json"})
        body = json.dumps(data).encode() if data else None
        try:
            with urllib.request.urlopen(req, data=body, timeout=90, context=CTX) as z:
                return z.status, json.loads(z.read() or "{}")
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", required=True)
    ap.add_argument("--repo", default="gerador-relatorios-fiscais")
    ap.add_argument("--usuario", default="victorararuna")
    a = ap.parse_args()

    gh = GH(a.token)
    st, u = gh.api(f"{gh.base}/user")
    if st != 200:
        print(f"token inválido ({st})")
        return 1
    usuario = u.get("login", a.usuario)
    print(f"autenticado como: {usuario}")

    # repo
    st, r = gh.api(f"{gh.base}/repos/{usuario}/{a.repo}")
    if st == 200:
        print(f"repositório existe: {r['html_url']}")
    else:
        st, r = gh.api(f"{gh.base}/user/repos", "POST", {
            "name": a.repo,
            "description": "Motor de demonstrativos fiscais (RREO e RGF) sobre a "
                           "Matriz de Saldos Contábeis do Siconfi",
            "private": False,
            "has_issues": True, "has_wiki": False, "auto_init": False,
        })
        if st not in (200, 201):
            print(f"erro ao criar o repositório: {st} {r.get('message')}")
            return 1
        print(f"repositório criado: {r['html_url']}")

    arquivos = listar()
    print(f"arquivos a enviar: {len(arquivos)}")
    ok = falha = 0
    for i, (rel, full) in enumerate(arquivos, 1):
        try:
            conteudo = open(full, "rb").read()
        except OSError as e:
            print(f"   [skip] {rel}: {e}")
            continue
        # se o arquivo ja existe, a API exige o sha para atualizar
        sha = None
        st_get, info = gh.api(f"{gh.base}/repos/{usuario}/{a.repo}/contents/{rel}")
        if st_get == 200 and isinstance(info, dict):
            sha = info.get("sha")
        corpo = {"message": f"Atualiza {rel}",
                 "content": base64.b64encode(conteudo).decode()}
        if sha:
            corpo["sha"] = sha
        st, r = gh.api(f"{gh.base}/repos/{usuario}/{a.repo}/contents/{rel}", "PUT", corpo)
        if st in (200, 201):
            ok += 1
        else:
            falha += 1
            print(f"   [erro] {rel}: {st} {r.get('message')}")
        if i % 25 == 0:
            print(f"   {i}/{len(arquivos)} ...")
        time.sleep(0.2)

    # descrição e topics
    gh.api(f"{gh.base}/repos/{usuario}/{a.repo}", "PATCH", {
        "description": "Motor de demonstrativos fiscais (RREO e RGF) sobre a "
                       "Matriz de Saldos Contábeis do Siconfi — MDF 15ª edição",
    })
    gh.api(f"{gh.base}/repos/{usuario}/{a.repo}/topics", "PUT", {
        "names": ["contabilidade-publica", "siconfi", "rgf", "rreo", "lrf",
                  "mdf", "tesouro-nacional", "python", "msc"],
    })

    print()
    print(f"enviados: {ok} | falhas: {falha}")
    print(f"repositório: https://github.com/{usuario}/{a.repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
