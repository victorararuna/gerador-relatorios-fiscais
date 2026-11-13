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
RE_PAR = re.compile(
    r"(\d\d\.\d\d\.\d\d\.\d\d)\s+(\d\.\d\.\d\d\.\d{6})\s+[A-Za-zÀ-ÿ]"
    r".*?\s+(" + NUM + r") (?:" + NUM + r" ){6}")
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

#: expurgo das obrigações patronais dos demais Poderes (MAPA linhas 164 a 180)
EXPURGO_PATRONAL = [
    "31.91.13.22", "31.91.13.43", "31.91.13.49", "31.91.13.71",   # ALRN
    "31.91.13.46",                                                # DPRN
    "31.91.13.25", "31.91.13.48", "31.91.13.53", "31.91.13.75",   # MPRN
    "31.91.13.23", "31.91.13.44", "31.91.13.50", "31.91.13.72",   # TCE
    "31.91.13.24", "31.91.13.45", "31.91.13.51", "31.91.13.73",   # TJRN
]

#: pensões — naturezas da parte bruta (MAPA linhas 210 a 227)
PENSOES = [
    # usa-se o agregado 31.90.03.00 no lugar dos subelementos: em janeiro/2026
    # ele traz R$ 20.427.820,81 que a abertura por subelemento não evidencia
    "31.90.03.00",
    "31.90.91.10", "31.90.91.13", "31.90.91.16",
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
    pares = {}
    for pagina in paginas:
        texto = re.sub(r"\s+", " ", pagina.texto())
        for m in RE_LINHA.finditer(texto):
            nums = re.findall(NUM, m.group(0))
            if len(nums) >= 3:
                valores[m.group(1)] = _num(nums[2])
        for m in RE_PAR.finditer(texto):
            nums = re.findall(NUM, m.group(0))
            if len(nums) >= 3:
                pares[(m.group(1), m.group(2))] = _num(nums[2])
    valores["__pares__"] = pares
    return valores


def secoes(mes: str) -> dict:
    """As seções da MAPA que já têm regra fechada."""
    import expurgo_poderes as E
    import nao_executada as NE

    comp = ler_comparativo(mes)
    total_gnd31 = comp.get("31.00.00.00", 0.0)

    bruto_apos = sum(comp.get(nd, 0.0) for nd in APOSENTADORIAS)
    ieo = E.total(E.ler_periodo(mes))
    ded_apos = ieo["aposentadorias"] + ieo["apos_tesouro"]

    bruto_pens = sum(comp.get(nd, 0.0) for nd in PENSOES)
    terceirizacao = comp.get("33.90.34.00", 0.0) + comp.get("33.90.92.34", 0.0) \
        + comp.get("33.90.91.34", 0.0)
    patronal_bruto = comp.get("31.90.13.00", 0.0) + comp.get("31.91.13.00", 0.0)
    patronal = patronal_bruto - sum(comp.get(nd, 0.0) for nd in EXPURGO_PATRONAL)
    vencimentos = (comp.get("31.00.00.00", 0.0) - sum(comp.get(nd, 0.0) for nd in APOSENTADORIAS)
                   - sum(comp.get(nd, 0.0) for nd in PENSOES) - patronal_bruto)
    nao_exec = NE.valores().get(mes, 0.0)
    ded_pens = ieo["pensoes"]

    return {
        "gnd31": total_gnd31,
        "aposentadorias_bruto": bruto_apos,
        "aposentadorias_deducao": ded_apos,
        "aposentadorias": bruto_apos - ded_apos,
        "pensoes_bruto": bruto_pens,
        "pensoes_deducao": ded_pens,
        "pensoes": bruto_pens - ded_pens,
        "terceirizacao": terceirizacao,
        "vencimentos": vencimentos,
        "patronal": patronal,
        "nao_executada": nao_exec,
        "despesa_bruta": (vencimentos + patronal + (bruto_apos - ded_apos)
                          + (bruto_pens - ded_pens) + terceirizacao + nao_exec),
    }


#: fontes vinculadas ao RPPS (MAPA linhas 288 a 328)
def _rpps(fonte: str) -> bool:
    return fonte[2:6] in ("8.00", "8.01", "8.02", "8.03", "8.04")


def quadro_ii(mes: str) -> dict:
    """Despesas Não Computadas (MAPA L252 -> QUADRO L26)."""
    import expurgo_poderes as E
    import nao_executada as NE

    c = ler_comparativo(mes)
    pares = c.pop("__pares__", {})

    indenizacoes = c.get("31.90.94.00", 0.0) + c.get("31.91.94.00", 0.0)
    judicial = c.get("31.90.91.00", 0.0) + c.get("31.91.91.00", 0.0)
    # DEA só é deduzida em dezembro (Nota Explicativa nº 4). A parcela
    # executada na fonte 0.8.00 já entra deduzida no mês (MAPA linha 276).
    dea_800 = sum(v for (nd, f), v in pares.items()
                  if nd == "31.90.92.00" and f[2:6] == "8.00")
    dea = dea_800

    apos_rpps = sum(v for (nd, f), v in pares.items()
                    if nd == "31.90.01.00" and _rpps(f))
    pens_rpps = sum(v for (nd, f), v in pares.items()
                    if nd == "31.90.03.00" and _rpps(f))
    ieo = E.total(E.ler_periodo(mes))
    # dedução dos demais Poderes: apenas as fontes vinculadas
    ded_apos = ieo["aposentadorias"]
    ded_pens = ieo["pensoes_rpps"]
    inativos = (apos_rpps - ded_apos) + (pens_rpps - ded_pens)

    # usa-se a linha agregada do grupo 31 em cada fonte (as linhas filhas
    # repetem o mesmo valor e somá-las duplicaria)
    acs = sum(v for (nd, f), v in pares.items()
              if f[2:6] == "6.04" and nd in ("31.00.00.00", "33.90.34.00",
                                             "33.90.91.34", "33.90.92.34"))
    enfermagem_base = sum(v for (nd, f), v in pares.items()
                          if f[2:6] == "6.05" and nd in ("31.00.00.00", "33.90.34.00",
                                                         "33.90.91.34", "33.90.92.34"))
    enfermagem = round(enfermagem_base * 0.72, 2)

    return {
        "indenizacoes": indenizacoes,
        "judicial": judicial,
        "dea": dea,
        "inativos": inativos,
        "apos_rpps": apos_rpps,
        "pens_rpps": pens_rpps,
        "ded_apos": ded_apos,
        "ded_pens": ded_pens,
        "acs": acs,
        "enfermagem_base": enfermagem_base,
        "enfermagem": enfermagem,
        "total": indenizacoes + judicial + dea + inativos + acs + enfermagem,
        "nao_executada": NE.valores().get(mes, 0.0),
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
    print(f"  terceirização (L245) ....... {s['terceirizacao']:>18,.2f}")
    print(f"  vencimentos (L8) ........... {s['vencimentos']:>18,.2f}")
    print(f"  patronal (L102 líquida) .... {s['patronal']:>18,.2f}")
    print(f"  não executada (L251) ....... {s['nao_executada']:>18,.2f}")
    print(f"  DESPESA BRUTA (I) .......... {s['despesa_bruta']:>18,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


