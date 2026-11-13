# -*- coding: utf-8 -*-
"""Valida o de-para do Anexo 1 nas três janelas de 12 meses possíveis.

* 2025 Q3 — jan/2025 a dez/2025
* 2026 Q1 — mai/2025 a abr/2026
* 2026 Q2 — set/2025 a ago/2026
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from app.anexo1_msc import (MES_DO_QUADRIMESTRE, PO_EXECUTIVO,  # noqa: E402
                            apurar_janela, conferir, nao_executada)

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF_DIR = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
           r"\siconfi_rn\RGF")

CASOS = [(2025, 3), (2026, 1), (2026, 2)]


def caminho_rgf(ano: int, quad: int) -> str:
    return os.path.join(RGF_DIR, str(ano),
                        f"RGF_24_{ano}_quad{quad}_anexo01.csv")


def main() -> int:
    acervo_raiz = MSC
    import app.anexo1_msc as M

    acervo = M.Acervo(acervo_raiz)

    for filtrar in (False, True):
        print("=" * 104)
        print(f"filtro de CO em aposentadorias/pensões: {'SIM' if filtrar else 'NÃO'}")
        for ano, quad in CASOS:
            arq = caminho_rgf(ano, quad)
            if not os.path.exists(arq):
                print(f"\n{ano} Q{quad}: arquivo ausente")
                continue
            res = apurar_janela(acervo, ano, MES_DO_QUADRIMESTRE[quad],
                                PO_EXECUTIVO, filtrar_co=filtrar)
            ne = nao_executada(acervo, res.periodos, PO_EXECUTIVO)
            ini = f"{res.periodos[0][0]}-{res.periodos[0][1]:02d}"
            fim = f"{res.periodos[-1][0]}-{res.periodos[-1][1]:02d}"
            print(f"\n{ano} Q{quad}  ({ini} a {fim})")
            print(f"{'linha':<50}{'oficial':>18}{'apurado':>18}{'dif':>15}{'%':>8}")
            for rot, of, ms in conferir(res, arq, nao_exec=ne):
                dif = ms - of
                pct = dif / of * 100 if of else float("nan")
                print(f"{rot[:48]:<50}{of:>18,.2f}{ms:>18,.2f}{dif:>15,.2f}{pct:>7.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
