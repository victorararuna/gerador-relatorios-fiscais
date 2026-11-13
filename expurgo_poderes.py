# -*- coding: utf-8 -*-
"""Expurgo do Anexo 1 — leitura do IEO por blocos de subação.

O IEO é emitido por Subação / Fonte / Elemento. Cada subação abre um bloco que
vai até a próxima; dentro dele vêm as fontes e os elementos.

Regra do expurgo (validada contra a planilha da equipe em set/2026):

    aposentadorias (31.90.01, fonte 0.8.00)
  + pensões        (31.90.03, fonte 0.8.00)
  + patronal       (31.91.13, fonte 0.5.00)
  dos cinco Poderes: 218401, 221201, 222201, 222401, 222501

Os blocos de pensões usam outra codificação de subação e trazem o Poder descrito
por extenso — o leitor identifica pelo texto do bloco.
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

BASE = r"C:\Users\victo\Downloads\Arquivos etonjones"
UG = "162233"

POR_CODIGO = {"218401": "DPRN", "221201": "TJRN", "222201": "ALRN",
              "222401": "MPRN", "222501": "TCE"}
POR_TEXTO = (
    ("pensionistas - tribunal de justica", "TJRN"),
    ("pensionistas - tribunal de contas", "TCE"),
    ("pensionistas - assembleia legislativa", "ALRN"),
    ("pensionistas - ministerio publico", "MPRN"),
    ("pensionistas - defensoria", "DPRN"),
    ("pensionistas - defensoria publica", "DPRN"),
)
#: pensões especiais e montepio executadas na UG 162011 (IPERN)
PENSAO_ESP = {"412301": "ALRN", "412401": "MPRN", "412501": "TCE",
              "412601": "TJRN", "412701": "TJRN"}
PODERES = ("DPRN", "TJRN", "ALRN", "MPRN", "TCE")

RE_CODIGO = re.compile(r"^(\d{6})(?:\s|$)")
RE_FONTE = re.compile(r"^(\d\.\d\.\d{2}\.\d{6})(?:\s|$)")
RE_ELEMENTO = re.compile(r"^(\d{2}\.\d{2}\.\d{2})(?:\s|$)")
RE_NUMERO = re.compile(r"^-?\d{1,3}(?:\.\d{3})*,\d{2}$|^-?\d+,\d{2}$")


def _sem_acento(t: str) -> str:
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def _num(t: str) -> float:
    return float(t.replace(".", "").replace(",", "."))


def _linhas(pagina, janela: float = 4.0):
    por_y = defaultdict(list)
    for it in pagina.itens:
        por_y[round(it.y / janela)].append(it)
    return [(y, sorted(por_y[y], key=lambda i: i.x)) for y in sorted(por_y, reverse=True)]


def ler_mes(arquivo: str) -> dict:
    import leitor_pdf as LP

    saida = {p: {"aposentadorias": 0.0, "pensoes": 0.0, "patronal": 0.0,
                 "exerc_ant": 0.0, "indeniz": 0.0, "apos_tesouro": 0.0, "pensoes_rpps": 0.0}
             for p in PODERES}
    for pagina in LP.ler_pdf(arquivo):
        x_liq = next((it.x for it in pagina.itens
                      if it.texto.strip() == "Liquidado"), None)
        if x_liq is None:
            continue
        linhas = _linhas(pagina)
        # separa em blocos que começam por um código de 6 dígitos
        blocos, atual = [], None
        for y, itens in linhas:
            primeiro = itens[0].texto.strip() if itens else ""
            m = RE_CODIGO.match(primeiro)
            if m:
                atual = {"codigo": m.group(1), "linhas": []}
                blocos.append(atual)
            if atual is not None:
                atual["linhas"].append((y, itens))
        for bloco in blocos:
            texto = _sem_acento(" ".join(i.texto for _, itens in bloco["linhas"] for i in itens))
            poder = POR_CODIGO.get(bloco["codigo"])
            origem = "codigo"
            if poder is None and bloco["codigo"] in PENSAO_ESP:
                poder, origem = PENSAO_ESP[bloco["codigo"]], "pensao_esp"
            if poder is None:
                for chave, nome in POR_TEXTO:
                    if chave in texto:
                        poder, origem = nome, "texto"
                        break
            if poder is None:
                continue
            fonte = elemento = None
            total_050 = patr_050 = 0.0
            for y, itens in bloco["linhas"]:
                primeiro = itens[0].texto.strip() if itens else ""
                numeros = [i for i in itens if RE_NUMERO.match(i.texto.strip())]
                mf = RE_FONTE.match(primeiro)
                if mf:
                    fonte, elemento = mf.group(1), None
                    # o total da fonte é o valor na coluna Liquidado
                    if fonte.startswith("0.5.00") and len(numeros) >= 3:
                        total_050 = _num(min(numeros, key=lambda i: abs(i.x - x_liq)).texto.strip())
                    continue
                me = RE_ELEMENTO.match(primeiro)
                if me:
                    elemento = me.group(1)
                if elemento is None:
                    continue
                if len(numeros) < 3:
                    continue
                alvo = min(numeros, key=lambda i: abs(i.x - x_liq))
                valor = _num(alvo.texto.strip())
                # bloco identificado pelo código: aposentadorias e patronal
                # bloco identificado pela descrição: pensões dos pensionistas
                if origem == "codigo":
                    if elemento == "31.90.01" and (fonte or "").startswith("0.8.00"):
                        saida[poder]["aposentadorias"] += valor
                    elif elemento == "31.91.13" and (fonte or "").startswith("0.5.00"):
                        patr_050 += valor
                    elif elemento == "31.90.92":
                        saida[poder]["exerc_ant"] += valor
                    elif elemento == "31.90.94":
                        saida[poder]["indeniz"] += valor
                elif origem == "pensao_esp":
                    # pensões especiais e montepio do IPERN: Tesouro + RPPS
                    if elemento == "31.90.03" and (fonte or "").startswith(("0.5.00", "0.8.04")):
                        saida[poder]["pensoes"] += valor
                        if (fonte or "").startswith("0.8.04"):
                            saida[poder]["pensoes_rpps"] += valor
                    elif elemento == "31.90.92":
                        # DEA de pensões (MAPA linhas 234, 239 e 244)
                        saida[poder]["pensoes"] += valor
                elif elemento == "31.90.03" and (fonte or "").startswith(("0.5.00", "0.8.00", "0.8.04")):
                    saida[poder]["pensoes"] += valor
                    if (fonte or "").startswith(("0.8.00", "0.8.04")):
                        saida[poder]["pensoes_rpps"] += valor
                elif elemento == "31.90.92" and origem == "texto":
                    # DEA de pensões nos blocos da UG 162233 (linhas 234 e 244)
                    saida[poder]["pensoes"] += valor
            saida[poder]["patronal"] += patr_050
            # na fonte 0.5.00 o total da fonte é a soma dos elementos: o que não
            # for patronal é aposentadoria paga pelo Tesouro
            if origem == "codigo" and total_050 > patr_050:
                saida[poder]["apos_tesouro"] += total_050 - patr_050
    return saida


#: Estornos que o IEO imprime como valor positivo. Quando o "Disponível" fica
#: maior que o "Atualizado", o empenho foi cancelado — o manual registra o caso
#: do MPRN em fevereiro/2026 (-R$ 17.144,40 na fonte 0.8.00).
ESTORNOS = {("Fevereiro", "MPRN"): -17144.40}


def ler_periodo(mes: str) -> dict:
    """Soma as duas UGs do RPPS: 162233 (FUNFIRN) e 162011 (IPERN)."""
    somado = {p: {"aposentadorias": 0.0, "pensoes": 0.0, "patronal": 0.0,
                  "exerc_ant": 0.0, "indeniz": 0.0, "apos_tesouro": 0.0, "pensoes_rpps": 0.0}
              for p in PODERES}
    for ug in ("162233", "162011"):
        arq = os.path.join(BASE, f"Imprimir Execução Orçamentária - IEO_{ug}_{mes}.pdf")
        if not os.path.exists(arq):
            continue
        for poder, vals in ler_mes(arq).items():
            for k, v in vals.items():
                somado[poder][k] += v
    for (m, poder), valor in ESTORNOS.items():
        if m == mes and valor < 0 and somado[poder]["aposentadorias"] > 0:
            somado[poder]["aposentadorias"] = -abs(somado[poder]["aposentadorias"])
    return somado


def total(dados: dict) -> dict:
    return {k: sum(d[k] for d in dados.values())
            for k in ("aposentadorias", "pensoes", "patronal", "exerc_ant", "indeniz", "apos_tesouro", "pensoes_rpps")}


def main() -> int:
    mes = sys.argv[1] if len(sys.argv) > 1 else "Setembro"
    arquivo = os.path.join(BASE, f"Imprimir Execução Orçamentária - IEO_{UG}_{mes}.pdf")
    if not os.path.exists(arquivo):
        print(f"ausente: {arquivo}")
        return 1
    dados = ler_mes(arquivo)
    print(f"IEO {UG} — {mes}")
    print(f"{'Poder':<7}{'aposentadorias':>18}{'pensões':>15}{'patronal':>15}")
    for p in PODERES:
        d = dados[p]
        print(f"{p:<7}{d['aposentadorias']:>18,.2f}{d['pensoes']:>15,.2f}{d['patronal']:>15,.2f}")
    t = total(dados)
    soma = t["aposentadorias"] + t["pensoes"] + t["patronal"]
    print(f"{'TOTAL':<7}{t['aposentadorias']:>18,.2f}{t['pensoes']:>15,.2f}{t['patronal']:>15,.2f}")
    print(f"\nexpurgo = {soma:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())










