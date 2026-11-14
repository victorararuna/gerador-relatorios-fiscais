# -*- coding: utf-8 -*-
"""Gera o kit de preenchimento: por anexo, cada linha e o valor apurado.

Quando os arquivos oficiais chegarem, o preenchimento e mecanico: cada linha do
demonstrativo tem um valor ja apurado e conferido aqui.

Uso:
    python preenchimento.py
"""
from __future__ import annotations

import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

#: orcamento do arquivo: grupos na ordem em que aparecem no RGF/RREO
ORDEM = (
    "RGF Anexo 1 - 2026",
    "RGF Anexo 1 - rubricas",
    "RGF Anexo 1 - totais",
    "RGF Anexo 1 - por Poder",
    "RGF Anexo 1 - limites",
    "RGF Anexo 2",
    "RGF Anexo 2 - somas",
    "RGF Anexo 3 - 2025",
    "RGF Anexo 4 - 2025",
    "RGF Anexo 5",
    "RGF Anexo 5 - totais",
    "RGF Anexo 6 - 2025",
    "RGF Anexo 6",
    "RGF Anexo 2 - 2026",
    "RGF Anexo 3 - 2026",
    "RREO Anexo 1",
    "RREO Anexo 2",
    "RREO Anexo 2 - totais",
    "RREO Anexo 3",
    "RREO Anexo 4",
    "RREO Anexo 7",
    "RREO Anexo 9",
    "RREO Anexo 13",
    "RREO Anexo 13 - projeções",
    "RREO Anexo 14",
    "RREO Anexo 2 - 2026",
    "RREO Anexo 7 - 2026",
    "RREO Anexo 14 - 2026",
)


def _brl(v: float) -> str:
    return f"{v:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def main() -> int:
    import verificacao as V

    grupos = V._grupos()
    linhas = [
        "# Kit de preenchimento",
        "",
        "Gerado por `preenchimento.py` a partir do motor. **Cada linha traz o valor",
        "apurado e conferido** — quando o arquivo oficial chegar, é copiar.",
        "",
        f"Total: **{sum(len(g) for g in grupos.values())} linhas** em "
        f"{len(grupos)} grupos.",
        "",
        "> Valores em reais. `OK` = confere com o publicado ao centavo; "
        "`DIF` = divergente, com causa em `docs/DIVERGENCIAS.md`.",
        "",
    ]

    nomes = [n for n in ORDEM if n in grupos]
    nomes += [n for n in grupos if n not in nomes]

    for nome in nomes:
        itens = grupos[nome]
        if not itens:
            continue
        linhas += [f"## {nome}", "", "| linha | valor apurado | |", "|---|---:|---|"]
        for x in itens:
            marca = "OK" if x["ok"] else "DIF"
            linhas.append(f"| {x['item']} | {_brl(x['apurado'])} | {marca} |")
        linhas.append("")

    destino = os.path.join(RAIZ, "docs", "PREENCHIMENTO.md")
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))
    print(f"ok -> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
