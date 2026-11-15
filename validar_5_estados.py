# -*- coding: utf-8 -*-
"""Valida o gerador contra o RGF publicado de cada estado (rodada 167).

Para cada estado de teste:

1. busca o **RGF Anexo 1 publicado** no Siconfi (`tt/rgf`), coluna de 12 meses;
2. calcula as mesmas linhas pela **matriz de dezembro** do estado;
3. compara linha a linha.

E o teste mais duro que existe: nao compara com planilha de equipe nem com
benchmark — compara com o que o proprio Estado entregou ao Tesouro.

A descoberta que abriu a porta: o endpoint `rgf` exige `co_esfera`, `co_poder`
e `in_periodicidade` alem dos parametros obvios. Sem eles, devolve zero.

Uso:
    python validar_5_estados.py
    python validar_5_estados.py --ano 2025 --periodo 3
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.parse
import urllib.request
import json

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

FONTE = os.path.join(RAIZ, "dados", "teste_estados")
API = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rgf"

CODIGO_UF = {"RO": 11, "AC": 12, "AM": 13, "RR": 14, "PA": 15, "AP": 16,
             "TO": 17, "MA": 21, "PI": 22, "CE": 23, "RN": 24, "PB": 25,
             "PE": 26, "AL": 27, "SE": 28, "BA": 29, "MG": 31, "ES": 32,
             "RJ": 33, "SP": 35, "PR": 41, "SC": 42, "RS": 43, "MS": 50,
             "MT": 51, "GO": 52, "DF": 53}

#: rotulo no RGF publicado -> campo do nosso apurar()
LINHAS = {
    "Vencimentos, Vantagens e Outras Despesas Variáveis": "vencimentos",
    "Obrigações Patronais": "patronal",
    "Aposentadorias, Reserva e Reformas": "aposentadorias",
    "Pensões": "pensoes",
}


def baixar_publicado(ente: int, ano: int, periodo: int) -> dict:
    """{(conta, coluna): valor} do RGF Anexo 1 publicado."""
    itens, offset = [], 0
    while True:
        p = {"an_exercicio": ano, "nr_periodo": periodo,
             "co_tipo_demonstrativo": "RGF", "no_anexo": "RGF-Anexo 01",
             "co_esfera": "E", "co_poder": "E", "in_periodicidade": "Q",
             "id_ente": ente, "limit": 5000, "offset": offset}
        url = API + "?" + urllib.parse.urlencode(p)
        with urllib.request.urlopen(url, timeout=180) as r:
            d = json.loads(r.read().decode())
        it = d.get("items", [])
        itens.extend(it)
        if not d.get("hasMore") or not it:
            break
        offset += 5000
    # as colunas <MR-11> a <MR> sao os DOZE MESES: <MR> e dezembro, nao o total.
    # o total de 12 meses e a soma das doze.
    soma: dict = {}
    for x in itens:
        if not str(x.get("coluna", "")).startswith("<MR"):
            continue
        soma[x["conta"]] = soma.get(x["conta"], 0.0) + x["valor"]
    return {(conta, "<MR>"): valor for conta, valor in soma.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description="Compara com o RGF publicado")
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--periodo", type=int, default=3)
    args = ap.parse_args()

    if not os.path.isdir(FONTE):
        print(f"sem matrizes em {FONTE}")
        return 2

    import msc_pessoal as M
    from teste_5_estados import converter

    ufs = sorted(d for d in os.listdir(FONTE)
                 if os.path.isdir(os.path.join(FONTE, d)))
    if not ufs:
        return 2

    resumo = []
    for uf in ufs:
        ente = CODIGO_UF.get(uf, 0)
        caminho = converter(uf, args.ano, 12)
        if not caminho:
            print(f"{uf}: sem matriz de dezembro/{args.ano}")
            continue
        try:
            publicado = baixar_publicado(ente, args.ano, args.periodo)
        except Exception as e:
            print(f"{uf}: erro ao buscar publicado — {type(e).__name__} {str(e)[:40]}")
            continue
        if not publicado:
            print(f"{uf}: sem RGF publicado para {args.ano} p{args.periodo}")
            continue

        d = M.apurar(M.ler_msc(caminho))
        print(f"\n=== {uf} ({ente}) — RGF {args.ano} p{args.periodo}")
        print(f"{'linha':<46}{'nosso':>18}{'publicado':>18}{'dif %':>9}")
        for rotulo, campo in LINHAS.items():
            pub = publicado.get((rotulo, "<MR>"))
            if pub is None:
                continue
            nosso = d.get(campo, 0.0)
            pct = (nosso - pub) / pub * 100 if pub else 0.0
            print(f"{rotulo[:44]:<46}{nosso:>18,.2f}{pub:>18,.2f}{pct:>8.2f}%")
            resumo.append((uf, rotulo[:20], pct))
        # a despesa bruta publicada
        pub_i = publicado.get(("DESPESA BRUTA COM PESSOAL (I)", "<MR>"))
        if pub_i:
            bruto = (d.get("vencimentos", 0.0) + d.get("patronal", 0.0)
                     + d.get("aposentadorias", 0.0) + d.get("pensoes", 0.0)
                     + d.get("terc", d.get("terceirizacao", 0.0)))
            pct = (bruto - pub_i) / pub_i * 100
            print(f"{'I — soma das nossas linhas':<46}{bruto:>18,.2f}{pub_i:>18,.2f}{pct:>8.2f}%")
            resumo.append((uf, "I", pct))

    if resumo:
        print("\n" + "=" * 60)
        piores = sorted(resumo, key=lambda x: -abs(x[2]))[:5]
        print("maiores desvios:")
        for uf, rot, pct in piores:
            print(f"   {uf} {rot:<22}{pct:>8.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
