# -*- coding: utf-8 -*-
"""Confere o exercício e o mês de cada relatório do SIGEF/RN da pasta.

Uso:
    python verificar_anos.py <pasta> --ano 2026

Sai com código 1 se algum arquivo não for do período esperado — barrando a
extração errada antes de qualquer soma.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from fonte_sigef import ErroFonte, ler_cabecalho  # noqa: E402

MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")


def mes_do_nome(nome: str) -> str | None:
    for nome_mes in MESES:
        if nome_mes.lower() in nome.lower():
            return nome_mes
    return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("pasta", nargs="?", default=r"C:\Users\victo\Downloads\Arquivos etonjones")
    p.add_argument("--ano", type=int, default=2026)
    args = p.parse_args()
    import leitor_pdf as LP

    arquivos = sorted(glob.glob(os.path.join(args.pasta, "*.pdf")))
    ok = erros = 0
    for arq in arquivos:
        nome = os.path.basename(arq)
        if not nome.startswith(("Imprimir", "Comparativo")):
            continue
        texto = re.sub(r"\s+", " ", LP.ler_pdf(arq)[0].texto())
        ano, mes = ler_cabecalho(texto)
        esperado = mes_do_nome(nome)
        problemas = []
        if ano != args.ano:
            problemas.append(f"ano {ano} != {args.ano}")
        if esperado and mes and mes.lower() != esperado.lower():
            problemas.append(f"mês {mes} != {esperado}")
        if problemas:
            erros += 1
            print(f"ERRO  {nome}: " + "; ".join(problemas))
        else:
            ok += 1
            print(f"ok    {nome}: {ano} {mes}")
    print(f"\n{ok} conferem, {erros} divergem")
    return 1 if erros else 0


if __name__ == "__main__":
    raise SystemExit(main())
