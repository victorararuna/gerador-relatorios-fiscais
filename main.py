# -*- coding: utf-8 -*-
"""Ponto de entrada da aplicacao de demonstrativos fiscais (MDF/Siconfi).

Uso:
    python main.py            abre a interface
    python main.py --cli ...  executa sem interface (para lote/CI)

CLI:
    python main.py --cli --entrada "pasta" --saida "pasta"
"""
from __future__ import annotations

import argparse
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))


def _cli(entrada: str, saida: str) -> int:
    import gerador
    import rascunho
    import validacao

    docs = []
    if os.path.isdir(entrada):
        docs = rascunho.ler_pasta(entrada)
    else:
        docs = [rascunho.ler_rascunho(entrada)]
    if not docs:
        print("nenhum rascunho reconhecido", file=sys.stderr)
        return 1

    total_erros = total_alertas = 0
    for d in docs:
        achados = validacao.validar_documento(d)
        r = validacao.resumo(achados)
        total_erros += r["erro"]
        total_alertas += r["alerta"]
        print(f"\n=== {d.resumo()}  ({d.arquivo_origem})")
        print(f"    ente: {d.ente.nome} | instituição: {d.ente.instituicao}")
        print(f"    conferência: {r['erro']} erro(s), {r['alerta']} alerta(s)")
        for a in achados[:6]:
            print(f"      - {a}")
        for res in gerador.gerar_documento(d, saida):
            if res.get("status") == "ok":
                for arq in res["arquivos"]:
                    print(f"    gerado: {arq}")
            else:
                print(f"    {res['anexo']}: {res.get('mensagem', res.get('status'))}")
    print(f"\nresumo: {total_erros} erro(s), {total_alertas} alerta(s)")
    return 0 if total_erros == 0 else 2


def main() -> int:
    ap = argparse.ArgumentParser(description="Demonstrativos fiscais MDF/Siconfi")
    ap.add_argument("--cli", action="store_true", help="executa sem interface")
    ap.add_argument("--entrada", default="dados", help="pasta ou arquivo .xls de entrada")
    ap.add_argument("--saida", default="saida", help="pasta de saída")
    args = ap.parse_args()

    if args.cli:
        return _cli(args.entrada, args.saida)

    import ui
    ui.rodar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
