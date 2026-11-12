# -*- coding: utf-8 -*-
"""Descoberta da aba que carrega os rótulos oficiais de cada anexo (caminho 3).

As planilhas de trabalho do Estado espelham o rascunho do Siconfi em alguma aba
(SICONFI, Rascunho, SIAI, Anexo NN...). Em vez de fixar nomes, procuramos a aba
e a coluna cujos valores acompanham os do rascunho, na mesma ordem.

Alinhamento em duas etapas:
  1. ancora   - localiza no arquivo de trabalho o primeiro valor do rascunho
                (o cabecalho do anexo ocupa muitas linhas, entao o deslocamento
                inicial pode ser grande);
  2. sequencia - a partir da ancora, cada valor e casado com a proxima
                ocorrencia na janela seguinte (tolera linhas a mais na planilha,
                que correspondem a linhas vazias descartadas na exportacao).

Uso:
    python ferramentas/descobrir_rotulos.py            (diagnostico)
    python ferramentas/descobrir_rotulos.py --gerar    (grava o catalogo)
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import unicodedata
import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

warnings.filterwarnings("ignore")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "app"))

from rascunho import ler_rascunho  # noqa: E402

TEMP = r"C:\Users\victo\AppData\Local\Temp"
PASTA_SAIDA = os.path.join(RAIZ, "dados", "catalogo")
MAX_BURACO = 8          # linhas a mais que a planilha pode ter entre dois valores
TOL = 0.5               # tolerancia de comparacao (centavos)


@dataclass
class Mapeamento:
    arquivo: str
    aba: str
    coluna: int
    taxa: float
    posicoes: List[int] = field(default_factory=list)
    rotulos: List[Tuple[str, int, bool]] = field(default_factory=list)
    colunas: List[dict] = field(default_factory=list)


def _norm(t: str) -> str:
    base = "".join(c for c in unicodedata.normalize("NFKD", t or "")
                   if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", base).strip().lower()


def _nivel(texto: str) -> int:
    return min((len(texto) - len(texto.lstrip(" "))) // 2, 6)


def _eh_total(texto: str) -> bool:
    t = _norm(texto)
    return bool(re.search(r"\((i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s*$", t)) or t.endswith("total")


def valores_rascunho(doc, numero: int) -> List[List[Optional[float]]]:
    """Series candidatas do rascunho.

    Inclui (a) cada coluna de valores do 1o quadro e (b) o anexo inteiro, com as
    linhas de todos os quadros concatenadas - esta ultima casa com abas que
    espelham o anexo completo (ex.: MATRIZ-SICONF do anexo 6).
    """
    anexo = doc.anexo(numero)
    if not anexo or not anexo.blocos:
        return []
    series: List[List[Optional[float]]] = []

    bloco = anexo.blocos[0]
    for col in bloco.colunas:
        if col.tipo == "percentual":
            continue
        serie = [l.valor(col.chave) for l in bloco.linhas]
        if sum(1 for v in serie if v is not None) >= 5:
            series.append(serie)

    completa: List[Optional[float]] = []
    for b in anexo.blocos:
        if not b.colunas:
            continue
        chave = b.colunas[0].chave
        completa.extend(l.valor(chave) for l in b.linhas)
    if sum(1 for v in completa if v is not None) >= 5:
        series.append(completa)
    return series


NOMES_PREFERIDOS = [
    ("siconfi", 0.12),
    ("siconf", 0.12),
    ("matriz", 0.10),
    ("rascunho", 0.08),
    ("conf siconfi", 0.06),
    ("anexo", 0.05),
    ("sia", 0.03),
]


def _bonus_nome(nome: str) -> float:
    baixo = _norm(nome)
    for chave, valor in NOMES_PREFERIDOS:
        if chave in baixo:
            return valor
    return 0.0


def _serie(ws, col: int, limite: int = 500) -> List[Optional[float]]:
    saida: List[Optional[float]] = []
    for cell in ws.iter_rows(min_col=col, max_col=col, max_row=limite, values_only=True):
        v = cell[0]
        saida.append(float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None)
    return saida


def _textos(ws, limite: int = 500) -> List[str]:
    """Texto BRUTO da coluna A (sem strip), para preservar a indentacao."""
    saida = []
    for cell in ws.iter_rows(min_col=1, max_col=1, max_row=limite, values_only=True):
        v = cell[0]
        saida.append("" if v is None else str(v))
    return saida


def _igual(a: Optional[float], b: Optional[float]) -> bool:
    if a is None or b is None:
        return False
    return abs(a - b) <= max(TOL, abs(a) * 1e-9)


def alinhar(alvo: List[Optional[float]], fonte: List[Optional[float]]) -> Tuple[List[int], float]:
    """Ancora no primeiro valor e segue em sequencia, tolerando buracos."""
    posicoes: List[int] = [-1] * len(alvo)
    primeiro = next((i for i, v in enumerate(alvo) if v is not None), None)
    if primeiro is None:
        return posicoes, 0.0

    ancora = -1
    for k, f in enumerate(fonte):
        if _igual(alvo[primeiro], f):
            ancora = k
            break
    if ancora < 0:
        return posicoes, 0.0

    posicoes[primeiro] = ancora
    acertos = 1
    comparaveis = 1
    j = ancora + 1
    for i in range(primeiro + 1, len(alvo)):
        v = alvo[i]
        if v is None:
            continue
        comparaveis += 1
        limite = min(len(fonte), j + MAX_BURACO + 1)
        achou = -1
        for k in range(j, limite):
            if _igual(v, fonte[k]):
                achou = k
                break
        if achou >= 0:
            posicoes[i] = achou
            acertos += 1
            j = achou + 1
    taxa = acertos / comparaveis if comparaveis else 0.0
    return posicoes, taxa


def alinhar_posicional(alvo: List[Optional[float]], fonte: List[Optional[float]]) -> Tuple[List[int], float]:
    """Fallback: ancora no primeiro valor casado e segue por posicao relativa.

    Serve para quadros pequenos em que os valores do rascunho divergem dos da
    planilha (ex.: anexo 13, cuja aba espelha outro periodo), mas a estrutura
    de linhas e a mesma.
    """
    posicoes: List[int] = [-1] * len(alvo)
    primeiro = next((i for i, v in enumerate(alvo) if v is not None), None)
    if primeiro is None:
        return posicoes, 0.0
    ancora = -1
    for k, f in enumerate(fonte):
        if _igual(alvo[primeiro], f):
            ancora = k
            break
    if ancora < 0:
        return posicoes, 0.0
    for i in range(len(alvo)):
        j = ancora + (i - primeiro)
        if 0 <= j < len(fonte):
            posicoes[i] = j
    return posicoes, 1.0


def _textos_col(ws, col: int, limite: int = 500) -> List[str]:
    """Texto bruto de uma coluna (sem strip), para leitura de cabecalhos."""
    saida = []
    for cell in ws.iter_rows(min_col=col, max_col=col, max_row=limite, values_only=True):
        v = cell[0]
        saida.append("" if v is None else str(v))
    return saida


def _cabecalho_das_colunas(mapa, textos_cols, largura: int):
    """Le os titulos de coluna das linhas imediatamente acima do primeiro dado."""
    posicoes = [p for p in mapa.posicoes if p >= 0]
    if not posicoes:
        return []
    ancora = min(posicoes)
    colunas = []
    for c in range(2, largura + 1):
        textos = textos_cols.get(c, [])
        partes = []
        for i in range(max(0, ancora - 6), ancora):
            if i < len(textos):
                v = re.sub(r"\s+", " ", textos[i]).strip()
                if v and v not in partes:
                    partes.append(v)
        if not partes:
            continue
        colunas.append(dict(indice=c - 2, titulo=partes[-1],
                            superior=" / ".join(partes[:-1])))
    return colunas


def _series_bloco(bloco) -> List[List[Optional[float]]]:
    """Series de valores de um quadro (uma por coluna monetaria com conteudo)."""
    series: List[List[Optional[float]]] = []
    for col in bloco.colunas:
        if col.tipo == "percentual":
            continue
        serie = [l.valor(col.chave) for l in bloco.linhas]
        if sum(1 for v in serie if v is not None) >= 1:
            series.append(serie)
    return series


def mapear_blocos(doc, numero: int):
    """Devolve {indice_do_quadro: Mapeamento} para todos os quadros do anexo."""
    import openpyxl

    anexo = doc.anexo(numero)
    if not anexo:
        return {}
    arquivos: List[str] = []
    for padrao in (f"RREO 2026_B4_{numero:02d} *.xlsx", f"RREO 2026_B*_{numero:02d} *.xlsx"):
        arquivos = glob.glob(os.path.join(TEMP, padrao))
        if arquivos:
            break
    if not arquivos:
        return {}

    saida = {}
    wb = openpyxl.load_workbook(arquivos[0], data_only=True, read_only=True)
    abas = []
    for nome in wb.sheetnames:
        ws = wb[nome]
        if ws.max_row < 5 or ws.max_column < 2:
            continue
        largura = min(ws.max_column, 10)
        textos_cols = {}
        for c in range(2, largura + 1):
            textos_cols[c] = _textos_col(ws, c)
        abas.append((nome, _textos(ws), [_serie(ws, c) for c in range(2, largura + 1)],
                     textos_cols, largura))

    for idx, bloco in enumerate(anexo.blocos):
        alvos = _series_bloco(bloco)
        if not alvos:
            continue
        melhor = None
        for nome, textos, series, textos_cols, largura in abas:
            for desloc, serie in enumerate(series, start=2):
                for alvo in alvos:
                    posicoes, taxa = alinhar(alvo, serie)
                    if taxa < 0.85 and len([v for v in alvo if v is not None]) <= 15:
                        posicoes, taxa = alinhar_posicional(alvo, serie)
                    if taxa < 0.85:
                        continue
                    rotulos = []
                    vazios = 0
                    for pos in posicoes:
                        if pos < 0 or pos >= len(textos):
                            rotulos.append(("", 0, False))
                            vazios += 1
                            continue
                        bruto = textos[pos]
                        limpo = re.sub(r"\s+", " ", bruto).strip()
                        if not limpo:
                            vazios += 1
                        rotulos.append((limpo, _nivel(bruto), _eh_total(limpo)))
                    cobertura = 1 - vazios / len(rotulos) if rotulos else 0.0
                    nota = taxa * 0.5 + cobertura * 0.4 + _bonus_nome(nome)
                    if melhor is None or nota > melhor.taxa:
                        melhor = Mapeamento(os.path.basename(arquivos[0]), nome, desloc, nota,
                                            posicoes, rotulos)
        if melhor:
            melhor.colunas = _cabecalho_das_colunas(melhor, textos_cols, largura)
            saida[idx] = melhor
    wb.close()
    return saida


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gerar", action="store_true")
    ap.add_argument("--rascunho", default=os.path.join(TEMP, "planilha_auditoria (1).xls"))
    args = ap.parse_args()

    doc = ler_rascunho(args.rascunho)
    total_ok = total_quadros = 0
    for numero in (3, 4, 6, 7, 13):
        anexo = doc.anexo(numero)
        if not anexo:
            print(f"Anexo {numero:02d}: ausente no rascunho")
            continue
        mapa = mapear_blocos(doc, numero)
        total_quadros += len(anexo.blocos)
        print(f"Anexo {numero:02d}: {len(mapa)}/{len(anexo.blocos)} quadros com rotulos")
        blocos_json = []
        for idx, m in sorted(mapa.items()):
            preenchidos = sum(1 for r in m.rotulos if r[0])
            print(f"    quadro {idx + 1:2}: {m.aba[:22]:22} col {m.coluna} "
                  f"nota {m.taxa:.2f} rotulos {preenchidos}/{len(m.rotulos)}")
            blocos_json.append(dict(indice=idx, fonte=m.arquivo, aba=m.aba, coluna=m.coluna,
                                    nota=round(m.taxa, 4),
                                    rotulos=[dict(texto=tt, nivel=nn, total=tt_)
                                             for tt, nn, tt_ in m.rotulos],
                                    colunas=m.colunas))
        total_ok += len(mapa)
        if args.gerar and blocos_json:
            os.makedirs(PASTA_SAIDA, exist_ok=True)
            destino = os.path.join(PASTA_SAIDA, f"rotulos_RREO_{numero:02d}.json")
            with open(destino, "w", encoding="utf-8") as f:
                json.dump(dict(anexo=f"RREO-{numero:02d}", blocos=blocos_json),
                          f, ensure_ascii=False, indent=1)
            print(f"    -> {destino}")
    print(f"total: {total_ok}/{total_quadros} quadros cobertos")
    return 0 if total_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
