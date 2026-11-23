# -*- coding: utf-8 -*-
"""RREO Anexo 2 completo pela MSC — todas as colunas (rodada 180).

Blocos: **exceto intra (I)**, **intra (II)** e **total (III)**. As funcoes
aparecem nos tres; as subfuncoes so no bloco I.

A matriz sustenta todas as colunas:

    dotacao inicial     = 5.2.2.1.1  (classe 5) por funcao/subfuncao
    dotacao atualizada  = 5.2.2.1.*  (classe 5)
    empenhada           = 6.2.2.1.3.* (classe 6)
    liquidada           = 6.2.2.1.3.03/04/07
    paga                = 6.2.2.1.3.04

A separacao intra x exceto usa a **modalidade da ND** (91 = intra), a mesma do
Anexo 1. O intra por funcao do bloco II pode ser replicado do ultimo Anexo 2
publicado, quando informado.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

MAPA_JSON = os.path.join(RAIZ, "dados", "mapeamentos", "anexo2_subfuncoes_rr.json")

COL_DOT_INI = "DOTAÇÃO INICIAL"
COL_DOT_ATU = "DOTAÇÃO ATUALIZADA (a)"
COL_EMP_BIM = "DESPESAS EMPENHADAS NO BIMESTRE"
COL_EMP_ATE = "DESPESAS EMPENHADAS ATÉ O BIMESTRE (b)"
COL_PCT_B = "% (b/total b)"
COL_SALDO_C = "SALDO (c) = (a-b)"
COL_LIQ_BIM = "DESPESAS LIQUIDADAS NO BIMESTRE"
COL_LIQ_ATE = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (d)"
COL_PCT_D = "% (d/total d)"
COL_SALDO_E = "SALDO (e) = (a-d)"
COL_PCT_B3 = "% (b/III b)"
COL_PCT_D3 = "% (d/III d)"

CONTAS_EMP = "62213"
CONTAS_LIQ = ("622130300", "622130400", "622130700")
CONTA_PAGA = "622130400"

EXCETO = lambda m: m != "91"
INTRA = lambda m: m == "91"
TOTAL = lambda m: True


def _movimento(raiz, ano, meses):
    """(empenhada, liquidada, paga) por (funcao, subfuncao, modalidade)."""
    from acervo import Acervo
    ac = Acervo(raiz)
    emp = defaultdict(float)
    liq = defaultdict(float)
    pag = defaultdict(float)
    for m in meses:
        try:
            regs = ac.ler(ano, m, classe=6, tipo_valor="period_change")
        except Exception:
            continue
        for r in regs:
            c = r.conta or ""
            if not c.startswith(CONTAS_EMP):
                continue
            f = (r.funcao or "").strip()
            if not f:
                continue
            k = (f, (r.subfuncao or "").strip(), (r.nd or "")[2:4])
            emp[k] += r.liquido
            if c in CONTAS_LIQ:
                liq[k] += r.liquido
            if c == CONTA_PAGA:
                pag[k] += r.liquido
    return emp, liq, pag


def _dotacao(raiz, ano, mes):
    """(inicial, atualizada) por (funcao, subfuncao, modalidade)."""
    from acervo import Acervo
    ac = Acervo(raiz)
    ini = defaultdict(float)
    atu = defaultdict(float)
    for r in ac.ler(ano, mes, classe=5, tipo_valor="ending_balance"):
        c = r.conta or ""
        if not c.startswith("5221"):
            continue
        f = (r.funcao or "").strip()
        if not f:
            continue
        k = (f, (r.subfuncao or "").strip(), (r.nd or "")[2:4])
        v = -(r.valor if (r.natureza or "") == "C" else -r.valor)
        if c.startswith("52211"):
            ini[k] += v
        atu[k] += v
    return ini, atu


def _soma(d, f, s, mod_f):
    if s is None:
        return sum(v for k, v in d.items() if k[0] == f and mod_f(k[2]))
    return sum(v for k, v in d.items() if k[0] == f and k[1] == s and mod_f(k[2]))


def intra_publicada(caminho: str) -> dict:
    """Bloco II (intra) por funcao, do RREO publicado."""
    import csv
    bloco = 0
    out = {}
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            c = r["conta"]
            if c.startswith("DESPESAS (EXCETO INTRA"):
                bloco = 1
                continue
            if c.startswith("DESPESAS (INTRA"):
                bloco = 2
                continue
            if c.startswith("TOTAL (III)"):
                bloco = 3
                continue
            if bloco == 2 and r["coluna"] == COL_LIQ_ATE:
                out[c] = float(r["valor"])
    return out


def celulas(raiz: str, ano: int, bimestre: int,
            intra_pub: dict | None = None) -> dict:
    import rreo_gerador as G
    from rreo_gerador import meses_do_bimestre

    if not os.path.exists(MAPA_JSON):
        return {}
    mapa = json.load(open(MAPA_JSON, encoding="utf-8"))
    rev = {(f, s): rotulo for rotulo, (f, s) in mapa.items()}

    meses = meses_do_bimestre(bimestre)
    mes_fim = 2 * bimestre
    emp, liq, pag = _movimento(raiz, ano, meses)
    emp_b, liq_b, _ = _movimento(raiz, ano, [mes_fim - 1, mes_fim])
    dot_ini, dot_atu = _dotacao(raiz, ano, mes_fim)

    tot_emp = sum(emp.values())
    tot_liq = sum(liq.values())

    cel = {}

    def put(conta, coluna, valor, occ=0):
        cel[(conta, coluna, occ)] = valor

    def preencher(nome, f, s, occ, mod_f, liq_ate=None):
        e = _soma(emp, f, s, mod_f)
        eb = _soma(emp_b, f, s, mod_f)
        l = liq_ate if liq_ate is not None else _soma(liq, f, s, mod_f)
        lb = _soma(liq_b, f, s, mod_f)
        di = _soma(dot_ini, f, s, mod_f)
        da = _soma(dot_atu, f, s, mod_f)
        put(nome, COL_DOT_INI, di, occ)
        put(nome, COL_DOT_ATU, da, occ)
        put(nome, COL_EMP_BIM, eb, occ)
        put(nome, COL_EMP_ATE, e, occ)
        put(nome, COL_SALDO_C, da - e, occ)
        put(nome, COL_LIQ_BIM, lb, occ)
        put(nome, COL_LIQ_ATE, l, occ)
        put(nome, COL_SALDO_E, da - l, occ)
        if tot_emp:
            put(nome, COL_PCT_B, e / tot_emp * 100, occ)
            if occ == 2:
                put(nome, COL_PCT_B3, e / tot_emp * 100, occ)
        if tot_liq:
            put(nome, COL_PCT_D, l / tot_liq * 100, occ)
            if occ == 2:
                put(nome, COL_PCT_D3, l / tot_liq * 100, occ)

    # ---- funcoes: occ0 exceto, occ1 intra, occ2 total
    for cod, nome in G.FUNCOES.items():
        preencher(nome, cod, None, 0, EXCETO)
        preencher(nome, cod, None, 1, INTRA)
        preencher(nome, cod, None, 2, TOTAL)

    # ---- subfuncoes (bloco I)
    for (f, s), rotulo in rev.items():
        preencher(rotulo, f, s, 0, EXCETO)

    # ---- "FUxx - Demais Subfuncoes" = funcao exceto - subfuncoes listadas
    for cod, nome in G.FUNCOES.items():
        rot = f"FU{cod} - Demais Subfunções"
        if not any(r.startswith(f"FU{cod} - Demais") for r in rev.values()):
            continue
        def resto(d, lista):
            return _soma(d, cod, None, EXCETO) - sum(
                v for k, v in d.items()
                if k[0] == cod and (k[0], k[1]) in rev and EXCETO(k[2]))
        e = resto(emp, rev)
        eb = resto(emp_b, rev)
        l = resto(liq, rev)
        lb = resto(liq_b, rev)
        di = resto(dot_ini, rev)
        da = resto(dot_atu, rev)
        put(rot, COL_DOT_INI, di, 0)
        put(rot, COL_DOT_ATU, da, 0)
        put(rot, COL_EMP_BIM, eb, 0)
        put(rot, COL_EMP_ATE, e, 0)
        put(rot, COL_SALDO_C, da - e, 0)
        put(rot, COL_LIQ_BIM, lb, 0)
        put(rot, COL_LIQ_ATE, l, 0)
        put(rot, COL_SALDO_E, da - l, 0)
    return cel
