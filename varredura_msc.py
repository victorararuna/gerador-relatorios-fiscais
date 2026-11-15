# -*- coding: utf-8 -*-
"""Varredura: o que da para gerar so com a MSC (rodada 161).

Percorre os modulos do gerador e classifica cada um pela FONTE DE GERACAO —
nao pela fonte de conferencia. O CSV publicado do Siconfi e referencia de teste;
a pergunta aqui e o que o motor precisa para produzir o numero.

Categorias:
    MSC          so a matriz de saldos contabeis
    MSC+SICONFI  a matriz mais algum anexo publicado (para parametros)
    PDF          precisa dos PDFs do SIGEF (Comparativo / IEO / balancete)
    PLANILHA     precisa das planilhas da equipe (RELATORIOS CONTAG)
    MANUAL       precisa de valor digitado a mao
"""
from __future__ import annotations

import ast
import os
import sys

RAIZ = r"C:\Users\victo\OneDrive\Documents\deepseek-harness\default-workspace\repo-github"
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

#: o que cada modulo le
SINAIS = {
    "PDF": ("ler_comparativo", "ler_pdf", "expurgo_poderes", "expurgo_ieo",
            "leitor_pdf", "Comparativo", "Imprimir"),
    "PLANILHA": ("ler_base", "PLANILHA", "openpyxl", "RELATÓRIOS CONTAG",
                 "RELATORIOS CONTAG"),
    "MANUAL": ("CONTROLE_RP", "DIFERENCA_EMPENHADO"),
    "SICONFI": ("RGF_RGF-Anexo", "RREO_RREO-Anexo", "siconfi"),
    "MSC": ("acervo", "Acervo", "classe=6", "classe=8", "classe=2"),
}

MODULOS = [
    "mapa_anexo1", "nao_executada", "expurgo_poderes", "expurgo_ieo",
    "rcl_msc", "rgf_anexo2_dcl", "rgf_anexo2_base", "rgf_anexo5_disp",
    "rgf_anexo5_vinculacao", "rreo_anexo2", "rreo_anexo3", "rreo_anexo4_blocos",
    "rreo_anexo6", "rreo_anexo7", "rreo_anexo9", "rreo_anexo11",
    "rreo_anexo13", "rreo_anexo14", "rreo_gerador",
]


def ler_fonte(nome: str) -> str:
    for pasta in (RAIZ, os.path.join(RAIZ, "app")):
        caminho = os.path.join(pasta, nome + ".py")
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8", errors="ignore") as fh:
                return fh.read()
    return ""


def classificar(texto: str) -> list[str]:
    achados = [cat for cat, marcas in SINAIS.items()
               if any(m in texto for m in marcas)]
    return achados or ["?"]


def main() -> int:
    print(f"{'modulo':<26}{'fonte(s) de geracao':<34}{'so MSC?'}")
    print("-" * 74)
    so_msc = 0
    total = 0
    for nome in MODULOS:
        texto = ler_fonte(nome)
        if not texto:
            print(f"{nome:<26}{'(nao encontrado)':<34}")
            continue
        total += 1
        cats = classificar(texto)
        precisa_pdf = "PDF" in cats
        marca = "SIM" if not precisa_pdf else "nao"
        if not precisa_pdf:
            so_msc += 1
        print(f"{nome:<26}{', '.join(cats):<34}{marca}")
    print("-" * 74)
    print(f"{so_msc} de {total} modulos rodam sem PDF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
