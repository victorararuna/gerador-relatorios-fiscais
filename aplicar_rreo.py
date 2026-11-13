# -*- coding: utf-8 -*-
"""Aplica os mapeamentos do RREO na MSC, combinando conta e natureza.

Diferença em relação ao aplicador do RGF: no RREO, a apuração de cada célula
combina **dois critérios**:

1. **Conta contábil** — vem do cabeçalho da coluna (linha 15 do mapeamento).
   Para "Receitas Realizadas" é ``CC começada por LISTA: 6212,6213``.

2. **Natureza** — vem da linha (coluna 2). Para "Receitas (exceto intra)" é
   ``NR começada por 1,2 EXCETO ...``.

O valor da célula é a soma dos registros que atendem **aos dois**.

Uso:

    python aplicar_rreo.py --anexo "RREO - ANEXO 01" --ano 2026 --bimestre 4
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import filtros2 as F
import siconfi_declaracao as S
from acervo import Acervo

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")
MAPEAMENTOS = os.path.join(RAIZ, "dados", "mapeamentos", "rreo")


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


def abrir_mapeamento(chave: str):
    for p in glob.glob(os.path.join(MAPEAMENTOS, "**", "*.xlsx"), recursive=True):
        if chave.upper() in os.path.basename(p).upper():
            wb = openpyxl.load_workbook(p, data_only=True)
            return p, wb
    return None, None


def criterios_de_coluna(ws) -> dict:
    """Critério de conta por coluna.

    Duas estruturas aparecem:
      * Anexo 1 — um critério por coluna na linha 15 (c4, c6, c8...);
      * Anexo 3 — um critério único na linha 18 (c4), valendo para todas as
        colunas mensais.
    """
    saida = {}
    for c in range(2, ws.max_column + 1):
        v = ws.cell(15, c).value
        if isinstance(v, str) and ("CC" in v.upper() or "LISTA" in v.upper()):
            saida[c] = v.strip()
    if not saida:
        for l in range(15, 22):
            v = ws.cell(l, 4).value
            if isinstance(v, str) and ("6.2.1.2" in v or "CC " in v.upper()):
                saida[4] = v.strip()
                break
    return saida


def linhas_do_anexo(ws) -> list:
    saida = []
    for l in range(16, ws.max_row + 1):
        esp = ws.cell(l, 1).value
        filtro = ws.cell(l, 2).value
        if esp is None:
            continue
        esp = str(esp).strip()
        if len(esp) < 4:
            continue
        if esp.startswith(("Atualiz", "Tabela", "<", "RELAT", "DEMON", "ORÇAM",
                           "RREO -", "ESPECIF", "Critérios", "FILTROS")):
            continue
        saida.append((l, esp, str(filtro or "").strip()))
    return saida


def apurar(acervo: Acervo, ano: int, mes: int,
           filtro_conta: str, filtro_linha: str) -> float:
    """Soma o que atende ao filtro de conta **e** ao de natureza.

    O critério de conta pode citar várias contas somadas
    (``6.2.1.2... + (-) 6.2.1.3...``): nesse caso a relação é **OU** — o
    registro entra se casar com qualquer uma. O filtro de natureza, quando
    existe, é **E**.
    """
    fc = F.interpretar(filtro_conta)
    fl = F.interpretar(filtro_linha)
    total = 0.0
    for r in acervo.ler(ano, mes):
        if not fc.invalido and not any(c.casar(r) for c in fc.condicoes):
            continue
        if not fl.invalido and not fl.aplicar(r):
            continue
        total += r.liquido
    return total


def main(anexo_chave: str, ano: int, bimestre: int) -> int:
    caminho, wb = abrir_mapeamento(anexo_chave)
    if wb is None:
        print(f"mapeamento não encontrado: {anexo_chave}")
        return 1
    ws = wb[wb.sheetnames[0]]
    cols = criterios_de_coluna(ws)
    linhas = linhas_do_anexo(ws)
    print(f"mapeamento: {os.path.basename(caminho)}")
    print(f"colunas com critério: { {c: cols[c][:34] for c in cols} }")
    print(f"linhas: {len(linhas)}")

    # coluna alvo: a de receitas realizadas / empenhadas
    alvo = None
    for c in cols:
        if "6212" in cols[c] or "6221" in cols[c] or "6229" in cols[c]:
            alvo = c
            break
    if alvo is None and cols:
        alvo = list(cols)[-1]
    print(f"coluna alvo: c{alvo} -> {cols.get(alvo, '')[:50]}")

    acervo = Acervo(ACERVO)
    meses = list(range(1, bimestre * 2 + 1))

    # acumula por linha
    resultado = []
    for l, esp, filtro in linhas:
        tot = 0.0
        for m in meses:
            if acervo.tem(ano, m):
                tot += apurar(acervo, ano, m, cols.get(alvo, ""), filtro)
        resultado.append((esp, tot))

    # homólogo
    tipo = f"RREO-Anexo {anexo_chave.split('ANEXO')[-1].strip()[:2]}" \
        if "ANEXO" in anexo_chave.upper() else "RREO-Anexo 01"
    try:
        hom = S.rreo(tipo, ano, bimestre)
    except Exception:  # noqa: BLE001
        hom = None

    out = Workbook()
    w = out.active
    w.title = "Anexo"
    w.sheet_view.showGridLines = False
    w["A1"] = f"{anexo_chave} — {ano} B{bimestre}"
    w["A1"].font = Font(name="Arial", size=12, bold=True)
    w["A2"] = f"Contas: {cols.get(alvo, '')[:70]}"
    w["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, (t, larg) in enumerate((("Especificação", 52), ("MSC", 20),
                                   ("Homologado", 20), ("%", 10), ("Situação", 14)), 1):
        c = w.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        w.column_dimensions[chr(64 + j)].width = larg

    r = 5
    n_ok = n_div = 0
    for esp, val in resultado:
        of = None
        if hom is not None:
            for candidata in ("DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)",
                              "RECEITAS REALIZADAS ATÉ O BIMESTRE (c)",
                              "Até o Bimestre (c)"):
                of = hom.valor(esp, candidata, prefixo=True)
                if of:
                    break
        pct = (val - of) / of if (of and abs(of) > 1) else None
        sit, cor = classif(pct)
        if pct is not None:
            if sit in ("fecha", "confere"):
                n_ok += 1
            elif sit == "divergente":
                n_div += 1
        w.cell(r, 1, esp[:60]).font = Font(name="Arial", size=8)
        c = w.cell(r, 2, round(val, 2))
        c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        c = w.cell(r, 3, round(of, 2) if of is not None else "—")
        if of is not None:
            c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        c = w.cell(r, 4, pct if pct is not None else "—")
        c.number_format = "0.00%"
        c.font = Font(name="Arial", size=8)
        c = w.cell(r, 5, sit)
        c.font = Font(name="Arial", size=8, bold=sit == "divergente")
        c.fill = cor
        if of is not None:
            print(f"   {esp[:42]:42} {val:>18,.2f} {of:>18,.2f} {pct*100:>+8.2f}% {sit}")
        elif abs(val) > 1000:
            print(f"   {esp[:42]:42} {val:>18,.2f} {'—':>18} {'—':>8} sem par")
        r += 1

    destino = os.path.join(RAIZ, "saida",
                           f"RREO_{anexo_chave.split()[-1]}_{ano}_B{bimestre}.xlsx")
    out.save(destino)
    print()
    print(f"fecham: {n_ok} | divergem: {n_div}")
    print(f"gerado: {destino}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--anexo", required=True)
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=4)
    a = ap.parse_args()
    raise SystemExit(main(a.anexo, a.ano, a.bimestre))
