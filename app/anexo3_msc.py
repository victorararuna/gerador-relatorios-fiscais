# -*- coding: utf-8 -*-
"""RCL a partir do RREO Anexo 3 e montagem do RGF Anexo 3 (Garantias).

A RCL não vem da MSC: vem do RREO Anexo 3 (Demonstrativo da Receita Corrente
Líquida), que já está no acervo. Conferido com o RGF homologado de 2025: os três
valores batem ao centavo.

O Anexo 3 do RN é vazio de garantias — o demonstrativo traz apenas a RCL, a RCL
ajustada e os limites (22% da RCL ajustada e 90% de alerta).
"""
from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

__all__ = ["RCL", "ler_rcl", "linhas_anexo3", "conferir_anexo3"]

#: limite de garantias dos Estados — Resolução do Senado 43/2001
PERCENTUAL_GARANTIAS = 0.22
PERCENTUAL_ALERTA = 0.90


@dataclass
class RCL:
    rcl: float
    transferencias: float
    ajustada_endividamento: float
    ajustada_pessoal: float

    def limites_garantias(self) -> Tuple[float, float]:
        limite = self.ajustada_endividamento * PERCENTUAL_GARANTIAS
        return limite, limite * PERCENTUAL_ALERTA


CAMPOS = {
    "rcl": "RECEITA CORRENTE LÍQUIDA (III)",
    "transferencias": "(-) Transferências Obrigatórias da União",
    "ajustada_endividamento": ("RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO "
                              "DOS LIMITES DE ENDIVIDAMENTO"),
    "ajustada_pessoal": ("RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO "
                         "DOS LIMITES DA DESPESA COM PESSOAL"),
}


def _norm(texto: str) -> str:
    """Normaliza rótulo para comparação: minúsculas, sem acento de caixa/espaços."""
    t = texto.lower()
    for ruim in ("( - )", "( -)", "(- )", "( ", " )", "(", ")"):
        t = t.replace(ruim, " ")
    return " ".join(t.split())


def ler_rcl(caminho: str, coluna: str = "TOTAL (ÚLTIMOS 12 MESES)") -> RCL:
    """Lê a RCL do RREO Anexo 3 na coluna pedida (padrão: últimos 12 meses)."""
    achados: Dict[str, float] = {}
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] != coluna:
                continue
            alvo = _norm(r["conta"])
            for chave, prefixo in CAMPOS.items():
                if chave in achados:
                    continue
                if alvo.startswith(_norm(prefixo)):
                    achados[chave] = float(r["valor"])
    if "rcl" not in achados:
        raise ValueError(f"RCL não encontrada em {caminho}")
    # a linha de emendas só aparece nas colunas mensais; nos últimos 12 meses
    # ela é a diferença entre a RCL e a RCL ajustada
    if "transferencias" not in achados and "ajustada_endividamento" in achados:
        achados["transferencias"] = (achados["rcl"]
                                     - achados["ajustada_endividamento"])
    return RCL(rcl=achados["rcl"],
               transferencias=achados.get("transferencias", 0.0),
               ajustada_endividamento=achados.get("ajustada_endividamento",
                                                  achados["rcl"]),
               ajustada_pessoal=achados.get("ajustada_pessoal", achados["rcl"]))


def linhas_anexo3(rcl: RCL) -> List[Tuple[str, float]]:
    """As cinco linhas do Anexo 3 para um ente sem garantias concedidas."""
    limite, alerta = rcl.limites_garantias()
    return [
        ("RECEITA CORRENTE LÍQUIDA - RCL (VI)", rcl.rcl),
        ("(-) Transferências Obrigatórias da União Relativas às Emendas "
         "Individuals (art. 166-A, §1º, da CF)", rcl.transferencias),
        ("RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DE "
         "ENDIVIDAMENTO (VII)", rcl.ajustada_endividamento),
        ("LIMITE DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL", limite),
        ("LIMITE DE ALERTA (inciso III § 1º do art. 59 da LRF)", alerta),
    ]


def conferir_anexo3(nossas: List[Tuple[str, float]], caminho_rgf: str,
                    coluna: str = "Até o 3º Quadrimestre") -> List[Tuple[str, float, float]]:
    oficiais: Dict[str, float] = {}
    with open(caminho_rgf, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == coluna:
                oficiais.setdefault(r["conta"], float(r["valor"]))
    saida = []
    for rotulo, valor in nossas:
        of = next((v for c, v in oficiais.items() if c.startswith(rotulo[:40])),
                  float("nan"))
        saida.append((rotulo, of, valor))
    return saida


def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="RGF Anexo 3 (garantias) a partir do RREO Anexo 3.")
    ap.add_argument("--rreo", required=True, help="RREO ... anexo03.csv")
    ap.add_argument("--rgf", help="RGF ... anexo03.csv homologado")
    ap.add_argument("--coluna", default="TOTAL (ÚLTIMOS 12 MESES)")
    ap.add_argument("--coluna-rgf", default="Até o 3º Quadrimestre")
    args = ap.parse_args()

    rcl = ler_rcl(args.rreo, args.coluna)
    print(f"RCL ................ {rcl.rcl:>18,.2f}")
    print(f"(-) emendas ........ {rcl.transferencias:>18,.2f}")
    print(f"RCL ajustada ....... {rcl.ajustada_endividamento:>18,.2f}")
    print(f"RCL ajustada (DTP) . {rcl.ajustada_pessoal:>18,.2f}")

    if args.rgf:
        print()
        for rotulo, of, ms in conferir_anexo3(linhas_anexo3(rcl), args.rgf,
                                                 args.coluna_rgf):
            pct = (ms / of - 1) * 100 if of else float("nan")
            print(f"{rotulo[:58]:<60}{of:>18,.2f}{ms:>18,.2f}{pct:>8.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

