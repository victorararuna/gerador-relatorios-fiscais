# -*- coding: utf-8 -*-
"""Comparação mês a mês: MSC 2025 x RGF 2025 Q3 (Anexo 1, Executivo)."""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_msc import Acervo  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn\RGF\2025\RGF_24_2025_quad3_anexo01.csv")

PO_EXEC = {"10111", "10112", "60611"}
CONTAS = ("622130300", "622130400", "622130700")

LINHA = {
    "319001": "aposentadorias",
    "319003": "pensoes",
    "319011": "vencimentos", "319012": "vencimentos", "319016": "vencimentos",
    "319017": "vencimentos", "319004": "vencimentos", "319007": "vencimentos",
    "319013": "patronal", "319113": "patronal",
    "319091": "judiciais",
    "319092": "exerc_ant", "319192": "exerc_ant", "319096": "exerc_ant",
    "319094": "indenizacoes",
}
COLUNAS = ["<MR-11>", "<MR-10>", "<MR-9>", "<MR-8>", "<MR-7>", "<MR-6>",
           "<MR-5>", "<MR-4>", "<MR-3>", "<MR-2>", "<MR-1>", "<MR>"]


def apurar_meses():
    acervo = Acervo(MSC)
    por_mes = defaultdict(lambda: defaultdict(float))
    for mes in acervo.meses(2025, 6, "period_change"):
        for r in acervo.ler(2025, mes):
            if r.conta not in CONTAS or r.po not in PO_EXEC or not r.nd:
                continue
            if r.nd.startswith("33"):
                if r.nd[:6] == "339034" or r.nd.endswith("34"):
                    por_mes[mes]["terceirizacao"] += r.liquido
                continue
            por_mes[mes][LINHA.get(r.nd[:6], "vencimentos")] += r.liquido
    return por_mes


def oficial():
    tab = defaultdict(dict)
    with open(RGF, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["coluna"] in COLUNAS:
                tab[r["conta"]][r["coluna"]] = float(r["valor"])
    return tab


def main() -> int:
    nosso = apurar_meses()
    of = oficial()

    def soma(mes, keys):
        return sum(nosso[mes][k] for k in keys)

    grupos = [
        ("DESPESA BRUTA (I)", ("vencimentos", "patronal", "aposentadorias",
                               "pensoes", "terceirizacao", "judiciais",
                               "exerc_ant", "indenizacoes")),
        ("Pessoal Ativo", ("vencimentos", "patronal")),
        ("Vencimentos", ("vencimentos",)),
        ("Obrigações Patronais", ("patronal",)),
        ("Inativo e Pensionistas", ("aposentadorias", "pensoes")),
        ("Aposentadorias", ("aposentadorias",)),
        ("Pensões", ("pensoes",)),
        ("Terceirizados", ("terceirizacao",)),
    ]
    rotulos_oficiais = {
        "DESPESA BRUTA (I)": "DESPESA BRUTA COM PESSOAL (I)",
        "Pessoal Ativo": "Pessoal Ativo",
        "Vencimentos": "Vencimentos, Vantagens e Outras Despesas Variáveis",
        "Obrigações Patronais": "Obrigações Patronais",
        "Inativo e Pensionistas": "Pessoal Inativo e Pensionistas",
        "Aposentadorias": "Aposentadorias, Reserva e Reformas",
        "Pensões": "Pensões",
        "Terceirizados": "Outras Despesas de Pessoal decorrentes de Contratos de Terceirizados",
    }

    for nome, chaves in grupos:
        chave_of = rotulos_oficiais[nome]
        if chave_of not in of:
            print(f"\n[{nome}] rótulo oficial não encontrado")
            continue
        print(f"\n{nome}")
        print(f"{'mês':<6}{'oficial':>18}{'MSC':>18}{'dif':>16}{'%':>8}")
        soma_of = soma_msc = 0.0
        for i, col in enumerate(COLUNAS, start=1):
            o = of[chave_of].get(col, 0.0)
            m = soma(i, chaves)
            soma_of += o
            soma_msc += m
            pct = (m / o - 1) * 100 if o else 0.0
            print(f"{i:<6}{o:>18,.2f}{m:>18,.2f}{m - o:>16,.2f}{pct:>7.2f}%")
        pct = (soma_msc / soma_of - 1) * 100 if soma_of else 0.0
        print(f"{'TOT':<6}{soma_of:>18,.2f}{soma_msc:>18,.2f}"
              f"{soma_msc - soma_of:>16,.2f}{pct:>7.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
