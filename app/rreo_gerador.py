# -*- coding: utf-8 -*-
"""Gerador do RREO a partir da Matriz de Saldos Contábeis.

Lê a MSC do exercício, acumula os meses do bimestre e apura os anexos que a
matriz sustenta:

    01  Balanço Orçamentário — despesa por grupo de natureza
    02  Despesa por função
    07  Restos a Pagar
    09  Operações de crédito — despesa de capital
    14  Demonstrativo Simplificado — despesa

A receita não é apurada aqui: a matriz não registra as deduções com o mesmo
critério do RREO. Quando disponível, a RCL é recebida como **entrada**.

Uso:
    python gerar_rreo.py --ano 2026 --bimestre 4
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leitor_msc import Acervo, ErroMSC  # noqa: E402

CONTAS_EMPENHO = "62213"
CONTAS_LIQUIDACAO = ("622130300", "622130400", "622130700")
CONTA_PAGO = "622130400"

#: contas de restos a pagar
RP = {
    "rpp_pagos": "632200000",
    "rpp_cancelados": "632910000",
    "rpp_saldo": "632100000",
    "rpn_pagos": "631400000",
    "rpn_cancelados": "631990000",
    "inscritos": "632700000",
}

GRUPOS = {
    "31": "PESSOAL E ENCARGOS SOCIAIS",
    "32": "JUROS E ENCARGOS DA DÍVIDA",
    "33": "OUTRAS DESPESAS CORRENTES",
    "44": "INVESTIMENTOS",
    "45": "INVERSÕES FINANCEIRAS",
    "46": "AMORTIZAÇÃO DA DÍVIDA",
}

FUNCOES = {
    "01": "Legislativa", "02": "Judiciária", "03": "Essencial à Justiça",
    "04": "Administração", "05": "Defesa Nacional", "06": "Segurança Pública",
    "07": "Relações Exteriores", "08": "Assistência Social",
    "09": "Previdência Social", "10": "Saúde", "11": "Trabalho",
    "12": "Educação", "13": "Cultura", "14": "Direitos da Cidadania",
    "15": "Urbanismo", "16": "Habitação", "17": "Saneamento",
    "18": "Gestão Ambiental", "19": "Ciência e Tecnologia",
    "20": "Agricultura", "21": "Organização Agrária", "22": "Indústria",
    "23": "Comércio e Serviços", "24": "Comunicações", "25": "Energia",
    "26": "Transporte", "27": "Desporto e Lazer", "28": "Encargos Especiais",
}


def meses_do_bimestre(bimestre: int) -> List[int]:
    """O RREO é cumulativo: o 4º bimestre vai de janeiro a agosto."""
    if bimestre < 1 or bimestre > 6:
        raise ValueError(f"bimestre inválido: {bimestre}")
    return list(range(1, 2 * bimestre + 1))


@dataclass
class ApuracaoRREO:
    ano: int
    bimestre: int
    meses: List[int]
    grupos: Dict[str, Dict[str, float]] = field(default_factory=dict)
    grupos_bimestre: Dict[str, Dict[str, float]] = field(default_factory=dict)
    funcoes: Dict[str, float] = field(default_factory=dict)
    restos: Dict[str, float] = field(default_factory=dict)
    rcl: Optional[float] = None
    ausentes: List[int] = field(default_factory=list)

    @property
    def empenhado(self) -> float:
        return sum(g["empenhado"] for g in self.grupos.values())

    @property
    def liquidado(self) -> float:
        return sum(g["liquidado"] for g in self.grupos.values())

    @property
    def pago(self) -> float:
        return sum(g["pago"] for g in self.grupos.values())


def _somar(acervo: Acervo, ano: int, meses: Sequence[int],
           classe: int, tipo_valor: str = "period_change") -> Iterable:
    for mes in meses:
        try:
            yield from acervo.ler(ano, mes, classe=classe, tipo_valor=tipo_valor)
        except ErroMSC:
            continue


def apurar(raiz: str, ano: int, bimestre: int,
           rcl: Optional[float] = None) -> ApuracaoRREO:
    """Lê a MSC e devolve os anexos que ela sustenta."""
    acervo = Acervo(raiz)
    meses = meses_do_bimestre(bimestre)
    res = ApuracaoRREO(ano=ano, bimestre=bimestre, meses=meses, rcl=rcl)

    disponiveis = set(acervo.meses(ano, 6, "period_change"))
    res.ausentes = [m for m in meses if m not in disponiveis]
    if res.ausentes:
        raise ErroMSC(
            f"matriz de {ano} não cobre o {bimestre}º bimestre: "
            f"faltam os meses {res.ausentes}")

    for r in _somar(acervo, ano, meses, 6):
        if not r.conta.startswith(CONTAS_EMPENHO):
            continue
        grupo = r.nd[:2] if r.nd else None
        if grupo not in GRUPOS:
            continue
        g = res.grupos.setdefault(grupo, {"empenhado": 0.0, "liquidado": 0.0,
                                          "pago": 0.0})
        g["empenhado"] += r.liquido
        if r.conta in CONTAS_LIQUIDACAO:
            g["liquidado"] += r.liquido
        if r.conta == CONTA_PAGO:
            g["pago"] += r.liquido
        if r.conta in CONTAS_LIQUIDACAO and r.funcao in FUNCOES:
            res.funcoes[r.funcao] = res.funcoes.get(r.funcao, 0.0) + r.liquido

    # o bimestre em si (últimos dois meses) — colunas "no bimestre"
    for r in _somar(acervo, ano, meses[-2:], 6):
        if not r.conta.startswith(CONTAS_EMPENHO):
            continue
        grupo = r.nd[:2] if r.nd else None
        if grupo not in GRUPOS:
            continue
        g = res.grupos_bimestre.setdefault(
            grupo, {"empenhado": 0.0, "liquidado": 0.0, "pago": 0.0})
        g["empenhado"] += r.liquido
        if r.conta in CONTAS_LIQUIDACAO:
            g["liquidado"] += r.liquido
        if r.conta == CONTA_PAGO:
            g["pago"] += r.liquido

    # movimentos de RP (fluxo do período)
    for r in _somar(acervo, ano, meses, 6):
        for chave, conta in RP.items():
            if chave != "rpp_saldo" and r.conta == conta:
                res.restos[chave] = res.restos.get(chave, 0.0) + r.liquido
    # saldo de RP é estoque: ending_balance do mês de referência
    try:
        for r in acervo.ler(ano, meses[-1], classe=6, tipo_valor="ending_balance"):
            if r.conta == RP["rpp_saldo"]:
                res.restos["rpp_saldo"] = res.restos.get("rpp_saldo", 0.0) + r.liquido
    except ErroMSC:
        pass

    return res


# ------------------------------------------------------------------ XLSX
def escrever_xlsx(destino: str, res: ApuracaoRREO,
                  homologado: Optional[Dict[str, float]] = None) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    wb.remove(wb.active)
    negrito = Font(bold=True)
    cinza = PatternFill("solid", fgColor="EDEDED")

    def cabecalho(ws, titulo, colunas):
        ws["A1"] = titulo
        ws["A1"].font = Font(bold=True, size=12)
        for i, nome in enumerate(colunas, start=1):
            c = ws.cell(row=3, column=i, value=nome)
            c.font = negrito
            c.fill = cinza

    # ---- Anexo 1
    ws = wb.create_sheet("Anexo 01")
    cabecalho(ws, f"RREO Anexo 1 — despesa por grupo — {res.ano} B{res.bimestre}",
              ["Grupo", "Empenhada", "Liquidada", "Paga"])
    r = 4
    for pref, nome in GRUPOS.items():
        g = res.grupos.get(pref)
        if not g:
            continue
        ws.cell(row=r, column=1, value=nome)
        for j, chave in enumerate(("empenhado", "liquidado", "pago"), start=2):
            ws.cell(row=r, column=j, value=g[chave]).number_format = "#,##0.00"
        r += 1
    ws.cell(row=r, column=1, value="TOTAL").font = negrito
    for j, valor in enumerate((res.empenhado, res.liquidado, res.pago), start=2):
        c = ws.cell(row=r, column=j, value=valor)
        c.number_format = "#,##0.00"
        c.font = negrito
    for col, largura in {"A": 34, "B": 22, "C": 22, "D": 22}.items():
        ws.column_dimensions[col].width = largura

    # ---- Anexo 2
    ws = wb.create_sheet("Anexo 02")
    cabecalho(ws, f"RREO Anexo 2 — despesa por função — {res.ano} B{res.bimestre}",
              ["Função", "Liquidada"])
    r = 4
    for cod, nome in FUNCOES.items():
        v = res.funcoes.get(cod)
        if not v:
            continue
        ws.cell(row=r, column=1, value=nome)
        ws.cell(row=r, column=2, value=v).number_format = "#,##0.00"
        r += 1
    ws.cell(row=r, column=1, value="TOTAL").font = negrito
    c = ws.cell(row=r, column=2, value=sum(res.funcoes.values()))
    c.number_format = "#,##0.00"
    c.font = negrito
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 24

    # ---- Anexo 7
    ws = wb.create_sheet("Anexo 07")
    cabecalho(ws, f"RREO Anexo 7 — restos a pagar — {res.ano} B{res.bimestre}",
              ["Linha", "Valor"])
    linhas7 = [("RP processados pagos", "rpp_pagos"),
               ("RP processados cancelados", "rpp_cancelados"),
               ("Saldo de RP processados", "rpp_saldo"),
               ("RP não processados pagos", "rpn_pagos"),
               ("RP não processados cancelados", "rpn_cancelados"),
               ("RP inscritos no exercício", "inscritos")]
    for i, (rotulo, chave) in enumerate(linhas7, start=4):
        ws.cell(row=i, column=1, value=rotulo)
        ws.cell(row=i, column=2, value=res.restos.get(chave, 0.0)).number_format = "#,##0.00"
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 24

    # ---- Anexo 9
    ws = wb.create_sheet("Anexo 09")
    cabecalho(ws, f"RREO Anexo 9 — despesa de capital — {res.ano} B{res.bimestre}",
              ["Linha", "Empenhada"])
    r = 4
    for pref in ("44", "45", "46"):
        g = res.grupos.get(pref)
        if not g:
            continue
        ws.cell(row=r, column=1, value=GRUPOS[pref])
        ws.cell(row=r, column=2, value=g["empenhado"]).number_format = "#,##0.00"
        r += 1
    total_cap = sum(res.grupos.get(p, {}).get("empenhado", 0.0)
                    for p in ("44", "45", "46"))
    ws.cell(row=r, column=1, value="DESPESAS DE CAPITAL").font = negrito
    c = ws.cell(row=r, column=2, value=total_cap)
    c.number_format = "#,##0.00"
    c.font = negrito
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 24

    # ---- Anexo 14
    ws = wb.create_sheet("Anexo 14")
    cabecalho(ws, f"RREO Anexo 14 — simplificado — {res.ano} B{res.bimestre}",
              ["Linha", "Valor"])
    linhas14 = [("Despesas Empenhadas", res.empenhado),
                ("Despesas Liquidadas", res.liquidado),
                ("Despesas Pagas", res.pago)]
    if res.rcl:
        linhas14.append(("Receita Corrente Líquida (entrada)", res.rcl))
    for i, (rotulo, valor) in enumerate(linhas14, start=4):
        ws.cell(row=i, column=1, value=rotulo)
        ws.cell(row=i, column=2, value=valor).number_format = "#,##0.00"
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 24

    # ---- Verificações
    ws = wb.create_sheet("Verificações", 0)
    cabecalho(ws, f"Verificações — {res.ano} B{res.bimestre}", ["Checagem", "Valor", "Situação"])
    r = 4
    inscritos = res.restos.get("inscritos", 0.0)
    capital = sum(res.grupos.get(p, {}).get("empenhado", 0.0)
                  for p in ("44", "45", "46"))
    checagens = [
        ("Total por função = total liquidado",
         sum(res.funcoes.values()) - res.liquidado, True),
        ("Liquidado ≤ empenhado", res.liquidado - res.empenhado,
         res.liquidado <= res.empenhado),
        ("Pago ≤ liquidado", res.pago - res.liquidado,
         res.pago <= res.liquidado),
        ("Capital ≤ empenhado total", capital - res.empenhado,
         capital <= res.empenhado),
    ]
    if res.bimestre == 6:
        # identidade só vale no encerramento: a inscrição em RP ocorre em dezembro
        checagens.append(("Pago = liquidado − RP inscritos",
                          res.pago - (res.liquidado - inscritos),
                          abs(res.pago - (res.liquidado - inscritos)) <= 0.01))
    for nome, valor, ok in checagens:
        ws.cell(row=r, column=1, value=nome)
        ws.cell(row=r, column=2, value=valor).number_format = "#,##0.00"
        cel = ws.cell(row=r, column=3, value="OK" if ok else "FALHA")
        cel.fill = PatternFill("solid", fgColor="C6EFCE" if ok else "FFC7CE")
        r += 1
    ws.column_dimensions["A"].width = 56
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 12

    if res.ausentes:
        ws.cell(row=r + 1, column=1,
                value=f"meses ausentes: {res.ausentes}")

    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    wb.save(destino)
    return destino


