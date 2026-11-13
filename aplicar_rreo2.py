# -*- coding: utf-8 -*-
"""Aplica os mapeamentos do RREO com cálculo hierárquico.

Os anexos têm dois tipos de linha:

* **apurada por filtro** — o mapeamento dá conta + natureza, e o valor sai da
  MSC;
* **calculada** — o mapeamento diz "Resultado de fórmula", e o valor é a soma
  das linhas **filhas**, identificadas pela indentação da coluna 1.

Este módulo lê a hierarquia pela indentação, apura as folhas e soma os ramos.

Uso:

    python aplicar_rreo2.py --anexo "RREO - ANEXO 03" --ano 2026 --bimestre 4
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
from acervo import Acervo

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")
MAPEAMENTOS = os.path.join(RAIZ, "dados", "mapeamentos", "rreo")

IGNORAR = ("Atualiz", "Tabela", "<", "RELAT", "DEMON", "ORÇAM", "RREO -",
           "ESPECIF", "Critérios", "FILTROS",
           "ACIMA DA", "ABAIXO DA", "IDENTIFICAÇÃO")


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


def normalizar(t: str) -> str:
    t = unicodedata.normalize("NFKD", t or "")
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^a-z0-9 ()/=+-]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def abrir(chave: str):
    for p in glob.glob(os.path.join(MAPEAMENTOS, "**", "*.xlsx"), recursive=True):
        if chave.upper() in os.path.basename(p).upper():
            return p, openpyxl.load_workbook(p, data_only=True)
    return None, None


def coluna_alvo(ws, linha_crit: int) -> int:
    """Escolhe a coluna acumulada da seção, pela especificidade da conta.

    As colunas de um bloco têm critérios diferentes (dotação, empenhada,
    liquidada, paga). A comparação com o homologado usa a **liquidada** na
    despesa e a **realizada** na receita — ambas marcadas "SEM MÊS".
    """
    melhor, score = 0, -1
    for c in range(4, ws.max_column + 1):
        v = str(ws.cell(linha_crit, c).value or "")
        if not v.upper().startswith("CC"):
            continue
        u = v.upper()
        if "SEM MÊS" not in u and "SEM MES" not in u:
            continue
        if "6221303" in v or "6221304" in v:
            s = 3
        elif "6212" in v:
            s = 2
        elif "62213" in v:
            s = 1
        else:
            continue
        if s > score:
            melhor, score = c, s
    return melhor


def linha_de_criterio(ws) -> list:
    """Linhas do mapeamento que trazem critérios de conta utilizáveis.

    Só entram as linhas que têm uma **coluna acumulada** com critério de conta:
    as linhas 96/97, por exemplo, só descrevem as colunas de saldo e não marcam
    início de bloco.
    """
    linhas = []
    for l in range(1, ws.max_row + 1):
        for c in range(4, ws.max_column + 1):
            v = ws.cell(l, c).value
            if isinstance(v, str) and v.strip().upper().startswith("CC"):
                if coluna_alvo(ws, l):
                    linhas.append(l)
                break
    return linhas


def criterio_da_linha(ws, linha_excel: int, criterios: list) -> str:
    """O critério da seção a que a linha pertence (o mais próximo acima)."""
    acima = [l for l in criterios if l <= linha_excel]
    if not acima:
        return ""
    base = max(acima)
    col = coluna_alvo(ws, base)
    v = ws.cell(base, col).value if col else None
    return str(v).strip() if isinstance(v, str) else ""


def criterio_conta(ws, coluna: int = 0) -> str:
    """O critério de conta da coluna que se quer apurar.

    O mapeamento é uma grade: cada coluna do anexo tem o **seu** critério de
    conta na linha 15. A coluna pedida vem por argumento; sem ela, procura-se a
    coluna "(c)" (Até o Bimestre), que é a acumulada — a que se compara com o
    homologado. Antes isto pegava a primeira coluna (Previsão Inicial, conta
    5211) e por isso toda a apuração saía zerada.
    """
    if coluna:
        v = ws.cell(15, coluna).value
        return str(v).strip() if isinstance(v, str) else ""
    # coluna acumulada: linha 13 traz "(c)"
    for c in range(2, ws.max_column + 1):
        rotulo = ws.cell(13, c).value
        if isinstance(rotulo, str) and rotulo.strip().lower() == "(c)":
            v = ws.cell(15, c).value
            if isinstance(v, str) and "CC" in v.upper():
                return v.strip()
    # sem rótulo: última coluna com critério de conta
    for c in range(ws.max_column, 1, -1):
        v = ws.cell(15, c).value
        if isinstance(v, str) and "CC" in v.upper():
            return v.strip()
    return ""


def ler_linhas(ws, criterios: list | None = None) -> list:
    """(indentação, especificação, filtro, valor, linha, bloco) de cada linha.

    O mapeamento tem **vários blocos** (receita, despesa, intra-receita,
    intra-despesa), cada um com sua própria linha de critérios. O bloco entra na
    estrutura para que a hierarquia não misture rótulos repetidos entre blocos.
    """
    criterios = criterios or []
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
        bloco = max([c for c in criterios if c <= l], default=0)
        saida.append([indent, esp, filtro, None, l, bloco])
    return saida


def apurar_linha(acervo, meses, crit_conta, filtro_linha) -> float:
    fc = F.interpretar(crit_conta)
    fl = F.interpretar(filtro_linha)
    tot = 0.0
    for m in meses:
        if not acervo.tem(2026 if ano_global == 2026 else ano_global, m):
            continue
        for r in acervo.ler(ano_global, m):
            if not fc.invalido and not any(c.casar(r) for c in fc.condicoes):
                continue
            if not fl.invalido and not fl.aplicar(r):
                continue
            tot += r.liquido
    return tot


ano_global = 2026


def calcular_hierarquia(linhas: list) -> None:
    """Ramos = soma dos filhos diretos; folhas = filtro. Hierarquia por bloco.

    Filhos só valem dentro do mesmo bloco: o mapeamento repete rótulos nos
    blocos intra, e misturá-los contaminava a soma.
    """
    n = len(linhas)
    for i in range(n - 1, -1, -1):
        indent, esp, filtro, valor, linha_excel, bloco = linhas[i]
        filhos = []
        j = i + 1
        while j < n and linhas[j][5] == bloco and linhas[j][0] > indent:
            filhos.append(j)
            j += 1
        diretos = []
        for k in filhos:
            if not diretos or linhas[k][0] == linhas[diretos[0]][0]:
                diretos.append(k)
        if diretos:
            soma = sum(linhas[k][3] or 0.0 for k in diretos)
            # o valor apurado pelo filtro do ramo prevalece quando existe; só se
            # ele vier zerado (filtro insatisfazível) é que se usa a soma
            if not valor:
                linhas[i][3] = soma


def main(anexo_chave: str, ano: int, bimestre: int, coluna: int = 0) -> int:
    global ano_global
    ano_global = ano
    caminho, wb = abrir(anexo_chave)
    if wb is None:
        print(f"mapeamento não encontrado: {anexo_chave}")
        return 1
    ws = wb[wb.sheetnames[0]]
    crit = criterio_conta(ws, coluna)
    criterios = linha_de_criterio(ws)
    linhas = ler_linhas(ws, criterios)
    print(f"mapeamento: {os.path.basename(caminho)}")
    print(f"critério de conta: {crit[:70]}")
    print(f"linhas: {len(linhas)}  blocos: {sorted(set(l[5] for l in linhas))}")

    acervo = Acervo(ACERVO)
    meses = list(range(1, bimestre * 2 + 1))

    # apura as folhas (linhas com filtro válido)
    for ln in linhas:
        indent, esp, filtro, _, linha_excel, _bloco = ln
        fl = F.interpretar(filtro)
        if not fl.invalido:
            crit_ln = criterio_da_linha(ws, linha_excel, criterios) or crit
            ln[3] = apurar_linha(acervo, meses, crit_ln, filtro)

    # soma os ramos
    calcular_hierarquia(linhas)

    # homólogo
    num = re.search(r"ANEXO\s*(\d+)", anexo_chave, re.I)
    tipo = f"RREO-Anexo {int(num.group(1)):02d}" if num else "RREO-Anexo 01"
    try:
        hom = S.rreo(tipo, ano, bimestre)
    except Exception:  # noqa: BLE001
        hom = None
    indice = {}
    if hom is not None:
        for c in hom.contas():
            indice[normalizar(c)] = c

    out = Workbook()
    w = out.active
    w.sheet_view.showGridLines = False
    w["A1"] = f"{anexo_chave} — {ano} B{bimestre}"
    w["A1"].font = Font(name="Arial", size=12, bold=True)
    w["A2"] = f"Conta: {crit[:80]}"
    w["A2"].font = Font(name="Arial", size=8, italic=True)
    for j, (t, larg) in enumerate((("Especificação", 56), ("MSC", 20),
                                   ("Homologado", 20), ("%", 10), ("Situação", 14)), 1):
        c = w.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        w.column_dimensions[chr(64 + j)].width = larg

    r = 5
    n_ok = n_div = 0
    for indent, esp, filtro, valor in (l[:4] for l in linhas):
        of = None
        rot = indice.get(normalizar(esp))
        if hom is not None and rot:
            for col in ("RECEITAS REALIZADAS ATÉ O BIMESTRE (c)",
                        "Até o Bimestre (c)", "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)",
                        "<MR>", "<MR-11>"):
                of = hom.valor(rot, col)
                if of:
                    break
        pct = (valor - of) / of if (of and valor is not None and abs(of) > 1) else None
        sit, cor = classif(pct)
        if pct is not None:
            if sit in ("fecha", "confere"):
                n_ok += 1
            elif sit == "divergente":
                n_div += 1
        w.cell(r, 1, ("   " * (indent // 4)) + esp[:56]).font = Font(name="Arial", size=8)
        c = w.cell(r, 2, round(valor, 2) if valor is not None else "—")
        if valor is not None:
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
        if pct is not None:
            print(f"   {esp[:44]:44} {valor:>18,.2f} {of:>18,.2f} {pct*100:>+8.2f}% {sit}")
        r += 1

    destino = os.path.join(RAIZ, "saida",
                           f"{anexo_chave.replace(' ', '_')}_{ano}_B{bimestre}_h.xlsx")
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
    ap.add_argument("--coluna", type=int, default=0,
                    help="coluna do mapeamento (padrão: a acumulada \"(c)\")")
    a = ap.parse_args()
    raise SystemExit(main(a.anexo, a.ano, a.bimestre))




