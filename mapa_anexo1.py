# -*- coding: utf-8 -*-
"""MAPA do RGF Anexo 1 — construção a partir dos relatórios do SIGEF/RN.

Aplica a especificação de `docs/MANUAL_MAPA_ANEXO1.md` aos arquivos de
`Arquivos etonjones`:

* **Comparativo** — valor liquidado no mês por natureza de despesa (linha sem
  fonte = soma das modalidades, que é o que a MAPA usa nas linhas "31.XX.");
* **IEO 162233 / 162011** — deduções dos demais Poderes.

Trava do manual: a soma das naturezas do grupo 31 deve bater com a linha
`31.00.00.00` do Comparativo.
"""
from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

BASE = r"C:\Users\victo\Downloads\Arquivos etonjones"
NUM = r"-?\d{1,3}(?:\.\d{3})*,\d{2}"
RE_LINHA = re.compile(
    r"(\d\d\.\d\d\.\d\d\.\d\d)\s+([A-Za-zÀ-ÿ].*?)\s+(" + NUM + r") (?:" + NUM + r" ){6}")

#: aposentadorias — naturezas da parte bruta (MAPA linhas 183 a 202)
APOSENTADORIAS = [
    # usa-se o agregado 31.90.01.00 no lugar dos subelementos: em janeiro/2026
    # ele traz R$ 52.409.610,36 que a abertura por subelemento não evidencia
    "31.90.01.00", "31.90.86.00",
    "31.90.91.03", "31.90.91.09", "31.90.91.12", "31.90.91.15",
    "31.90.91.18", "31.90.91.23", "31.90.91.24", "31.90.91.28",
    "31.90.91.29", "31.90.92.01", "31.90.92.02", "31.90.92.50",
    "31.90.92.86", "31.90.94.03", "31.90.94.04", "31.91.86.00",
]

#: pensões — naturezas da parte bruta (MAPA linhas 210 a 227)
PENSOES = [
    "31.90.03.01", "31.90.03.02", "31.90.03.04", "31.90.03.05",
    "31.90.03.08", "31.90.91.10", "31.90.91.13", "31.90.91.16",
    "31.90.91.19", "31.90.91.30", "31.90.91.31", "31.90.91.36",
    "31.90.91.37", "31.90.92.03", "31.90.92.06", "31.90.94.05",
    "31.90.94.06", "31.90.94.13",
]


def _num(t: str) -> float:
    return float(t.replace(".", "").replace(",", "."))


def ler_comparativo(mes: str, ano: int = 2026) -> dict:
    """natureza (formato 31.90.11.00) -> liquidada no mês.

    Valida o exercício e o mês no cabeçalho antes de somar: uma extração de
    outro período levantaria `ErroFonte` em vez de contaminar a apuração.
    """
    import leitor_pdf as LP
    from fonte_sigef import ErroFonte, ler_cabecalho, validar

    arquivo = os.path.join(
        BASE, f"Comparativo Despesa Autorizada Empenhada Liquidada e Paga_{mes}.pdf")
    paginas = LP.ler_pdf(arquivo)
    cabecalho = re.sub(r"\s+", " ", paginas[0].texto())
    validar(*ler_cabecalho(cabecalho), ano, mes, os.path.basename(arquivo))
    valores = {}
    for pagina in paginas:
        texto = re.sub(r"\s+", " ", pagina.texto())
        for m in RE_LINHA.finditer(texto):
            nums = re.findall(NUM, m.group(0))
            if len(nums) >= 3:
                valores[m.group(1)] = _num(nums[2])
    return valores


def secoes(mes: str) -> dict:
    """As seções da MAPA que já têm regra fechada."""
    import expurgo_poderes as E

    comp = ler_comparativo(mes)
    total_gnd31 = comp.get("31.00.00.00", 0.0)

    bruto_apos = sum(comp.get(nd, 0.0) for nd in APOSENTADORIAS)
    ieo = E.total(E.ler_periodo(mes))
    ded_apos = ieo["aposentadorias"] + ieo["apos_tesouro"]

    bruto_pens = sum(comp.get(nd, 0.0) for nd in PENSOES)
    ded_pens = ieo["pensoes"]

    return {
        "gnd31": total_gnd31,
        "aposentadorias_bruto": bruto_apos,
        "aposentadorias_deducao": ded_apos,
        "aposentadorias": bruto_apos - ded_apos,
        "pensoes_bruto": bruto_pens,
        "pensoes_deducao": ded_pens,
        "pensoes": bruto_pens - ded_pens,
    }


def main() -> int:
    mes = sys.argv[1] if len(sys.argv) > 1 else "Setembro"
    s = secoes(mes)
    print(f"MAPA — {mes}")
    print(f"  GND 31 (trava) ............. {s['gnd31']:>18,.2f}")
    print(f"  aposentadorias bruto ....... {s['aposentadorias_bruto']:>18,.2f}")
    print(f"  (-) dedução ................ {s['aposentadorias_deducao']:>18,.2f}")
    print(f"  aposentadorias líquido ..... {s['aposentadorias']:>18,.2f}")
    print(f"  pensões bruto .............. {s['pensoes_bruto']:>18,.2f}")
    print(f"  (-) dedução ................ {s['pensoes_deducao']:>18,.2f}")
    print(f"  pensões líquido ............ {s['pensoes']:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


