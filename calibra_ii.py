# -*- coding: utf-8 -*-
"""Calibração das linhas do grupo II (despesas não computadas)."""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF_DIR = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
           r"\siconfi_rn\RGF")
CASOS = [(2025, 3), (2026, 1), (2026, 2)]

OFICIAIS = {
    "indenizacoes": "Indenizações por Demissão e Incentivos à Demissão Voluntária",
    "judiciais": "Decorrentes de Decisão Judicial de Período Anterior ao da Apuração",
    "exerc_ant": "Despesas de Exercícios Anteriores de Período Anterior ao da Apuração",
    "vinculados": "Inativos e Pensionistas com Recursos Vinculados",
    "enfermagem": "Parcela dedutível referente ao piso salarial do Enfermeiro",
    "total_ii": "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)",
}


def ler_oficiais(ano, quad):
    arq = os.path.join(RGF_DIR, str(ano), f"RGF_24_{ano}_quad{quad}_anexo01.csv")
    saida = {}
    with open(arq, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"].startswith("TOTAL"):
                saida.setdefault(r["conta"], float(r["valor"]))
    return saida


def apurar_componentes(acervo, pares):
    comp = {"indenizacoes": 0.0, "judiciais": 0.0, "exerc_ant": 0.0,
            "exerc_92": 0.0, "exerc_192": 0.0, "exerc_196": 0.0,
            "fr18": 0.0, "fr1800": 0.0, "fr18_co": 0.0,
            "enfermagem_base": 0.0}
    co_benef = M.CO_BENEFICIO
    for ano, mes in pares:
        for r in acervo.ler(ano, mes):
            if r.conta not in M.CONTAS_LIQUIDACAO or r.po not in M.PO_EXECUTIVO:
                continue
            nd = r.nd
            elem = nd[:6]
            if elem == "319094":
                comp["indenizacoes"] += r.liquido
            elif elem == "319091":
                comp["judiciais"] += r.liquido
            elif elem == "319092":
                comp["exerc_92"] += r.liquido
            elif elem == "319192":
                comp["exerc_192"] += r.liquido
            elif elem == "319196":
                comp["exerc_196"] += r.liquido
            if elem in ("319001", "319003") and r.fr.startswith("18"):
                comp["fr18"] += r.liquido
                if r.fr == "1800":
                    comp["fr1800"] += r.liquido
                if r.compl in co_benef:
                    comp["fr18_co"] += r.liquido
            if r.fr.startswith("1605"):
                comp["enfermagem_base"] += r.liquido
    return comp


def main() -> int:
    acervo = M.Acervo(MSC)
    print(f"{'componente':<32}" + "".join(f"{f'{a}Q{q}':>18}" for a, q in CASOS))
    linhas = {}
    for ano, quad in CASOS:
        pares = M.periodos_janela(ano, M.MES_DO_QUADRIMESTRE[quad])
        linhas[(ano, quad)] = apurar_componentes(acervo, pares)

    for chave in ("indenizacoes", "judiciais", "exerc_92", "exerc_192",
                  "exerc_196", "fr18", "fr1800", "fr18_co", "enfermagem_base"):
        print(f"{chave:<32}" + "".join(f"{linhas[c][chave]:>18,.2f}" for c in CASOS))

    print(f"\n{'oficial':<32}" + "".join(f"{f'{a}Q{q}':>18}" for a, q in CASOS))
    ofs = {c: ler_oficiais(*c) for c in CASOS}
    for chave, rotulo in OFICIAIS.items():
        if chave == "total_ii":
            continue
        print(f"{chave:<32}" + "".join(f"{ofs[c].get(rotulo, 0.0):>18,.2f}" for c in CASOS))

    print("\nfaixas de dedução da enfermagem (base x percentual):")
    for c in CASOS:
        base = linhas[c]["enfermagem_base"]
        of = ofs[c].get(OFICIAIS["enfermagem"], 0.0)
        print(f"   {c[0]}Q{c[1]}  base={base:,.2f}  oficial={of:,.2f}  "
              f"razão={of / base if base else 0:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
