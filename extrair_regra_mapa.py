# -*- coding: utf-8 -*-
"""Extrai a regra de composicao de cada rubrica do MAPA do auditor (passo 1).

O MAPA (`aba Mapeamento`) tem uma secao por rubrica, e dentro dela uma linha por
natureza. A ordem das linhas e a propria regra: o que esta entre o titulo e o
proximo titulo entra na rubrica.

Secoes no workbook de 2026 Q2:
    L8    Vencimentos          -> L9  a L101
    L102  Obrigacoes Patronais -> L103 a L180
    L182  Aposentadorias       -> L183 a L208
    L209  Pensoes              -> L210 a L244

Uso:
    python extrair_regra_mapa.py "caminho\\do\\RGF 2026_Q2_01 ....xlsx"
"""
from __future__ import annotations

import json
import os
import re
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_regra_auditor.json")

#: titulo -> (linhas que SOMAM, linhas que SUBTRAEM)
#:
#: No patronal, as linhas 164 a 180 sao **memoria** do expurgo: o valor publicado
#: ja e o liquido das linhas 103 a 163. Nas de inativos e pensoes, o expurgo
#: (ultimas linhas) e subtraido de verdade.
SECOES = {
    "vencimentos": ((9, 101), None),
    "patronal": ((103, 163), None),
    "memo_expurgo_patronal": ((164, 180), None),
    "aposentadorias": ((183, 202), (203, 208)),
    "pensoes": ((210, 227), (228, 244)),
}


def _natureza(rotulo: str) -> str | None:
    """Devolve o codigo da natureza da linha, ou None se nao for detalhe."""
    limpo = rotulo.replace("(-)", "").replace("(+)", "").strip()
    m = re.match(r"^(\d{2}\.(?:XX|\d{2})\.\d{2}\.\d{2})", limpo)
    return m.group(1) if m else None


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python extrair_regra_mapa.py <arquivo.xlsx>")
        return 2

    wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
    ws = wb["Mapeamento"]

    saida = {"fonte": os.path.basename(sys.argv[1]), "secoes": {}}
    for nome, (soma, subtrai) in SECOES.items():
        linhas = []
        for faixa, sinal_base in ((soma, 1.0), (subtrai, -1.0)):
            if faixa is None:
                continue
            for r in range(faixa[0], faixa[1] + 1):
                rotulo = ws.cell(r, 2).value
                if not isinstance(rotulo, str) or not rotulo.strip():
                    continue
                codigo = _natureza(rotulo)
                if codigo is None:
                    continue
                sinal = -sinal_base if "(-)" in rotulo else sinal_base
                linhas.append({"linha": r, "codigo": codigo, "sinal": sinal,
                               "rotulo": rotulo.strip()})
        saida["secoes"][nome] = linhas

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=1)

    print(f"{len(saida['secoes'])} secoes extraidas")
    for nome, linhas in saida["secoes"].items():
        entram = sum(1 for x in linhas if x["sinal"] > 0)
        saem = sum(1 for x in linhas if x["sinal"] < 0)
        print(f"   {nome:<16}{len(linhas):>4} linhas ({entram} entram, {saem} saem)")
    print(f"\nok -> {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
