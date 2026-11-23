# -*- coding: utf-8 -*-
"""RREO Anexo 1 completo por ocorrencia (rodada 177).

O Anexo 1 oficial repete os grupos de despesa em dois blocos — "exceto intra"
e "intra" —, e a matriz separa os dois pela **modalidade da natureza** (ND):

    90  aplicacao direta                -> exceto intra
    91  operacao entre orgaos do ente   -> intra-orcamentaria

Este modulo apura o Anexo 1 inteiro (receita e despesa, previsao/dotacao e
execucao) e devolve `{(conta, coluna, ocorrencia): valor}`, onde a ocorrencia
0 e o bloco exceto-intra e 1 o bloco intra. `comparar` confere com um template
publicado preservando ordem e repeticao.

Formulas calibradas contra o RREO Anexo 1 publicado do RN (2025 B6).
"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

P_INI = "PREVISÃO INICIAL"
P_ATU = "PREVISÃO ATUALIZADA (a)"
NO_BIM = "No Bimestre (b)"
ATE = "Até o Bimestre (c)"
SALDO_REC = "SALDO (a-c)"
PCT_B = "% (b/a)"
PCT_C = "% (c/a)"
D_INI = "DOTAÇÃO INICIAL (d)"
D_ATU = "DOTAÇÃO ATUALIZADA (e)"
E_BIM = "DESPESAS EMPENHADAS NO BIMESTRE"
E_ATE = "DESPESAS EMPENHADAS ATÉ O BIMESTRE (f)"
SALDO_G = "SALDO (g) = (e-f)"
L_BIM = "DESPESAS LIQUIDADAS NO BIMESTRE"
L_ATE = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)"
SALDO_I = "SALDO (i) = (e-h)"
P_ATE = "DESPESAS PAGAS ATÉ O BIMESTRE (j)"

CATEGORIAS = {
    "11": "IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA",
    "12": "CONTRIBUIÇÕES", "13": "RECEITA PATRIMONIAL",
    "14": "RECEITA AGROPECUÁRIA", "15": "RECEITA INDUSTRIAL",
    "16": "RECEITA DE SERVIÇOS", "17": "TRANSFERÊNCIAS CORRENTES",
    "19": "OUTRAS RECEITAS CORRENTES", "21": "OPERAÇÕES DE CRÉDITO",
    "22": "ALIENAÇÃO DE BENS", "23": "AMORTIZAÇÕES DE EMPRÉSTIMOS",
    "24": "TRANSFERÊNCIAS DE CAPITAL", "29": "OUTRAS RECEITAS DE CAPITAL",
}
GRUPOS = {"31": "PESSOAL E ENCARGOS SOCIAIS", "32": "JUROS E ENCARGOS DA DÍVIDA",
          "33": "OUTRAS DESPESAS CORRENTES", "44": "INVESTIMENTOS",
          "45": "INVERSÕES FINANCEIRAS", "46": "AMORTIZAÇÃO DA DÍVIDA"}
R_CORRENTE = "RECEITAS CORRENTES"
R_CAPITAL = "RECEITAS DE CAPITAL"
R_EXCETO = "RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)"
R_INTRA = "RECEITAS (INTRA-ORÇAMENTÁRIAS) (II)"
R_SUB = "SUBTOTAL DAS RECEITAS (III) = (I + II)"
R_TOTAL = "TOTAL DAS RECEITAS (V) = (III + IV)"
ROT_SALDO_EX = ("SALDOS DE EXERCÍCIOS ANTERIORES",
                "Superávit Financeiro Utilizado para Créditos Adicionais")
ROT_DEFICIT = "DÉFICIT (VI)"
#: NR[:3] -> subcategoria (calibrado contra o RREO Anexo 1 publicado do RN)
SUBCATEGORIAS = {
    "111": "Impostos", "112": "Taxas", "121": "Contribuições Sociais",
    "131": "Exploração do Patrimônio Imobiliário do Estado",
    "132": "Valores Mobiliários", "133": "Exploração de Recursos Naturais",
    "136": "Cessão de Direitos",
    "139": "Demais Receitas Patrimoniais",
    "161": "Serviços Administrativos e Comerciais Gerais",
    "169": "Outros Serviços",
    "171": "Transferências da União e de suas Entidades",
    "173": "Transferências dos Municípios e de suas Entidades",
    "174": "Transferências de Instituições Privadas",
    "175": "Transferências de Outras Instituições Públicas",
    "179": "Demais Transferências Correntes",
    "191": "Multas Administrativas, Contratuais e Judiciais",
    "192": "Indenizações, Restituições e Ressarcimentos",
    "199": "Demais Receitas Correntes",
    "211": "Operações de Crédito - Mercado Interno",
    "212": "Operações de Crédito - Mercado Externo",
    "221": "Alienação de Bens Móveis",
    "242": "Transferências dos Estados e do Distrito Federal e de suas Entidades",
    "299": "Demais Receitas de Capital",
}
MODO = {"0": "90", "1": "91"}      # ocorrencia -> modalidade


def _classe5_raw(raiz, ano, mes):
    from acervo import Acervo
    return list(Acervo(raiz).ler(ano, mes, classe=5, tipo_valor="ending_balance"))


def _prev(raiz, ano, mes):
    """Previsao da receita por natureza completa (NR)."""
    from acervo import Acervo
    ac = Acervo(raiz)
    prev = defaultdict(float)
    for r in ac.ler(ano, mes, classe=5, tipo_valor="ending_balance"):
        c = r.conta or ""
        nr = r.nr or ""
        if not nr:
            continue
        v = -(r.valor if (r.natureza or "") == "C" else -r.valor)
        if c.startswith(("52111", "52112")):
            prev[("ini", nr)] += v
        if c.startswith("521"):
            prev[("atu", nr)] += v
    return prev


def _dot(raiz, ano, mes):
    """Dotacao da despesa por (grupo, modalidade)."""
    from acervo import Acervo
    ac = Acervo(raiz)
    dot = defaultdict(float)
    for r in ac.ler(ano, mes, classe=5, tipo_valor="ending_balance"):
        c = r.conta or ""
        nd = r.nd or ""
        if len(nd) < 4:
            continue
        v = -(r.valor if (r.natureza or "") == "C" else -r.valor)
        chave = (nd[:2], nd[2:4])
        if c.startswith("52211"):
            dot[("ini",) + chave] += v
        if c.startswith("5221"):
            dot[("atu",) + chave] += v
    return dot


def _receita(raiz, ano, meses):
    from acervo import Acervo
    ac = Acervo(raiz)
    por = defaultdict(float)
    for m in meses:
        try:
            regs = ac.ler(ano, m, classe=6, tipo_valor="period_change")
        except Exception:
            continue
        for r in regs:
            c = r.conta or ""
            nr = r.nr or ""
            if nr and c.startswith(("6212", "6213")):
                por[nr] += r.liquido
    return por


def _despesa(raiz, ano, meses):
    from acervo import Acervo
    ac = Acervo(raiz)
    acc = defaultdict(lambda: {"e": 0.0, "l": 0.0, "p": 0.0})
    for m in meses:
        try:
            regs = ac.ler(ano, m, classe=6, tipo_valor="period_change")
        except Exception:
            continue
        for r in regs:
            c = r.conta or ""
            if not c.startswith("62213"):
                continue
            nd = r.nd or ""
            if len(nd) < 4:
                continue
            k = (nd[:2], nd[2:4])
            acc[k]["e"] += r.liquido
            if c in ("622130300", "622130400", "622130700"):
                acc[k]["l"] += r.liquido
            if c == "622130400":
                acc[k]["p"] += r.liquido
    return acc


def celulas(raiz: str, ano: int, bimestre: int,
            subcategorias: dict | None = None) -> dict:
    """Celulas do Anexo 1.

    `subcategorias` e o mapa NR -> rotulo da subcategoria da receita. Se None,
    usa `SUBCATEGORIAS` (calibrado no RN). Um ente pode precisar de mapa
    proprio (AL, por exemplo, usa NR 134 para "Exploracao de Recursos
    Naturais" e NR 172 para "Transferencias dos Estados"). O mapa pode repetir
    o mesmo rotulo: a ocorrencia (0, 1, ...) segue a ordem de emissao do mapa,
    o que cobre os rotulos que o publicado repete em blocos diferentes.
    """
    from rreo_gerador import meses_do_bimestre
    mapa = SUBCATEGORIAS if subcategorias is None else subcategorias
    mes_fim = 2 * bimestre
    meses = meses_do_bimestre(bimestre)

    prev = _prev(raiz, ano, mes_fim)
    dot = _dot(raiz, ano, mes_fim)
    arr = _receita(raiz, ano, meses)
    arr_bim = _receita(raiz, ano, [mes_fim - 1, mes_fim])
    desp = _despesa(raiz, ano, meses)
    desp_bim = _despesa(raiz, ano, [mes_fim - 1, mes_fim])

    cel = {}

    def put(conta, coluna, valor, occ=0):
        cel[(conta, coluna, occ)] = valor

    # ---- receita: agrega por natureza (NR) nas visoes [:2] e [:3]
    def prev_agg(tipo, prefixo):
        return sum(v for k, v in prev.items() if k[0] == tipo and k[1].startswith(prefixo))

    def arr_agg(fonte, prefixo):
        return sum(v for k, v in fonte.items() if k.startswith(prefixo))

    for origem, rotulo in CATEGORIAS.items():
        put(rotulo, P_INI, prev_agg("ini", origem))
        put(rotulo, P_ATU, prev_agg("atu", origem))
        put(rotulo, NO_BIM, arr_agg(arr_bim, origem))
        put(rotulo, ATE, arr_agg(arr, origem))
    # subcategorias (NR[:3]) — a ocorrencia cresce quando o mapa repete rotulo
    vistos = {}
    for prefixo, rotulo in mapa.items():
        occ = vistos.get(rotulo, 0)
        vistos[rotulo] = occ + 1
        put(rotulo, P_INI, prev_agg("ini", prefixo), occ)
        put(rotulo, P_ATU, prev_agg("atu", prefixo), occ)
        put(rotulo, NO_BIM, arr_agg(arr_bim, prefixo), occ)
        put(rotulo, ATE, arr_agg(arr, prefixo), occ)
    for rotulo, dig in ((R_CORRENTE, ("1",)), (R_CAPITAL, ("2",)),
                        (R_EXCETO, ("1", "2")), (R_INTRA, ("7",))):
        put(rotulo, P_INI, sum(v for k, v in prev.items() if k[0] == "ini" and k[1][0] in dig))
        put(rotulo, P_ATU, sum(v for k, v in prev.items() if k[0] == "atu" and k[1][0] in dig))
        put(rotulo, NO_BIM, sum(v for k, v in arr_bim.items() if k[0] in dig))
        put(rotulo, ATE, sum(v for k, v in arr.items() if k[0] in dig))
    for col in (P_INI, P_ATU, NO_BIM, ATE):
        put(R_SUB, col, cel[(R_EXCETO, col, 0)] + cel[(R_INTRA, col, 0)])
        put(R_TOTAL, col, cel[(R_SUB, col, 0)])

    # superavit/déficit e saldos de exercicios anteriores
    saldo_ex_ant = sum(-(r.valor if (r.natureza or "") == "C" else -r.valor)
                       for r in _classe5_raw(raiz, ano, mes_fim)
                       if (r.conta or "").startswith("5221301"))
    for rotulo in ROT_SALDO_EX:
        put(rotulo, ATE, saldo_ex_ant)
        put(rotulo, NO_BIM, 0.0)
    for rotulo, occ in {(k[0], k[2]) for k in cel}:
        a = cel.get((rotulo, P_ATU, occ))
        c = cel.get((rotulo, ATE, occ))
        b = cel.get((rotulo, NO_BIM, occ))
        if a is not None and c is not None:
            put(rotulo, SALDO_REC, a - c, occ)
            if a:
                put(rotulo, PCT_B, (b or 0.0) / a * 100, occ)
                put(rotulo, PCT_C, c / a * 100, occ)

    # ---- despesa por bloco
    # occ 1 = intra (modalidade 91); occ 0 = exceto intra = TOTAL - intra.
    # Nao basta a modalidade 90: ha 40, 41, 50, 71... que tambem sao exceto intra.
    for occ, filtro in ((1, lambda m: m == "91"), (0, lambda m: m != "91")):
        for pref, nome in GRUPOS.items():
            e = sum(desp.get((pref, m), {}).get("e", 0.0)
                    for m in {k[1] for k in desp if k[0] == pref} if filtro(m))
            l = sum(desp.get((pref, m), {}).get("l", 0.0)
                    for m in {k[1] for k in desp if k[0] == pref} if filtro(m))
            p = sum(desp.get((pref, m), {}).get("p", 0.0)
                    for m in {k[1] for k in desp if k[0] == pref} if filtro(m))
            eb = sum(desp_bim.get((pref, m), {}).get("e", 0.0)
                     for m in {k[1] for k in desp_bim if k[0] == pref} if filtro(m))
            lb = sum(desp_bim.get((pref, m), {}).get("l", 0.0)
                     for m in {k[1] for k in desp_bim if k[0] == pref} if filtro(m))
            di = sum(dot.get(("ini", pref, m), 0.0)
                     for m in {k[2] for k in dot if k[0] == "ini" and k[1] == pref}
                     if filtro(m))
            da = sum(dot.get(("atu", pref, m), 0.0)
                     for m in {k[2] for k in dot if k[0] == "atu" and k[1] == pref}
                     if filtro(m))
            put(nome, D_INI, di, occ)
            put(nome, D_ATU, da, occ)
            put(nome, E_BIM, eb, occ)
            put(nome, E_ATE, e, occ)
            put(nome, SALDO_G, da - e, occ)
            put(nome, L_BIM, lb, occ)
            put(nome, L_ATE, l, occ)
            put(nome, SALDO_I, da - l, occ)
            put(nome, P_ATE, p, occ)

    # deficit = despesa empenhada total - receita arrecadada (quando positiva)
    despesa_total = sum(desp.get((p, m), {}).get("e", 0.0)
                        for p in GRUPOS for m in {k[1] for k in desp if k[0] == p})
    put(ROT_DEFICIT, ATE, max(0.0, despesa_total - cel.get((R_TOTAL, ATE, 0), 0.0)))

    # ---- agregados de despesa por bloco
    COLS_D = (D_INI, D_ATU, E_BIM, E_ATE, SALDO_G, L_BIM, L_ATE, SALDO_I, P_ATE)
    nomes = {p: n for p, n in GRUPOS.items()}
    for occ in (0, 1):
        def soma_cols(prefs, col):
            return sum(cel.get((nomes[p], col, occ), 0.0) for p in prefs)

        corr = ("31", "32", "33")
        cap = ("44", "45", "46")
        for col in COLS_D:
            put("DESPESAS CORRENTES", col, soma_cols(corr, col), occ)
            put("DESPESAS DE CAPITAL", col, soma_cols(cap, col), occ)
    # VIII (exceto) e IX (intra) — incluem TODA a despesa MENOS a reserva de
    # contingencia (ND 99), que o Siconfi reporta em linha propria.
    todos_nd = {k[0] for k in desp} - {"99"}
    dot_all = defaultdict(float)
    for (tipo, pref, modal), v in dot.items():
        if pref == "99":          # reserva de contingencia: linha propria
            continue
        dot_all[(tipo, modal)] += v

    def desp_total_modal(fonte, modal_filtro, campo):
        return sum(fonte.get((g, m), {}).get(campo, 0.0)
                   for g in todos_nd for m in {k[1] for k in fonte if k[0] == g}
                   if modal_filtro(m))

    def dot_total_modal(tipo, modal_filtro):
        return sum(v for (t, m), v in dot_all.items()
                   if t == tipo and modal_filtro(m))

    exceto = lambda m: m != "91"
    intra = lambda m: m == "91"
    for col in COLS_D:
        if col in (D_INI, D_ATU):
            tipo = "ini" if col == D_INI else "atu"
            viii = dot_total_modal(tipo, exceto)
            ix = dot_total_modal(tipo, intra)
        elif col in (E_BIM, L_BIM):
            campo = "e" if col == E_BIM else "l"
            viii = desp_total_modal(desp_bim, exceto, campo)
            ix = desp_total_modal(desp_bim, intra, campo)
        elif col in (E_ATE, L_ATE, P_ATE):
            campo = "p" if col == P_ATE else ("e" if col == E_ATE else "l")
            viii = desp_total_modal(desp, exceto, campo)
            ix = desp_total_modal(desp, intra, campo)
        else:  # SALDO_G / SALDO_I
            campo = "e" if col == SALDO_G else "l"
            viii = dot_total_modal("atu", exceto) - desp_total_modal(desp, exceto, campo)
            ix = dot_total_modal("atu", intra) - desp_total_modal(desp, intra, campo)
        put("DESPESAS (EXCETO INTRA-ORÇAMENTÁRIAS) (VIII)", col, viii)
        put("DESPESAS (INTRA-ORÇAMENTÁRIAS) (IX)", col, ix)
        put("SUBTOTAL DAS DESPESAS (X) = (VIII + IX)", col, viii + ix)
        put("TOTAL DAS DESPESAS (XII) = (X + XI)", col, viii + ix)
    rec_total = cel.get((R_TOTAL, ATE, 0), 0.0)
    deficit = cel.get((ROT_DEFICIT, ATE, 0), 0.0)
    put("TOTAL COM DÉFICIT (VII) = (V + VI)", ATE, rec_total + deficit)
    put("TOTAL COM SUPERÁVIT (XIV) = (XII + XIII)", ATE,
        cel.get(("TOTAL DAS DESPESAS (XII) = (X + XI)", E_ATE, 0), 0.0))

    # ---- linhas residuais: demais correntes (0) e reserva de contingencia (ND 99)
    for occ, filtro in ((0, exceto), (1, intra)):
        for col in COLS_D:
            put("Demais Despesas Correntes", col,
                cel.get(("OUTRAS DESPESAS CORRENTES", col, occ), 0.0), occ)
            if col in (D_INI, D_ATU):
                tipo = "ini" if col == D_INI else "atu"
                v = sum(val for (t, p, m), val in dot.items()
                        if t == tipo and p == "99" and filtro(m))
            elif col in (E_BIM, L_BIM):
                campo = "e" if col == E_BIM else "l"
                v = sum(desp_bim.get(("99", m), {}).get(campo, 0.0)
                        for m in {k[1] for k in desp_bim if k[0] == "99"} if filtro(m))
            elif col in (E_ATE, L_ATE, P_ATE):
                campo = "p" if col == P_ATE else ("e" if col == E_ATE else "l")
                v = sum(desp.get(("99", m), {}).get(campo, 0.0)
                        for m in {k[1] for k in desp if k[0] == "99"} if filtro(m))
            else:
                v = 0.0
            put("RESERVA DE CONTINGÊNCIA", col, v, occ)
    return cel


def ler_template(caminho: str):
    saida = []
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            saida.append((r["conta"], r["coluna"], float(r["valor"])))
    return saida


def comparar(raiz: str, ano: int, bimestre: int, template: str,
             subcategorias: dict | None = None):
    cel = celulas(raiz, ano, bimestre, subcategorias)
    ocorr = defaultdict(int)
    ok = dif = 0
    piores = []
    for conta, coluna, valor in ler_template(template):
        occ = ocorr[(conta, coluna)]
        ocorr[(conta, coluna)] += 1
        nosso = cel.get((conta, coluna, occ))
        if nosso is None:
            continue
        if abs(nosso - valor) < 0.01:
            ok += 1
        else:
            dif += 1
            piores.append((conta, coluna, occ, nosso, valor))
    return ok, dif, piores


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default=os.path.join(RAIZ, "dados", "rr_msc"))
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=5)
    ap.add_argument("--template")
    ap.add_argument("--subcategorias",
                    help="JSON com o mapa NR -> subcategoria da receita")
    a = ap.parse_args()
    sub = None
    if a.subcategorias:
        import json
        with open(a.subcategorias, encoding="utf-8") as fh:
            _d = json.load(fh)
        sub = _d.get("subcategorias", _d) if isinstance(_d, dict) else _d
    if a.template:
        ok, dif, piores = comparar(a.raiz, a.ano, a.bimestre, a.template, sub)
        print(f"exatas {ok} | divergentes {dif}")
        for c, col, o, n, v in sorted(piores, key=lambda x: -abs(x[3] - x[4]))[:12]:
            print(f"   {c[:38]:<40}{col[:22]:<24}occ{o} {n:>16,.0f}{v:>16,.0f}{n-v:>14,.0f}")
    else:
        cel = celulas(a.raiz, a.ano, a.bimestre, sub)
        print(f"{len(cel)} celulas")
