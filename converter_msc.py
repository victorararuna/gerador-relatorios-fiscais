# -*- coding: utf-8 -*-
"""Converte a MSC do formato antigo (16 colunas) para o formato longo.

Formato antigo (SIAFIC/Siconfi até 2024):

    CONTA;IC1;TIPO1;IC2;TIPO2;...;IC6;TIPO6;Valor;Tipo_valor;Natureza_valor

Os atributos vêm em pares (valor, tipo) e a posição varia. Tipos observados:
PO (poder/órgão), FR (fonte de recursos), CO (complemento da fonte),
ND (natureza da despesa), NR (natureza da receita), AI (ano de inscrição),
FP, FS, DC.

Formato longo (2025+):

    tipo_matriz,cod_ibge,classe_conta,conta_contabil,poder_orgao,
    ano_fonte_recursos,fonte_recursos,funcao,subfuncao,exercicio,
    mes_referencia,educacao_saude,data_referencia,entrada_msc,
    natureza_despesa,ano_inscricao,natureza_receita,valor,natureza_conta,
    tipo_valor,complemento_fonte

Uso:

    python converter_msc.py --origem "24EX-2026-08-006.csv" --destino dados/acervo
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter
from pathlib import Path

#: tipos de atributo do formato antigo -> coluna do formato longo
MAPA = {
    "PO": "poder_orgao",
    "FR": "fonte_recursos",
    "CO": "complemento_fonte",
    "ND": "natureza_despesa",
    "NR": "natureza_receita",
    "AI": "ano_inscricao",
    "FS": "fonte_sigef",
    "FP": "fonte_programa",
    "DC": "destinacao",
}

COLUNAS = ["tipo_matriz", "cod_ibge", "classe_conta", "conta_contabil",
           "poder_orgao", "ano_fonte_recursos", "fonte_recursos", "funcao",
           "subfuncao", "exercicio", "mes_referencia", "educacao_saude",
           "data_referencia", "entrada_msc", "natureza_despesa",
           "ano_inscricao", "natureza_receita", "valor", "natureza_conta",
           "tipo_valor", "complemento_fonte", "fonte_sigef", "fonte_programa",
           "destinacao"]


def detectar_cabecalho(caminho: str) -> tuple:
    """('24EX', 2026, 8) da primeira linha."""
    with open(caminho, encoding="utf-8", errors="replace") as f:
        linha = f.readline().strip()
    m = re.match(r"(\d+)EX;(\d{4})-(\d{2})", linha)
    if not m:
        return ("", 0, 0)
    return (m.group(1), int(m.group(2)), int(m.group(3)))


def converter(origem: str, destino_dir: str, ente: str = "24") -> dict:
    """Converte um arquivo e grava RN_<ano>_<mm>_classe<n>_<tipo>.csv."""
    _, ano, mes = detectar_cabecalho(origem)
    if not ano:
        raise ValueError(f"cabeçalho não reconhecido: {origem}")

    por_classe: dict = {}
    tipos_vistos = Counter()
    total = 0
    descartados = 0

    with open(origem, encoding="utf-8", errors="replace", newline="") as fh:
        fh.readline()
        rd = csv.reader(fh, delimiter=";")
        next(rd)
        for c in rd:
            if len(c) != 16:
                descartados += 1
                continue
            conta = c[0].strip()
            if not conta:
                descartados += 1
                continue
            try:
                valor = float(c[13].replace(",", "."))
            except ValueError:
                descartados += 1
                continue
            tipo_valor = c[14].strip().lower()
            natureza = c[15].strip().upper()[:1]
            if tipo_valor not in ("beginning_balance", "period_change", "ending_balance"):
                descartados += 1
                continue

            reg = {k: "" for k in COLUNAS}
            reg.update({
                "tipo_matriz": "MSCC",
                "cod_ibge": ente,
                "classe_conta": conta[0],
                "conta_contabil": conta,
                "exercicio": str(ano),
                "mes_referencia": str(mes),
                "data_referencia": f"{ano}-{mes:02d}-01",
                "valor": f"{valor:.2f}",
                "natureza_conta": natureza,
                "tipo_valor": tipo_valor,
            })
            # atributos em pares
            for i in range(6):
                ic = c[2 * i + 1].strip()
                tipo = c[2 * i + 2].strip().upper()
                if not ic or not tipo:
                    continue
                tipos_vistos[tipo] += 1
                col = MAPA.get(tipo)
                if col:
                    reg[col] = ic

            chave = (conta[0], tipo_valor)
            por_classe.setdefault(chave, []).append(reg)
            total += 1

    os.makedirs(destino_dir, exist_ok=True)
    gerados = []
    for (classe, tipo_valor), regs in por_classe.items():
        nome = f"RN_{ano}_{mes:02d}_classe{classe}_{tipo_valor}.csv"
        caminho = os.path.join(destino_dir, nome)
        with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";",
                               extrasaction="ignore")
            w.writeheader()
            w.writerows(regs)
        gerados.append((nome, len(regs)))

    return {"ano": ano, "mes": mes, "linhas": total, "descartados": descartados,
            "arquivos": gerados, "tipos": dict(tipos_vistos)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Converte MSC antiga para formato longo.")
    ap.add_argument("--origem", required=True)
    ap.add_argument("--destino", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "dados", "acervo"))
    ap.add_argument("--ente", default="24")
    a = ap.parse_args()
    r = converter(a.origem, a.destino, a.ente)
    print(f"MSC {r['ano']}-{r['mes']:02d}: {r['linhas']} linhas "
          f"({r['descartados']} descartadas)")
    print("tipos de atributo:", r["tipos"])
    print(f"arquivos gerados em {a.destino}:")
    for nome, n in sorted(r["arquivos"]):
        print(f"   {nome:44} {n:>7} linhas")
