# -*- coding: utf-8 -*-
"""Atalho: confere o Anexo 1 (2025 Q3) contra o homologado.

    python verificar_anexo1.py

Equivale a ``app/anexo1_msc.py --raiz <acervo> --ano 2025 --rgf <csv>``.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from app.anexo1_msc import _cli  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn\RGF\2025\RGF_24_2025_quad3_anexo01.csv")

if __name__ == "__main__":
    sys.argv = ["anexo1_msc", "--raiz", MSC, "--ano", "2025", "--rgf", RGF]
    raise SystemExit(_cli())
