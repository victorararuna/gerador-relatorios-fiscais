# -*- coding: utf-8 -*-
"""RREO Anexo 4 — aplica os blocos do mapeamento na ordem certa.

Cada linha do demonstrativo tem dois blocos:

1. **principal** — seleciona por fonte de recursos (FR, posição 2, tamanho 3),
   natureza da despesa (ND) e, quando há, subfunção (FS, posição 3, tamanho 3
   sobre a concatenação função + subfunção);
2. **complementar** — seleciona o que o principal não pega: FR **exceto** uma
   lista, complemento de fonte (CO) numa lista, mesma ND e mesma FS.

A união dos dois é o valor da linha. Aplicar só o principal deixa dinheiro de
fora; aplicar os dois sem controle conta duas vezes.
"""
from __future__ import annotations

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "dados", "acervo", "2025")
LIQ = {"622130300", "622130400", "622130700"}

APOS_CIVIL = {"0101", "0106", "0118", "0151", "0199", "9109", "9115",
              "9123", "9128", "9201", "9403"}
PENS_CIVIL = {"0301", "0303", "0305", "0351", "0399", "9110", "9116",
              "9130", "9136", "9203", "9413"}
PENS_MIL = {"0302", "0304", "0308", "0352", "0389", "9113", "9119",
            "9131", "9137", "9203", "9406"}
INAT_MIL = {"31900121", "31900123", "31900126", "31900152", "31900189",
            "31909112", "31909118", "31909124", "31909129", "31909201",
            "31909291", "31909294", "31909404"}
CO_CIVIL = {"1111", "1121", "1122", "1123", "1124", "1125", "1131",
            "1132", "1141", "1151"}

CIVIL_EXCETO = {"800", "801", "803", "804"}
MIL_EXCETO = {"800", "801", "802", "803", "804"}


def _pos(valor: str, inicial: int, tamanho: int) -> str:
    return (valor or "")[inicial - 1:inicial - 1 + tamanho]


def _fs(reg) -> str:
    """Função + subfunção concatenadas; FS usa a posição 3, tamanho 3."""
    return f"{reg.get('funcao') or ''}{reg.get('subfuncao') or ''}"


def _registros():
    for mes in range(1, 13):
        p = os.path.join(BASE, f"RN_2025_{mes:02d}_classe6_period_change.csv")
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["conta_contabil"] not in LIQ:
                    continue
                yield r


def _valor(r) -> float:
    v = float(r.get("valor") or 0)
    return v if (r.get("natureza_conta") or "").upper().startswith("C") else -v


def apurar(linha: str) -> tuple[float, float]:
    """(bloco principal, incremento do bloco complementar)."""
    principal = complementar = 0.0
    for r in _registros():
        nd = r.get("natureza_despesa") or ""
        fr = _pos(r.get("fonte_recursos") or "", 2, 3)
        co = (r.get("complemento_fonte") or "").strip()
        fs = _pos(_fs(r), 3, 3)
        v = _valor(r)
        if linha == "apos_civil":
            base = nd.startswith("3190") and nd[4:8] in APOS_CIVIL
            if base and fr == "800":
                principal += v
            elif base and fr not in CIVIL_EXCETO and co in CO_CIVIL and fs == "272":
                complementar += v
        elif linha == "pens_civil":
            base = nd.startswith("3190") and nd[4:8] in PENS_CIVIL
            if base and fr == "800":
                principal += v
            elif base and fr not in CIVIL_EXCETO and co in CO_CIVIL and fs == "272":
                complementar += v
        elif linha == "inat_mil":
            base = nd.startswith("3190") and nd in INAT_MIL
            if base and fr == "803":
                principal += v
            elif base and fr not in MIL_EXCETO and co == "2211" and fs == "274":
                complementar += v
        elif linha == "pens_mil":
            base = nd.startswith("3190") and nd[4:8] in PENS_MIL
            if base and fr == "803":
                principal += v
            elif base and fr not in MIL_EXCETO and co == "2211" and fs == "274":
                complementar += v
    return principal, complementar


OFICIAL = {
    "apos_civil": ("Aposentadorias civis", 4_917_756_724.31),
    "pens_civil": ("Pensões por morte civis", 640_868_408.22),
    "inat_mil": ("Inatividade militar", 675_066_910.71),
    # corrigido: 119.906.956,64 era a linha das pensões militares do bloco
    # principal, não o total; o total publicado é 250.915.256,72
    "pens_mil": ("Pensões militares", 250_915_256.72),
}


def main() -> int:
    print(f"{'linha':<26}{'principal':>18}{'complementar':>16}{'total':>18}"
          f"{'oficial':>18}{'dif':>10}")
    for chave, (nome, oficial) in OFICIAL.items():
        p, c = apurar(chave)
        total = p + c
        print(f"{nome:<26}{p:>18,.2f}{c:>16,.2f}{total:>18,.2f}"
              f"{oficial:>18,.2f}{total - oficial:>10,.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
