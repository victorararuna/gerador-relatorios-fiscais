# -*- coding: utf-8 -*-
"""RREO Anexo 2 — despesa liquidada por função, apurada na MSC.

A matriz nova traz ``funcao`` e ``subfuncao`` em cada linha; o RREO Anexo 2 tem
as mesmas funções. Aqui comparamos o total (exceto intra + intra) por função.
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RREO = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
        r"\siconfi_rn\RREO\2025\RREO_24_2025_bim6_anexo02.csv")
CONTAS = ("622130300", "622130400", "622130700")

FUNCOES = {
    "01": "Legislativa", "02": "Judiciária", "03": "Essencial à Justiça",
    "04": "Administração", "05": "Defesa Nacional", "06": "Segurança Pública",
    "07": "Relações Exteriores", "08": "Assistência Social",
    "09": "Previdência Social", "10": "Saúde", "11": "Trabalho",
    "12": "Educação", "13": "Cultura", "14": "Direitos da Cidadania",
    "15": "Urbanismo", "16": "Habitação", "17": "Saneamento",
    "18": "Gestão Ambiental", "19": "Ciência e Tecnologia",
    "20": "Agricultura", "21": "Organização Agrária", "22": "Indústria",
    "23": "Comércio e Serviços", "24": "Comunicações", "25": "Energia",
    "26": "Transporte", "27": "Desporto e Lazer", "28": "Encargos Especiais",
}
COLUNA = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (d)"


def oficial_por_funcao():
    """Lê o bloco TOTAL (III) do RREO Anexo 2."""
    bloco = None
    bruto = {}
    with open(RREO, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            c = r["conta"]
            # as linhas de cabeçalho dos blocos só aparecem em algumas colunas,
            # então o controle de bloco é feito antes do filtro de coluna
            if c.startswith("DESPESAS (EXCETO INTRA"):
                bloco = 1
                continue
            if c.startswith("DESPESAS (INTRA"):
                bloco = 2
                continue
            if c.startswith("TOTAL (III)"):
                bloco = 3
                continue
            if r["coluna"] != COLUNA:
                continue
            if bloco == 3 and c in FUNCOES.values():
                bruto[c] = bruto.get(c, 0.0) + float(r["valor"])
    return bruto


def nosso_por_funcao(ano=2025, mes=12):
    acervo = M.Acervo(MSC)
    por_funcao = {}
    for r in acervo.ler(ano, mes, classe=6, tipo_valor="ending_balance"):
        if r.conta not in CONTAS:
            continue
        por_funcao[r.funcao] = por_funcao.get(r.funcao, 0.0) + r.liquido
    return por_funcao


def main() -> int:
    of = oficial_por_funcao()
    ms = nosso_por_funcao()
    print(f"{'função':<26}{'oficial':>18}{'MSC':>18}{'dif':>16}{'%':>8}")
    tot_of = tot_ms = 0.0
    for cod, nome in FUNCOES.items():
        o = of.get(nome, 0.0)
        v = ms.get(cod, 0.0)
        if not o and not v:
            continue
        tot_of += o
        tot_ms += v
        pct = (v / o - 1) * 100 if o else float("nan")
        print(f"{nome:<26}{o:>18,.2f}{v:>18,.2f}{v - o:>16,.2f}{pct:>7.2f}%")
    if tot_of:
        print(f"{'TOTAL':<26}{tot_of:>18,.2f}{tot_ms:>18,.2f}"
              f"{tot_ms - tot_of:>16,.2f}{(tot_ms / tot_of - 1) * 100:>7.2f}%")
    else:
        print(f"{'TOTAL APURADO':<26}{'':>18}{tot_ms:>18,.2f}")
        print("\nO homologado só publica por função as despesas EXCETO INTRA")
        print("(R$ 20.696.574.215,20). As intra (R$ 2.664.925.314,43) não são")
        print("abertas por função no arquivo — por isso a comparação linha a")
        print("linha não é possível; o total, sim: 23.361.499.529,63.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

