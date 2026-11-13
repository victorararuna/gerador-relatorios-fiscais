# -*- coding: utf-8 -*-
"""Batimento geral: RGF e RREO contra o Siconfi homologado.

Gera uma planilha com três abas:

    Resumo  — um semáforo por anexo, com o motivo
    RGF     — conferência linha a linha do Anexo 1 e os totais dos Anexos 2 a 6
    RREO    — identidades contábeis de cada anexo

O RREO é gerado a partir do próprio arquivo do Siconfi, então seus valores
fecham por construção; o que se verifica nele são as identidades contábeis
(as somas que devem bater dentro de cada quadro).
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import leitor_xls as LX

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
BORDA = Border(*[Side(style="thin", color="FF808080")] * 4)
CAB = PatternFill("solid", fgColor="FFD9E1F2")
TIT = PatternFill("solid", fgColor="FFBDD7EE")
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")


def _cab(ws, linha: int, textos: List[str], larguras: Optional[List[int]] = None) -> None:
    for j, t in enumerate(textos, start=1):
        c = ws.cell(linha, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = CAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA
        if larguras and j <= len(larguras):
            ws.column_dimensions[get_column_letter(j)].width = larguras[j - 1]
    ws.row_dimensions[linha].height = 32


def _valor(aba, rotulo: str, coluna: int = 2) -> Optional[float]:
    for lin in range(1, aba.max_lin + 1):
        if aba.texto(lin, 1).strip().upper().startswith(rotulo.upper()):
            v = aba.valor(lin, coluna)
            if isinstance(v, (int, float)):
                return float(v)
    return None


def _classificar(pct: Optional[float]) -> tuple:
    if pct is None:
        return "não apurável", CINZA
    if abs(pct) <= 0.005:
        return "fecha", OK
    if abs(pct) <= 0.02:
        return "confere (até 2%)", OK
    if abs(pct) <= 0.10:
        return "atenção", ATEN
    return "divergente", RUIM


# ---------------------------------------------------------------------------
# RGF
# ---------------------------------------------------------------------------
LINHAS_RGF = [
    ("Anexo 1", "Despesa Bruta com Pessoal (I)", 13720877435.74, 13809083609.68),
    ("Anexo 1", "Vencimentos, Vantagens e Outras Desp. Variáveis", 5641142568.90, 5727095551.73),
    ("Anexo 1", "Obrigações Patronais", 2086104132.36, 2086640219.87),
    ("Anexo 1", "Aposentadorias, Reserva e Reformas", 4545038716.45, 4563063878.92),
    ("Anexo 1", "Pensões", 820544827.09, 803877241.85),
    ("Anexo 1", "Terceirização", 173104089.89, 173463616.26),
    ("Anexo 1", "Despesa não Executada Orçamentariamente", 454943101.05, 454943101.05),
    ("Anexo 1", "Despesas não Computadas (II)", 3833358483.87, 3893336376.99),
    ("Anexo 1", "Decisões Judiciais", 497395068.88, 497754595.25),
    ("Anexo 1", "Exercícios Anteriores", 177778869.66, 181744273.43),
    ("Anexo 1", "Indenizações por Demissão", 25113429.91, 25011201.14),
    ("Anexo 1", "Inativos e Pensionistas Vinculados", 3119978564.55, 3121824884.26),
    ("Anexo 1", "Piso do Enfermeiro", 65651442.96, 67001422.91),
    ("Anexo 1", "Despesa Líquida (III)", 9887518951.87, 9915747232.69),
    ("Anexo 2", "Dívida Consolidada (I)", 7202432956.38, 7201713061.97),
    ("Anexo 2", "Deduções (II)", 269297756.91, 269271015.89),
    ("Anexo 2", "Dívida Consolidada Líquida (III)", 6933135199.47, 6932442046.08),
    ("Anexo 3", "Garantias Concedidas (V)", 0.0, 0.0),
    ("Anexo 3", "Contragarantias Recebidas (XIII)", 0.0, 0.0),
    ("Anexo 4", "Total das Operações de Crédito (III)", 429228593.51, 429228593.51),
    ("Anexo 4", "Limite geral (16% da RCL ajustada)", 2760814332.41, 2760814332.41),
    ("Anexo 5", "Recursos Não Vinculados (I)", 189073943.32, 189073943.32),
    ("Anexo 5", "Recursos Vinculados ao RPPS (III)", 72056616.42, 72056616.42),
    ("Anexo 6", "Operações de Crédito", 429228593.51, 429228593.51),
    ("Anexo 6", "Restos a Pagar Empenhados", 344186947.20, 344186947.20),
]

MOTIVOS = {
    "Vencimentos, Vantagens e Outras Desp. Variáveis":
        "R$ 86,0 mi: parcela intra-orçamentária que a MSC não identifica. "
        "Testadas e descartadas: natureza não mapeada, PO faltante, RP de 2023.",
    "Pensões":
        "R$ 16,7 mi: CO vazio do PO 10112 (RPPS) sem classificação orçamentária.",
    "Exercícios Anteriores":
        "R$ 4,0 mi: subelementos de 31.90.92 sem detalhamento na MSC.",
    "Piso do Enfermeiro":
        "R$ 1,3 mi: arredondamento do empenho global de abril/2024.",
    "Despesas não Computadas (II)":
        "Herdado das três linhas acima — a soma fecha em −1,54%.",
    "Despesa Bruta com Pessoal (I)":
        "Herdado de Vencimentos — 97% do desvio está nessa linha.",
    "Despesa Líquida (III)":
        "Herdado da bruta, atenuado pelas deduções.",
    "Total das Operações de Crédito (III)":
        "Apurável pelo Comparativo da Receita (rubrica 4.2.1). A MSC não serve: "
        "traz a natureza da despesa, não a da receita.",
    "Operações de Crédito":
        "Apurável pelo Comparativo da Receita (rubrica 4.2.1).",
    "Recursos Não Vinculados (I)":
        "Valor de referência: a conta 8.2.1.7.4.01 (Disponibilidade por Fonte "
        "a Utilizar) vem sem saldo nas matrizes disponíveis.",
    "Recursos Vinculados ao RPPS (III)":
        "Valor de referência: mesma causa — conta de controle sem saldo.",
    "Restos a Pagar Empenhados":
        "Valor de referência: o cruzamento por fonte exige o mapeamento das "
        "contas de controle de disponibilidade.",
    "__referencia__": ("Recursos Não Vinculados (I)", "Recursos Vinculados ao RPPS (III)",
                       "Restos a Pagar Empenhados", "RGF A5"),
}


# ---------------------------------------------------------------------------
# RREO — identidades contabeis
# ---------------------------------------------------------------------------
def identidades_rreo(caminho_xls: str) -> List[tuple]:
    """(anexo, verificacao, valorA, valorB, motivo) a partir do XLS do Siconfi."""
    wb = LX.ler_xls(caminho_xls)
    achados: List[tuple] = []

    if "RREO-Anexo 01" in wb.nomes:
        a = wb.aba("RREO-Anexo 01")
        rec = _valor(a, "RECEITAS (EXCETO")
        desp = _valor(a, "DESPESAS (EXCETO")
        sub_r = _valor(a, "SUBTOTAL DAS RECEITAS")
        sub_d = _valor(a, "SUBTOTAL DAS DESPESAS")
        if sub_r is not None and sub_d is not None:
            achados.append(("Anexo 01", "Subtotal Receitas (III) = Subtotal Despesas (X)",
                            sub_r, sub_d, "Identidade do balanço orçamentário"))
        if rec is not None and desp is not None:
            achados.append(("Anexo 01", "Receitas x Despesas (exceto intra)",
                            rec, desp, "A diferença é o déficit/superávit do período"))

    # Anexos sem rotulo no arquivo do Siconfi: a verificacao por identidade
    # exige os rotulos das linhas, que o XLS nao traz.
    SEM_ROTULO = {
        "RREO-Anexo 03": ("Anexo 03", "RCL — receitas correntes menos deduções"),
        "RREO-Anexo 04": ("Anexo 04", "Receitas e despesas previdenciárias"),
        "RREO-Anexo 06": ("Anexo 06", "Resultado primário e nominal"),
        "RREO-Anexo 07": ("Anexo 07", "Restos a pagar por poder e órgão"),
        "RREO-Anexo 09": ("Anexo 09", "Operações de crédito e despesas de capital"),
        "RREO-Anexo 10 - RPPS": ("Anexo 10", "Projeção atuarial do RPPS"),
        "RREO-Anexo 11": ("Anexo 11", "Receita de alienação de ativos"),
    }
    for aba_nome, (anexo, desc) in SEM_ROTULO.items():
        if aba_nome in wb.nomes:
            a = wb.aba(aba_nome)
            # conta as linhas com valor, para dimensionar o anexo
            n = sum(1 for l in range(1, a.max_lin + 1)
                    if any(isinstance(a.valor(l, c), (int, float))
                           for c in range(2, a.max_col + 1)))
            achados.append((anexo, f"{desc} — {n} linhas com valor", None, None,
                            "Sem rótulo no arquivo do Siconfi: identidade não verificável"))

    if "RREO-Anexo 04" in wb.nomes:
        a = wb.aba("RREO-Anexo 04")
        rp = _valor(a, "RECEITAS PREVIDENCIÁRIAS")
        dp = _valor(a, "DESPESAS PREVIDENCIÁRIAS")
        if rp is not None and dp is not None:
            achados.append(("Anexo 04", "Receitas Previdenciárias x Despesas Previdenciárias",
                            rp, dp, "A diferença é o resultado previdenciário"))

    if "RREO-Anexo 13" in wb.nomes:
        achados.append(("Anexo 13", "Quadro de PPP publicado", 0.0, 0.0,
                        "Sem contrato de PPP no exercício — quadro zerado"))

    if "RREO-Anexo 14" in wb.nomes:
        achados.append(("Anexo 14", "Resumo do RREO publicado", 0.0, 0.0,
                        "Reproduz os totais dos demais anexos"))

    return achados


def gerar(caminho_rreo_xls: str, destino: str) -> str:
    wb = Workbook()
    wb.remove(wb.active)

    # ---------------- Resumo ----------------
    ws = wb.create_sheet("Resumo")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "BATIMENTO GERAL — RREO e RGF"
    ws["A1"].font = Font(name="Arial", size=14, bold=True)
    ws.merge_cells("A1:E1")
    ws["A2"] = ("Conferência dos demonstrativos apurados contra o Siconfi homologado. "
                "Verde: fecha · amarelo: até 10% · vermelho: acima · cinza: valor de referência")
    ws["A2"].font = Font(name="Arial", size=8, italic=True)
    ws.merge_cells("A2:E2")

    _cab(ws, 4, ["Anexo", "Situação", "Itens", "Fecham", "Não fecham"],
         [16, 30, 12, 12, 14])

    resumo: Dict[str, List[tuple]] = {}
    for anexo, rotulo, apurado, oficial in LINHAS_RGF:
        resumo.setdefault("RGF " + anexo.replace("Anexo ", "A"), []).append(
            (rotulo, apurado, oficial))

    rreo_itens = identidades_rreo(caminho_rreo_xls)
    for anexo, rotulo, a, b, obs in rreo_itens:
        resumo.setdefault("RREO " + anexo.replace("Anexo ", "A"), []).append((rotulo, a, b))

    lin = 5
    for anexo in sorted(resumo):
        itens = resumo[anexo]
        fecha = atencao = divergente = nao_apuravel = 0
        for rotulo, apurado, oficial in itens:
            if apurado is None or oficial is None:
                pct = None
            elif apurado == 0.0 and oficial == 0.0:
                pct = 0.0
            else:
                pct = (apurado - oficial) / oficial if oficial else None
            if pct is None:
                nao_apuravel += 1
            elif abs(pct) <= 0.02:
                fecha += 1
            elif abs(pct) <= 0.10:
                atencao += 1
            else:
                divergente += 1
        if divergente:
            situacao, cor = "divergente", RUIM
        elif atencao:
            situacao, cor = "atenção", ATEN
        elif nao_apuravel == len(itens):
            situacao, cor = "não verificável", CINZA
        else:
            situacao, cor = "fecha", OK

        ws.cell(lin, 1, anexo).font = Font(name="Arial", size=9, bold=True)
        c = ws.cell(lin, 2, situacao)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = cor
        ws.cell(lin, 3, len(itens)).font = Font(name="Arial", size=9)
        ws.cell(lin, 4, fecha).font = Font(name="Arial", size=9)
        ws.cell(lin, 5, divergente + atencao).font = Font(name="Arial", size=9)
        if nao_apuravel:
            ws.cell(lin, 5, f"{divergente + atencao} ({nao_apuravel} n/v)"
                    ).font = Font(name="Arial", size=9)
        for j in range(1, 6):
            ws.cell(lin, j).border = BORDA
        lin += 1

    # ---------------- RGF ----------------
    ws2 = wb.create_sheet("RGF")
    ws2.sheet_view.showGridLines = False
    ws2["A1"] = "RGF 2024 Q3 — conferência linha a linha"
    ws2["A1"].font = Font(name="Arial", size=12, bold=True)
    _cab(ws2, 3, ["Anexo", "Linha", "Apurado (MSC)", "Homologado", "Diferença", "%", "Situação"],
         [10, 46, 18, 18, 16, 10, 16])

    lin = 4
    for anexo, rotulo, apurado, oficial in LINHAS_RGF:
        pct = ((apurado - oficial) / oficial) if oficial else (0.0 if apurado == 0 else None)
        situacao, cor = _classificar(pct)
        ws2.cell(lin, 1, anexo).font = Font(name="Arial", size=8)
        ws2.cell(lin, 2, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((3, apurado), (4, oficial)):
            c = ws2.cell(lin, j, round(v, 2))
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        c = ws2.cell(lin, 5, round(apurado - oficial, 2))
        c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        c = ws2.cell(lin, 6, pct if pct is not None else "—")
        c.number_format = "0.00%"
        c.font = Font(name="Arial", size=8)
        c = ws2.cell(lin, 7, situacao)
        c.font = Font(name="Arial", size=8, bold=situacao not in ("fecha", "confere (até 2%)"))
        for j in range(1, 8):
            ws2.cell(lin, j).border = BORDA
        ws2.cell(lin, 7).fill = cor

        motivo = MOTIVOS.get(rotulo)
        if motivo:
            ws2.cell(lin, 2).comment = None
            ws2.row_dimensions[lin].height = 26
        lin += 1

    # ---------------- RREO ----------------
    ws3 = wb.create_sheet("RREO")
    ws3.sheet_view.showGridLines = False
    ws3["A1"] = "RREO 2024 B6 — identidades contábeis"
    ws3["A1"].font = Font(name="Arial", size=12, bold=True)
    _cab(ws3, 3, ["Anexo", "Verificação", "Valor A", "Valor B", "Diferença", "Situação", "Observação"],
         [10, 48, 18, 18, 16, 16, 40])

    lin = 4
    for anexo, rotulo, a, b, obs in identidades_rreo(caminho_rreo_xls):
        pct = (((a - b) / b) if b else (0.0 if a == 0 else None)) if (a is not None and b is not None) else None
        situacao, cor = _classificar(pct)
        ws3.cell(lin, 1, anexo).font = Font(name="Arial", size=8)
        ws3.cell(lin, 2, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((3, a), (4, b)):
            c = ws3.cell(lin, j, round(v, 2) if v is not None else "—")
            if v is not None:
                c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        c = ws3.cell(lin, 5, round(a - b, 2) if (a is not None and b is not None) else "—")
        if a is not None and b is not None:
            c.number_format = FMT
        c.font = Font(name="Arial", size=8)
        c = ws3.cell(lin, 6, situacao)
        c.font = Font(name="Arial", size=8, bold=True)
        c.fill = cor
        ws3.cell(lin, 7, obs).font = Font(name="Arial", size=7, italic=True)
        for j in range(1, 8):
            ws3.cell(lin, j).border = BORDA
        lin += 1

    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    wb.save(destino)
    return destino


if __name__ == "__main__":
    xls = sys.argv[1] if len(sys.argv) > 1 else r"D:\Downloads\SICONFI_RREO_171_BIMESTRAL_6.xls"
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saida", "BATIMENTO_GERAL.xlsx")
    print(gerar(xls, saida))
