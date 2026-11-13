# -*- coding: utf-8 -*-
"""RREO Anexo 3 (RCL) — apuração com cálculo mensal e deduções.

Três características que o diferenciam dos outros anexos:

1. **Colunas mensais** — 12 colunas (`<MR-11>` a `<MR>`), a janela móvel.
2. **Linhas calculadas** — "Resultado de fórmula" soma as filhas (indentação).
3. **Deduções** — a RCL é `I − II`, e a maior dedução é o **FUNDEB**
   (conta `6.2.1.3.1.01.00`), que o mapeamento chama de "Mapeamento na célula".

Uso:

    python gerar_rreo_a3.py --ano 2026 --bimestre 4
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import filtros2 as F
import siconfi_declaracao as S
from acervo import Acervo, periodos_janela

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")
MAPEAMENTOS = os.path.join(RAIZ, "dados", "mapeamentos", "rreo")

IGNORAR = ("Atualiz", "Tabela", "<", "RELAT", "DEMON", "ORÇAM", "RREO -",
           "ESPECIF", "Critérios", "FILTROS")


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


def abrir():
    for p in glob.glob(os.path.join(MAPEAMENTOS, "**", "*ANEXO 03*.xlsx"),
                       recursive=True):
        return p, openpyxl.load_workbook(p, data_only=True)
    return None, None


def ler_linhas(ws):
    saida = []
    for l in range(16, ws.max_row + 1):
        bruto = ws.cell(l, 1).value
        if not isinstance(bruto, str) or not bruto.strip():
            continue
        texto = bruto.rstrip()
        esp = texto.strip()
        if len(esp) < 4 or esp.startswith(IGNORAR):
            continue
        indent = len(texto) - len(texto.lstrip())
        filtro = ws.cell(l, 2).value
        filtro = str(filtro).strip() if filtro is not None else ""
        criterio = ws.cell(l, 3).value
        criterio = str(criterio).strip() if criterio is not None else ""
        saida.append({"linha": l, "indent": indent, "esp": esp,
                      "filtro": filtro, "criterio": criterio, "valor": None})
    return saida


def conta_pontuada(texto):
    """Extrai prefixos de conta de um critério textual."""
    prefixos = []
    for m in re.finditer(r"\b(\d(?:\.\d+){4,})\b", texto or ""):
        prefixos.append(m.group(1).replace(".", ""))
    return prefixos


def apurar_mes(acervo, ano, mes, filtros):
    """Soma por linha num mês."""
    tot = 0.0
    for r in acervo.ler(ano, mes):
        conta = r.conta or ""
        ok = False
        for f in filtros:
            if f.invalido:
                continue
            if any(c.casar(r) for c in f.condicoes):
                ok = True
                break
        if ok:
            tot += r.liquido
    return tot


def main(ano: int, bimestre: int) -> int:
    caminho, wb = abrir()
    if wb is None:
        print("mapeamento do Anexo 3 não encontrado")
        return 1
    aba = "Anexo 3 - RCL Estados"
    ws = wb[aba] if aba in wb.sheetnames else wb[wb.sheetnames[0]]
    linhas = ler_linhas(ws)
    print(f"mapeamento: {os.path.basename(caminho)}")
    print(f"linhas: {len(linhas)}")

    acervo = Acervo(ACERVO)
    janela = periodos_janela(ano, bimestre * 2)
    print(f"janela: {janela[0][0]}-{janela[0][1]:02d} a {janela[-1][0]}-{janela[-1][1]:02d}")

    # filtra por conta (6.2.1.2 e 6.2.1.3) e NR corrente
    f_conta = F.interpretar("6.2.1.2.0.00.00")
    fnr = F.interpretar("NR começada por 1,2")

    # apura cada linha folha (com filtro de NR)
    for ln in linhas:
        fl = F.interpretar(ln["filtro"])
        if fl.invalido:
            # "Mapeamento na célula": usa o critério textual
            prefixos = conta_pontuada(ln["criterio"])
            if prefixos:
                # quando o criterio cita varias contas com "e", a linha e a
                # primeira (a segunda e a forma alternativa de apuracao)
                ln["prefixos"] = prefixos[:1]
            continue
        ln["filtro_obj"] = fl

    def valor_linha(ln, ano_m, mes_m) -> float:
        # linhas de deducao ("Mapeamento na celula") trazem a propria conta
        # no criterio (6213...) e nao devem passar pelo filtro f_conta (6212)
        usar_fconta = "prefixos" not in ln
        tot = 0.0
        for r in acervo.ler(ano_m, mes_m):
            if usar_fconta and not f_conta.invalido and                     not any(c.casar(r) for c in f_conta.condicoes):
                continue
            if "filtro_obj" in ln:
                if not ln["filtro_obj"].aplicar(r):
                    continue
            elif "prefixos" in ln:
                if not any((r.conta or "").startswith(p) for p in ln["prefixos"]):
                    continue
            else:
                continue
            # nas linhas de deducao a conta e devedora; o liquido (C-D) vem
            # negativo, mas a linha do anexo e positiva
            tot += (-r.liquido if "prefixos" in ln else r.liquido)
        return tot

    # O A3 tem 12 colunas mensais: comparamos a coluna <MR> (o mes de
    # referencia), nao o acumulado da janela.
    ano_ref, mes_ref = janela[-1]
    for ln in linhas:
        ln["valor"] = valor_linha(ln, ano_ref, mes_ref)

    # hierarquia: linhas de fórmula = soma das filhas
    n = len(linhas)
    for i in range(n - 1, -1, -1):
        ln = linhas[i]
        if "filtro_obj" in ln or "prefixos" in ln:
            continue
        filhos = []
        j = i + 1
        while j < n and linhas[j]["indent"] > ln["indent"]:
            filhos.append(j)
            j += 1
        diretos = []
        for k in filhos:
            if not diretos or linhas[k]["indent"] == linhas[diretos[0]]["indent"]:
                diretos.append(k)
        if diretos:
            valores = [linhas[k]["valor"] or 0.0 for k in diretos]
            if "LÍQUIDA (III)" in ln["esp"].upper() or "(III) = (I" in ln["esp"].upper():
                # RCL = receitas correntes (I) - deducoes (II)
                ln["valor"] = (valores[0] - sum(valores[1:])) if valores else 0.0
            else:
                ln["valor"] = sum(valores)

    # A RCL (III) nao e filha de ninguem: e (I) - (II), ambas de nivel 0.
    receitas = next((x["valor"] for x in linhas
                     if x["esp"].startswith("RECEITAS CORRENTES (I)")), None)
    deducoes = next((x["valor"] for x in linhas
                     if x["esp"].startswith("DEDUÇÕES (II)")), None)
    for x in linhas:
        if "LÍQUIDA (III)" in x["esp"].upper() and "RECEITA CORRENTE" in x["esp"].upper():
            if receitas is not None and deducoes is not None:
                x["valor"] = receitas - deducoes

    # homólogo
    h = S.rreo("RREO-Anexo 03", ano, bimestre)

    out = Workbook()
    w = out.active
    w.sheet_view.showGridLines = False
    w["A1"] = f"RREO Anexo 3 — RCL {ano} B{bimestre}"
    w["A1"].font = Font(name="Arial", size=12, bold=True)
    for j, (t, larg) in enumerate((("Especificação", 56), ("MSC", 20),
                                   ("Homologado (<MR>)", 20), ("%", 10),
                                   ("Situação", 14)), 1):
        c = w.cell(3, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        w.column_dimensions[chr(64 + j)].width = larg

    r = 4
    n_ok = n_div = 0
    for ln in linhas:
        of = h.valor(ln["esp"], "<MR>", prefixo=True)
        pct = (ln["valor"] - of) / of if (of and abs(of) > 1) else None
        sit, cor = classif(pct)
        if pct is not None:
            if sit in ("fecha", "confere"):
                n_ok += 1
            elif sit == "divergente":
                n_div += 1
        w.cell(r, 1, ("  " * (ln["indent"] // 4)) + ln["esp"][:54]).font = \
            Font(name="Arial", size=8)
        c = w.cell(r, 2, round(ln["valor"], 2))
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
            print(f"   {ln['esp'][:44]:44} {ln['valor']:>18,.2f} "
                  f"{of:>18,.2f} {pct*100:>+8.2f}% {sit}")
        r += 1

    destino = os.path.join(RAIZ, "saida", f"RREO_A3_{ano}_B{bimestre}.xlsx")
    out.save(destino)
    print()
    print(f"fecham: {n_ok} | divergem: {n_div}")
    print(f"gerado: {destino}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=4)
    a = ap.parse_args()
    raise SystemExit(main(a.ano, a.bimestre))
