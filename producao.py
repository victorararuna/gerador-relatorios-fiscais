# -*- coding: utf-8 -*-
"""Modo produção: recebe os insumos do fechamento e gera os relatórios.

Feito para o fechamento de outubro/2026. Recebe uma pasta com:

    matriz/        MSC em formato longo (RN_2026_10_classeN_period_change.csv)
    balancete.xls  Balancete Consolidado (Ano Base do exercício, Encerramento)
    receita.xls    Comparativo da Receita Orçada com a Arrecadada
    siconfi/       (opcional) anexos baixados da API, para conferência

E produz:

    RGF_<ano>_Q<q>_Anexo1.xlsx     no layout oficial
    CONFERENCIA.xlsx               apurado × homologado (se houver siconfi)
    relatorio.txt                  o que foi feito, com os números

Uso:

    python producao.py --entrada "C:\\fechamento\\2026-10" --ano 2026 --quadrimestre 3
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import balancete
import gerar_oficial
import msc_receita
import siconfi_declaracao as S
from acervo import Acervo, janela_do_quadrimestre
from gerar_anexo1_acervo import apurar_com_mensal
from siconfi import normalizar

FMT = '#,##0.00;[Red]-#,##0.00;"-"'
OK = PatternFill("solid", fgColor="FFC6EFCE")
ATEN = PatternFill("solid", fgColor="FFFFEB9C")
RUIM = PatternFill("solid", fgColor="FFFFC7CE")
CINZA = PatternFill("solid", fgColor="FFE7E6E6")


def classif(pct):
    if pct is None:
        return "sem referência", CINZA
    if abs(pct) <= 0.005:
        return "fecha", OK
    if abs(pct) <= 0.02:
        return "confere", OK
    if abs(pct) <= 0.05:
        return "atenção", ATEN
    return "divergente", RUIM


def achar(pasta: Path, *termos) -> Path | None:
    """Primeiro arquivo .xls/.xlsx cujo nome contém todos os termos."""
    for f in pasta.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in (".xls", ".xlsx"):
            continue
        nome = f.name.lower()
        if all(t.lower() in nome for t in termos):
            return f
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera os relatórios a partir do fechamento.")
    ap.add_argument("--entrada", required=True, help="pasta com matriz/, balancete e receita")
    ap.add_argument("--ano", type=int, required=True)
    ap.add_argument("--quadrimestre", type=int, default=3, choices=(1, 2, 3))
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()

    raiz = Path(args.entrada)
    if not raiz.is_dir():
        print(f"ERRO: pasta não encontrada: {raiz}")
        return 1
    saida = Path(args.saida) if args.saida else raiz / "saida"
    saida.mkdir(parents=True, exist_ok=True)

    log = []
    def diz(msg):
        print(msg)
        log.append(msg)

    diz(f"ENTRADA: {raiz}")
    diz(f"SAIDA  : {saida}")
    diz("")

    # ---------- 1. matriz ----------
    pasta_matriz = raiz / "matriz" if (raiz / "matriz").is_dir() else raiz
    acervo_qtd = sum(1 for _ in pasta_matriz.rglob("*.csv"))
    diz(f"[1/4] Matrizes encontradas: {acervo_qtd} CSV")
    if acervo_qtd == 0:
        diz("ERRO: nenhuma matriz na pasta.")
        return 1

    destino_acervo = raiz / "_acervo"
    if destino_acervo.exists():
        shutil.rmtree(destino_acervo, ignore_errors=True)
    r = normalizar(str(pasta_matriz), str(destino_acervo))
    diz(f"      normalizadas: {r['novos']} novas, {r['existentes']} existentes")

    acervo = Acervo(str(destino_acervo))
    janela = janela_do_quadrimestre(args.ano, args.quadrimestre, acervo)
    diz(f"      janela: {len(janela)} de 12 meses", )
    if janela:
        diz(f"      {janela[0][0]}-{janela[0][1]:02d} a {janela[-1][0]}-{janela[-1][1]:02d}")
    if len(janela) < 12:
        diz(f"      AVISO: faltam {12 - len(janela)} meses para fechar a janela")

    # ---------- 2. balancete ----------
    diz("")
    arq_bal = achar(raiz, "balancete")
    ne = 0.0
    if arq_bal:
        ano_bal = balancete.ano_base(str(arq_bal))
        diz(f"[2/4] Balancete: {arq_bal.name} (Ano Base {ano_bal})")
        if ano_bal == str(args.ano):
            ne = balancete.nao_executada(str(arq_bal))
            diz(f"      despesa não executada: {ne:,.2f}")
        else:
            diz(f"      IGNORADO: o ano base não é {args.ano}")
    else:
        diz("[2/4] Balancete: NÃO ENCONTRADO — a não executada ficará zerada")

    # ---------- 3. receita ----------
    diz("")
    arq_rec = achar(raiz, "receita")
    oc = None
    if arq_rec:
        try:
            oc = msc_receita.apurar(str(arq_rec))["operacoes_credito"]
            diz(f"[3/4] Receita: {arq_rec.name}")
            diz(f"      operações de crédito: {oc:,.2f}")
        except Exception as e:  # noqa: BLE001
            diz(f"[3/4] Receita: ERRO ao ler — {type(e).__name__}: {e}")
    else:
        diz("[3/4] Receita: NÃO ENCONTRADA — operações de crédito não apuradas")

    # ---------- 4. apuração ----------
    diz("")
    diz("[4/4] Apurando o Anexo 1 ...")
    linhas, mensal = apurar_com_mensal(acervo, janela)
    linhas["nao_executada"] = ne
    linhas["bruta"] = (linhas.get("vencimentos", 0.0) + linhas.get("patronal", 0.0)
                       + linhas.get("aposentadorias", 0.0) + linhas.get("pensoes", 0.0)
                       + linhas.get("terceirizacao", 0.0) + ne)
    linhas["deducoes"] = (linhas.get("judiciais", 0.0) + linhas.get("exerc_ant", 0.0)
                          + linhas.get("indenizacoes", 0.0)
                          + linhas.get("vinculados", 0.0) + linhas.get("enfermagem", 0.0))
    linhas["liquida"] = linhas["bruta"] - linhas["deducoes"]

    colunas = {}
    for i, (ano_m, mes_m) in enumerate(janela):
        col = 2 + i
        if col > 13:
            break
        do_mes = mensal.get((ano_m, mes_m), {})
        for campo in ("vencimentos", "patronal", "aposentadorias", "pensoes", "terceirizacao"):
            colunas.setdefault(campo, {})[col] = do_mes.get(campo, 0.0)
        colunas.setdefault("bruta", {})[col] = sum(
            do_mes.get(c, 0.0) for c in ("vencimentos", "patronal", "aposentadorias",
                                         "pensoes", "terceirizacao", "judiciais",
                                         "contratacao_temporaria"))

    campos = ("bruta", "vencimentos", "patronal", "aposentadorias", "pensoes",
              "terceirizacao", "exerc_ant", "indenizacoes", "vinculados",
              "enfermagem", "nao_executada", "deducoes", "liquida")
    valores = {k: linhas.get(k, 0.0) for k in campos}

    arq_saida = saida / f"RGF_{args.ano}_Q{args.quadrimestre}_Anexo1.xlsx"
    gerar_oficial.gerar(str(arq_saida), valores, {}, {}, {}, {}, colunas)
    diz(f"      gerado: {arq_saida.name}")

    # ---------- conferência ----------
    diz("")
    ref = None
    try:
        ref = S.referencia_rgf(args.ano, args.quadrimestre)
        diz("Conferência contra o Siconfi:")
    except Exception:  # noqa: BLE001
        diz("Conferência: sem arquivo do Siconfi baixado")

    wb = Workbook()
    ws = wb.active
    ws.title = "Conferência"
    ws["A1"] = f"RGF {args.ano} Q{args.quadrimestre} — Anexo 1"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    ws["A2"] = "Apurado a partir dos insumos do fechamento"
    ws["A2"].font = Font(name="Arial", size=8, italic=True)

    for j, t in enumerate(["Linha", "Apurado", "Homologado", "Diferença", "%", "Situação"], 1):
        c = ws.cell(4, j, t)
        c.font = Font(name="Arial", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor="FFD9E1F2")
        ws.column_dimensions[chr(64 + j)].width = (44 if j == 1 else 18) if j != 6 else 14

    mapa = [
        ("Despesa Bruta (I)", "bruta", "bruta"),
        ("Vencimentos", "vencimentos", "vencimentos"),
        ("Obrigações Patronais", "patronal", "patronal"),
        ("Aposentadorias", "aposentadorias", "aposentadorias"),
        ("Pensões", "pensoes", "pensoes"),
        ("Terceirização", "terceirizacao", "terceirizacao"),
        ("Despesa não Executada", "nao_executada", "nao_executada"),
        ("Despesas não Computadas (II)", "deducoes", "deducoes"),
        ("Despesa Líquida (III)", "liquida", "liquida"),
        ("Inativos Vinculados", "vinculados", "vinculados"),
        ("Piso do Enfermeiro", "enfermagem", "enfermagem"),
    ]
    lin = 5
    for rotulo, chave, chave_ref in mapa:
        ap = valores.get(chave)
        of = ref.get(chave_ref) if ref else None
        pct = (ap - of) / of if (ap is not None and of) else None
        sit, cor = classif(pct)
        ws.cell(lin, 1, rotulo).font = Font(name="Arial", size=8)
        for j, v in ((2, ap), (3, of)):
            c = ws.cell(lin, j, round(v, 2) if v is not None else "—")
            if v is not None:
                c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        if pct is not None:
            c = ws.cell(lin, 4, round(ap - of, 2))
            c.number_format = FMT
            c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 5, pct if pct is not None else "—")
        c.number_format = "0.00%"
        c.font = Font(name="Arial", size=8)
        c = ws.cell(lin, 6, sit)
        c.font = Font(name="Arial", size=8, bold=sit == "divergente")
        c.fill = cor
        if pct is not None:
            diz(f"   {rotulo:32} {ap:>18,.2f}  {pct*100:+.2f}%  {sit}")
        lin += 1

    arq_conf = saida / "CONFERENCIA.xlsx"
    wb.save(arq_conf)
    diz(f"      gerado: {arq_conf.name}")

    # ---------- relatório ----------
    arq_txt = saida / "relatorio.txt"
    arq_txt.write_text("\n".join(log), encoding="utf-8")
    print()
    print(f"Pronto. Arquivos em: {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
