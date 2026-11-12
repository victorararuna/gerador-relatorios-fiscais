# -*- coding: utf-8 -*-
"""RGF Anexo 1 — Despesa com Pessoal — geração a partir das fontes primárias.

Fluxo:
  1. Comparativos mensais  -> despesa por natureza, 12 meses (fontes_despesa)
  2. Notas de empenho das células 162011/162233, separadas pelo complemento de
     empenho (que nomeia o poder) -> inativos e pensões dos outros poderes
  3. Subelementos de 31.91.13 -> obrigações patronais dos outros poderes
  4. RREO Anexo 3 (6º bimestre) -> RCL dos últimos 12 meses

O demonstrativo é do PODER EXECUTIVO: as naturezas 31.90.01, 31.90.03 e as
obrigações patronais vêm com todos os poderes (a autarquia e o fundo estão sob a
UG do Executivo), por isso subtraímos a parcela dos demais poderes.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fontes_despesa as F
import fontes_empenho as E
import fontes_empenho_detalhe as ED

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF808080")] * 4)
CAB = PatternFill("solid", fgColor="FFDDEBF7")
SUB = PatternFill("solid", fgColor="FFF2F2F2")
TOT = PatternFill("solid", fgColor="FFE2EFDA")
PEND = PatternFill("solid", fgColor="FFFFF2CC")

RCL_2024 = 17259989216.73

# ADCT, art. 38, § 2º (EC 127/2022) - dedução do piso da enfermagem por exercício
PISO_ENFERMAGEM = {2022: 1.00, 2023: 1.00, 2024: 0.90, 2025: 0.80, 2026: 0.70,
                   2027: 0.60, 2028: 0.50, 2029: 0.40, 2030: 0.30, 2031: 0.20,
                   2032: 0.10, 2033: 0.00}
FONTE_ENFERMAGEM = "0.6.05"
DESPESA_NAO_EXECUTADA = 454943101.05
LIMITE = 0.60

SUBS_PODER = {
    "ALRN": ["31.91.13.22", "31.91.13.43", "31.91.13.49"],
    "TCERN": ["31.91.13.23", "31.91.13.44", "31.91.13.50"],
    "TJRN": ["31.91.13.24", "31.91.13.45", "31.91.13.51"],
    "MPRN": ["31.91.13.25", "31.91.13.48", "31.91.13.53"],
    "DPRN": ["31.91.13.13", "31.91.13.43", "31.91.13.46"],
}


def _fonte_mensal(res, serie, prefixo: str) -> List[float]:
    """Valores mensais de uma fonte de recurso, como apurados nos Comparativos."""
    dados = serie.por_fonte_mensal.get(prefixo + ".000000")
    return list(dados) if dados else [0.0] * 12


def _cab(ws, linha: int, textos: List[str], altura: int = 30) -> None:
    for j, t in enumerate(textos, start=1):
        c = ws.cell(linha, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA
    ws.row_dimensions[linha].height = altura


def _linha_valores(ws, linha: int, rotulo: str, serie, total: Optional[float],
                   negrito: bool = False, origem: str = "", preenchimento=None) -> None:
    c = ws.cell(linha, 1, rotulo)
    c.font = Font(name="Arial", size=9, bold=negrito)
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    c.border = BORDA
    o = ws.cell(linha, 2, origem)
    o.font = Font(name="Arial", size=7, italic=True, color="FF666666")
    o.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    o.border = BORDA
    for i in range(12):
        v = serie.liquidada[i] if serie else None
        cel = ws.cell(linha, 3 + i, v)
        cel.number_format = FMT
        cel.font = Font(name="Arial", size=8)
        cel.border = BORDA
    cel = ws.cell(linha, 15, total)
    cel.number_format = FMT
    cel.font = Font(name="Arial", size=9, bold=True)
    cel.border = BORDA
    if preenchimento:
        for j in range(1, 16):
            ws.cell(linha, j).fill = preenchimento


def gerar(pasta: str, destino: str, rcl: float = RCL_2024) -> str:
    res = F.ler_comparativos(pasta)
    notas = E.ler_pasta(pasta)

    # linhas de detalhe das notas: trazem poder (complemento) + fonte + natureza
    detalhes = ED.ler_pasta(pasta)
    vistos = set()
    detalhes = [d for d in detalhes
                if (d.mes, d.complemento, d.natureza, round(d.liquidado, 2)) not in vistos
                and not vistos.add((d.mes, d.complemento, d.natureza, round(d.liquidado, 2)))]

    # inativos/pensoes dos OUTROS poderes (todas as fontes) - a excluir da despesa bruta
    outros: Dict[str, float] = {}
    for d in detalhes:
        if d.poder != "EXECUTIVO":
            outros[d.poder] = outros.get(d.poder, 0.0) + d.liquidado
    ded_inativos_pensoes = sum(outros.values())

    # fonte 0.8 (recursos vinculados) dos outros poderes - nao pode ser deduzida aqui
    vinculados_outros = sum(d.liquidado for d in detalhes
                            if d.poder != "EXECUTIVO" and d.fonte.startswith("0.8"))

    # patronal dos outros poderes (pelo subelemento)
    pat_outros = {}
    for poder, subs in SUBS_PODER.items():
        pat_outros[poder] = sum(res.por_natureza[s].total()
                                for s in subs if s in res.por_natureza)
    ded_patronal = sum(pat_outros.values())

    # series
    s_venc = F.SerieMensal()
    for el in ("31.90.04", "31.90.07", "31.90.11", "31.90.12", "31.90.16", "31.90.17"):
        s_venc.somar(res.elemento(el))
    s_pat = F.SerieMensal()
    s_pat.somar(res.elemento("31.90.13"))
    s_pat.somar(res.elemento("31.91.13"))
    s_apo = res.elemento("31.90.01")
    # recursos vinculados ao RPPS (fonte 0.8) — dedutíveis pelo art. 19, § 1º, VI, "a".
    # A fonte 0.8 e apurada sobre o total (todos os poderes); aplicamos a proporcao
    # da parcela do Executivo para nao deduzir duas vezes.
    ded_vinculados_total = 0.0
    for serie_inat in (s_apo, res.elemento("31.90.03")):
        for fonte, valor in getattr(serie_inat, "por_fonte", {}).items():
            if fonte.startswith("0.8"):
                ded_vinculados_total += valor
    # deducao = vinculados do Executivo = total 0.8 (todos) - 0.8 dos outros poderes
    ded_vinculados = ded_vinculados_total - vinculados_outros

    # piso da enfermagem: base = fonte 0.605 nas naturezas de pessoal (grupo 31)
    # base = total do grupo "Pessoal e Encargos Sociais" (31.00.00.00), que ja
    # consolida todas as naturezas; usar os subtotais (31.90 etc.) duplicaria
    serie_pessoal = None
    for chave in ("31.00.00.00", "31.90.00.00"):
        if chave in res.por_natureza:
            serie_pessoal = res.por_natureza[chave]
            break
    # A base e mensal. Meses com valor muito acima da mediana correspondem a
    # empenho global (o piso pago de uma vez) e nao ao piso do mes - nesses
    # casos usa-se a mediana. Ver docs/MAPEAMENTO_STN_ANEXO1.md, secao 9.
    base_enfermagem = 0.0
    if serie_pessoal:
        meses = [v for v in _fonte_mensal(res, serie_pessoal, FONTE_ENFERMAGEM) if v]
        mediana = sorted(meses)[len(meses) // 2] if meses else 0.0
        for v in _fonte_mensal(res, serie_pessoal, FONTE_ENFERMAGEM):
            if v and mediana and v > mediana * 5:
                base_enfermagem += mediana      # empenho global: usa o valor tipico
            else:
                base_enfermagem += v
    percentual_enfermagem = PISO_ENFERMAGEM.get(2024, 0.0)
    ded_enfermagem = base_enfermagem * percentual_enfermagem
    s_pen = res.elemento("31.90.03")
    s_jud = res.elemento("31.90.91")
    s_exa = res.elemento("31.90.92")

    wb = Workbook()
    ws = wb.active
    ws.title = "Anexo 1"
    ws.sheet_view.showGridLines = False

    ws["A1"] = "ESTADO DO RIO GRANDE DO NORTE"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A1"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A1:O1")
    ws["A2"] = "RELATÓRIO DE GESTÃO FISCAL — DEMONSTRATIVO DA DESPESA COM PESSOAL"
    ws["A2"].font = Font(name="Arial", size=11, bold=True)
    ws["A2"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A2:O2")
    ws["A3"] = "PODER EXECUTIVO · 3º QUADRIMESTRE DE 2024 (JANEIRO A DEZEMBRO) · MDF 14ª EDIÇÃO"
    ws["A3"].font = Font(name="Arial", size=9, bold=True)
    ws["A3"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A3:O3")
    ws["A4"] = "RGF — Anexo 1 (LRF, Art. 55, inciso I, alínea “a”) · R$ 1,00"
    ws["A4"].font = Font(name="Arial", size=8, italic=True)
    ws["A4"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A4:O4")

    _cab(ws, 6, ["DISCRIMINAÇÃO", "ORIGEM (natureza da despesa)"] +
         [f"MR{-11 + i}" if i < 11 else "MR" for i in range(12)] + ["TOTAL 12 MESES"])

    lin = 7
    ws.cell(lin, 1, "DESPESA BRUTA COM PESSOAL (I)").font = Font(name="Arial", size=9, bold=True)
    lin += 1
    _linha_valores(ws, lin, "  Pessoal Ativo", None, None, negrito=True)
    lin += 1
    _linha_valores(ws, lin, "     Vencimentos, Vantagens e Outros", s_venc, s_venc.total(),
                   origem="31.90.04/07/11/12/16/17")
    lin += 1
    _linha_valores(ws, lin, "     Obrigações Patronais", s_pat, s_pat.total() - ded_patronal,
                   origem=f"31.90.13 + 31.91.13 (-) {ded_patronal:,.2f} dos outros poderes")
    lin += 1
    _linha_valores(ws, lin, "  Pessoal Inativo e Pensionistas", None, None, negrito=True)
    lin += 1
    parte_apo = s_apo.total()
    parte_pen = s_pen.total()
    _linha_valores(ws, lin, "     Aposentadorias, Reserva e Reformas", s_apo,
                   parte_apo - (ded_inativos_pensoes * parte_apo / (parte_apo + parte_pen)),
                   origem="31.90.01 (-) inativos dos outros poderes (complemento de empenho)")
    lin += 1
    _linha_valores(ws, lin, "     Pensões", s_pen,
                   parte_pen - (ded_inativos_pensoes * parte_pen / (parte_apo + parte_pen)),
                   origem="31.90.03 (-) pensões dos outros poderes (complemento de empenho)")
    lin += 1
    _linha_valores(ws, lin, "  Outras Despesas de Pessoal de Terceirização", None, 0.0,
                   origem="31.90.34 — sem movimento")
    lin += 1
    _linha_valores(ws, lin, "  Despesa com Pessoal não Executada Orçamentariamente", None,
                   DESPESA_NAO_EXECUTADA,
                   origem="conta contábil 8.6.3.3.1.02.00.00 (saldo credor dez/2024)")

    bruta = (s_venc.total() + s_pat.total() - ded_patronal +
             (parte_apo + parte_pen) - ded_inativos_pensoes + DESPESA_NAO_EXECUTADA)
    lin += 1
    _linha_valores(ws, lin, "DESPESA BRUTA COM PESSOAL (I)", None, bruta, negrito=True,
                   preenchimento=SUB)

    lin += 2
    ws.cell(lin, 1, "DESPESAS NÃO COMPUTADAS (II)").font = Font(name="Arial", size=9, bold=True)
    lin += 1
    _linha_valores(ws, lin, "  Decorrentes de Decisão Judicial", s_jud, s_jud.total(), origem="31.90.91")
    lin += 1
    _linha_valores(ws, lin, "  Despesas de Exercícios Anteriores", s_exa, s_exa.total(), origem="31.90.92")
    lin += 1
    _linha_valores(ws, lin, "  Inativos e Pensionistas com Recursos Vinculados", None,
                   ded_vinculados,
                   origem="art. 19, § 1º, VI, 'a', da LRF — fontes 0.8 (RPPS)")
    lin += 1
    _linha_valores(ws, lin, "  Parcela dedutível do piso do Enfermeiro e afins", None,
                   ded_enfermagem,
                   origem=f"ADCT art. 38, § 2º — {percentual_enfermagem:.0%} da fonte 0.605 "
                          f"({base_enfermagem:,.2f})")
    deducao = s_jud.total() + s_exa.total() + ded_vinculados + ded_enfermagem
    lin += 1
    _linha_valores(ws, lin, "DESPESAS NÃO COMPUTADAS (II)", None, deducao, negrito=True, preenchimento=SUB)

    lin += 2
    _linha_valores(ws, lin, "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)", None,
                   bruta - deducao, negrito=True, preenchimento=TOT)

    # ---------------- quadro 2 ----------------
    lin += 2
    ws.cell(lin, 1, "APURAÇÃO DO CUMPRIMENTO DO LIMITE").font = Font(name="Arial", size=10, bold=True)
    lin += 1
    itens = [
        ("Receita Corrente Líquida (RCL) — últimos 12 meses", rcl, "RREO Anexo 3, 6º bimestre/2024"),
        ("% da despesa líquida sobre a RCL", bruta - deducao, ""),
        ("Limite legal (60% da RCL)", rcl * LIMITE, "art. 20, III, 'c', da LRF"),
        ("Excedente / (folga)", (bruta - deducao) - rcl * LIMITE, ""),
    ]
    for nome, valor, obs in itens:
        ws.cell(lin, 1, nome).font = Font(name="Arial", size=9)
        if nome.startswith("%"):
            c = ws.cell(lin, 15, (bruta - deducao) / rcl)
            c.number_format = "0.00%"
        else:
            c = ws.cell(lin, 15, valor)
            c.number_format = FMT
        c.font = Font(name="Arial", size=9, bold=True)
        c.border = BORDA
        ws.cell(lin, 2, obs).font = Font(name="Arial", size=7, italic=True)
        lin += 1

    lin += 1
    pct = (bruta - deducao) / rcl
    aviso = ("ACIMA DO LIMITE DE 60%" if pct > LIMITE else "DENTRO DO LIMITE")
    c = ws.cell(lin, 1, f"Situação: {aviso}")
    c.font = Font(name="Arial", size=10, bold=True, color="FFC00000" if pct > LIMITE else "FF375623")

    # ---------------- memoria de calculo ----------------
    ws2 = wb.create_sheet("Memória de cálculo")
    ws2.sheet_view.showGridLines = False
    ws2["A1"] = "MEMÓRIA DE CÁLCULO — deduções de escopo (outros poderes)"
    ws2["A1"].font = Font(name="Arial", size=12, bold=True)
    lin = 3
    _cab(ws2, lin, ["Item", "Valor"])
    lin += 1
    for poder, valor in sorted(outros.items(), key=lambda x: -x[1]):
        ws2.cell(lin, 1, f"Inativos/pensões — {poder}").font = Font(name="Arial", size=9)
        c = ws2.cell(lin, 2, valor); c.number_format = FMT; c.font = Font(name="Arial", size=9)
        lin += 1
    ws2.cell(lin, 1, "Subtotal inativos/pensões").font = Font(name="Arial", size=9, bold=True)
    c = ws2.cell(lin, 2, ded_inativos_pensoes); c.number_format = FMT
    c.font = Font(name="Arial", size=9, bold=True)
    lin += 2
    for poder, valor in sorted(pat_outros.items(), key=lambda x: -x[1]):
        ws2.cell(lin, 1, f"Patronal — {poder}").font = Font(name="Arial", size=9)
        c = ws2.cell(lin, 2, valor); c.number_format = FMT; c.font = Font(name="Arial", size=9)
        lin += 1
    ws2.cell(lin, 1, "Subtotal patronal").font = Font(name="Arial", size=9, bold=True)
    c = ws2.cell(lin, 2, ded_patronal); c.number_format = FMT
    c.font = Font(name="Arial", size=9, bold=True)
    lin += 2
    ws2.cell(lin, 1, f"Notas de empenho lidas: {len(notas)} · complementos únicos: {len(E.consolidar(notas))}").font = Font(name="Arial", size=8, italic=True)
    ws2.column_dimensions["A"].width = 56
    ws2.column_dimensions["B"].width = 22

    # ---------------- natureza detalhada ----------------
    ws3 = wb.create_sheet("Séries por natureza")
    ws3.sheet_view.showGridLines = False
    _cab(ws3, 1, ["Natureza"] + [F.MESES[i][:3].title() for i in range(12)] + ["Total"])
    lin = 2
    for nat in sorted(res.por_natureza):
        s = res.por_natureza[nat]
        ws3.cell(lin, 1, nat).font = Font(name="Arial", size=8)
        for i in range(12):
            c = ws3.cell(lin, 2 + i, s.liquidada[i])
            c.number_format = FMT; c.font = Font(name="Arial", size=8)
        c = ws3.cell(lin, 14, s.total()); c.number_format = FMT
        c.font = Font(name="Arial", size=8, bold=True)
        lin += 1
    ws3.column_dimensions["A"].width = 15
    for j in range(2, 15):
        ws3.column_dimensions[get_column_letter(j)].width = 14

    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 34
    for j in range(3, 15):
        ws.column_dimensions[get_column_letter(j)].width = 14
    ws.column_dimensions["O"].width = 19
    ws.freeze_panes = "C7"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino


if __name__ == "__main__":
    entrada = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\victo\AppData\Local\Temp"
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saida", "RGF_2024_Q3_Anexo1.xlsx")
    print(gerar(entrada, saida))
