# -*- coding: utf-8 -*-
"""Anexo 2 (DCL): reconciliação por componente — oficial x contas candidatas."""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
RGF = (r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code"
       r"\siconfi_rn\RGF\2025\RGF_24_2025_quad3_anexo02.csv")
COLUNA = "Até o 3º Quadrimestre"

# candidatos por componente (códigos de 9 dígitos da MSC)
COMPONENTES = {
    "Precatórios": ("221110302", "221110303"),
    "Dívida Contratual/Empréstimos": ("222210200", "222110298", "222130401",
                                      "223110103", "223110402", "223110403"),
    "Outras Dívidas": ("218910106", "218810110", "218910200", "218919800"),
}


def oficial():
    d = {}
    with open(RGF, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == COLUNA:
                d.setdefault(r["conta"], float(r["valor"]))
    return d


def saldos():
    acervo = M.Acervo(MSC)
    s = {}
    for r in acervo.ler(2025, 12, classe=2, tipo_valor="ending_balance"):
        s[r.conta] = s.get(r.conta, 0.0) + r.liquido
    return s


def main() -> int:
    of = oficial()
    s = saldos()

    print(f"{'componente':<34}{'oficial':>18}{'MSC':>18}{'dif':>16}")
    total_of = total_ms = 0.0
    for nome, contas in COMPONENTES.items():
        ms = sum(s.get(c, 0.0) for c in contas)
        # o oficial não tem linha com esse nome exato: usa os blocos conhecidos
        total_ms += ms
        print(f"{nome:<34}{'':>18}{ms:>18,.2f}")
        for c in contas:
            print(f"    {c:<30}{'':>18}{s.get(c, 0.0):>18,.2f}")

    blocos = {
        "Precatórios Posteriores a 05/05/2000 (inclusive) Vencidos e Não Pagos": None,
        "Dívida Contratual": None,
        "Outras Dívidas": None,
        "DÍVIDA CONSOLIDADA - DC (I)": None,
        "DEDUÇÕES (II)": None,
        "DÍVIDA CONSOLIDADA LÍQUIDA (DCL) (III) = (I - II)": None,
        "RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DE ENDIVIDAMENTO (VI) = (IV -": None,
    }
    print(f"\n{'bloco oficial':<66}{'valor':>18}")
    for k in blocos:
        for conta, v in of.items():
            if conta.startswith(k[:40]):
                print(f"{conta[:64]:<66}{v:>18,.2f}")
                break
    print(f"\nsoma dos candidatos = {total_ms:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
