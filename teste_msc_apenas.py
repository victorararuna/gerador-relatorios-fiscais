# -*- coding: utf-8 -*-
"""O Anexo 1 sai só da MSC? Teste decisivo (rodada 160).

A pergunta: a STN so recebe a MSC e faz todos os batimentos com ela. Se e assim,
nos tambem deveriamos conseguir gerar o Anexo 1 sem os PDFs do SIGEF.

O `mapa_anexo1` le o **Comparativo** (PDF) porque foi o caminho que funcionou. Mas
a MSC carrega as duas dimensoes que o Comparativo da: `natureza_despesa` e
`fonte_recursos`. Entao a tabela cruzada ND x fonte e derivavel da matriz.

Este script calcula vencimentos e patronal pela MSC e compara com o valor do
Comparativo — que, por sua vez, bate com o publicado ao centavo.
"""
from __future__ import annotations

import os
import sys

RAIZ = r"C:\Users\victo\OneDrive\Documents\deepseek-harness\default-workspace\repo-github"
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

import mapa_anexo1 as MAPA  # noqa: E402
from acervo import Acervo  # noqa: E402

#: contas de liquidacao (as tres que o mapeamento usa)
CONTAS_LIQ = ("622130300", "622130400", "622130700")
#: Poderes do Executivo
PO_EXEC = ("10111", "10112", "60611")
#: fontes que saem do bruto da patronal (as vinculadas ao RPPS e intra)
FONTES_INTRA = ("8.00",)

MESES = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
         5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto"}


def _chave(nd: str) -> str:
    """ND de 8 digitos -> a chave de 4 partes do Comparativo (31.90.11.00)."""
    nd = (nd or "").replace(".", "")
    if len(nd) != 8:
        return ""
    return f"{nd[0:2]}.{nd[2:4]}.{nd[4:6]}.{nd[6:8]}"


def _casa(nd: str, chave: str) -> bool:
    """O ND casa com a chave? "XX" e modalidade livre; subelemento "00" e qualquer."""
    partes = chave.split(".")
    if len(partes) != 4:
        return False
    if partes[0] != nd[0:2]:
        return False
    if partes[1] != "XX" and partes[1] != nd[2:4]:
        return False
    if partes[2] != nd[4:6]:
        return False
    if partes[3] != "00" and partes[3] != nd[6:8]:
        return False
    return True


def apurar_mes(ac: Acervo, ano: int, mes: int) -> dict:
    """Vencimentos e patronal a partir da matriz."""
    import json
    regra = json.load(open(os.path.join(RAIZ, "dados", "benchmarks",
                                        "anexo1_regra_auditor.json"), encoding="utf-8"))
    venc_chaves = [x["codigo"] for x in regra["secoes"]["vencimentos"] if x["sinal"] > 0]
    expurgo = [c for c in MAPA.EXPURGO_PATRONAL]

    vencimentos = 0.0
    patronal_bruto = 0.0
    expurgo_total = 0.0
    intra = 0.0

    for r in ac.ler(ano, mes, classe=6, tipo_valor="period_change"):
        if (r.conta or "") not in CONTAS_LIQ:
            continue
        if (r.po or "") not in PO_EXEC:
            continue
        nd = (r.nd or "").replace(".", "")
        if len(nd) != 8:
            continue
        valor = r.liquido

        # vencimentos: naturezas da lista
        if any(_casa(nd, c) for c in venc_chaves):
            vencimentos += valor
        # patronal bruta: elemento 13 e a DEA da patronal
        if nd[:2] == "31" and nd[4:6] == "13":
            patronal_bruto += valor
        if nd in ("31909213", "31909218", "31900700"):
            patronal_bruto += valor
        if nd[:2] == "31" and nd[4:6] in ("91", "92") and nd[:4] in ("3191",):
            intra += valor
        # expurgo
        if any(_casa(nd, c) for c in expurgo):
            expurgo_total += valor

    return {
        "vencimentos": vencimentos,
        "patronal": patronal_bruto + intra - expurgo_total,
    }


def main() -> int:
    ac = Acervo(os.path.join(RAIZ, "dados", "acervo"))
    print(f"{'mes':<12}{'campo':<14}{'MSC':>18}{'Comparativo':>18}{'dif':>14}")
    for mes, nome in MESES.items():
        try:
            via_matriz = apurar_mes(ac, 2026, mes)
            via_pdf = MAPA.secoes(nome)
        except Exception as e:
            print(f"{nome:<12}erro: {type(e).__name__} {e}")
            continue
        for campo in ("vencimentos", "patronal"):
            a = via_matriz[campo]
            b = via_pdf[campo]
            marca = "OK" if abs(a - b) < 0.01 else "DIF"
            print(f"{nome:<12}{campo:<14}{a:>18,.2f}{b:>18,.2f}{a-b:>14,.2f}  {marca}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
