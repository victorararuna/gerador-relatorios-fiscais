# -*- coding: utf-8 -*-
"""Expurgo do Anexo 1 — aposentadorias e pensões dos demais Poderes no IEO.

Regra (verificada contra a planilha da equipe, set/2026):

    expurgo = aposentadorias (31.90.01, fonte 0.8.00)
            + pensões        (31.90.03, fonte 0.8.00)
            + patronal       (31.91.13, fonte 0.5.00)
    dos Poderes: 218401 DPRN, 221201 TJRN, 222201 ALRN,
                 222401 MPRN, 222501 TCE

O IEO quebra cada registro em várias linhas físicas, então a leitura usa a
geometria do PDF: y identifica a linha, x identifica a coluna.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

BASE = r"C:\Users\victo\Downloads\Arquivos etonjones"
PODERES = {"218401": "DPRN", "221201": "TJRN", "222201": "ALRN",
           "222401": "MPRN", "222501": "TCE"}
UG = "162233"

RE_CODIGO = re.compile(r"^(\d{6})(?:\s|$)")
RE_FONTE = re.compile(r"^(\d\.\d\.\d{2}\.\d{6})(?:\s|$)")
RE_ELEMENTO = re.compile(r"^(\d{2}\.\d{2}\.\d{2})(?:\s|$)")
RE_NUMERO = re.compile(r"^-?\d{1,3}(?:\.\d{3})*,\d{2}$|^-?\d+,\d{2}$")


def _sem_acento(t: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def _num(t: str) -> float:
    return float(t.replace(".", "").replace(",", "."))


def _x_liquidado(pagina) -> float | None:
    for it in pagina.itens:
        if it.texto.strip() == "Liquidado":
            return it.x
    return None


def ler_mes(arquivo: str) -> dict:
    """Poder -> {'aposentadorias','pensoes','patronal'} (coluna Liquidado)."""
    import leitor_pdf as LP

    saida = {p: {"aposentadorias": 0.0, "pensoes": 0.0, "patronal": 0.0}
             for p in PODERES.values()}
    for pagina in LP.ler_pdf(arquivo):
        x_liq = _x_liquidado(pagina)
        if x_liq is None:
            continue
        # agrupa linhas físicas próximas (o IEO quebra o registro em 2-3 linhas)
        por_y = defaultdict(list)
        for it in pagina.itens:
            por_y[round(it.y / 4.0)].append(it)
        poder = fonte = elemento = None
        for y in sorted(por_y, reverse=True):
            itens = sorted(por_y[y], key=lambda i: i.x)
            primeiro = itens[0].texto.strip() if itens else ""
            m = RE_CODIGO.match(primeiro)
            if m and m.group(1) in PODERES:
                poder, fonte, elemento = PODERES[m.group(1)], None, None
            elif m:
                poder, fonte, elemento = None, None, None
            else:
                mf = RE_FONTE.match(primeiro)
                if mf:
                    fonte, elemento = mf.group(1), None
                else:
                    me = RE_ELEMENTO.match(primeiro)
                    if me:
                        elemento = me.group(1)

            if poder is None or elemento is None:
                continue
            numeros = [i for i in itens if RE_NUMERO.match(i.texto.strip())]
            if len(numeros) < 3:
                continue
            alvo = min(numeros, key=lambda i: abs(i.x - x_liq))
            valor = _num(alvo.texto.strip())
            if elemento == "31.90.01" and (fonte or "").startswith("0.8.00"):
                saida[poder]["aposentadorias"] += valor
            elif elemento == "31.90.03" and (fonte or "").startswith("0.8.00"):
                saida[poder]["pensoes"] += valor
            elif elemento == "31.91.13" and (fonte or "").startswith("0.5.00"):
                saida[poder]["patronal"] += valor
    return saida


def total(dados: dict) -> dict:
    return {k: sum(d[k] for d in dados.values())
            for k in ("aposentadorias", "pensoes", "patronal")}


def main() -> int:
    mes = sys.argv[1] if len(sys.argv) > 1 else "Setembro"
    arquivo = os.path.join(BASE, f"Imprimir Execução Orçamentária - IEO_{UG}_{mes}.pdf")
    if not os.path.exists(arquivo):
        print(f"ausente: {arquivo}")
        return 1
    dados = ler_mes(arquivo)
    print(f"IEO {UG} — {mes}")
    print(f"{'Poder':<7}{'aposentadorias':>18}{'pensões':>15}{'patronal':>15}")
    for p in PODERES.values():
        d = dados[p]
        print(f"{p:<7}{d['aposentadorias']:>18,.2f}{d['pensoes']:>15,.2f}{d['patronal']:>15,.2f}")
    t = total(dados)
    soma = t["aposentadorias"] + t["pensoes"] + t["patronal"]
    print(f"{'TOTAL':<7}{t['aposentadorias']:>18,.2f}{t['pensoes']:>15,.2f}{t['patronal']:>15,.2f}")
    print(f"\nexpurgo = {soma:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


