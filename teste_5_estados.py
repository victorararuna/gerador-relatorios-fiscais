# -*- coding: utf-8 -*-
"""Roda o gerador nas matrizes dos cinco estados (rodada 166).

A pergunta: o sistema, construido sobre o Rio Grande do Norte, funciona fora
dele? Para cada estado sorteado o teste:

1. converte as matrizes do formato longo para o formato de instancia;
2. roda o modulo de pessoal (`msc_pessoal`) — o coracao do Anexo 1;
3. roda o pipeline completo, quando ha matriz de dezembro.

Uso:
    python teste_5_estados.py
    python teste_5_estados.py --ano 2026 --mes 9
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import traceback

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

FONTE = os.path.join(RAIZ, "dados", "teste_estados")
SAIDA = os.path.join(RAIZ, "_inst_estados")

CODIGO_UF = {"RO": 11, "AC": 12, "AM": 13, "RR": 14, "PA": 15, "AP": 16,
             "TO": 17, "MA": 21, "PI": 22, "CE": 23, "RN": 24, "PB": 25,
             "PE": 26, "AL": 27, "SE": 28, "BA": 29, "MG": 31, "ES": 32,
             "RJ": 33, "SP": 35, "PR": 41, "SC": 42, "RS": 43, "MS": 50,
             "MT": 51, "GO": 52, "DF": 53}

PARES = (("PO", "poder_orgao"), ("FP", "ano_fonte_recursos"),
         ("FR", "fonte_recursos"), ("CO", "complemento_fonte"),
         ("ND", "natureza_despesa"), ("NR", "natureza_receita"),
         ("AI", "ano_inscricao"), ("FS", "fonte_sigef"), ("DC", "destinacao"))
CABECALHO = ("CONTA;IC1;TIPO1;IC2;TIPO2;IC3;TIPO3;IC4;TIPO4;IC5;TIPO5;"
             "IC6;TIPO6;Valor;Tipo_valor;Natureza_conta;")
CABECALHO = ("CONTA;IC1;TIPO1;IC2;TIPO2;IC3;TIPO3;IC4;TIPO4;IC5;TIPO5;"
             "IC6;TIPO6;Valor;Tipo_valor;Natureza_valor")


def converter(uf: str, ano: int, mes: int) -> str | None:
    """Converte as matrizes de um estado para o formato de instancia."""
    pasta = os.path.join(FONTE, uf)
    if not os.path.isdir(pasta):
        return None
    arquivos = sorted(n for n in os.listdir(pasta)
                      if n.startswith(f"{uf}_{ano}_{mes:02d}_") and n.endswith(".csv"))
    if not arquivos:
        return None
    destino_dir = os.path.join(SAIDA, uf)
    os.makedirs(destino_dir, exist_ok=True)
    codigo = CODIGO_UF.get(uf, 0)
    saida = os.path.join(destino_dir, f"{codigo}EX-{ano}-{mes:02d}.csv")
    total = 0
    with open(saida, "w", encoding="utf-8", newline="") as fh:
        fh.write(f"{codigo}EX;{ano}-{mes:02d}\n")
        fh.write(CABECALHO + "\n")
        esc = csv.writer(fh, delimiter=";", lineterminator="\n")
        for nome in arquivos:
            caminho = os.path.join(pasta, nome)
            # o acervo do RN usa ponto e virgula; o download de teste saiu com
            # virgula. Detecta pelo cabecalho em vez de fixar.
            with open(caminho, encoding="utf-8", newline="") as origem:
                cab = origem.readline()
                origem.seek(0)
                sep = ";" if cab.count(";") > cab.count(",") else ","
                for reg in csv.DictReader(origem, delimiter=sep):
                    pares = [(t, reg[c]) for t, c in PARES if (reg.get(c) or "").strip()]
                    linha = [reg.get("conta_contabil", "")]
                    for i in range(6):
                        if i < len(pares):
                            linha.extend([pares[i][1], pares[i][0]])
                        else:
                            linha.extend(["", ""])
                    linha.extend([reg.get("valor", "0"),
                                  reg.get("tipo_valor", ""),
                                  reg.get("natureza_conta", "")])
                    esc.writerow(linha)
                    total += 1
    return saida if total else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Testa o gerador em outros estados")
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--mes", type=int, default=9)
    args = ap.parse_args()

    if not os.path.isdir(FONTE):
        print(f"sem matrizes em {FONTE} — rode baixar_matrizes_teste.py")
        return 2

    ufs = sorted(d for d in os.listdir(FONTE) if os.path.isdir(os.path.join(FONTE, d)))
    import msc_pessoal as M

    print(f"{'UF':<4}{'linhas':>9}{'vencimentos':>20}{'patronal':>20}{'aposent.':>20}")
    print("-" * 74)
    for uf in ufs:
        caminho = converter(uf, args.ano, args.mes)
        if not caminho:
            print(f"{uf:<4}{'(sem matriz do mes)':>40}")
            continue
        try:
            r = M.ler_msc(caminho)
            d = M.apurar(r)
            n = sum(1 for _ in open(caminho, encoding="utf-8"))
            print(f"{uf:<4}{n:>9}{d['vencimentos']:>20,.2f}"
                  f"{d['patronal']:>20,.2f}{d['aposentadorias']:>20,.2f}")
        except Exception as e:
            print(f"{uf:<4}{'ERRO':>9}  {type(e).__name__}: {str(e)[:50]}")
            traceback.print_exc()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
