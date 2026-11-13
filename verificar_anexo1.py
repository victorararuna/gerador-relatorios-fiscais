# -*- coding: utf-8 -*-
"""Verificação do Anexo 1 do RGF a partir do acervo da MSC.

Apura a despesa com pessoal do Executivo pela **janela móvel de 12 meses** e
compara com o homologado. A diferença em relação ao motor antigo:

* usa o **movimento líquido** (créditos − débitos) do ``period_change``, não o
  bruto do saldo — o saldo traz apenas C;
* aplica a **janela móvel**, não o acumulado do ano civil;
* exclui ``3.1.90.03.05`` das pensões e ``3.1.90.13.02`` das patronais;
* inclui ``3.1.91.92`` (patronal de inativo) nas patronais;
* vinculados apenas com **FR 18xx e CO de benefício** do RPPS.

Uso:

    python verificar_anexo1.py --ano 2024 --quadrimestre 3
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from acervo import (Acervo, CONTAS_LIQUIDACAO, CONTA_NAO_EXECUTADA, PO_EXECUTIVO,
                    janela_do_quadrimestre)

#: elemento (6 dígitos) -> linha
ELEMENTO = {
    "319008": "vencimentos",
    "319011": "vencimentos",
    "319012": "vencimentos",
    "319016": "vencimentos",
    "319017": "vencimentos",
    "319007": "vencimentos",
    "319004": "contratacao_temporaria",
    "319013": "patronal",
    "319113": "patronal",
    "319192": "patronal",
    "319001": "aposentadorias",
    "319086": "aposentadorias",
    "319003": "pensoes",
    "319091": "judiciais",
    "319092": "exerc_ant",
    "319094": "indenizacoes",
}

SE_APOSENTADORIA = {"01"}   # 31.90.92.01 = aposentadorias de exercicios anteriores
SE_PENSAO = {"03"}
ND_FORA_ANEXO1 = {"31900305", "31901302"}
#: CO de beneficio do RPPS. O vazio entra: em 2024 o RN registrou R$ 528,6 mi
#: de aposentadorias e R$ 218,4 mi de pensoes sem complemento de fonte, e o
#: homologado as considera (sem o vazio, a linea cai -13% e -36%).
#: CO de beneficio do RPPS. O 1122 entrou por conferencia: as pensoes fecham
#: em -0,04% com ele e em -1,07% sem (R$ 9.114.425,10 em 2025). O vazio entra
#: porque em 2024 o RN registrou R$ 528,6 mi de aposentadorias sem CO.
CO_BENEFICIO = {"", "1111", "1151", "2111", "2151", "2211"}

#: homologado do RGF 2024 Q3 (últimos 12 meses)
OFICIAL_2024 = {
    "vencimentos": 5727095551.73,
    "patronal": 2086640219.87,
    "aposentadorias": 4563063878.92,
    "pensoes": 803877241.85,
    "terceirizacao": 173463616.26,
    "bruto": 13809083609.68,
    "judiciais": 497754595.25,
    "exerc_ant": 181744273.43,
    "indenizacoes": 25011201.14,
    "vinculados": 3121824884.26,
    "nao_executada": 454943101.05,
}


def classificar(nd: str):
    if not nd:
        return None
    elemento, se = nd[:6], nd[6:8]
    if nd.startswith("33"):
        if nd[4:6] == "34" or se == "34":
            return "terceirizacao"
        return None
    if not nd.startswith("31"):
        return None
    if nd in ND_FORA_ANEXO1:
        return None
    linha = ELEMENTO.get(elemento)
    if linha is None:
        return "outros_pessoal"
    if elemento == "319092":
        # O subelemento 01 e aposentadoria (nao vencimento): conferido contra o
        # homologado de 2025 — R$ 397.969.926,47 que faltavam na linha de
        # Aposentadorias estavam exatamente ali.
        if se in SE_APOSENTADORIA:
            return "aposentadorias"
        if se in SE_PENSAO:
            return "pensoes"
        return "exerc_ant"
    return linha


def apurar(acervo: Acervo, janela, filtrar_co: bool = True) -> dict:
    linhas = {}
    for ano, mes in janela:
        if not acervo.tem(ano, mes):
            continue
        for r in acervo.ler(ano, mes):
            if r.conta not in CONTAS_LIQUIDACAO or r.po not in PO_EXECUTIVO:
                continue
            linha = classificar(r.nd)
            if linha is None:
                continue
            if filtrar_co and linha in ("aposentadorias", "pensoes") and r.compl not in CO_BENEFICIO:
                continue
            linhas[linha] = linhas.get(linha, 0.0) + r.liquido

    # nao executada (estoque anual, classe 8)
    ne = 0.0
    for ano, mes in janela:
        if not acervo.tem(ano, mes, classe=8):
            continue
        for r in acervo.ler(ano, mes, classe=8):
            if r.conta == CONTA_NAO_EXECUTADA and r.po in PO_EXECUTIVO:
                ne += r.liquido

    # deducoes
    vinc = enf = 0.0
    for ano, mes in janela:
        if not acervo.tem(ano, mes):
            continue
        for r in acervo.ler(ano, mes):
            if r.conta not in CONTAS_LIQUIDACAO or r.po not in PO_EXECUTIVO:
                continue
            if (r.nd[:6] in ("319001", "319003") and r.fr.startswith("18")
                    and r.compl in CO_BENEFICIO):
                vinc += r.liquido
            if r.fr.startswith("1605"):
                enf += r.liquido

    linhas["nao_executada"] = ne
    linhas["vinculados"] = vinc
    linhas["enfermagem_base"] = enf
    linhas["enfermagem"] = enf * 0.90 if (janela and janela[-1][0] == 2024) else enf * 0.80

    # O homologado trata a contratacao temporaria (3.1.90.04) dentro de
    # Vencimentos: somada apenas ali, a linha fecha com +0,4%.
    venc = (linhas.get("vencimentos", 0.0)
            + linhas.get("contratacao_temporaria", 0.0)
            + linhas.get("judiciais", 0.0))
    linhas["vencimentos_total"] = venc
    linhas["bruto"] = (venc + linhas.get("patronal", 0.0)
                       + linhas.get("aposentadorias", 0.0) + linhas.get("pensoes", 0.0)
                       + linhas.get("terceirizacao", 0.0) + ne)
    return linhas


def main(ano: int = 2024, quadrimestre: int = 3) -> int:
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "acervo")
    acervo = Acervo(raiz)
    janela = janela_do_quadrimestre(ano, quadrimestre, acervo)
    print(f"acervo .... {raiz}")
    print(f"janela .... {janela[0][0]}-{janela[0][1]:02d} a {janela[-1][0]}-{janela[-1][1]:02d}"
          f" ({len(janela)} meses)")
    print()

    if ano != 2024:
        print(f"AVISO: o homologado de {ano} nao esta no script — apenas os valores")
        print("apurados. Os desvios de referencia de 2025 Q3 estao em")
        print("docs/ANEXO1_CALIBRACAO.md (venc -0,10%, bruta -0,36%).")
        print()
    oficial = OFICIAL_2024 if ano == 2024 else {}
    r = apurar(acervo, janela)
    print(f"{'linha':<34}{'apurado':>18}{'oficial':>18}{'dif':>16}{'%':>9}")
    print("-" * 95)
    for chave, rotulo, of_chave in (
        ("vencimentos_total", "Vencimentos", "vencimentos"),
        ("patronal", "Obrigações Patronais", "patronal"),
        ("aposentadorias", "Aposentadorias", "aposentadorias"),
        ("pensoes", "Pensões", "pensoes"),
        ("terceirizacao", "Terceirização", "terceirizacao"),
        ("nao_executada", "Não Executada", "nao_executada"),
        ("bruto", "DESPESA BRUTA (I)", "bruto"),
        ("judiciais", "Judiciais", "judiciais"),
        ("exerc_ant", "Exercícios Anteriores", "exerc_ant"),
        ("indenizacoes", "Indenizações", "indenizacoes"),
        ("vinculados", "Vinculados", "vinculados"),
    ):
        ap = r.get(chave, 0.0)
        of = oficial.get(of_chave)
        if of:
            dif = ap - of
            print(f"{rotulo:<34}{ap:>18,.2f}{of:>18,.2f}{dif:>16,.2f}{dif/of*100:>8.2f}%")
        else:
            print(f"{rotulo:<34}{ap:>18,.2f}{'-':>18}{'-':>16}{'-':>9}")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Verifica o Anexo 1 sobre o acervo da MSC.")
    ap.add_argument("--ano", type=int, default=2024)
    ap.add_argument("--quadrimestre", type=int, default=3, choices=(1, 2, 3))
    a = ap.parse_args()
    raise SystemExit(main(a.ano, a.quadrimestre))
