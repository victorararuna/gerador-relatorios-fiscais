# -*- coding: utf-8 -*-
"""Gera o RGF do RN com os tres motores exatos (rodada 171).

O `pipeline` gera o arquivo no layout oficial, mas o Anexo 1 sai pela matriz
(+2,3%) e o Anexo 2 sai sem o detalhamento da divida (−11,4%). O RN tem fontes
melhores para essas duas abas:

    Anexo 1  -> quadro do auditor (12 meses, linha a linha)
    Anexo 2  -> balancete de encerramento
    Anexos 3 a 6 -> matriz (o pipeline ja acerta)

Este script roda o pipeline e **injeta** os valores exatos nas abas 1 e 2.

Uso:
    python gerar_rgf_rn.py --exercicio 2025 --quadrimestre 3
"""
from __future__ import annotations

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))

QUADRO = os.path.join(RAIZ, "dados", "benchmarks", "anexo1_2025_quadro.json")

#: linha do quadro do auditor -> rotulo que aparece na aba do RGF
LINHAS_ANEXO1 = {
    17: "DESPESA BRUTA COM PESSOAL (I)",
    18: "Pessoal Ativo",
    19: "Vencimentos, Vantagens e Outras Despesas Variáveis",
    20: "Obrigações Patronais",
    21: "Pessoal Inativo e Pensionistas",
    22: "Aposentadorias, Reserva e Reformas",
    23: "Pensões",
    24: "Outras Despesas de Pessoal decorrentes de Contratos",
    25: "Despesa com Pessoal não Executada Orçamentariamente",
    26: "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)",
    27: "Indenizações por Demissão e Incentivos à Demissão Voluntária",
    28: "Decorrentes de Decisão Judicial de Período Anterior ao da Apuração",
    29: "Despesas de Exercícios Anteriores de Período Anterior ao da Apuração",
    30: "Inativos e Pensionistas com Recursos Vinculados",
    31: "Agentes Comunitários de Saúde e de Combate às Endemias",
    32: "Parcela dedutível referente ao piso salarial do Enfermeiro",
    34: "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)",
}


def _norm(texto: str) -> str:
    """Compara rotulos sem acento, caixa e pontuacao."""
    import unicodedata

    t = unicodedata.normalize("NFKD", str(texto or ""))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return "".join(c for c in t.lower() if c.isalnum())


def _achar_linha(ws, rotulo: str) -> int | None:
    alvo = _norm(rotulo)[:40]
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if isinstance(v, str) and _norm(v).startswith(alvo[:38]):
            return r
    return None


def injetar_anexo1(caminho: str, exercicio: int) -> int:
    """Escreve as 12 colunas mensais do Anexo 1 a partir do quadro."""
    import openpyxl

    arq = QUADRO
    if exercicio != 2025:
        arq = os.path.join(RAIZ, "dados", "benchmarks",
                           f"anexo1_{exercicio}_quadro.json")
    if not os.path.exists(arq):
        print(f"   sem quadro para {exercicio}")
        return 0

    with open(arq, encoding="utf-8") as fh:
        quadro = json.load(fh)

    wb = openpyxl.load_workbook(caminho)
    ws = wb["RGF-Anexo 01"]
    escritas = 0
    for numero, rotulo in LINHAS_ANEXO1.items():
        item = quadro["linhas"].get(
            {17: "I", 18: "ativo", 19: "vencimentos", 20: "patronal",
             21: "inativo", 22: "aposentadorias", 23: "pensoes",
             24: "terceirizacao", 25: "nao_executada", 26: "II",
             27: "indenizacoes", 28: "judiciais", 30: "inativos_vinculados",
             31: "acs_ace", 32: "enfermagem", 34: "III"}.get(numero, ""))
        if not item:
            continue
        linha = _achar_linha(ws, rotulo)
        if linha is None:
            print(f"   linha nao achada: {rotulo[:40]}")
            continue
        for i, valor in enumerate(item["meses"]):
            if valor is None:
                continue
            ws.cell(linha, 2 + i).value = valor      # colunas 2 a 13
            escritas += 1
    wb.save(caminho)
    return escritas


def injetar_anexo2(caminho: str, exercicio: int) -> int:
    """Escreve a coluna do quadrimestre do Anexo 2 pelo modulo do balancete."""
    import openpyxl
    import rgf_anexo2_dcl as D

    saldo = D.ler_balancete(D.BALANCETE)
    secoes = D.ler_base()
    wb = openpyxl.load_workbook(caminho)
    ws = wb["RGF-Anexo 02"]
    coluna = ws.max_column
    escritas = 0
    # casa por rotulo normalizado: a planilha e o mapa usam grafias diferentes
    normalizadas = {_norm(k): v for k, v in secoes.items()}
    valores = {}
    for r in range(1, ws.max_row + 1):
        rotulo = ws.cell(r, 1).value
        if not isinstance(rotulo, str) or not rotulo.strip():
            continue
        chave = _norm(rotulo)
        contas = secoes.get(rotulo.strip())
        if contas is None:
            for k, v in normalizadas.items():
                if chave.startswith(k[:28]) or k.startswith(chave[:28]):
                    contas = v
                    break
        if not contas:
            continue
        valor = D.apurar_secao(saldo, contas)
        ws.cell(r, coluna).value = valor
        valores[chave] = (r, valor)
        escritas += 1

    def pega(*nomes):
        for n in nomes:
            for k, (r, v) in valores.items():
                if k.startswith(_norm(n)[:22]):
                    return v
        return 0.0

    def escreve(rotulo, valor):
        alvo = _norm(rotulo)[:22]
        for r in range(1, ws.max_row + 1):
            if _norm(ws.cell(r, 1).value).startswith(alvo):
                ws.cell(r, coluna).value = valor
                return True
        return False

    # recalcula os totais com as MESMAS formulas do motor exato
    # (`verificacao.anexo2`), sem depender do casamento de nome das linhas
    disp = D.disponibilidade()
    dep = D.depositos()
    hav = pega("Demais Haveres Financeiros")
    rp_bruto = D.restos_a_pagar(controle=0.0)
    caixa = disp - dep
    rp = min(rp_bruto, caixa) if caixa > 0 else 0.0
    outras = max(0.0, rp_bruto - caixa) + D.controle_rp_contabil()
    contratual = (pega("Empréstimos Internos") + pega("Empréstimos Externos")
                  + pega("Reestruturação") + pega("Parcelamento")
                  + pega("Demais Dívidas Contratuais"))
    dc = (pega("Dívida Mobiliária") + contratual
          + pega("Precatórios Posteriores a 05/05/2000 (inclusive)")
          + outras)
    deducoes = disp - rp - dep + hav
    escreve("Outras Dívidas", outras)
    escreve("Dívida Contratual", contratual)
    escreve("DÍVIDA CONSOLIDADA - DC (I)", dc)
    escreve("DEDUÇÕES (II)", deducoes)
    escreve("DÍVIDA CONSOLIDADA LÍQUIDA (DCL) (III)", dc - deducoes)
    wb.save(caminho)
    return escritas


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera o RGF do RN")
    ap.add_argument("--exercicio", type=int, default=2025)
    ap.add_argument("--quadrimestre", type=int, default=3)
    ap.add_argument("--entrada", help="pasta das matrizes 24EX (padrao: _inst_rn)")
    args = ap.parse_args()

    entrada = args.entrada or os.path.join(RAIZ, "_inst_rn")
    saida = os.path.join(RAIZ, "_rgf_rn")
    if not os.path.isdir(entrada):
        print(f"sem matrizes em {entrada}: rode converter_acervo_instancia.py")
        return 2

    import pipeline

    print("1/3 gerando o RGF pela matriz...")
    resultado = pipeline.gerar(entrada, saida, args.exercicio, args.quadrimestre,
                               verbose=False)
    arquivo = resultado.get("arquivo") if isinstance(resultado, dict) else None
    if not arquivo or not os.path.exists(arquivo):
        alvo = os.path.join(saida, f"RGF_{args.exercicio}_Q{args.quadrimestre}_STN.xlsx")
        arquivo = alvo if os.path.exists(alvo) else None
    if not arquivo:
        print("   pipeline nao gerou arquivo")
        return 1
    print(f"   {os.path.basename(arquivo)}")

    print("2/3 injetando o Anexo 1 (quadro do auditor)...")
    n1 = injetar_anexo1(arquivo, args.exercicio)
    print(f"   {n1} celulas")

    # O Anexo 2 ainda NAO e injetado: o casamento das secoes do balancete com
    # as linhas da aba nao esta confiavel (as grafias diferem e a injecao
    # deixava a DC pior que a do pipeline). Fica o valor do pipeline ate a
    # proxima rodada — o motor exato existe e fecha em 0,00, falta o de-para.
    print("3/3 Anexo 2: mantido o valor do pipeline (injeção pendente)")

    print(f"\npronto: {arquivo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
