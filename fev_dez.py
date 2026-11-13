# -*- coding: utf-8 -*-
"""Por que fevereiro/2025 fica 109 mi abaixo e dezembro 63 mi acima?"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn\RGF\2025\RGF_24_2025_quad3_anexo01.csv")
COLUNAS = {2: "<MR-10>", 12: "<MR>"}

ROTULOS = {
    "vencimentos": "Vencimentos, Vantagens e Outras Despesas Variáveis",
    "patronal": "Obrigações Patronais",
    "aposentadorias": "Aposentadorias, Reserva e Reformas",
    "pensoes": "Pensões",
}


def main() -> int:
    of = {}
    with open(RGF, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            of.setdefault(r["coluna"], {})[r["conta"]] = float(r["valor"])

    acervo = M.Acervo(MSC)
    for mes in (2, 12):
        res = M.apurar(acervo, 2025, [mes])
        ne = M.nao_executada(acervo, [(2025, mes)])
        col = COLUNAS[mes]
        print(f"\n2025-{mes:02d}  (coluna {col})")
        print(f"{'linha':<50}{'oficial':>18}{'MSC':>18}{'dif':>16}")
        for chave, rotulo in ROTULOS.items():
            o = of[col].get(rotulo, 0.0)
            v = res.get(chave)
            print(f"{rotulo[:48]:<50}{o:>18,.2f}{v:>18,.2f}{v - o:>16,.2f}")
        o = of[col].get("DESPESA BRUTA COM PESSOAL (I)", 0.0)
        v = (res.get("vencimentos") + res.get("judiciais") + res.get("patronal")
             + res.get("aposentadorias") + res.get("pensoes")
             + res.get("terceirizacao") + ne)
        print(f"{'I':<50}{o:>18,.2f}{v:>18,.2f}{v - o:>16,.2f}")
        print(f"{'  (não executada do mês)':<50}{'':>18}{ne:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
