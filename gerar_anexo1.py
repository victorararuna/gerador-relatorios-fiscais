# -*- coding: utf-8 -*-
"""Gera o Anexo 1 do RGF em XLSX, com aba de verificações.

    python gerar_anexo1.py            # 2025 Q3, 2026 Q1 e 2026 Q2
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402
from app.relatorio_anexo1 import (escrever_xlsx, ler_oficiais,  # noqa: E402
                                  linhas_anexo1)

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF_DIR = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
           r"\siconfi_rn\RGF")
SAIDA = os.path.join(AQUI, "saida")

CASOS = [(2025, 3), (2026, 1), (2026, 2)]

OBSERVACOES = [
    "Vencimentos inclui sentenças judiciais (3.1.90.91), como na apresentação oficial.",
    "31.90.04 (contratação por tempo determinado) não entra: a linha oficial não o absorve.",
    "31.90.03.05 não compõe Pensões — é o que fecha a linha nas três janelas.",
    "31.90.13.02 fora das patronais; 31.91.92 dentro, conforme o mapeamento da STN.",
    "Despesa não executada lida em fluxo da conta 8.6.3.3.1.00.00 (classe 8).",
    "Exercícios anteriores: o homologado repete R$ 248.732.357,39 nos três períodos; "
    "o valor apurado é o que a matriz oferece.",
]


def main() -> int:
    acervo = M.Acervo(MSC)
    for ano, quad in CASOS:
        pares = M.periodos_janela(ano, M.MES_DO_QUADRIMESTRE[quad])
        res = M.apurar_janela(acervo, ano, M.MES_DO_QUADRIMESTRE[quad])
        ded = M.deducoes(acervo, pares)
        ne = M.nao_executada(acervo, pares)
        linhas = linhas_anexo1(res, ded, ne)

        arq_of = os.path.join(RGF_DIR, str(ano),
                              f"RGF_24_{ano}_quad{quad}_anexo01.csv")
        oficial = ler_oficiais(arq_of) if os.path.exists(arq_of) else None

        ini = f"{pares[0][0]}-{pares[0][1]:02d}"
        fim = f"{pares[-1][0]}-{pares[-1][1]:02d}"
        titulo = f"RGF — Anexo 1 (Despesa com Pessoal) — {ano} Q{quad} — {ini} a {fim}"

        print("=" * 96)
        print(titulo)
        print(f"{'linha':<62}{'apurado':>18}{'homologado':>18}{'%':>9}")
        for ln in linhas:
            of = (oficial or {}).get(ln.descricao)
            pct = (ln.valor / of - 1) * 100 if of else float("nan")
            marca = "  <<<" if of and abs(pct) > 2 else ""
            print(f"{'  ' * ln.nivel + ln.descricao[:58]:<62}"
                  f"{ln.valor:>18,.2f}"
                  f"{(of if of else 0):>18,.2f}{pct:>8.2f}%{marca}")

        destino = os.path.join(SAIDA, f"RGF_{ano}_Q{quad}_Anexo01_MSC.xlsx")
        escrever_xlsx(destino, linhas, titulo=titulo,
                      oficial=oficial,
                      fonte="Matriz de Saldos Contábeis (Siconfi) — contas "
                            "6.2.2.1.3.03/04/07, movimento líquido",
                      observacoes=OBSERVACOES)
        print(f"\n  -> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
