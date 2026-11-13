# -*- coding: utf-8 -*-
"""Pipeline dos demonstrativos: recebe uma pasta de matrizes e gera os relatórios.

Uso:
    python gerar_relatorios.py --entrada <pasta> [--saida <pasta>]

A pasta de entrada pode conter as Matrizes de Saldos Contábeis (arquivos
`instancia.csv`) em qualquer organização de subpastas. O pipeline:

1. lê a primeira linha de cada matriz (`24EX;2024-12`) e identifica a data;
2. escolhe a matriz de dezembro do exercício como base do RGF;
3. usa as de abril e agosto para as colunas dos quadrimestres;
4. usa as mensais (se existirem) para as colunas mensais do Anexo 1;
5. gera o RGF no layout oficial, com a aba de verificações.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gerar_oficial
import gerar_stn
import msc_dcl
import msc_pessoal as M


@dataclass
class Matriz:
    caminho: str
    ente: str
    exercicio: int
    mes: int

    @property
    def data(self) -> str:
        return f"{self.exercicio}-{self.mes:02d}"


@dataclass
class Conjunto:
    dezembro: Optional[Matriz] = None
    abril: Optional[Matriz] = None
    agosto: Optional[Matriz] = None
    mensais: Dict[int, Matriz] = field(default_factory=dict)
    todas: List[Matriz] = field(default_factory=list)


def _ler_cabecalho(caminho: str) -> Optional[tuple]:
    """Primeira linha da matriz: '24EX;2024-12'."""
    try:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            linha = f.readline().strip()
    except OSError:
        return None
    m = re.match(r"(\d+)EX;(\d{4})-(\d{2})", linha)
    if not m:
        return None
    return m.group(1), int(m.group(2)), int(m.group(3))


def achar_receita(pasta: str) -> Optional[str]:
    """Localiza o Comparativo da Receita Oncada com a Arrecadada."""
    for raiz, _, arquivos in os.walk(pasta):
        for nome in arquivos:
            baixo = nome.lower()
            if baixo.endswith((".xls", ".xlsx")) and "receita" in baixo and "comparativo" in baixo:
                return os.path.join(raiz, nome)
    return None


def escanear(pasta: str) -> List[Matriz]:
    """Encontra todas as matrizes (instancia.csv) sob a pasta."""
    achados: List[Matriz] = []
    for raiz, _, arquivos in os.walk(pasta):
        for nome in arquivos:
            if not nome.lower().endswith(".csv"):
                continue
            caminho = os.path.join(raiz, nome)
            cab = _ler_cabecalho(caminho)
            if not cab:
                continue
            ente, exercicio, mes = cab
            achados.append(Matriz(caminho=caminho, ente=ente,
                                  exercicio=exercicio, mes=mes))
    return sorted(achados, key=lambda m: (m.exercicio, m.mes))


def montar_conjunto(matrizes: List[Matriz], exercicio: int) -> Conjunto:
    """Separa as matrizes por papel, para o exercício pedido."""
    c = Conjunto(todas=matrizes)
    for m in matrizes:
        if m.exercicio != exercicio:
            continue
        if m.mes == 12:
            c.dezembro = m
        elif m.mes == 4:
            c.abril = m
        elif m.mes == 8:
            c.agosto = m
        c.mensais[m.mes] = m
    return c


def _pasta_mensal(conjunto: Conjunto, destino: str) -> Optional[str]:
    """Monta a estrutura mesN/instancia.csv esperada por colunas_mensais."""
    if len(conjunto.mensais) < 12:
        return None
    base = os.path.join(destino, "_mensais_tmp")
    for mes, m in conjunto.mensais.items():
        alvo = os.path.join(base, f"mes{mes}")
        os.makedirs(alvo, exist_ok=True)
        destino_arq = os.path.join(alvo, "instancia.csv")
        if os.path.abspath(m.caminho) != os.path.abspath(destino_arq):
            try:
                if os.path.exists(destino_arq):
                    os.remove(destino_arq)
                os.link(m.caminho, destino_arq)
            except OSError:
                import shutil
                shutil.copyfile(m.caminho, destino_arq)
    return base


def gerar(entrada: str, saida: str, exercicio: Optional[int] = None,
          quadrimestre: int = 3, verbose: bool = True) -> dict:
    """Executa o pipeline completo e devolve o caminho dos arquivos gerados."""
    def log(msg: str) -> None:
        if verbose:
            print(msg)

    log(f"Procurando matrizes em: {entrada}")
    matrizes = escanear(entrada)
    if not matrizes:
        raise SystemExit("Nenhuma matriz (instancia.csv) encontrada na pasta.")

    anos = sorted({m.exercicio for m in matrizes})
    log(f"  {len(matrizes)} matriz(es) encontrada(s) — exercício(s): {anos}")

    if exercicio is None:
        exercicio = max(anos)
    conjunto = montar_conjunto(matrizes, exercicio)

    if not conjunto.dezembro:
        raise SystemExit(f"Não há matriz de dezembro de {exercicio}.")

    log(f"  Base: {os.path.basename(conjunto.dezembro.caminho)} ({conjunto.dezembro.data})")
    if conjunto.abril:
        log(f"  1º quadrimestre: {conjunto.abril.data}")
    if conjunto.agosto:
        log(f"  2º quadrimestre: {conjunto.agosto.data}")
    if len(conjunto.mensais) == 12:
        log("  Série mensal completa (12 matrizes)")

    os.makedirs(saida, exist_ok=True)

    # parametros do pipeline
    gerar_stn.ARQUIVOS = {}
    anterior = next((m for m in matrizes
                     if m.exercicio == exercicio - 1 and m.mes == 12), None)
    if anterior:
        gerar_stn.ARQUIVOS[f"{anterior.data}"] = anterior.caminho
    if conjunto.abril:
        gerar_stn.ARQUIVOS[conjunto.abril.data] = conjunto.abril.caminho
    if conjunto.agosto:
        gerar_stn.ARQUIVOS[conjunto.agosto.data] = conjunto.agosto.caminho
    gerar_stn.ARQUIVOS[conjunto.dezembro.data] = conjunto.dezembro.caminho

    gerar_stn.PASTA_MENSAL = _pasta_mensal(conjunto, saida)

    # comparativo da receita: fornece as operacoes de credito (rubrica 4.2.1)
    receita = achar_receita(entrada)
    gerar_stn.ARQUIVO_RECEITA = receita
    if receita:
        log(f"  Comparativo da Receita: {os.path.basename(receita)}")
    else:
        log("  Comparativo da Receita: nao encontrado (operacoes de credito ficam zeradas)")

    nome = f"RGF_{exercicio}_Q{quadrimestre}_STN.xlsx"
    destino = os.path.join(saida, nome)
    log(f"Gerando {nome} ...")
    gerar_stn.main(conjunto.dezembro.caminho, destino,
                   anterior.caminho if anterior else None)

    log(f"Pronto: {destino}")
    return {"rgf": destino, "exercicio": exercicio, "matrizes": len(matrizes),
            "receita": receita}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Gera os demonstrativos do RGF a partir das MSC.")
    ap.add_argument("--entrada", required=True, help="pasta com as matrizes (instancia.csv)")
    ap.add_argument("--saida", default=None, help="pasta de destino")
    ap.add_argument("--exercicio", type=int, default=None)
    ap.add_argument("--quadrimestre", type=int, default=3)
    args = ap.parse_args()
    saida = args.saida or os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida")
    gerar(args.entrada, saida, args.exercicio, args.quadrimestre)
