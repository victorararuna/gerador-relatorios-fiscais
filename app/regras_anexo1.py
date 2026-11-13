# -*- coding: utf-8 -*-
"""Regras de validação do Siconfi aplicadas ao Anexo 1.

Transcrição das regras estruturais extraídas de
``MDF_STN/2026/02_instrucoes_stn_siconfi/2026_Regras_Validacao_RGF.pdf``
(ver docs/REGRAS_VALIDACAO_ANEXO1_2026.md). São as conferências que o próprio
Siconfi faz ao receber a declaração — usá-las é a melhor aproximação de
"publicável" sem o gabarito do ente.

    python app/regras_anexo1.py --raiz <acervo>
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TOLERANCIA = 0.01  # o Siconfi trabalha com 2 casas


@dataclass
class Resultado:
    codigo: str
    descricao: str
    esperado: float
    informado: float

    @property
    def ok(self) -> bool:
        return abs(self.esperado - self.informado) <= TOLERANCIA

    @property
    def diferenca(self) -> float:
        return self.informado - self.esperado


def _soma(*valores: Optional[float]) -> float:
    return sum(v or 0.0 for v in valores)


def validar(valores: Dict[str, float],
            mensal: Optional[Dict[int, Dict[str, float]]] = None) -> List[Resultado]:
    """Confere as regras estruturais do Anexo 1 sobre um conjunto de linhas."""
    v = valores
    r: List[Resultado] = []

    ativo = _soma(v.get("vencimentos"), v.get("patronal"))
    r.append(Resultado("ES1017", "Pessoal Ativo = Vencimentos + Obrigações Patronais",
                       ativo, v.get("ativo", ativo)))

    inativo = _soma(v.get("aposentadorias"), v.get("pensoes"))
    r.append(Resultado("ES1018", "Inativo e Pensionistas = Aposentadorias + Pensões",
                       inativo, v.get("inativo", inativo)))

    bruto = _soma(ativo, inativo, v.get("terceirizacao"), v.get("nao_executada"))
    r.append(Resultado(
        "ES1005", "I = Pessoal Ativo + Inativo + Terceirização + Não Executada",
        bruto, v.get("I", bruto)))

    ii = _soma(v.get("indenizacoes"), v.get("judiciais"), v.get("exerc_ant"),
               v.get("vinculados"), v.get("enfermagem"))
    r.append(Resultado(
        "ES1016", "II = Indenizações + Decisão Judicial + Exercícios Anteriores "
                  "+ Vinculados + Piso do Enfermeiro", ii, v.get("II", ii)))

    r.append(Resultado("ED1002", "III = I - II",
                       _soma(v.get("I"), -v.get("II")), v.get("III", 0.0)))

    if mensal:
        for linha in ("I",):
            total_meses = sum(m.get(linha, 0.0) for m in mensal.values())
            if linha in v:
                r.append(Resultado(
                    "ES1019", f"{linha} = somatório dos 12 meses",
                    total_meses, v[linha]))
    return r


def imprimir(resultados: List[Resultado]) -> bool:
    largura = 74
    todos_ok = True
    for res in resultados:
        marca = "OK " if res.ok else "ERRO"
        if not res.ok:
            todos_ok = False
        print(f"  {res.codigo:<8} {marca}  {res.descricao[:largura]}")
        if not res.ok:
            print(f"           esperado {res.esperado:>18,.2f}  "
                  f"informado {res.informado:>18,.2f}  "
                  f"dif {res.diferenca:>14,.2f}")
    return todos_ok


def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Valida o Anexo 1 pelas regras do Siconfi.")
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--quadrimestre", type=int, default=3)
    args = ap.parse_args()

    import anexo1_msc as M
    from relatorio_anexo1 import linhas_anexo1

    acervo = M.Acervo(args.raiz)
    pares = M.periodos_janela(args.ano, M.MES_DO_QUADRIMESTRE[args.quadrimestre])
    res = M.apurar_janela(acervo, args.ano, M.MES_DO_QUADRIMESTRE[args.quadrimestre])
    ded = M.deducoes(acervo, pares)
    ne = M.nao_executada(acervo, pares)
    linhas = {ln.chave: ln.valor for ln in linhas_anexo1(res, ded, ne)}

    print(f"Regras de validação do Siconfi — Anexo 1 — {args.ano} "
          f"Q{args.quadrimestre}")
    ok = imprimir(validar(linhas))
    print(f"\n{'todas as regras atendidas' if ok else 'há regras violadas'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_cli())
