# -*- coding: utf-8 -*-
"""Gera o RREO de Roraima a partir da MSC, sem gabarito (rodada 174).

O usuario forneceu outubro/2026 (instancia) e a API tem jan-set. O 5o bimestre
de 2026 (set-out) acumula janeiro a outubro. Este script:

1. apura os anexos que a matriz sustenta com o `app/rreo_gerador.py`
   (Anexos 1, 2, 7, 9, 14 + Verificacoes);
2. tenta a RCL (Anexo 3) e os anexos 11 e 13 apontando os modulos para a pasta
   de RR — quando o dado nao cobre a janela, registra a ausencia em vez de
   inventar numero.

Uso:
    python gerar_rreo_rr.py --bimestre 5
"""
from __future__ import annotations

import argparse
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

RR_MSC = os.path.join(RAIZ, "dados", "rr_msc")
SAIDA = os.path.join(RAIZ, "saida", "RR")


def main() -> int:
    ap = argparse.ArgumentParser(description="RREO de RR sem gabarito")
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=5)
    args = ap.parse_args()

    import rreo_gerador as G

    print(f"Apurando RREO de RR — {args.ano} B{args.bimestre} "
          f"(meses 1 a {2 * args.bimestre})...")
    try:
        res = G.apurar(RR_MSC, args.ano, args.bimestre)
    except Exception as e:
        print(f"ERRO na apuracao: {type(e).__name__}: {e}")
        return 1

    os.makedirs(SAIDA, exist_ok=True)
    destino = os.path.join(SAIDA, f"RREO_RR_{args.ano}_B{args.bimestre}.xlsx")
    G.escrever_xlsx(destino, res)
    print(f"   empenhado: {res.empenhado:,.2f}")
    print(f"   liquidado: {res.liquidado:,.2f}")
    print(f"   pago:      {res.pago:,.2f}")
    print(f"   funcoes:   {len(res.funcoes)}")
    print(f"   -> {destino}")

    # ---- RCL (Anexo 3): janela de 12 meses terminada no mes de referencia
    mes_ref = 2 * args.bimestre
    try:
        import rcl_msc
        rcl_msc.ACERVO = RR_MSC
        rcl = rcl_msc.apurar(args.ano, mes_ref)
        print(f"\nRCL (janela 12 meses ate {args.ano}-{mes_ref:02d}):")
        for k, v in rcl.items():
            print(f"   {k:<28}{v:>18,.2f}")
        _anexo3(destino, rcl, args.ano, args.bimestre)
    except Exception as e:
        print(f"\nRCL nao apurada: {type(e).__name__}: {str(e)[:80]}")

    # ---- Anexo 11 (alienacao de ativos) e Anexo 13 (PPP)
    for mod, fn, args, aba, titulo in (
            ("rreo_anexo11", "linhas", (args.ano,), "Anexo 11",
             f"RREO Anexo 11 — Alienação de Ativos — {args.ano} B{args.bimestre}"),
            ("rreo_anexo13", "saldos", (args.ano, mes_ref), "Anexo 13",
             f"RREO Anexo 13 — Parcerias Público-Privadas — {args.ano} B{args.bimestre}")):
        try:
            m = __import__(mod)
            if hasattr(m, "ACERVO"):
                m.ACERVO = RR_MSC
            dados = getattr(m, fn)(*args)
            _aba_simples(destino, aba, titulo, dados)
            print(f"{aba}: {len(dados)} linhas")
        except Exception as e:
            print(f"{aba} nao apurado: {type(e).__name__}: {str(e)[:60]}")

    return 0


def _aba_simples(destino: str, aba: str, titulo: str, dados: dict) -> None:
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill

    wb = load_workbook(destino)
    if aba in wb.sheetnames:
        del wb[aba]
    ws = wb.create_sheet(aba)
    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=12)
    ws["A3"], ws["B3"] = "Linha", "Valor"
    for c in ("A3", "B3"):
        ws[c].font = Font(bold=True)
        ws[c].fill = PatternFill("solid", fgColor="EDEDED")
    r = 4
    for k, v in dados.items():
        ws.cell(row=r, column=1, value=str(k))
        if isinstance(v, (int, float)):
            ws.cell(row=r, column=2, value=v).number_format = "#,##0.00"
        else:
            ws.cell(row=r, column=2, value=str(v))
        r += 1
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 24
    wb.save(destino)


def _anexo3(destino: str, rcl: dict, ano: int, bimestre: int) -> None:
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill

    wb = load_workbook(destino)
    if "Anexo 03" in wb.sheetnames:
        del wb["Anexo 03"]
    ws = wb.create_sheet("Anexo 03")
    ws["A1"] = f"RREO Anexo 3 — Receita Corrente Líquida — {ano} B{bimestre}"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A3"], ws["B3"] = "Componente", "Valor"
    for c in ("A3", "B3"):
        ws[c].font = Font(bold=True)
        ws[c].fill = PatternFill("solid", fgColor="EDEDED")
    r = 4
    for k, v in rcl.items():
        ws.cell(row=r, column=1, value=k)
        ws.cell(row=r, column=2, value=v).number_format = "#,##0.00"
        r += 1
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 24
    wb.save(destino)


if __name__ == "__main__":
    raise SystemExit(main())
