# -*- coding: utf-8 -*-
"""Gera o RREO de um bimestre a partir da matriz e confere com o homologado.

    python gerar_rreo.py --ano 2026 --bimestre 4
    python gerar_rreo.py --ano 2026 --bimestre 5 --rcl 21000000000

Sem `--rcl`, o demonstrativo simplificado sai sem a linha da RCL — a matriz não
a apura com o critério do RREO.
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from app import rreo_layout_anexos as L  # noqa: E402
from app.rreo_gerador import GRUPOS, apurar, escrever_xlsx  # noqa: E402
from app.rreo_layout import gerar_workbook  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RREO = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn\RREO"
SAIDA = os.path.join(AQUI, "saida")


def ler_linha(arquivo: str, prefixo: str, coluna: str) -> float | None:
    if not os.path.exists(arquivo):
        return None
    with open(arquivo, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == coluna and r["conta"].startswith(prefixo):
                return float(r["valor"])
    return None


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Gera o RREO a partir da MSC.")
    ap.add_argument("--raiz", default=MSC)
    ap.add_argument("--ano", type=int, required=True)
    ap.add_argument("--bimestre", type=int, required=True)
    ap.add_argument("--rcl", type=float, default=None)
    ap.add_argument("--saida", default=SAIDA)
    args = ap.parse_args()

    res = apurar(args.raiz, args.ano, args.bimestre, rcl=args.rcl)
    ini = f"{res.meses[0]:02d}"
    fim = f"{res.meses[-1]:02d}"
    print(f"RREO {args.ano} B{args.bimestre} — meses {ini} a {fim} "
          f"({len(res.meses)} meses)\n")

    print(f"{'grupo':<30}{'empenhada':>18}{'liquidada':>18}{'paga':>18}")
    for pref, nome in GRUPOS.items():
        g = res.grupos.get(pref)
        if not g:
            continue
        print(f"{nome[:28]:<30}{g['empenhado']:>18,.2f}"
              f"{g['liquidado']:>18,.2f}{g['pago']:>18,.2f}")
    print(f"{'TOTAL':<30}{res.empenhado:>18,.2f}{res.liquidado:>18,.2f}"
          f"{res.pago:>18,.2f}")

    print(f"\nfunções apuradas: {len(res.funcoes)}  "
          f"soma {sum(res.funcoes.values()):,.2f}")

    print("\nrestos a pagar:")
    for chave, valor in res.restos.items():
        print(f"   {chave:<16}{valor:>18,.2f}")

    destino = os.path.join(args.saida, f"RREO_{args.ano}_B{args.bimestre}_MSC.xlsx")
    escrever_xlsx(destino, res)
    print(f"\n-> {destino}")

    # ---- layout oficial
    def molde(n: int) -> str | None:
        p = os.path.join(RREO, str(args.ano),
                         f"RREO_24_{args.ano}_bim{args.bimestre}_anexo{n:02d}.csv")
        if os.path.exists(p):
            return p
        p2 = os.path.join(RREO, "2025", f"RREO_24_2025_bim6_anexo{n:02d}.csv")
        return p2 if os.path.exists(p2) else None

    titulo = f"RREO {args.ano} — {args.bimestre}º bimestre — apurado na MSC"
    anexos = []
    for n, nome, celulas in (
            (1, "Anexo 01", L.anexo1(res)),
            (7, "Anexo 07", L.anexo7(res)),
            (9, "Anexo 09", L.anexo9(res)),
            (14, "Anexo 14", L.anexo14(res))):
        m = molde(n)
        if m:
            anexos.append((nome, m, celulas, f"{titulo} — Anexo {n:02d}"))

    if anexos:
        destino_layout = os.path.join(
            args.saida, f"RREO_{args.ano}_B{args.bimestre}_LAYOUT.xlsx")
        gerar_workbook(destino_layout, anexos,
                       nota="Molde: arquivo oficial do Siconfi. "
                            "Células em branco = não apuradas na matriz.")
        print(f"-> {destino_layout}  ({len(anexos)} anexos no layout oficial)")

    # comparação com o homologado, quando existir
    pasta = os.path.join(RREO, str(args.ano))
    arq = lambda n: os.path.join(pasta, f"RREO_24_{args.ano}_bim{args.bimestre}_anexo{n:02d}.csv")
    comparacoes = [
        ("Anexo 1 — total liquidado", res.liquidado,
         ler_linha(arq(1), "TOTAL DAS DESPESAS (XII)",
                   "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)")),
        ("Anexo 7 — RP processados pagos", res.restos.get("rpp_pagos", 0.0),
         ler_linha(arq(7), "TOTAL (III)", "Pagos (c)")),
        ("Anexo 7 — saldo de RP processados", res.restos.get("rpp_saldo", 0.0),
         ler_linha(arq(7), "TOTAL (III)", "Saldo e = (a + b) - (c + d)")),
        ("Anexo 14 — despesas empenhadas", res.empenhado,
         ler_linha(arq(14), "Despesas Empenhadas", "Até o Bimestre")),
        ("Anexo 14 — despesas pagas", res.pago,
         ler_linha(arq(14), "Despesas Pagas", "Até o Bimestre")),
    ]
    if any(of is not None for _, _, of in comparacoes):
        print(f"\n{'conferência':<36}{'nosso':>18}{'homologado':>18}{'dif':>12}")
        for nome, nosso, of in comparacoes:
            if of is None:
                print(f"{nome:<36}{nosso:>18,.2f}{'—':>18}{'—':>12}")
                continue
            print(f"{nome:<36}{nosso:>18,.2f}{of:>18,.2f}{nosso - of:>12,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

