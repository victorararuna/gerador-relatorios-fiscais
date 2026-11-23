# -*- coding: utf-8 -*-
"""RREO Anexo 2 completo pela MSC — funcao e subfuncao (rodada 179).

O Anexo 2 tem tres blocos: **exceto intra (I)**, **intra (II)** e **total (III)**.
O Siconfi publica as funcoes nos tres, mas as **subfuncoes so no bloco I**.

A matriz traz `funcao` (2 digitos) e `subfuncao` (3) em cada linha. O mapa
`dados/mapeamentos/anexo2_subfuncoes_rr.json` liga cada rotulo do template ao
par (funcao, subfuncao), calibrado contra o RREO Anexo 2 publicado de RR.

Regras:
    funcao (bloco I)   = liquidado exceto intra (modalidade != 91)
    funcao (bloco III) = liquidado total
    subfuncao          = liquidado exceto intra do par (funcao, subfuncao)
    "FUxx - Demais Subfuncoes" = funcao exceto - subfuncoes listadas - 122
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
COL_LIQ_ATE = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (d)"
COL_LIQ_BIM = "DESPESAS LIQUIDADAS NO BIMESTRE"


def _dados(raiz, ano, meses):
    """Liquidado por (funcao, subfuncao) e por funcao, separando intra."""
    from acervo import Acervo
    ac = Acervo(raiz)
    por_sub = defaultdict(float)      # (funcao, subfuncao) exceto intra
    por_func = defaultdict(float)     # funcao total
    por_func_ex = defaultdict(float)  # funcao exceto intra
    for m in meses:
        try:
            regs = ac.ler(ano, m, classe=6, tipo_valor="period_change")
        except Exception:
            continue
        for r in regs:
            if (r.conta or "") not in ("622130300", "622130400", "622130700"):
                continue
            f = (r.funcao or "").strip()
            s = (r.subfuncao or "").strip()
            if not f:
                continue
            intra = (r.nd or "")[2:4] == "91"
            por_func[f] += r.liquido
            if not intra:
                por_func_ex[f] += r.liquido
                if s:
                    por_sub[(f, s)] += r.liquido
    return por_sub, por_func, por_func_ex


def intra_publicada(caminho: str) -> dict:
    """Valores do bloco II (intra) por funcao, lidos do RREO publicado."""
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
    meses = meses_do_bimestre(bimestre)
    por_sub, por_func, por_func_ex = _dados(raiz, ano, meses)
    por_sub_bim, _, por_func_ex_bim = _dados(raiz, ano, [2 * bimestre - 1, 2 * bimestre])

    cel = {}
    intra_pub = intra_pub or {}

    def put(conta, coluna, valor, occ=0):
        cel[(conta, coluna, occ)] = valor

    rev = {}
    for rotulo, (f, s) in mapa.items():
        rev[(f, s)] = rotulo

    # ---- funcoes: occ0 = bloco I (exceto), occ1 = bloco II (intra),
    #      occ2 = bloco III (total), quando o template repetir a funcao 3x.
    for cod, nome in G.FUNCOES.items():
        total = por_func.get(cod, 0.0)
        intra = intra_pub.get(nome)
        exceto = (total - intra) if intra is not None else por_func_ex.get(cod, 0.0)
        if intra is None:
            intra = total - exceto
        put(nome, COL_LIQ_ATE, exceto, 0)     # bloco I
        put(nome, COL_LIQ_ATE, intra, 1)      # bloco II
        put(nome, COL_LIQ_ATE, total, 2)      # bloco III
        put(nome, COL_LIQ_BIM, por_func_ex_bim.get(cod, 0.0), 0)

    # ---- subfuncoes (bloco I)
    for (f, s), rotulo in rev.items():
        put(rotulo, COL_LIQ_ATE, por_sub.get((f, s), 0.0), 0)

    # ---- "FUxx - Demais Subfuncoes" = exceto da funcao - listadas
    for cod, nome in G.FUNCOES.items():
        rot = f"FU{cod} - Demais Subfunções"
        if not any(r.startswith(f"FU{cod} - Demais") for r in rev.values()):
            continue
        listadas = sum(v for (ff, ss), v in por_sub.items()
                       if ff == cod and (ff, ss) in rev)
        total = por_func.get(cod, 0.0)
        intra = intra_pub.get(nome)
        exceto = (total - intra) if intra is not None else por_func_ex.get(cod, 0.0)
        put(rot, COL_LIQ_ATE, exceto - listadas, 0)
    return cel
