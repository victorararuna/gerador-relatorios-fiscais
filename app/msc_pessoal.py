# -*- coding: utf-8 -*-
"""Apuração da despesa com pessoal a partir da Matriz de Saldos Contábeis (MSC).

A MSC do Siconfi (formato "instancia.csv") traz, para cada conta contábil, as
informações complementares que o Anexo 1 do RGF exige:

    PO  - Poder/Órgão (10111 Governo, 10112 RPPS, 60611 Defensoria, ...)
    ND  - Natureza da despesa (31901100 = 3.1.90.11.00)
    FR  - Fonte de recurso (1605 = 0.6.05)
    CO  - Classificação orçamentária

Despesa liquidada = saldo final das contas:
    6.2.2.1.3.03.00  crédito empenhado liquidado a pagar
  + 6.2.2.1.3.04.00  crédito empenhado liquidado pago
  + 6.2.2.1.3.07.00  empenhos liquidados inscritos em restos a pagar processados

(conforme Módulo 16 da STN, p. 63)

Recorte do Poder Executivo = POs 10111 + 10112 + 60611.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from typing import Dict, List

CONTAS_LIQUIDACAO = ("622130300", "622130400", "622130700")
CONTA_NAO_EXECUTADA = "863310000"

PO_GOVERNO = "10111"
PO_RPPS = "10112"
PO_DEFENSORIA = "60611"
PO_EXECUTIVO = {PO_GOVERNO, PO_RPPS, PO_DEFENSORIA}

FR_ENFERMAGEM = "1605"          # 0.6.05 - piso da enfermagem
PERCENTUAL_ENFERMAGEM = 0.90    # ADCT art. 38, § 2º - exercício de 2024

# linhas do Anexo 1 (validado contra o RGF 2024 Q3 homologado)
LINHA_POR_ELEMENTO = {
    "319001": "aposentadorias",
    "319003": "pensoes",
    "319011": "vencimentos",
    "319012": "vencimentos",
    "319016": "vencimentos",
    "319017": "vencimentos",
    "319004": "vencimentos",
    "319007": "vencimentos",
    "319013": "patronal",
    "319113": "patronal",
    "319091": "judiciais",       # sentencas judiciais inteiras
    "319092": "exercicios_anteriores",
    "319192": "exercicios_anteriores",
    "319094": "indenizacoes",
    "319096": "exercicios_anteriores",
}


@dataclass
class LinhaMSC:
    nd: str
    po: str
    fr: str
    co: str
    liquidado: float      # movimento liquido (credito - debito)
    bruto: float = 0.0    # apenas os creditos (despesa do periodo)


@dataclass
class ResultadoMSC:
    linhas: List[LinhaMSC] = field(default_factory=list)

    def por_nd(self, executivo: bool = True) -> Dict[str, float]:
        saida: Dict[str, float] = {}
        for l in self.linhas:
            if executivo and l.po not in PO_EXECUTIVO:
                continue
            saida[l.nd] = saida.get(l.nd, 0.0) + l.liquidado
        return saida

    def por_po(self) -> Dict[str, float]:
        saida: Dict[str, float] = {}
        for l in self.linhas:
            saida[l.po] = saida.get(l.po, 0.0) + l.liquidado
        return saida

    def total(self, executivo: bool = True) -> float:
        return sum(self.por_nd(executivo).values())


def ler_msc(caminho: str) -> ResultadoMSC:
    resultado = ResultadoMSC()
    with open(caminho, encoding="utf-8", errors="replace", newline="") as f:
        f.readline()
        rd = csv.reader(f, delimiter=";")
        next(rd)
        for c in rd:
            alvo = c[0] in CONTAS_LIQUIDACAO or c[0] == CONTA_NAO_EXECUTADA
            if len(c) != 16 or not alvo or c[14] != "ending_balance":
                continue
            po = nd = fr = co = ""
            for i in range(1, 13, 2):
                tipo = c[i + 1]
                if tipo == "PO":
                    po = c[i]
                elif tipo == "ND":
                    nd = c[i]
                elif tipo == "FR":
                    fr = c[i]
                elif tipo == "CO":
                    co = c[i]
            if c[0] == CONTA_NAO_EXECUTADA:
                nd = CONTA_NAO_EXECUTADA
            if not nd:
                continue
            if not (nd.startswith("31") or nd.startswith("33")
                    or nd == CONTA_NAO_EXECUTADA):
                continue
            try:
                bruto = float(c[13].replace(",", "."))
            except ValueError:
                continue
            # As contas 6.2.2.1.3.03/04/07 sao contas de VPD: a despesa e o
            # movimento CREDOR liquido. Lancamentos a debito (estornos,
            # pagamentos) reduzem o valor do periodo.
            valor = bruto if c[15] == "C" else -bruto
            credito = bruto if c[15] == "C" else 0.0
            resultado.linhas.append(LinhaMSC(nd=nd, po=po, fr=fr, co=co,
                                             liquidado=valor, bruto=credito))
    return resultado


def apurar(resultado: ResultadoMSC) -> Dict[str, float]:
    """Aplica o de-para da STN e devolve as linhas do Anexo 1 (Executivo)."""
    linhas = {k: 0.0 for k in ("vencimentos", "patronal", "aposentadorias", "pensoes",
                               "terceirizacao", "exercicios_anteriores", "judiciais",
                               "indenizacoes")}
    for l in resultado.linhas:
        if l.po not in PO_EXECUTIVO:
            continue
        valor = l.bruto
        elem = l.nd[:6]
        if l.nd.startswith("33"):
            # contratacao indireta: 33.xx.34 + 33.xx.91.34 + 33.xx.92.34
            if l.nd[:6] == "339034" or l.nd.endswith("34"):
                linhas["terceirizacao"] += l.bruto
            continue
        # Aposentadorias e pensoes: o mapeamento usa o CO (1111+1151 capitalizacao,
        # 2111+2151 reparticao). Na pratica o RN registra em 1111 e sem CO; os
        # demais CO (1121, 1122, 1131, 1141) sao de outros planos/poderes.
        if elem in ("319001", "319003"):
            if l.co not in ("", "1111", "1151", "2111", "2151"):
                continue
        # 31.90.13.02 nao compoe a linha de obrigacoes patronais do RGF
        if l.nd == "31901302":
            continue
        linhas[LINHA_POR_ELEMENTO.get(elem, "vencimentos")] += l.bruto

    return linhas


def nao_executada(resultado: ResultadoMSC) -> float:
    """Despesa com Pessoal nao Executada Orcamentariamente (conta 8.6.3.3.1.00.00)."""
    return sum(l.liquidado for l in resultado.linhas
               if l.nd == "863310000" and l.po in PO_EXECUTIVO)


def deducao_enfermagem(resultado: ResultadoMSC) -> Dict[str, float]:
    """Piso da enfermagem: percentual do exercicio sobre a fonte 0.605."""
    base = sum(l.liquidado for l in resultado.linhas
               if l.po in PO_EXECUTIVO and l.fr.startswith(FR_ENFERMAGEM))
    return {"base": base, "percentual": PERCENTUAL_ENFERMAGEM,
            "deducao": base * PERCENTUAL_ENFERMAGEM}


def deducao_vinculados(resultado: ResultadoMSC) -> float:
    """Inativos e pensionistas custeados com recursos vinculados (art. 19, § 1º, VI, 'a').

    Fontes 18xx (0.8.x) e CO do fundo (1111/1151 capitalizacao, 2111/2151
    reparticao), incluindo os lancamentos sem CO.
    """
    return sum(l.liquidado for l in resultado.linhas
               if l.po in PO_EXECUTIVO
               and l.nd[:6] in ("319001", "319003")
               and l.fr.startswith("18")
               and (l.co in ("", "1111", "1151", "2111", "2151")))
