# -*- coding: utf-8 -*-
"""Extrai do MDF/instruções as páginas que tratam do Anexo 2 (DCL)."""
from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

from leitor_pdf import ler_pdf  # noqa: E402

ALVOS = ("Dívida Consolidada", "Divida Consolidada", "Anexo 2", "ANEXO 2")


def main() -> int:
    caminho = sys.argv[1]
    print(f"lendo {os.path.basename(caminho)} ({os.path.getsize(caminho)/1e6:.1f} MB)")
    paginas = ler_pdf(caminho)
    print(f"páginas: {len(paginas)}")
    achadas = []
    for p in paginas:
        t = p.texto()
        if any(a in t for a in ALVOS):
            achadas.append(p)
    print(f"páginas com menção: {[p.numero for p in achadas][:40]}")
    for p in achadas[:3]:
        t = re.sub(r"\s+", " ", p.texto())
        print(f"\n--- página {p.numero} ---\n{t[:1500]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
