# -*- coding: utf-8 -*-
"""Aba de verificação por anexo — valor apurado, homologado e desvio.

Gera `saida/verificacao_anexos.xlsx` com uma aba por demonstrativo e uma aba de
resumo. Cada linha traz o valor apurado pela matriz, o valor de referência
(homologado do Siconfi ou planilha da equipe) e o desvio.

Regra: **o desvio é sempre calculado, nunca arredondado para zero**. Um anexo
que não fecha aparece com o número e a explicação, não com "OK".
"""
from __future__ import annotations

import csv
import os
import sys
from collections import OrderedDict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))
sys.path.insert(0, AQUI)

SAIDA = os.path.join(AQUI, "saida")
SICONFI = os.path.join(AQUI, "dados", "siconfi")

MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro")

#: coluna do CSV do RGF para cada mês de 2026 (o <MR> é agosto)
COLUNA_RGF = {1: "<MR-7>", 2: "<MR-6>", 3: "<MR-5>", 4: "<MR-4>",
              5: "<MR-3>", 6: "<MR-2>", 7: "<MR-1>", 8: "<MR>"}


def _linha(item: str, apurado: float, referencia: float,
           obs: str = "") -> dict:
    desvio = apurado - referencia
    return {"item": item, "apurado": apurado, "referencia": referencia,
            "desvio": desvio, "ok": abs(desvio) < 1.0, "obs": obs}


# --------------------------------------------------------------------------
def anexo1() -> list[dict]:
    """RGF Anexo 1 — I, II e III por mês, contra o homologado do Siconfi."""
    import mapa_anexo1 as MAPA

    caminho = os.path.join(SICONFI, "rgf", "RGF_RGF-Anexo_01_24_2026_p2.csv")
    if not os.path.exists(caminho):
        return []
    rows = list(csv.DictReader(open(caminho, encoding="utf-8-sig"), delimiter=";"))
    oficial = {}
    for r in rows:
        if r["conta"] in ("DESPESA BRUTA COM PESSOAL (I)",
                          "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)",
                          "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)"):
            oficial[(r["conta"], r["coluna"])] = float(r["valor"])

    saida = []
    for mes in range(1, 9):
        nome = MESES[mes - 1]
        s = MAPA.secoes(nome)
        q = MAPA.quadro_ii(nome)
        col = COLUNA_RGF[mes]
        pares = (
            ("I — Despesa Bruta", s["despesa_bruta"], "DESPESA BRUTA COM PESSOAL (I)"),
            ("II — Não Computadas", q["total"],
             "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)"),
            ("III — Despesa Líquida", s["despesa_bruta"] - q["total"],
             "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)"),
        )
        for rotulo, valor, chave in pares:
            ref = oficial.get((chave, col))
            if ref is None:
                continue
            saida.append(_linha(f"{nome} — {rotulo}", valor, ref))
    return saida


# --------------------------------------------------------------------------
def anexo5() -> list[dict]:
    """RGF Anexo 5 — as células contra a planilha da equipe (2025 Q3)."""
    import rgf_anexo5_vinculacao as A5

    filtros, oficial = A5.ler_planilha(A5.PLANILHA)
    if "Outras Vinculações Legais" in filtros:
        pos, tam, lista = filtros["Outras Vinculações Legais"]
        filtros["Outras Vinculações Legais"] = (pos, tam, [f for f in lista if f != "759"])
    saida = []
    for nome, fr in filtros.items():
        valores = oficial.get(nome)
        if not valores:
            continue
        for i, (chave, (prefixos, classe, sinal, excluir)) in enumerate(A5.COLUNAS.items()):
            if i >= len(valores) or valores[i] is None:
                continue
            v = A5.apurar(2025, 12, prefixos, fr, classe=classe, sinal=sinal,
                          excluir=excluir)
            if chave == "e" and nome == A5.LINHA_NAO_VINCULADOS:
                v += A5.apurar_nao_executada(2025, 12, fr)
            saida.append(_linha(f"{nome[:40]} ({chave})", v, valores[i]))
    return saida


# --------------------------------------------------------------------------
def anexo9() -> list[dict]:
    """RREO Anexo 9 — despesa de capital e receita de operações de crédito."""
    import rreo_anexo9 as A9

    of, ms, rec = A9.oficial(), A9.matriz(), A9.receita()
    saida = []
    for chave, rotulo in A9.LINHAS.items():
        saida.append(_linha(rotulo, ms.get(chave, 0.0), of.get(chave, 0.0)))
    saida.append(_linha("Receitas de operações de crédito (I)",
                        rec["realizadas"], of.get("receita", 0.0),
                        f"refinanciamento {rec['refinanciamento']:,.2f}"))
    return saida


# --------------------------------------------------------------------------
def anexo13() -> list[dict]:
    """RREO Anexo 13 — PPP: saldos e despesa do contrato."""
    import rreo_anexo13 as A13

    ant = A13.saldos(2025, 12)
    atu = A13.saldos(2026, 8)
    referencias = {
        "total_ativos": ("TOTAL DE ATIVOS", 400_000_000.00, 400_000_000.00),
        "total_passivos": ("TOTAL DE PASSIVOS", 215_455_288.93, 196_757_187.16),
        "atos_potenciais": ("ATOS POTENCIAIS PASSIVOS", 38_506_744.29, 413_225_632.16),
    }
    saida = []
    for chave, (rotulo, of_ant, of_atu) in referencias.items():
        saida.append(_linha(f"{rotulo} — 31/12/2025", ant[chave], of_ant))
        saida.append(_linha(f"{rotulo} — até o bimestre", atu[chave], of_atu))
    saida.append(_linha("Despesa do contrato (Arena das Dunas)",
                        A13.despesa_contrato(2026, 8), 102_811_000.00))
    return saida


# --------------------------------------------------------------------------
def anexo2() -> list[dict]:
    """RGF Anexo 2 — DCL contra a base da planilha da equipe."""
    import rgf_anexo2_dcl as D

    saldo = D.ler_balancete(D.BALANCETE)
    secoes = D.ler_base(D.PLANILHA)
    saida = []
    for nome, contas in secoes.items():
        if not contas:
            continue
        oficial = D.OFICIAL.get(nome)
        if oficial is None:
            continue
        saida.append(_linha(nome[:48], D.apurar_secao(saldo, contas), oficial))
    return saida


# --------------------------------------------------------------------------
FONTES = OrderedDict((
    ("RGF Anexo 1", anexo1),
    ("RGF Anexo 2", anexo2),
    ("RGF Anexo 5", anexo5),
    ("RREO Anexo 9", anexo9),
    ("RREO Anexo 13", anexo13),
))


def gerar(caminho: str | None = None) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    resumo = wb.active
    resumo.title = "RESUMO"
    resumo.append(["anexo", "células", "exatas", "divergentes", "desvio absoluto"])
    for c in range(1, 6):
        resumo.cell(1, c).font = Font(bold=True)

    for nome, funcao in FONTES.items():
        linhas = funcao()
        ws = wb.create_sheet(nome[:31])
        ws.append(["item", "apurado", "referência", "desvio", "situação", "observação"])
        for c in range(1, 7):
            ws.cell(1, c).font = Font(bold=True)
        exatas = 0
        soma = 0.0
        for l in linhas:
            exatas += bool(l["ok"])
            soma += abs(l["desvio"])
            ws.append([l["item"], l["apurado"], l["referencia"], l["desvio"],
                       "OK" if l["ok"] else "DIVERGENTE", l["obs"]])
            if not l["ok"]:
                ws.cell(ws.max_row, 5).fill = PatternFill("solid", fgColor="FFF2CC")
        for col, largura in (("A", 52), ("B", 20), ("C", 20), ("D", 16),
                             ("E", 14), ("F", 34)):
            ws.column_dimensions[col].width = largura
        resumo.append([nome, len(linhas), exatas, len(linhas) - exatas, soma])

    for col, largura in (("A", 16), ("B", 12), ("C", 12), ("D", 14), ("E", 22)):
        resumo.column_dimensions[col].width = largura
    destino = caminho or os.path.join(SAIDA, "verificacao_anexos.xlsx")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    wb.save(destino)
    return destino


def main() -> int:
    destino = gerar()
    print(f"planilha gerada: {destino}\n")
    print(f"{'anexo':<16}{'células':>9}{'exatas':>8}{'divergentes':>13}")
    for nome, funcao in FONTES.items():
        linhas = funcao()
        exatas = sum(1 for l in linhas if l["ok"])
        print(f"{nome:<16}{len(linhas):>9}{exatas:>8}{len(linhas) - exatas:>13}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
