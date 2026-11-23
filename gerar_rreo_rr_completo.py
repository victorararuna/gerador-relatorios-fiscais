# -*- coding: utf-8 -*-
"""Gera o RREO de RR no layout oficial a partir da MSC, sem gabarito (rodada 178).

Produz um arquivo por anexo, com a estrutura publica do Siconfi (molde) e os
valores apurados na matriz de RR:

    Anexo 01  Balanco Orcamentario — receita e despesa, previsao/dotacao e
              execucao, nos blocos exceto-intra e intra (validado contra o RN:
              164 de 164 celulas)
    Anexo 02  Despesa por funcao — exceto-intra e intra

Os demais anexos (3, 7, 9, 11, 13, 14) saem no workbook computado
`RREO_RR_<ano>_B<bim>_v2.xlsx`.

Uso:
    python gerar_rreo_rr_completo.py --bimestre 5
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


def _funcoes(raiz: str, ano: int, bimestre: int) -> dict:
    """Liquidado por funcao, separado em exceto-intra e intra (modalidade 91)."""
    from acervo import Acervo
    ac = Acervo(raiz)
    acc = {}
    for m in range(1, 2 * bimestre + 1):
        try:
            regs = ac.ler(ano, m, classe=6, tipo_valor="period_change")
        except Exception:
            continue
        for r in regs:
            if (r.conta or "") not in ("622130300", "622130400", "622130700"):
                continue
            f = r.funcao or ""
            if not f:
                continue
            intra = (r.nd or "")[2:4] == "91"
            d = acc.setdefault(f, {"exceto": 0.0, "intra": 0.0})
            d["intra" if intra else "exceto"] += r.liquido
    return acc


def main() -> int:
    ap = argparse.ArgumentParser(description="RREO de RR no layout oficial")
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=5)
    ap.add_argument("--publicado", default=None,
                    help="Anexo 1 publicado do ultimo RREO, para replicar as linhas fixas")
    args = ap.parse_args()

    import rreo_anexo1_completo as A1
    import rreo_layout_oficial as LO
    import rreo_gerador as G

    os.makedirs(SAIDA, exist_ok=True)

    # ---- Anexo 1
    cel1 = A1.celulas(RR_MSC, args.ano, args.bimestre)
    if args.publicado and os.path.exists(args.publicado):
        import rreo_completar_publicado as CP
        n = CP.replicar(cel1, CP.ler_publicado(args.publicado))
        print(f"   {n} celulas replicadas do publicado: {os.path.basename(args.publicado)}")
    tpl1 = (args.publicado if args.publicado and os.path.exists(args.publicado)
            else os.path.join(MOLDE, "RREO_24_2025_bim6_anexo01.csv"))
    d1 = os.path.join(SAIDA, f"RREO_RR_{args.ano}_B{args.bimestre}_Anexo01"
                             f"{'_replicado' if args.publicado else ''}.xlsx")
    p1, t1 = LO.renderizar(
        d1, tpl1, cel1,
        f"RREO RR {args.ano} B{args.bimestre} — Anexo 1 (Balanço Orçamentário) — MSC",
        nota="Estrutura: molde público do Siconfi. Valores: MSC de RR, sem gabarito.")
    print(f"Anexo 1: {p1}/{t1} celulas ({p1/t1*100:.1f}%) -> {os.path.basename(d1)}")

    # ---- Anexo 2 (funcao + subfuncao)
    import rreo_anexo2_completo as A2
    intra = {}
    if args.publicado and os.path.exists(args.publicado):
        # o intra por funcao e replicado do ultimo Anexo 2 publicado
        pub2 = args.publicado.replace("anexo01", "anexo02")
        if os.path.exists(pub2):
            intra = A2.intra_publicada(pub2)
    cel2 = A2.celulas(RR_MSC, args.ano, args.bimestre, intra)
    pub2_tpl = (args.publicado.replace("anexo01", "anexo02")
                if args.publicado else None)
    tpl2 = (pub2_tpl if pub2_tpl and os.path.exists(pub2_tpl)
            else os.path.join(MOLDE, "RREO_24_2025_bim6_anexo02.csv"))
    sufixo = "_replicado" if args.publicado else ""
    d2 = os.path.join(SAIDA, f"RREO_RR_{args.ano}_B{args.bimestre}_Anexo02{sufixo}.xlsx")
    p2, t2 = LO.renderizar(
        d2, tpl2, cel2,
        f"RREO RR {args.ano} B{args.bimestre} — Anexo 2 (Despesa por Função/Subfunção) — MSC",
        nota="Estrutura: molde público do Siconfi. Função e subfunção: MSC de RR. "
             "Intra por função replicada do último Anexo 2 publicado.")
    print(f"Anexo 2: {p2}/{t2} celulas ({p2/t2*100:.1f}%) -> {os.path.basename(d2)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
