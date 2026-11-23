# -*- coding: utf-8 -*-
"""Reconstroi a pasta MSC no formato antigo a partir do acervo (rodada 173).

A pasta `siconfi_rn_msc` que ficava em `AppData\\...\\Microsoft VS Code` sumiu.
Os modulos do caminho atual (`verificar_tudo`, `rreo_anexo2/7/9/14`,
`nao_executada`) leem a MSC pelo `app/leitor_msc.py`, que espera o nome
`MSC_24_<ano>_m<mm>_MSCC_msc_<grupo>_classe<n>_<tipo>.csv` e separador `;`.

O acervo (`dados/acervo`) tem os mesmos dados no formato longo, mas com nome
`RN_<ano>_<mm>_classe<n>_<tipo>.csv` e separador misto (`;` nos originais, `,`
nos baixados da API). Este script le o acervo, normaliza o separador e grava a
pasta `dados/siconfi_rn_msc` no formato que o leitor antigo espera.

Uso:
    python reconstruir_msc.py
"""
from __future__ import annotations

import csv
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")
DESTINO = os.path.join(RAIZ, "dados", "siconfi_rn_msc")

#: classe -> grupo do nome antigo
GRUPO = {1: "patrimonial", 2: "patrimonial", 3: "patrimonial", 4: "patrimonial",
         5: "orcamentaria", 6: "orcamentaria", 7: "controle", 8: "controle"}

PADRAO = re.compile(r"^RN_(\d{4})_(\d{2})_classe(\d)_(ending_balance|period_change)\.csv$")


def main() -> int:
    if not os.path.isdir(ACERVO):
        print(f"acervo inexistente: {ACERVO}")
        return 2
    feitos = 0
    for ano in sorted(os.listdir(ACERVO)):
        pasta = os.path.join(ACERVO, ano)
        if not os.path.isdir(pasta):
            continue
        destino_ano = os.path.join(DESTINO, ano)
        os.makedirs(destino_ano, exist_ok=True)
        for nome in sorted(os.listdir(pasta)):
            m = PADRAO.match(nome)
            if not m:
                continue
            a, mm, classe, tipo = m.groups()
            classe = int(classe)
            origem = os.path.join(pasta, nome)
            with open(origem, encoding="utf-8", newline="") as fh:
                cab = fh.readline()
                fh.seek(0)
                sep = ";" if cab.count(";") > cab.count(",") else ","
                leitor = csv.DictReader(fh, delimiter=sep)
                campos = leitor.fieldnames
                linhas = list(leitor)
            saida = os.path.join(
                destino_ano,
                f"MSC_24_{a}_m{mm}_MSCC_msc_{GRUPO[classe]}_classe{classe}_{tipo}.csv")
            with open(saida, "w", encoding="utf-8", newline="") as fh:
                esc = csv.DictWriter(fh, fieldnames=campos, delimiter=";",
                                     extrasaction="ignore")
                esc.writeheader()
                esc.writerows(linhas)
            feitos += 1
    print(f"{feitos} arquivos reconstituidos em {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
