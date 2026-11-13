# -*- coding: utf-8 -*-
"""Montagem do Anexo 1 em planilha, com aba de verificações."""
from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anexo1_msc import Apuracao, deducoes, nao_executada, percentual_enfermagem

ROTULO_I = "DESPESA BRUTA COM PESSOAL (I)"
ROTULO_II = "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)"
ROTULO_III = "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)"

ROTULOS_OFICIAIS = {
    "ativo": "Pessoal Ativo",
    "vencimentos": "Vencimentos, Vantagens e Outras Despesas Variáveis",
    "patronal": "Obrigações Patronais",
    "inativo": "Pessoal Inativo e Pensionistas",
    "aposentadorias": "Aposentadorias, Reserva e Reformas",
    "pensoes": "Pensões",
    "terceirizacao": ("Outras Despesas de Pessoal decorrentes de Contratos de "
                      "Terceirização ou de contratação de forma indireta "
                      "(§ 1º do art. 18 da LRF)"),
    "nao_executada": "Despesa com Pessoal não Executada Orçamentariamente",
    "indenizacoes": "Indenizações por Demissão e Incentivos à Demissão Voluntária",
    "judiciais": "Decorrentes de Decisão Judicial de Período Anterior ao da Apuração",
    "exerc_ant": ("Despesas de Exercícios Anteriores de Período Anterior ao "
                  "da Apuração"),
    "vinculados": "Inativos e Pensionistas com Recursos Vinculados",
    "enfermagem": ("Parcela dedutível referente ao piso salarial do Enfermeiro, "
                   "Técnico de Enfermagem, Auxiliar de Enfermagem e Parteira "
                   "(ADCT, art. 38, §2º)"),
    "I": ROTULO_I,
    "II": ROTULO_II,
    "III": ROTULO_III,
}


@dataclass
class Linha:
    nivel: int
    descricao: str
    chave: str
    valor: float
    total: bool = False


def linhas_anexo1(res: Apuracao, ded: Dict[str, float], ne: float) -> List[Linha]:
    """As 16 linhas do Anexo 1, na ordem oficial."""
    venc = res.get("vencimentos") + res.get("judiciais")
    ativo = venc + res.get("patronal")
    inativo = res.get("aposentadorias") + res.get("pensoes")
    bruto = (ativo + inativo + res.get("terceirizacao") + ne)

    ii = (res.get("indenizacoes") + res.get("judiciais") + res.get("exerc_ant")
          + ded["vinculados"] + ded["enfermagem"])

    return [
        Linha(0, ROTULO_I, "I", bruto, True),
        Linha(1, ROTULOS_OFICIAIS["ativo"], "ativo", ativo),
        Linha(2, ROTULOS_OFICIAIS["vencimentos"], "vencimentos", venc),
        Linha(2, ROTULOS_OFICIAIS["patronal"], "patronal", res.get("patronal")),
        Linha(1, ROTULOS_OFICIAIS["inativo"], "inativo", inativo),
        Linha(2, ROTULOS_OFICIAIS["aposentadorias"], "aposentadorias",
              res.get("aposentadorias")),
        Linha(2, ROTULOS_OFICIAIS["pensoes"], "pensoes", res.get("pensoes")),
        Linha(1, ROTULOS_OFICIAIS["terceirizacao"], "terceirizacao",
              res.get("terceirizacao")),
        Linha(1, ROTULOS_OFICIAIS["nao_executada"], "nao_executada", ne),
        Linha(0, ROTULO_II, "II", ii, True),
        Linha(2, ROTULOS_OFICIAIS["indenizacoes"], "indenizacoes",
              res.get("indenizacoes")),
        Linha(2, ROTULOS_OFICIAIS["judiciais"], "judiciais", res.get("judiciais")),
        Linha(2, ROTULOS_OFICIAIS["exerc_ant"], "exerc_ant", res.get("exerc_ant")),
        Linha(2, ROTULOS_OFICIAIS["vinculados"], "vinculados", ded["vinculados"]),
        Linha(2, ROTULOS_OFICIAIS["enfermagem"], "enfermagem", ded["enfermagem"]),
        Linha(0, ROTULO_III, "III", bruto - ii, True),
    ]


def ler_oficiais(caminho: str) -> Dict[str, float]:
    """Todas as linhas com TOTAL (ÚLTIMOS 12 MESES) do Anexo 1 homologado."""
    saida: Dict[str, float] = {}
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"].startswith("TOTAL"):
                saida.setdefault(r["conta"], float(r["valor"]))
    return saida


def escrever_xlsx(caminho: str, linhas: List[Linha], *,
                  titulo: str, oficial: Optional[Dict[str, float]] = None,
                  fonte: str = "", observacoes: Optional[List[str]] = None) -> str:
    """Grava o Anexo 1 com aba de verificações."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "RGF-Anexo 01"

    negrito = Font(bold=True)
    cinza = PatternFill("solid", fgColor="EDEDED")
    fino = Side(style="thin", color="BFBFBF")
    borda = Border(left=fino, right=fino, top=fino, bottom=fino)

    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = f"Fonte: {fonte}" if fonte else ""
    ws["A2"].font = Font(italic=True, size=8, color="666666")

    cabecalho = ["Descrição", "Valor apurado"]
    if oficial is not None:
        cabecalho += ["Homologado", "Diferença", "%"]
    for c, texto in enumerate(cabecalho, start=1):
        cel = ws.cell(row=4, column=c, value=texto)
        cel.font = negrito
        cel.fill = cinza
        cel.border = borda
        cel.alignment = Alignment(horizontal="center", wrap_text=True)

    for i, ln in enumerate(linhas, start=5):
        nome = ("    " * ln.nivel) + ln.descricao
        ws.cell(row=i, column=1, value=nome).border = borda
        cel = ws.cell(row=i, column=2, value=ln.valor)
        cel.number_format = "#,##0.00"
        cel.border = borda
        if ln.total:
            for c in range(1, 3):
                ws.cell(row=i, column=c).font = negrito
                ws.cell(row=i, column=c).fill = cinza
        if oficial is not None:
            of = oficial.get(ln.descricao)
            if of is not None:
                ws.cell(row=i, column=3, value=of).number_format = "#,##0.00"
                dif = ws.cell(row=i, column=4, value=ln.valor - of)
                dif.number_format = "#,##0.00"
                pct = ws.cell(row=i, column=5, value=(ln.valor / of - 1))
                pct.number_format = "0.00%"
                for c in range(3, 6):
                    ws.cell(row=i, column=c).border = borda

    larguras = {"A": 72, "B": 20, "C": 20, "D": 18, "E": 10}
    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura
    ws.freeze_panes = "A5"

    # ---------------- verificações ----------------
    vv = wb.create_sheet("Verificações")
    vv["A1"] = "Conferência linha a linha contra o homologado"
    vv["A1"].font = Font(bold=True, size=12)

    if oficial is None:
        vv["A3"] = "Sem arquivo homologado: relatório gerado apenas com os valores apurados."
    else:
        cab = ["Descrição", "Apurado", "Homologado", "Diferença", "%", "Situação"]
        for c, texto in enumerate(cab, start=1):
            cel = vv.cell(row=3, column=c, value=texto)
            cel.font = negrito
            cel.fill = cinza
            cel.border = borda
            r = 4
            for ln in linhas:
                of = oficial.get(ln.descricao)
                if of is None:
                    continue
                pct = ln.valor / of - 1 if of else 0.0
                vv.cell(row=r, column=1, value=ln.descricao).border = borda
                vv.cell(row=r, column=2, value=ln.valor).number_format = "#,##0.00"
                vv.cell(row=r, column=3, value=of).number_format = "#,##0.00"
                vv.cell(row=r, column=4, value=ln.valor - of).number_format = "#,##0.00"
                vv.cell(row=r, column=5, value=pct).number_format = "0.00%"
                if abs(pct) <= 0.005:
                    situacao, cor = "OK (≤ 0,5%)", "C6EFCE"
                elif abs(pct) <= 0.02:
                    situacao, cor = "Atenção (≤ 2%)", "FFEB9C"
                else:
                    situacao, cor = "Divergente (> 2%)", "FFC7CE"
                cel = vv.cell(row=r, column=6, value=situacao)
                cel.fill = PatternFill("solid", fgColor=cor)
                for c in range(1, 7):
                    vv.cell(row=r, column=c).border = borda
                r += 1

        r += 1
        vv.cell(row=r, column=1, value="Observações").font = negrito
        r += 1
        for obs in (observacoes or []):
            vv.cell(row=r, column=1, value="• " + obs)
            r += 1

    for col, largura in {"A": 72, "B": 20, "C": 20, "D": 18, "E": 10,
                         "F": 20}.items():
        vv.column_dimensions[col].width = largura

    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    wb.save(caminho)
    return caminho
