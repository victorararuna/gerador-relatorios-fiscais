# -*- coding: utf-8 -*-
"""Gera o Anexo 1 do RGF a partir do acervo da MSC (formato longo).

Usa a janela móvel de 12 meses e o movimento líquido do ``period_change``. O
resultado é gravado no layout oficial, com as colunas mensais e a aba de
verificações.

Uso:

    python gerar_anexo1_acervo.py --ano 2025 --quadrimestre 3
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from acervo import (Acervo, CONTAS_LIQUIDACAO, CONTA_NAO_EXECUTADA, PO_EXECUTIVO,
                    janela_do_quadrimestre)
from verificar_anexo1 import classificar, CO_BENEFICIO

import balancete
import gerar_oficial
import layout_stn as L

#: caminho do Balancete Consolidado (opcional) — fornece a classe 8
ARQUIVO_BALANCETE = None


def apurar_com_mensal(acervo: Acervo, janela):
    """Devolve (linhas, mensal) — mensal indexado pelo mês (1..12)."""
    linhas = {}
    mensal = {}
    for ano, mes in janela:
        do_mes = {}
        for r in acervo.ler(ano, mes):
            if r.conta not in CONTAS_LIQUIDACAO or r.po not in PO_EXECUTIVO:
                continue
            linha = classificar(r.nd)
            if linha is None:
                continue
            if linha in ("aposentadorias", "pensoes") and r.compl not in CO_BENEFICIO:
                continue
            linhas[linha] = linhas.get(linha, 0.0) + r.liquido
            do_mes[linha] = do_mes.get(linha, 0.0) + r.liquido
        mensal[(ano, mes)] = do_mes

    # nao executada: classe 8 da MSC, ou o balancete de encerramento
    ne = 0.0
    for ano, mes in janela:
        if not acervo.tem(ano, mes, 8):
            continue
        for r in acervo.ler(ano, mes, classe=8):
            if r.conta == CONTA_NAO_EXECUTADA and r.po in PO_EXECUTIVO:
                ne += r.liquido
    if ne == 0.0 and ARQUIVO_BALANCETE and os.path.exists(ARQUIVO_BALANCETE):
        ne = balancete.nao_executada(ARQUIVO_BALANCETE)
    linhas["nao_executada"] = ne

    # deducoes
    vinc = enf = 0.0
    for ano, mes in janela:
        for r in acervo.ler(ano, mes):
            if r.conta not in CONTAS_LIQUIDACAO or r.po not in PO_EXECUTIVO:
                continue
            if (r.nd[:6] in ("319001", "319003") and r.fr.startswith("18")
                    and r.compl in CO_BENEFICIO):
                vinc += r.liquido
            if r.fr.startswith("1605"):
                enf += r.liquido
    pct = {2024: 0.90, 2025: 0.80, 2026: 0.70}.get(janela[-1][0], 0.80)
    linhas["vinculados"] = vinc
    linhas["enfermagem"] = enf * pct

    # Vencimentos inclui a contratacao temporaria e as decisoes judiciais.
    # Testado: com as judiciais aqui a despesa bruta fecha em -0,65%; sem elas,
    # em -4,77%. O homologado as apresenta tambem no grupo II, mas a linha de
    # Vencimentos o acompanha melhor quando elas permanecem no ativo.
    linhas["vencimentos"] = (linhas.get("vencimentos", 0.0)
                             + linhas.get("contratacao_temporaria", 0.0)
                             + linhas.get("judiciais", 0.0))
    linhas["bruta"] = (linhas["vencimentos"] + linhas.get("patronal", 0.0)
                       + linhas.get("aposentadorias", 0.0) + linhas.get("pensoes", 0.0)
                       + linhas.get("terceirizacao", 0.0) + ne)
    linhas["deducoes"] = (linhas.get("judiciais", 0.0)
                          + linhas.get("exerc_ant", 0.0)
                          + linhas.get("indenizacoes", 0.0)
                          + vinc + linhas["enfermagem"])
    linhas["liquida"] = linhas["bruta"] - linhas["deducoes"]
    return linhas, mensal


def main(ano: int = 2025, quadrimestre: int = 3,
         caminho_balancete: str | None = None) -> int:
    global ARQUIVO_BALANCETE
    ARQUIVO_BALANCETE = caminho_balancete
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "acervo")
    acervo = Acervo(raiz)
    janela = janela_do_quadrimestre(ano, quadrimestre, acervo)
    if not janela:
        print("acervo sem os meses da janela")
        return 1

    print(f"acervo .... {raiz}")
    print(f"janela .... {janela[0][0]}-{janela[0][1]:02d} a {janela[-1][0]}-{janela[-1][1]:02d}"
          f" ({len(janela)} meses)")

    linhas, mensal = apurar_com_mensal(acervo, janela)

    # colunas mensais: cada mes da janela -> coluna 2..13
    colunas = {}
    for i, (ano_m, mes_m) in enumerate(janela):
        col = 2 + i
        if col > 13:
            break
        for campo in ("vencimentos", "patronal", "aposentadorias", "pensoes",
                      "terceirizacao"):
            valor = mensal.get((ano_m, mes_m), {}).get(campo, 0.0)
            if campo == "vencimentos":
                valor += (mensal.get((ano_m, mes_m), {}).get("judiciais", 0.0)
                          + mensal.get((ano_m, mes_m), {}).get("contratacao_temporaria", 0.0))
            colunas.setdefault(campo, {})[col] = valor
        # a bruta mensal soma as cinco linhas do mes
        soma = sum(mensal.get((ano_m, mes_m), {}).get(c, 0.0) for c in
                   ("vencimentos", "patronal", "aposentadorias", "pensoes",
                    "terceirizacao"))
        soma += (mensal.get((ano_m, mes_m), {}).get("judiciais", 0.0)
                 + mensal.get((ano_m, mes_m), {}).get("contratacao_temporaria", 0.0))
        colunas.setdefault("bruta", {})[col] = soma

    valores = {k: linhas.get(k, 0.0) for k in
               ("bruta", "vencimentos", "patronal", "aposentadorias", "pensoes",
                "terceirizacao", "exerc_ant", "indenizacoes", "vinculados",
                "enfermagem", "nao_executada", "deducoes", "liquida")}

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida",
                           f"RGF_{ano}_Q{quadrimestre}_Anexo1_ACERVO.xlsx")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    gerar_oficial.gerar(destino, valores, {}, {}, {}, {}, colunas)
    print(f"\npronto: {destino}")
    print()
    for k, v in valores.items():
        print(f"   {k:18} {v:>20,.2f}")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--quadrimestre", type=int, default=3, choices=(1, 2, 3))
    ap.add_argument("--balancete", help="Balancete Consolidado (fornece a classe 8)")
    a = ap.parse_args()
    raise SystemExit(main(a.ano, a.quadrimestre, a.balancete))
