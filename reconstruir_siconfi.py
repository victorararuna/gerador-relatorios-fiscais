# -*- coding: utf-8 -*-
"""Reconstroi a pasta dos CSVs publicados no formato antigo (rodada 173).

A pasta `siconfi_rn` (em `AppData\\...\\Microsoft VS Code`) sumiu. Os modulos
`verificar_tudo` e `rreo_anexo2/7/9/14` esperam nomes como
`RREO_24_2025_bim6_anexo02.csv` em `RREO/2025/`.

O repo tem os mesmos CSVs em `dados/siconfi/<tipo>/` com o nome da API
(`RREO_RREO-Anexo_02_24_2025_p6.csv`). Este script copia renomeando para a
estrutura antiga em `dados/siconfi_rn`.

Uso:
    python reconstruir_siconfi.py
"""
from __future__ import annotations

import os
import re
import shutil

RAIZ = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(RAIZ, "dados", "siconfi")
DESTINO = os.path.join(RAIZ, "dados", "siconfi_rn")

#: RGF e quadrimestral (quad), RREO e bimestral (bim)
PREFIXO = {"rgf": "quad", "rreo": "bim"}
PADRAO = re.compile(r"^(RGF|RREO)_(?:RGF|RREO)-Anexo_(\d+)_(\d+)_(\d{4})_p(\d)\.csv$")


def main() -> int:
    if not os.path.isdir(ORIGEM):
        print(f"origem inexistente: {ORIGEM}")
        return 2
    feitos = 0
    for tipo in ("rgf", "rreo"):
        pasta = os.path.join(ORIGEM, tipo)
        if not os.path.isdir(pasta):
            continue
        for nome in sorted(os.listdir(pasta)):
            m = PADRAO.match(nome)
            if not m:
                continue
            sigla, anexo, ibge, ano, periodo = m.groups()
            destino_dir = os.path.join(DESTINO, sigla, ano)
            os.makedirs(destino_dir, exist_ok=True)
            novo = f"{sigla}_{ibge}_{ano}_{PREFIXO[tipo]}{periodo}_anexo{anexo}.csv"
            shutil.copyfile(os.path.join(pasta, nome), os.path.join(destino_dir, novo))
            feitos += 1
    print(f"{feitos} CSVs reconstituidos em {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
