# -*- coding: utf-8 -*-
"""Aplica um mapeamento da STN na MSC, multiclasse, e confere com o homologado.

Duas diferenças em relação à primeira versão:

1. **Multiclasse.** As linhas de dedução do Anexo 2 combinam contas das classes
   1 (ativo), 2 (passivo) e 6 (controles). Lemos todas.

2. **Casamento de nomes.** A especificação do mapeamento e o rótulo do Siconfi
   divergem em caixa e acentuação ("PRECATÓRIOS POSTERIORES..." × "Precatórios
   Posteriores..."). Normalizamos os dois lados antes de comparar.

Uso:

    python aplicar_mapeamento2.py --anexo "RGF - ANEXO 2" --ano 2026 --periodo 2
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import filtros2 as filtros
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

#: classes lidas para cada anexo
CLASSES = {"RGF - ANEXO 2": (1, 2, 6),
           "RGF - ANEXO 5": (1, 2, 6, 8)}


def normalizar(texto: str) -> str:
    """Minúsculas, sem acento, sem pontuação — para casar nomes."""
    t = unicodedata.normalize("NFKD", texto or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


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


def ler_saldos(acervo: Acervo, ano: int, mes: int, classes) -> list:
    regs = []
    for c in classes:
        if acervo.tem(ano, mes, c, "ending_balance"):
            regs.extend(acervo.ler(ano, mes, c, "ending_balance"))
    return regs


def main(anexo_chave: str, ano: int, periodo: int, mes: int) -> int:
    mp = M.por_anexo(anexo_chave)
    if not mp:
        print(f"mapeamento não encontrado: {anexo_chave}")
        return 1

    classes = CLASSES.get(anexo_chave.upper(), (1, 2, 6))
    acervo = Acervo(ACERVO)
    regs = ler_saldos(acervo, ano, mes, classes)
    print(f"mapeamento: {mp.nome}")
    print(f"MSC {ano}-{mes:02d} classes {classes}: {len(regs)} registros")

    # homólogo
    tipo = "RGF-Anexo 02" if "ANEXO 2" in anexo_chave.upper() else "RGF-Anexo 05"
    try:
        hom = S.rgf(tipo, ano, periodo)
    except Exception:  # noqa: BLE001
        hom = None

    coluna = f"Até o {periodo}º Quadrimestre"
    indice_hom = {}
    if hom is not None:
        for c in hom.contas():
            indice_hom[normalizar(c)] = c

    wb = Workbook()
    ws = wb.active
    ws.title = "Anexo"
    ws.sheet_view.showGridLines = False
    ws["A1"] = f"{mp.nome} — {ano} Q{periodo}"
    ws["A1"].font = Font(name="Arial", size=12, bold=True)
    ws["A2"] = (f"Filtros do mapeamento aplicados na MSC {ano}-{mes:02d} "
                f"(saldo; classes {', '.join(map(str, classes))})")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, (t, w) in enumerate((("Especificação", 50), ("MSC", 20),
                                ("Homologado", 20), ("Diferença", 18),
                                ("%", 10), ("Situação", 14)), 1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        ws.column_dimensions[chr(64 + j)].width = w

    ignorar = ("Atualiz", "Tabela", "<", "RELAT", "DEMON", "ORÇAM", "RGF -",
               "ESPECIF", "Critérios", "FILTROS")
    lin = 5
    n_ok = n_div = n_sem = 0
    for item in mp.linhas:
        esp = item.especificacao.strip()
        if len(esp) < 4 or esp.startswith(ignorar):
            continue
        f = filtros.interpretar(item.filtro)
        if f.invalido:
            continue
        # Saldo com o sinal da natureza: credora (C-D) para passivo e
        # controles; devedora (D-C) para o ativo. O `liquido` e C-D.
        ap = 0.0
        for r in regs:
            if not f.aplicar(r):
                continue
            ap += -r.liquido if (r.conta or "").startswith("1") else r.liquido

        rotulo = indice_hom.get(normalizar(esp))
        of = hom.valor(rotulo, coluna) if (hom is not None and rotulo) else None
        pct = (ap - of) / of if (of and abs(of) > 1) else None
        sit, cor = classif(pct)
        if pct is not None:
            if sit in ("fecha", "confere"):
                n_ok += 1
            elif sit == "divergente":
                n_div += 1
        else:
            n_sem += 1

        ws.cell(lin, 1, esp[:64]).font = Font(name="Arial", size=8)
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
        c.font = Font(name="Arial", size=8, bold=sit in ("divergente", "fecha"))
        c.fill = cor

        if of is not None:
            print(f"   {esp[:44]:44} {ap:>18,.2f} {of:>18,.2f} {pct*100:>+8.2f}%  {sit}")
        elif abs(ap) > 1000:
            print(f"   {esp[:44]:44} {ap:>18,.2f} {'—':>18} {'—':>9}  sem par")
        lin += 1

    destino = os.path.join(RAIZ, "saida",
                           f"{anexo_chave.replace(' ', '_')}_{ano}_Q{periodo}_v2.xlsx")
    wb.save(destino)
    print()
    print(f"fecham: {n_ok} | divergem: {n_div} | sem par: {n_sem}")
    print(f"gerado: {destino}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--anexo", required=True)
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--periodo", type=int, default=2)
    ap.add_argument("--mes", type=int, default=8)
    a = ap.parse_args()
    raise SystemExit(main(a.anexo, a.ano, a.periodo, a.mes))
