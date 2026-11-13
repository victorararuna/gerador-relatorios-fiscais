# -*- coding: utf-8 -*-
"""Extrai as regras de validação do RGF (PDF da STN) para uma tabela.

    python extrai_regras.py <pdf> <saida.md> [anexo]
"""
from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_pdf import ler_pdf  # noqa: E402

RE_CODIGO = re.compile(r"\bE([A-Z])(\d)(\d{3})\b")
TIPO = {
    "A": "Apuração de valor",
    "C": "Conformidade",
    "D": "Diferença",
    "E": "Equivalência de valores",
    "L": "Apuração de limites",
    "M": "Valor maior que zero",
    "N": "Preenchimento necessário",
    "P": "Apuração percentual",
    "S": "Somatório",
    "V": "Campo vazio",
}


def main() -> int:
    pdf, saida = sys.argv[1], sys.argv[2]
    filtro = sys.argv[3] if len(sys.argv) > 3 else None

    paginas = ler_pdf(pdf)
    texto = "\n".join(p.texto() for p in paginas)
    texto = re.sub(r"[ \t]+", " ", texto)

    achados = list(RE_CODIGO.finditer(texto))
    regras = []
    for i, m in enumerate(achados):
        fim = achados[i + 1].start() if i + 1 < len(achados) else len(texto)
        corpo = texto[m.end():fim].strip()
        regras.append((m.group(0), m.group(1), m.group(2),
                       re.sub(r"\s+", " ", corpo)))

    if filtro:
        regras = [r for r in regras if r[2] == filtro]

    with open(saida, "w", encoding="utf-8") as fh:
        fh.write(f"# Regras de validação — {os.path.basename(pdf)}\n\n")
        fh.write(f"{len(regras)} regras extraídas.\n\n")
        fh.write("| código | tipo | mensagem |\n|---|---|---|\n")
        for codigo, tipo, anexo, corpo in regras:
            fh.write(f"| `{codigo}` | {TIPO.get(tipo, tipo)} | "
                     f"{corpo[:400].replace('|', '/')} |\n")

    print(f"{len(regras)} regras -> {saida}")
    por_tipo = {}
    for _, tipo, _, _ in regras:
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    print("por tipo:", por_tipo)
    por_anexo = {}
    for _, _, anexo, _ in regras:
        por_anexo[anexo] = por_anexo.get(anexo, 0) + 1
    print("por anexo:", por_anexo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
