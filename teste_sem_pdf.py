# -*- coding: utf-8 -*-
"""Teste empirico: derruba os PDFs e ve o que o gerador ainda produz (rodada 161).

Em vez de adivinhar pela leitura do codigo, aponto as pastas de PDF para um
caminho inexistente e executo cada grupo da verificacao. O que continuar
produzindo numero nao depende do SIGEF.

Uso:
    python teste_sem_pdf.py
"""
from __future__ import annotations

import os
import sys

RAIZ = r"C:\Users\victo\OneDrive\Documents\deepseek-harness\default-workspace\repo-github"
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

FANTASMA = os.path.join(RAIZ, "_sem_pdf_aqui")


def main() -> int:
    import mapa_anexo1 as MAPA
    import nao_executada as NE

    # derruba as tres portas de entrada dos PDFs
    MAPA.BASE = FANTASMA
    MAPA.CANDIDATOS_BASE = (FANTASMA,)
    try:
        import expurgo_poderes as E
        E.BASE = FANTASMA
    except Exception:
        pass
    try:
        import expurgo_ieo as EI
        EI.BASE = FANTASMA
    except Exception:
        pass
    NE.BASE = FANTASMA

    # derruba tambem as planilhas da equipe
    import caminhos
    caminhos.relatorios_contag = lambda: FANTASMA
    for mod in ("rgf_anexo2_dcl", "rgf_anexo2_base", "rgf_anexo5_disp",
                "rgf_anexo5_vinculacao", "rreo_anexo13"):
        try:
            m = __import__(mod)
            if hasattr(m, "_BASE_CONTAG"):
                m._BASE_CONTAG = FANTASMA
            if hasattr(m, "PLANILHA"):
                m.PLANILHA = os.path.join(FANTASMA, "x.xlsx")
        except Exception:
            pass

    import verificacao as V

    grupos = dict(V.FONTES)
    print(f"{'grupo':<38}{'celulas':>9}{'so MSC?':>10}")
    print("-" * 60)
    sem_pdf = com_pdf = 0
    celulas_ok = 0
    for nome, funcao in grupos.items():
        try:
            itens = funcao()
        except Exception as e:
            print(f"{nome:<38}{'-':>9}{'FALHOU':>10}   ({type(e).__name__})")
            com_pdf += 1
            continue
        if not itens:
            print(f"{nome:<38}{0:>9}{'sem dado':>10}")
            continue
        exatas = sum(1 for x in itens if x.get("ok"))
        if exatas == len(itens):
            sem_pdf += 1
            celulas_ok += len(itens)
            marca = "SIM"
        else:
            com_pdf += 1
            marca = "parcial"
        print(f"{nome:<38}{len(itens):>9}{marca:>10}")
    print("-" * 60)
    print(f"grupos 100% sem PDF ...: {sem_pdf}")
    print(f"grupos que precisam ...: {com_pdf}")
    print(f"celulas exatas sem PDF : {celulas_ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
