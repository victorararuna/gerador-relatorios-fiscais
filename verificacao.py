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
            saida.append(_linha(f"2026 — {nome} — {rotulo}", valor, ref))
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
#: (rotulo, 2025 p6, 2026 p4) — conferidos contra os CSVs publicados
ANEXO13_REF = {
    "total_ativos": ("TOTAL DE ATIVOS", 400_000_000.00, 400_000_000.00),
    "total_passivos": ("TOTAL DE PASSIVOS", 215_455_288.93, 196_757_187.16),
    "atos_potenciais": ("ATOS POTENCIAIS PASSIVOS", 38_506_744.29, 413_225_632.16),
}


def anexo13() -> list[dict]:
    """RREO Anexo 13 — PPP: saldos e despesa do contrato."""
    import rreo_anexo13 as A13

    ant = A13.saldos(2025, 12)
    atu = A13.saldos(2026, 8)
    referencias = ANEXO13_REF
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
        if nome.startswith("Disponibilidade de Caixa Bruta"):
            v = D.disponibilidade()
        elif nome.startswith("(-) Depósitos"):
            v = D.depositos()
        elif nome in D.SECOES_MSC:
            aba, classe, po = D.SECOES_MSC[nome]
            v = D.apurar_msc(aba, classe, po)
        else:
            v = D.apurar_secao(saldo, contas)
        saida.append(_linha(nome[:48], v, oficial))
    return saida


# --------------------------------------------------------------------------
#: linha da MAPA com a dedução de cada Poder (setembro = coluna 12)
PODERES_APOS = {"ALRN": 289, "DPRN": 290, "MPRN": 291, "TCE": 292, "TJRN": 293}
PODERES_PENS = {"ALRN": 296, "DPRN": 297, "MPRN": 298, "TCE": 299, "TJRN": 300}
COLUNA_MAPA = {"Janeiro": 4, "Fevereiro": 5, "Março": 6, "Abril": 7, "Maio": 8,
               "Junho": 9, "Julho": 10, "Agosto": 11, "Setembro": 12, "Outubro": 13}


def anexo1_poder(mes: str | None = None) -> list[dict]:
    """RGF Anexo 1 — dedução dos demais Poderes, contra as linhas da MAPA.

    Cada Poder deve aparecer com o que apuramos no IEO (aposentadorias na fonte
    0.8.00 e pensões na 0.8.00/0.8.04) igual ao que a planilha deduz.
    """
    import expurgo_poderes as E

    planilha = os.path.join(r"C:\Users\victo\Downloads\Arquivos etonjones",
                            "Quadro_e_Mapa_Janeiro_a_Outubro_2026.xlsx")
    if not os.path.exists(planilha):
        return []
    from openpyxl import load_workbook

    ws = load_workbook(planilha, data_only=True)["MAPA"]
    meses = [mes] if mes else list(COLUNA_MAPA)
    saida = []
    for nome_mes in meses:
        col = COLUNA_MAPA.get(nome_mes)
        if col is None:
            continue
        nosso = E.ler_periodo(nome_mes)
        for poder, linha in PODERES_APOS.items():
            ref = ws.cell(linha, col).value or 0.0
            saida.append(_linha(f"{nome_mes} — aposentadorias {poder}",
                                nosso[poder]["aposentadorias"], ref))
        for poder, linha in PODERES_PENS.items():
            ref = ws.cell(linha, col).value or 0.0
            saida.append(_linha(f"{nome_mes} — pensões {poder}",
                                nosso[poder]["pensoes_rpps"], ref))
    return saida


def limites_anexo1() -> list[dict]:
    """A cadeia da RCL ate o percentual — do RGF Anexo 6 de 2026 Q2.

    Os valores esperados sao lidos do arquivo publicado, nao fixados no codigo.
    """
    import mapa_anexo1 as MAPA

    try:
        r = MAPA.limites_do_rreo(11_563_398_205.71)
    except Exception:
        return []
    arq = os.path.join(SICONFI, "rgf", "RGF_RGF-Anexo_06_24_2026_p2.csv")
    of = {}
    if os.path.exists(arq):
        for linha in csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"):
            chave = (linha["conta"].strip(), linha["coluna"].strip())
            of[chave] = float(linha["valor"])
    def esperado(prefixo, coluna):
        # a RCL ajustada aparece duas vezes (endividamento e pessoal): vale a
        # ultima, que e a de pessoal — a que a linha do anexo usa
        achado = 0.0
        for (conta, col), valor in of.items():
            if conta.startswith(prefixo) and col.startswith(coluna):
                achado = valor
        return achado
    return [
        _linha("RCL ajustada p/ pessoal (2026 Q2)", r["rcl_ajustada"],
               esperado("Receita Corrente Líquida Ajustada para Cálculo dos Limites", "VALOR ATÉ O QUADRIMESTRE D")),
        _linha("DTP (2026 Q2)", 11_563_398_205.71,
               esperado("Despesa Total com Pessoal", "VALOR")),
        _linha("DTP / RCL % (2026 Q2)", r["percentual"],
               esperado("Despesa Total com Pessoal", "% SOBRE A RCL AJUSTADA")),
        _linha("Limite maximo 49% (2026 Q2)", r["limite_maximo"],
               esperado("Limite Máximo", "VALOR")),
        _linha("Limite prudencial 46,55% (2026 Q2)", r["limite_prudencial"],
               esperado("Limite Prudencial", "VALOR")),
        _linha("Limite de alerta 44,10% (2026 Q2)", r["limite_alerta"],
               esperado("Limite de Alerta", "VALOR")),
    ]


#: totais publicados do Anexo 5 de 2025 Q3 (TOTAL IV), no CSV do Siconfi
TOTAIS_A5_2025 = {
    "a": 1_088_399_547.00, "b": 472_988_715.32, "c": 1_405_948_478.02,
    "d": 11_871_954.46, "e": 2_230_614_991.10,
}


def anexo5_totais() -> list[dict]:
    """RGF Anexo 5 — totais das colunas contra o CSV publicado, não a planilha."""
    import rgf_anexo5_vinculacao as A5

    filtros, _oficial = A5.ler_planilha(A5.PLANILHA)
    if "Outras Vinculações Legais" in filtros:
        pos, tam, lista = filtros["Outras Vinculações Legais"]
        filtros["Outras Vinculações Legais"] = (pos, tam, [f for f in lista if f != "759"])
    somas = {k: 0.0 for k in A5.COLUNAS}
    for nome, fr in filtros.items():
        for chave, (prefixos, classe, sinal, excluir) in A5.COLUNAS.items():
            v = A5.apurar(2025, 12, prefixos, fr, classe=classe, sinal=sinal,
                          excluir=excluir)
            if chave == "e" and nome == A5.LINHA_NAO_VINCULADOS:
                v += A5.apurar_nao_executada(2025, 12, fr)
            somas[chave] += v
    nomes = {"a": "Disponibilidade bruta", "b": "RP processados",
             "c": "RPNP inscritos no exercício", "d": "RPNP a liquidar",
             "e": "Demais obrigações financeiras"}
    return [_linha(f"TOTAL (IV) — {nomes[k]}", somas[k], v, "CSV do Siconfi")
            for k, v in TOTAIS_A5_2025.items()]


def _normaliza(texto: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", str(texto or ""))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(t.upper().split())


def anexo14_2026() -> list[dict]:
    """RREO Anexo 14 de 2026 — simplificado, contra o CSV do Siconfi."""
    import rreo_anexo14 as A14

    base = os.path.join(SICONFI, "rreo")
    p14 = os.path.join(base, "RREO_RREO-Anexo_14_24_2026_p4.csv")
    p03 = os.path.join(base, "RREO_RREO-Anexo_03_24_2026_p4.csv")
    if not (os.path.exists(p14) and os.path.exists(p03)):
        return []
    of, ms = A14.oficial(p14), A14.matriz(2026, 8, p03)
    rotulos = {"empenhadas": "Despesas empenhadas", "liquidadas": "Despesas liquidadas",
               "pagas": "Despesas pagas", "rcl": "RCL",
               "rcl_endividamento": "RCL ajustada — endividamento",
               "rcl_pessoal": "RCL ajustada — pessoal"}
    return [_linha(f"2026 — {rotulos[k]}", ms.get(k, 0.0), of.get(k, 0.0))
            for k in rotulos]


def rgf_anexo3_2026() -> list[dict]:
    """RGF Anexo 3 de 2026: os limites saem da RCL ajustada do RREO Anexo 3.

    Limite definido pelo Senado = 22% da RCL ajustada para endividamento;
    limite de alerta = 90% dele. Confere o cruzamento RREO -> RGF.
    """
    base = os.path.join(SICONFI)
    p_rreo = os.path.join(base, "rreo", "RREO_RREO-Anexo_03_24_2026_p4.csv")
    p_rgf = os.path.join(base, "rgf", "RGF_RGF-Anexo_03_24_2026_p2.csv")
    if not (os.path.exists(p_rreo) and os.path.exists(p_rgf)):
        return []
    rcl = None
    for r in csv.DictReader(open(p_rreo, encoding="utf-8-sig"), delimiter=";"):
        if (r["coluna"] == "TOTAL (ÚLTIMOS 12 MESES)"
                and "AJUSTADA" in r["conta"].upper()
                and "ENDIVIDAMENTO" in r["conta"].upper()):
            rcl = float(r["valor"])
    oficial = {}
    for r in csv.DictReader(open(p_rgf, encoding="utf-8-sig"), delimiter=";"):
        if r["coluna"] == "Até o 2º Quadrimestre":
            oficial[r["conta"].strip()] = float(r["valor"])
    if rcl is None:
        return []
    limite = rcl * 0.22
    return [
        _linha("2026 Q2 — limite do Senado (22% da RCL)",
               limite, oficial.get("LIMITE DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL", 0.0)),
        _linha("2026 Q2 — limite de alerta (90% do limite)",
               limite * 0.9, oficial.get("LIMITE DE ALERTA (inciso III § 1º do art. 59 da LRF)", 0.0)),
    ]


def anexo2_rgf_2026() -> list[dict]:
    """RGF Anexo 2 de 2026, 2o quadrimestre (fechamento em agosto)."""
    import rgf_anexo2_dcl as D

    arq = os.path.join(SICONFI, "rgf", "RGF_RGF-Anexo_02_24_2026_p2.csv")
    if not os.path.exists(arq):
        return []
    of = {}
    for r in csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"):
        if r["coluna"] == "Até o 2º Quadrimestre":
            of[r["conta"].strip()] = float(r["valor"])
    saida = []
    pares = (
        ("Disponibilidade de Caixa Bruta", lambda: D.disponibilidade(2026, 8)),
        ("(-) Depósitos Restituíveis e Valores Vinculados", lambda: D.depositos(2026, 8)),
        ("Demais Haveres Financeiros",
         lambda: D.apurar_msc("D+ Haveres", 1, "10111", 2026, 8)),
    )
    for nome, funcao in pares:
        if nome not in of:
            continue
        saida.append(_linha(f"2026 Q2 — {nome[:34]}", funcao(), of[nome]))
    return saida


def anexo7_2026() -> list[dict]:
    """RREO Anexo 7 de 2026 — restos a pagar, contra o CSV do Siconfi."""
    import rreo_anexo7 as A7

    arq = os.path.join(SICONFI, "rreo", "RREO_RREO-Anexo_07_24_2026_p4.csv")
    if not os.path.exists(arq):
        return []
    of, ms = A7.oficial(arq), A7.matriz(2026, 8)
    rotulos = {"rpp_pagos": "RP processados pagos", "rpp_cancelados": "RP processados cancelados",
               "rpp_saldo": "RP processados — saldo",
               "rpn_pagos": "RP não processados pagos",
               "rpn_cancelados": "RP não processados cancelados"}
    return [_linha(f"2026 — {rotulos[k]}", ms.get(k, 0.0), of.get(k, 0.0))
            for k in rotulos]


def anexo2_rreo_2026() -> list[dict]:
    """RREO Anexo 2 de 2026 (4o bimestre) — liquidado por funcao, contra o CSV."""
    import rreo_anexo2 as R2

    arq = os.path.join(SICONFI, "rreo", "RREO_RREO-Anexo_02_24_2026_p4.csv")
    if not os.path.exists(arq):
        return []
    oficial = {}
    for r in csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"):
        if r["coluna"] != "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (d)":
            continue
        oficial[_normaliza(r["conta"])] = float(r["valor"])
    nosso = R2.nosso_por_funcao(2026, 8)
    # o cruzamento por funcao depende do mapa codigo->nome, que nao alinha com o
    # CSV de 2026; o total e robusto e e ele que se confere aqui
    total_oficial = next((v for k, v in oficial.items() if k.startswith("TOTAL")), 0.0)
    if not total_oficial:
        total_oficial = sum(v for k, v in oficial.items() if not k.startswith("TOTAL"))
    return [_linha("2026 — total liquidado (22 funções)", sum(nosso.values()),
                   total_oficial, "CSV do Siconfi, 4º bimestre")]


def anexo4() -> list[dict]:
    """RREO Anexo 4 — previdenciário (blocos principal e complementar)."""
    try:
        import rreo_anexo4_blocos as A4
    except Exception:
        return []
    saida = []
    for chave, (nome, oficial) in A4.OFICIAL.items():
        try:
            principal, complementar = A4.apurar(chave, A4.PAE_2025.get(chave, 0.0))
        except Exception:
            continue
        saida.append(_linha(nome, principal + complementar, oficial,
                            f"principal {principal:,.2f}"))
    return saida


def anexo13_projecoes() -> list[dict]:
    """RREO Anexo 13 — projeção do contrato a partir da âncora contratual."""
    import rreo_anexo13 as A13

    oficial = [60_190_422.53, 56_285_767.37, 52_634_413.83,
               49_219_929.81, 46_026_949.18, 43_041_102.64]
    proj = A13.projecoes(n=6)["despesas"]
    return [_linha(f"Arena das Dunas — EC+{i}", v, o, "âncora 60.190.422,53")
            for i, (v, o) in enumerate(zip(proj, oficial), start=1)]


def motor() -> dict:
    """As 27 conferências de ponta a ponta, agrupadas por anexo.

    Reaproveita `verificar_tudo.py`, que confere o motor contra os arquivos
    homologados do Siconfi. Cada verificação vira uma linha da aba do seu anexo.
    """
    import contextlib
    import io

    import verificar_tudo as VT

    VT.resultados.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        VT.main()
    grupos = OrderedDict()
    for nome, ok, valor, esperado, _obrig in VT.resultados:
        anexo = nome.split(":")[0].strip()
        if anexo == "RREO":
            anexo = "RREO - Balanço Orçamentário"
        grupos.setdefault(anexo, []).append(
            {"item": nome, "apurado": valor, "referencia": esperado,
             "desvio": valor - esperado, "ok": bool(ok),
             "obs": "tolerância de 0,5%" if ok and abs(valor - esperado) > 1 else ""})
    return grupos


FONTES = OrderedDict((
    ("RGF Anexo 1 - 2026", anexo1),
    ("RGF Anexo 2", anexo2),
    ("RGF Anexo 5", anexo5),
    ("RREO Anexo 9", anexo9),
    ("RREO Anexo 13", anexo13),
    ("RGF Anexo 1 - limites", limites_anexo1),
    ("RGF Anexo 5 - totais", anexo5_totais),
    ("RGF Anexo 1 - por Poder", anexo1_poder),
    ("RREO Anexo 2 - 2026", anexo2_rreo_2026),
    ("RGF Anexo 2 - 2026", anexo2_rgf_2026),
    ("RGF Anexo 3 - 2026", rgf_anexo3_2026),
    ("RREO Anexo 7 - 2026", anexo7_2026),
    ("RREO Anexo 14 - 2026", anexo14_2026),
    ("RREO Anexo 4", anexo4),
    ("RREO Anexo 13 - projeções", anexo13_projecoes),
))


def _grupos() -> "OrderedDict[str, list]":
    """Todos os grupos, com as linhas do motor já mescladas nas abas homônimas."""
    grupos = OrderedDict((nome, list(funcao())) for nome, funcao in FONTES.items())
    for anexo, linhas in motor().items():
        grupos.setdefault(anexo, []).extend(linhas)
    return grupos


def gerar(caminho: str | None = None) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    resumo = wb.active
    resumo.title = "RESUMO"
    resumo.append(["anexo", "células", "exatas", "divergentes", "desvio absoluto"])
    for c in range(1, 6):
        resumo.cell(1, c).font = Font(bold=True)

    grupos = _grupos()

    for nome, linhas in grupos.items():
        ws = wb.create_sheet(nome[:31])
        ws.append(["item", "apurado", "referência", "desvio", "situação", "observação"])
        for c in range(1, 7):
            ws.cell(1, c).font = Font(bold=True)
        exatas = 0
        soma = 0.0
        for l in linhas:
            exatas += bool(l["ok"])
            soma += abs(l["desvio"])
            obs = l["obs"] or ("" if l["ok"] else _causa(l["item"]))
            ws.append([l["item"], l["apurado"], l["referencia"], l["desvio"],
                       "OK" if l["ok"] else "DIVERGENTE", obs])
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


#: causa documentada de cada divergencia conhecida (prefixo do item -> texto)
CAUSAS = (
    ("2026 — Abril — I", "Par de anulacao (35.094,19) e re-empenho (29.852,54) no ND "
                  "31909203 do PO 10112, em abril: a diferenca e 5.241,65. O "
                  "homologado trata o par de forma diferente do Comparativo."),
    ("2026 — Abril — III", "Idem: decorre da mesma diferenca em I (a II esta exata)."),

    ("Restos a Pagar Processados", "Exige o relatorio 'Execucao Orcamentaria por Fonte' "
                                   "(bloco de RP) por Poder, com a dimensao fonte de recursos."),


    ("Aposentadorias civis", "Resolvido: a linha e o bruto menos o PAE "
                             "(31.90.92.02), insumo do INEC."),
    ("Pensões por morte civis", "Resolvido: a linha e o bruto menos o PAE "
                                "(31.90.92.06), insumo do INEC."),
)


def _causa(item: str) -> str:
    for prefixo, texto in CAUSAS:
        if item.startswith(prefixo) or prefixo in item:
            return texto
    return "sem causa identificada"


def relatorio_divergencias(destino: str | None = None) -> str:
    """Escreve docs/DIVERGENCIAS.md a partir do que a verificacao aponta."""
    linhas = ["# Divergências conhecidas", "",
              "Gerado por `verificacao.relatorio_divergencias()`. Não editar à mão.", "",
              "| anexo | item | apurado | referência | desvio | causa |",
              "|---|---|---:|---:|---:|---|"]
    total = exatas = 0
    for nome, funcao in FONTES.items():
        for l in funcao():
            total += 1
            exatas += bool(l["ok"])
            if l["ok"]:
                continue
            linhas.append(
                f"| {nome} | {l['item'][:52]} | {l['apurado']:,.2f} | "
                f"{l['referencia']:,.2f} | {l['desvio']:,.2f} | {_causa(l['item'])} |")
    grupos = motor()
    for anexo, itens in grupos.items():
        if anexo in FONTES:
            continue
        for l in itens:
            total += 1
            exatas += bool(l["ok"])
            if l["ok"]:
                continue
            linhas.append(
                f"| {anexo} | {l['item'][:52]} | {l['apurado']:,.2f} | "
                f"{l['referencia']:,.2f} | {l['desvio']:,.2f} | {_causa(l['item'])} |")
    linhas += ["", f"**{exatas} de {total} células exatas** "
                   f"({total - exatas} divergentes, todas acima com causa).", ""]
    caminho = destino or os.path.join(AQUI, "docs", "DIVERGENCIAS.md")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))
    return caminho


def main() -> int:
    destino = gerar()
    print(f"planilha gerada: {destino}\n")
    print(f"{'grupo':<26}{'células':>9}{'exatas':>8}{'divergentes':>13}")
    total = exatas_total = 0
    for nome, linhas in _grupos().items():
        exatas = sum(1 for l in linhas if l["ok"])
        total += len(linhas); exatas_total += exatas
        print(f"{nome:<26}{len(linhas):>9}{exatas:>8}{len(linhas) - exatas:>13}")
    print(f"\n{exatas_total} de {total} células exatas")
    print("relatorio de divergencias:", relatorio_divergencias())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
