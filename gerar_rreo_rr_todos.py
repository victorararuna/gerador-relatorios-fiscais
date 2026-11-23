# -*- coding: utf-8 -*-
"""Gera TODOS os anexos do RREO de RR no layout do Siconfi (rodada 181).

Reaproveita:
    Anexo 1  rreo_anexo1_completo   (receita + despesa, previsao/dotacao/execucao)
    Anexo 2  rreo_anexo2_completo   (funcao + subfuncao, todas as colunas)
    Anexos 7, 9, 14  rreo_layout_anexos (adaptadores sobre rreo_gerador)
    Anexo 3  rcl_msc (RCL de 12 meses)

O molde de cada anexo e o proprio RREO publicado do ente (mesma estrutura que o
Siconfi espera). Os valores vem da MSC; do molde vem so a estrutura.

Uso:
    python gerar_rreo_rr_todos.py --ano 2026 --bimestre 5
"""
from __future__ import annotations

import argparse
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

RR_MSC = os.path.join(RAIZ, "dados", "rr_msc")
PUB = os.path.join(RAIZ, "dados", "rr_rreo_pub", "2026")
MOLDE_RN = os.path.join(RAIZ, "dados", "siconfi_rn", "RREO", "2025")
SAIDA = os.path.join(RAIZ, "saida", "RR")


def _molde(n: int) -> str | None:
    """Molde do proprio ente; se ele nao publicou o anexo, o do RN (estrutura
    padrao do Siconfi, identica entre entes)."""
    for bim in (4, 3):
        p = os.path.join(PUB, f"RREO_14_2026_bim{bim}_anexo{n:02d}.csv")
        if os.path.exists(p):
            return p
    p = os.path.join(MOLDE_RN, f"RREO_24_2025_bim6_anexo{n:02d}.csv")
    return p if os.path.exists(p) else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Todos os anexos do RREO de RR")
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=5)
    args = ap.parse_args()

    import rreo_layout_oficial as LO
    import rreo_gerador as G
    import rreo_anexo1_completo as A1
    import rreo_anexo2_completo as A2
    import rreo_layout_anexos as L
    from rreo_completar_publicado import ler_publicado, replicar

    os.makedirs(SAIDA, exist_ok=True)
    publicados = sorted(
        [os.path.join(PUB, f) for f in os.listdir(PUB) if f.endswith("anexo01.csv")],
        reverse=True)
    pub1 = publicados[0] if publicados else None

    res = G.apurar(RR_MSC, args.ano, args.bimestre)

    anexos = {}

    # ---- Anexo 1
    cel1 = A1.celulas(RR_MSC, args.ano, args.bimestre)
    if pub1:
        replicar(cel1, ler_publicado(pub1))
    anexos[1] = cel1

    # ---- Anexo 2
    intra = {}
    pub2 = _molde(2)
    if pub2:
        intra = A2.intra_publicada(pub2)
    anexos[2] = A2.celulas(RR_MSC, args.ano, args.bimestre, intra)

    # ---- Anexos 7, 9, 14 (adaptadores)
    anexos[7] = L.anexo7(res)
    anexos[9] = L.anexo9(res)
    anexos[14] = L.anexo14(res)

    # ---- Anexos 11 (alienacao) e 13 (PPP), apontando os modulos para RR
    import rreo_anexo11 as A11
    import rreo_anexo13 as A13
    for mod in (A11, A13):
        if hasattr(mod, "ACERVO"):
            mod.ACERVO = RR_MSC
        if hasattr(mod, "MSC"):
            mod.MSC = RR_MSC
    try:
        a11 = A11.linhas(args.ano)
        anexos[11] = {
            ("RECEITAS DE ALIENAÇÃO DE ATIVOS (I)", "RECEITAS REALIZADAS (b)"): a11["receitas_alienacao"],
            ("Receita de Alienação de Bens Móveis", "RECEITAS REALIZADAS (b)"): a11["moveis"],
            ("Receita de Rendimentos de Aplicações Financeiras", "RECEITAS REALIZADAS (b)"): a11["rendimentos"],
            ("APLICAÇÃO DOS RECURSOS DA ALIENAÇÃO DE ATIVOS (II)", "DESPESAS EMPENHADAS (e)"): a11["aplicacao"],
            ("Investimentos", "DESPESAS EMPENHADAS (e)"): a11["investimentos"],
        }
    except Exception as e:
        print(f"Anexo 11 nao apurado: {type(e).__name__}: {str(e)[:60]}")
    try:
        a13 = A13.saldos(args.ano, 2 * args.bimestre)
        anexos[13] = {
            ("Ativos Constituídos pela SPE", "SALDO FINAL ATÉ O BIMESTRE"): a13.get("ativos_spe", 0.0),
            ("Obrigações decorrentes de Ativos Constituídos pela SPE", "SALDO FINAL ATÉ O BIMESTRE"): a13.get("obrigacoes_spe", 0.0),
        }
    except Exception as e:
        print(f"Anexo 13 nao apurado: {type(e).__name__}: {str(e)[:60]}")

    # ---- Anexo 3 (RCL) — linhas principais na coluna de 12 meses
    try:
        import rcl_msc
        rcl_msc.ACERVO = RR_MSC
        v = rcl_msc.apurar(args.ano, 2 * args.bimestre)
        col = "TOTAL (ÚLTIMOS 12 MESES)"
        anexos[3] = {
            ("RECEITAS CORRENTES (I)", col): v["receitas_correntes"],
            ("DEDUÇÕES (II)", col): v["deducoes"],
            ("Transferências Constitucionais e Legais", col): v["transferencias"],
            ("Contrib. do Servidor para o Plano de Previdência", col): v["contrib_servidor"],
            ("Compensações Financ. entre Regimes Previdência", col): v["compensacao"],
            ("Rendimentos de Aplicações de Recursos Previdenciários", col): v["rend_prev"],
            ("Dedução de Receita para Formação do FUNDEB", col): v["fundeb"],
            ("RECEITA CORRENTE LÍQUIDA (III) = (I - II)", col): v["rcl"],
        }
    except Exception as e:
        print(f"Anexo 03 nao apurado: {type(e).__name__}: {str(e)[:60]}")

    total_geral = 0
    for n in (1, 2, 3, 7, 9, 11, 13, 14):
        molde = _molde(n)
        if not molde:
            print(f"Anexo {n:02d}: sem molde publicado")
            continue
        destino = os.path.join(SAIDA, f"RREO_RR_{args.ano}_B{args.bimestre}_Anexo{n:02d}.xlsx")
        p, t = LO.renderizar(
            destino, molde, anexos[n],
            f"RREO RR {args.ano} B{args.bimestre} — Anexo {n:02d} — MSC",
            nota="Estrutura: RREO publicado do ente. Valores: MSC de RR.")
        total_geral += p
        print(f"Anexo {n:02d}: {p}/{t} ({p / t * 100:.1f}%) -> {os.path.basename(destino)}")
    print(f"\n{total_geral} celulas preenchidas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
