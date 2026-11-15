# -*- coding: utf-8 -*-
"""Converte o acervo (formato longo) de volta para o formato de instancia.

O gerador oficial (`gerar_relatorios.py` -> `pipeline`) espera o arquivo que o
Estado envia ao Siconfi, com a primeira linha `24EX;AAAA-MM` e os atributos em
pares (IC, TIPO). A API do Siconfi entrega os mesmos dados no formato longo.

Este script faz a ponte: le os arquivos `RN_AAAA_MM_classe<n>_<tipo>.csv` do
acervo e grava um `24EX-AAAA-MM.csv` por mes.

O mapeamento vem do `converter_msc.py` (que faz o caminho inverso):

    PO -> poder_orgao        CO -> complemento_fonte    AI -> ano_inscricao
    FR -> fonte_recursos     ND -> natureza_despesa     FS -> fonte_sigef
    FP -> fonte_programa     NR -> natureza_receita     DC -> destinacao

Uso:
    python converter_acervo_instancia.py --ano 2026 --mes 8 --destino <pasta>
    python converter_acervo_instancia.py --ano 2025 --destino <pasta>
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ACERVO = os.path.join(RAIZ, "dados", "acervo")

#: ordem canonica dos pares no arquivo de instancia
PARES = (
    ("PO", "poder_orgao"),
    ("FP", "ano_fonte_recursos"),
    ("FR", "fonte_recursos"),
    ("CO", "complemento_fonte"),
    ("ND", "natureza_despesa"),
    ("NR", "natureza_receita"),
    ("AI", "ano_inscricao"),
    ("FS", "fonte_sigef"),
    ("DC", "destinacao"),
)
MAX_PARES = 6
CABECALHO = ("CONTA;IC1;TIPO1;IC2;TIPO2;IC3;TIPO3;IC4;TIPO4;IC5;TIPO5;"
             "IC6;TIPO6;Valor;Tipo_valor;Natureza_valor")


def _arquivos(ano: int, mes: int) -> list[str]:
    pasta = os.path.join(ACERVO, str(ano))
    if not os.path.isdir(pasta):
        return []
    prefixo = f"RN_{ano}_{mes:02d}_classe"
    return sorted(os.path.join(pasta, n) for n in os.listdir(pasta)
                  if n.startswith(prefixo) and n.endswith(".csv"))


def converter(ano: int, mes: int, destino: str, ente: str = "24") -> str | None:
    """Grava `24EX-AAAA-MM.csv` e devolve o caminho."""
    arquivos = _arquivos(ano, mes)
    if not arquivos:
        return None

    os.makedirs(destino, exist_ok=True)
    saida = os.path.join(destino, f"{ente}EX-{ano}-{mes:02d}.csv")
    linhas = 0
    with open(saida, "w", encoding="utf-8", newline="") as fh:
        fh.write(f"{ente}EX;{ano}-{mes:02d}\n")
        fh.write(CABECALHO + "\n")
        escritor = csv.writer(fh, delimiter=";", lineterminator="\n")
        for caminho in arquivos:
            with open(caminho, encoding="utf-8", newline="") as origem:
                for reg in csv.DictReader(origem, delimiter=";"):
                    pares = [(tipo, reg[col]) for tipo, col in PARES
                             if (reg.get(col) or "").strip()]
                    if len(pares) > MAX_PARES:
                        pares = pares[:MAX_PARES]
                    linha = [reg.get("conta_contabil", "")]
                    for i in range(MAX_PARES):
                        if i < len(pares):
                            linha.extend([pares[i][1], pares[i][0]])
                        else:
                            linha.extend(["", ""])
                    linha.extend([reg.get("valor", "0"),
                                  reg.get("tipo_valor", ""),
                                  reg.get("natureza_conta", "")])
                    escritor.writerow(linha)
                    linhas += 1
    return saida if linhas else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Acervo -> formato de instancia")
    ap.add_argument("--ano", type=int, required=True)
    ap.add_argument("--mes", type=int, help="so este mes (padrao: os doze)")
    ap.add_argument("--destino", required=True)
    args = ap.parse_args()

    meses = [args.mes] if args.mes else list(range(1, 13))
    feitos = 0
    for mes in meses:
        caminho = converter(args.ano, mes, args.destino)
        if caminho:
            feitos += 1
            print(f"   {os.path.basename(caminho)}")
    print(f"\n{feitos} arquivo(s) em {args.destino}")
    return 0 if feitos else 1


if __name__ == "__main__":
    raise SystemExit(main())
