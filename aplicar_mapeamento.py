# -*- coding: utf-8 -*-
"""Aplica um mapeamento da STN na MSC e compara com o anexo homologado.

O mapeamento diz, linha a linha, quais contas compõem cada item do anexo. Este
módulo lê o mapeamento, aplica os filtros na matriz e confere contra o valor
declarado no Siconfi.

Uso:

    python aplicar_mapeamento.py --anexo "RGF - ANEXO 2" --ano 2026 --periodo 2
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import filtros
import mapeamento as M
import siconfi_declaracao as S
from acervo import Acervo

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")


def classif(pct):
    if pct is None:
        return "sem par", CINZA
    if abs(pct) <= 0.005:
        return "fecha", OK
    if abs(pct) <= 0.02:
        return "confere", OK
    if abs(pct) <= 0.05:
        return "até 5%", ATEN
    return "divergente", RUIM


def apurar(acervo: Acervo, ano: int, mes: int, classe: int,
           tipo: str = "ending_balance") -> list:
    """Todos os registros do mês (saldo de fechamento)."""
    if not acervo.tem(ano, mes, classe, tipo):
        return []
    return list(acervo.ler(ano, mes, classe, tipo))


def main(anexo_chave: str, ano: int, periodo: int, mes: int,
         classe: int) -> int:
    mp = M.por_anexo(anexo_chave)
    if not mp:
        print(f"mapeamento não encontrado: {anexo_chave}")
        return 1

    acervo = Acervo(ACERVO)
    regs = apurar(acervo, ano, mes, classe)
    print(f"mapeamento: {mp.nome}")
    print(f"MSC: {ano}-{mes:02d} classe {classe} — {len(regs)} registros (saldo)")

    # homólogo
    try:
        hom = S.rgf("RGF-Anexo 02", ano, periodo)
    except Exception:  # noqa: BLE001
        hom = None

    coluna = f"Até o {periodo}º Quadrimestre"
    wb = Workbook()
    ws = wb.active
    ws.title = "Anexo"
    ws.sheet_view.showGridLines = False
    ws["A1"] = f"{mp.nome} — {ano} Q{periodo}"
    ws["A1"].font = Font(name="Arial", size=12, bold=True)
    ws["A2"] = f"Filtros do mapeamento aplicados na MSC ({ano}-{mes:02d}, saldo)"
    ws["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, (t, w) in enumerate((("Especificação", 46), ("MSC", 20),
                                ("Homologado", 20), ("Diferença", 18),
                                ("%", 10), ("Situação", 14)), 1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        ws.column_dimensions[chr(64 + j)].width = w

    lin = 5
    n_ok = n_div = 0
    for item in mp.linhas:
        esp = item.especificacao.strip()
        if len(esp) < 4 or esp.startswith(("Atualiz", "Tabela", "<", "RELAT",
                                           "DEMON", "ORÇAM", "RGF -", "ESPECIF",
                                           "Critérios", "DÍVIDA CONSOLIDADA ",
                                           "DEDUÇÕES", "Disponibilidade de Caixa")):
            continue
        f = filtros.interpretar(item.filtro)
        if f.invalido:
            continue
        ap = sum(r.liquido for r in regs if f.aplicar(r))
        of = None
        if hom is not None:
            of = hom.valor(esp, coluna, prefixo=True)
        pct = (ap - of) / of if (of and abs(of) > 1) else None
        sit, cor = classif(pct)
        if pct is not None:
            if sit in ("fecha", "confere"):
                n_ok += 1
            elif sit == "divergente":
                n_div += 1

        ws.cell(lin, 1, esp[:60]).font = Font(name="Arial", size=8)
        c = ws.cell(lin, 2, round(ap, 2))
        c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 3, round(of, 2) if of is not None else "—")
        if of is not None:
            c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        if of is not None:
            c = ws.cell(lin, 4, round(ap - of, 2))
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 5, pct if pct is not None else "—")
        c.number_format = "0.00%"
        c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 6, sit)
        c.font = Font(name="Arial", size=8,
                      bold=sit in ("divergente", "fecha"))
        c.fill = cor
        if of is not None:
            print(f"   {esp[:44]:44} {ap:>18,.2f} {of:>18,.2f} {pct*100:>+8.2f}%  {sit}")
        else:
            print(f"   {esp[:44]:44} {ap:>18,.2f} {'—':>18} {'—':>9}  {sit}")
        lin += 1

    destino = os.path.join(RAIZ, "saida",
                           f"{anexo_chave.replace(' ', '_')}_{ano}_Q{periodo}.xlsx")
    wb.save(destino)
    print()
    print(f"fecham: {n_ok} | divergem: {n_div}")
    print(f"gerado: {destino}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--anexo", required=True)
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--periodo", type=int, default=2)
    ap.add_argument("--mes", type=int, default=8)
    ap.add_argument("--classe", type=int, default=2)
    a = ap.parse_args()
    raise SystemExit(main(a.anexo, a.ano, a.periodo, a.mes, a.classe))
