# -*- coding: utf-8 -*-
"""RREO de RR no layout oficial do Siconfi, sem gabarito (rodada 174).

Usa o esqueleto publico do Siconfi (molde) apenas como ESTRUTURA de rotulos e
colunas — os valores vem todos da MSC de RR, apurados sem consultar o publicado.
O molde e o do RN (a estrutura e identica entre estados); nenhuma linha de valor
do RN e copiada.

Cobre os anexos de despesa que o adaptador sustenta: 1, 2, 7, 9, 14. A aba
Cobertura mostra quantas celulas do molde foram preenchidas.

Uso:
    python gerar_rreo_rr_layout.py --ano 2026 --bimestre 5
"""
from __future__ import annotations

import argparse
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

RR_MSC = os.path.join(RAIZ, "dados", "rr_msc")
MOLDE = os.path.join(RAIZ, "dados", "siconfi_rn", "RREO", "2025")
SAIDA = os.path.join(RAIZ, "saida", "RR")


def main() -> int:
    ap = argparse.ArgumentParser(description="RREO de RR no layout oficial")
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=5)
    args = ap.parse_args()

    import rreo_gerador as G
    import rreo_layout_anexos as L
    from rreo_layout import gerar_workbook

    # RCL como entrada do simplificado
    rcl = None
    try:
        import rcl_msc
        rcl_msc.ACERVO = RR_MSC
        rcl = rcl_msc.apurar(args.ano, 2 * args.bimestre).get("rcl")
    except Exception:
        pass

    res = G.apurar(RR_MSC, args.ano, args.bimestre, rcl=rcl)

    def molde(n: int) -> str:
        return os.path.join(MOLDE, f"RREO_24_2025_bim6_anexo{n:02d}.csv")

    titulo = f"RREO RR {args.ano} — {args.bimestre}º bimestre — apurado na MSC (sem gabarito)"

    # Anexo 2: despesa liquidada por funcao
    col_liq = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (d)"
    cel2 = {(G.FUNCOES[cod], col_liq): v
            for cod, v in res.funcoes.items() if cod in G.FUNCOES}

    anexos = [
        ("Anexo 01", molde(1), L.anexo1(res, ocorrencia=0), f"{titulo} — Anexo 01"),
        ("Anexo 02", molde(2), cel2, f"{titulo} — Anexo 02"),
        ("Anexo 07", molde(7), L.anexo7(res), f"{titulo} — Anexo 07"),
        ("Anexo 09", molde(9), L.anexo9(res), f"{titulo} — Anexo 09"),
        ("Anexo 14", molde(14), L.anexo14(res), f"{titulo} — Anexo 14"),
    ]
    anexos = [(n, m, c, t) for n, m, c, t in anexos if os.path.exists(m)]

    os.makedirs(SAIDA, exist_ok=True)
    destino = os.path.join(SAIDA, f"RREO_RR_{args.ano}_B{args.bimestre}_LAYOUT.xlsx")
    gerar_workbook(destino, anexos,
                   nota="Estrutura: molde público do Siconfi. Valores: MSC de RR, "
                        "apurados sem gabarito. Células em branco = não apuradas.")
    print(f"-> {destino}  ({len(anexos)} anexos no layout oficial)")
    print(f"   empenhado {res.empenhado:,.2f} | liquidado {res.liquidado:,.2f} "
          f"| pago {res.pago:,.2f}")
    if rcl:
        print(f"   RCL {rcl:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
