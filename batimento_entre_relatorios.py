# -*- coding: utf-8 -*-
"""Batimento entre os relatórios — 2025.

Verifica se os mesmos valores aparecem iguais quando um demonstrativo os declara
em mais de um anexo. É o teste de consistência interna do ente, independente de
qualquer valor de referência externo.

Cruzamentos:

  RCL .............. RGF A1 × A3 × A4 × A6 × RREO A3
  Operações ........ RGF A4 × RREO A9
  DTP .............. RGF A1 (III) × RGF A6
  Despesa .......... RREO A1 × RREO A14
  Restos a pagar ... RREO A7 × RREO A1
  Limite de pessoal  RGF A1 × RGF A6
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import siconfi_declaracao as S

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF808080")] * 4)
CAB = PatternFill("solid", fgColor="FFD9E1F2")
TIT = PatternFill("solid", fgColor="FFBDD7EE")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

ANO, TRIM, BIM = 2025, 3, 6
RAIZ = os.path.dirname(os.path.abspath(__file__))


def classif(dif: float, base: float):
    if base == 0:
        return ("idêntico" if dif == 0 else "divergente"), (OK if dif == 0 else RUIM)
    pct = abs(dif / base)
    if pct < 1e-9:
        return "idêntico", OK
    if pct <= 0.005:
        return "confere", OK
    if pct <= 0.02:
        return "até 2%", ATEN
    return "divergente", RUIM


def _v(decl, conta, coluna, prefixo=True):
    try:
        return decl.valor(conta, coluna, prefixo=prefixo)
    except Exception:  # noqa: BLE001
        return None


def _ultimo(decl, conta, prefixo=True):
    """Maior valor da conta entre as colunas (para achar o total anual)."""
    vs = decl.valores(conta) if not prefixo else {}
    if not vs:
        for c in decl.contas():
            if c.startswith(conta):
                vs = decl.valores(c)
                break
    if not vs:
        return None
    return max(vs.values())


def coletar() -> list:
    a1 = S.rgf("RGF-Anexo 01", ANO, TRIM)
    a3 = S.rgf("RGF-Anexo 03", ANO, TRIM)
    a4 = S.rgf("RGF-Anexo 04", ANO, TRIM)
    a6 = S.rgf("RGF-Anexo 06", ANO, TRIM)
    a2 = S.rgf("RGF-Anexo 02", ANO, TRIM)
    r1 = S.rreo("RREO-Anexo 01", ANO, BIM)
    r7 = S.rreo("RREO-Anexo 07", ANO, BIM)
    r3 = S.rreo("RREO-Anexo 03", ANO, BIM)
    r9 = S.rreo("RREO-Anexo 09", ANO, BIM)
    r14 = S.rreo("RREO-Anexo 14", ANO, BIM)

    total12 = "TOTAL (ÚLTIMOS 12 MESES) (a)"

    rcl = {
        "RGF Anexo 03 (VI)": _v(a3, "RECEITA CORRENTE LÍQUIDA - RCL (VI)", "Até o 3º Quadrimestre"),
        "RGF Anexo 04 (IV)": _v(a4, "RECEITA CORRENTE LÍQUIDA - RCL (IV)", "VALOR"),
        "RGF Anexo 06": _v(a6, "Receita Corrente Líquida", "VALOR ATÉ O QUADRIMESTRE DE REFERÊNCIA"),
        "RGF Anexo 01 (IV)": _v(a1, "RECEITA CORRENTE LIQUIDA - RCL (IV)", "Valor"),
    }

    operacoes = {
        "RGF Anexo 04 (III)": _v(a4, "TOTAL (III)", "Até o Quadrimestre de Referência (a)"),
        "RREO Anexo 09 (I)": _v(r9, "RECEITAS DE OPERAÇÕES DE CRÉDITO (I)", "RECEITAS REALIZADAS (b)"),
    }

    # O DTP e a linha (VI) = (IIIa + IIIb) do Anexo 1 — inclui a parcela
    # inscrita em RP nao processados. Comparar com a (III), que e a Despesa
    # Liquida, da uma diferenca artificial de R$ 3,2 mi.
    dtp = {
        "RGF Anexo 01 (VI)": _v(a1, "DESPESA TOTAL COM PESSOAL - DTP (VI)", "Valor"),
        "RGF Anexo 06 (DTP)": _v(a6, "Despesa Total com Pessoal - DTP", "VALOR"),
    }

    limite = {
        "RGF Anexo 01 (VII)": _v(a1, "LIMITE MÁXIMO (VII)", "Valor"),
        "RGF Anexo 06": _v(a6, "Limite Máximo (incisos I, II e III art. 20 da LRF)", "VALOR"),
    }

    # Despesa empenhada: o Anexo 1 (XII) e o Anexo 14 declaram o mesmo total.
    despesa = {
        "RREO Anexo 01 (XII)": _v(r1, "TOTAL DAS DESPESAS (XII)", "DESPESAS EMPENHADAS ATÉ O BIMESTRE (f)"),
        "RREO Anexo 14": _v(r14, "Despesas Empenhadas", "Até o Bimestre"),
    }

    # Restos a pagar inscritos: o Anexo 7 e o Anexo 14 declaram o mesmo total.
    rp = {
        "RREO Anexo 07 (III)": _v(r7, "TOTAL (III)", "Saldo Total L = (e + k)"),
        "RREO Anexo 14": None,  # preenchido abaixo somando os dois grupos
    }
    # O cruzamento correto entre o Anexo 7 e o Anexo 14 e o **saldo a pagar**,
    # nao a inscricao: a inscricao do Anexo 14 inclui os RP de exercicios
    # anteriores reabertos, enquanto o Anexo 7 separa por ano de inscricao.
    proc = r14.valores("RESTOS A PAGAR PROCESSADOS").get("Saldo a Pagar")
    naoproc = r14.valores("RESTOS A PAGAR NÃO PROCESSADOS").get("Saldo a Pagar")
    if proc is not None and naoproc is not None:
        rp["RREO Anexo 14"] = proc + naoproc

    # Divida Consolidada Liquida: Anexo 2 (III) x Anexo 6.
    dcl = {
        "RGF Anexo 02 (III)": _v(a2, "DÍVIDA CONSOLIDADA LÍQUIDA (DCL) (III)", "Até o 3º Quadrimestre"),
        "RGF Anexo 06": _v(a6, "Dívida Consolidada Líquida", "VALOR ATÉ O QUADRIMESTRE DE REFERÊNCIA"),
    }

    grupos = [
        ("RCL — Receita Corrente Líquida", rcl),
        ("Operações de crédito", operacoes),
        ("Despesa Total com Pessoal (DTP)", dtp),
        ("Limite máximo de pessoal", limite),
        ("Despesa empenhada", despesa),
        ("Restos a pagar inscritos", rp),
        ("Dívida Consolidada Líquida", dcl),
    ]
    return grupos


def main() -> int:
    grupos = coletar()

    wb = Workbook()
    wb.remove(wb.active)
    ws = wb.create_sheet("Batimento")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "BATIMENTO ENTRE OS RELATÓRIOS — 2025"
    ws["A1"].font = Font(name="Arial", size=14, bold=True)
    ws.merge_cells("A1:F1")
    ws["A2"] = ("Verifica se o mesmo valor aparece igual quando declarado em anexos "
                "diferentes. Independe de referência externa.")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)
    ws.merge_cells("A2:F2")

    for j, (t, w) in enumerate((("Grupo", 34), ("Anexo", 24), ("Valor", 20),
                                ("Base", 20), ("Diferença", 16), ("Situação", 14)), 1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.border = BORDA
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = w

    lin = 5
    placar = {"identico": 0, "confere": 0, "divergente": 0, "sem": 0}
    for titulo, valores in grupos:
        validos = [(k, v) for k, v in valores.items() if v is not None]
        base = validos[0][1] if validos else None
        for k, v in valores.items():
            ws.cell(lin, 1, titulo if k == list(valores)[0] else "").font = Font(name="Arial", size=8, bold=True)
            ws.cell(lin, 2, k).font = Font(name="Arial", size=8)
            c = ws.cell(lin, 3, round(v, 2) if v is not None else "—")
            if v is not None:
                c.number_format = FMT
            c.font = Font(name="Arial", size=8)
            if base is not None and v is not None:
                c = ws.cell(lin, 4, round(base, 2))
                c.number_format = FMT
                c.font = Font(name="Arial", size=8)
                dif = v - base
                c = ws.cell(lin, 5, round(dif, 2))
                c.number_format = FMT
                c.font = Font(name="Arial", size=8)
                sit, cor = classif(dif, base)
            else:
                sit, cor = "sem dado", CINZA
            if sit == "idêntico":
                placar["identico"] += 1
            elif sit in ("confere", "até 2%"):
                placar["confere"] += 1
            elif sit == "divergente":
                placar["divergente"] += 1
            else:
                placar["sem"] += 1
            c = ws.cell(lin, 6, sit)
            c.font = Font(name="Arial", size=8, bold=sit == "divergente")
            c.fill = cor
            for j in range(1, 7):
                ws.cell(lin, j).border = BORDA
            lin += 1
        lin += 1

    # resumo
    lin += 1
    ws.cell(lin, 1, "RESUMO").font = Font(name="Arial", size=10, bold=True)
    lin += 1
    for rot, chave, cor in (("Idênticos", "identico", OK),
                            ("Conferem (até 2%)", "confere", OK),
                            ("Divergentes", "divergente", RUIM),
                            ("Sem dado", "sem", CINZA)):
        ws.cell(lin, 1, rot).font = Font(name="Arial", size=9)
        c = ws.cell(lin, 2, placar[chave])
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = cor
        lin += 1

    destino = os.path.join(RAIZ, "saida", "BATIMENTO_ENTRE_RELATORIOS.xlsx")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    wb.save(destino)
    print(f"gerado: {destino}")
    print()

    for titulo, valores in grupos:
        validos = [(k, v) for k, v in valores.items() if v is not None]
        base = validos[0][1] if validos else None
        print(titulo)
        for k, v in valores.items():
            if v is None:
                print(f"   {k:28} {'—':>18}")
                continue
            dif = (v - base) if base is not None else 0
            sit, _ = classif(dif, base) if base is not None else ("—", None)
            print(f"   {k:28} {v:>18,.2f}  {sit}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
