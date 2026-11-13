# -*- coding: utf-8 -*-
"""Acervo da Matriz de Saldos Contábeis (formato longo).

A partir de 2025 o Siconfi entrega a MSC em **um arquivo por classe, mês e tipo
de saldo**, com os atributos em colunas próprias:

    RN_2024_12_classe6_period_change.csv

Colunas:

    tipo_matriz, cod_ibge, classe_conta, conta_contabil, poder_orgao,
    ano_fonte_recursos, fonte_recursos, funcao, subfuncao, exercicio,
    mes_referencia, educacao_saude, data_referencia, entrada_msc,
    natureza_despesa, ano_inscricao, natureza_receita, valor, natureza_conta,
    tipo_valor, complemento_fonte

Duas regras que os números obrigam:

1. ``ending_balance`` é o saldo de fechamento; ``period_change`` é o movimento.
   Nas contas de liquidação o saldo traz **apenas natureza C** — os débitos
   (estornos e baixas por pagamento) só existem no movimento. A despesa líquida
   (créditos − débitos) só pode ser apurada sobre o ``period_change``.

2. O Anexo 1 do RGF é **janela móvel de 12 meses** terminada no mês do
   quadrimestre (Q1 → abril, Q2 → agosto, Q3 → dezembro), não o acumulado do ano.
"""
from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

#: nome aceito: RN_2024_12_classe6_period_change.csv
#: e também o padrão oficial MSC_24_2024_m12_MSCC_msc_orcamentaria_classe6_...
PADRAO = re.compile(
    r"(?:RN|\w+)_(\d{4})_(\d{2})_classe(\d)_(ending_balance|period_change)\.csv$", re.I)

PADRAO_MSC = re.compile(
    r"^MSC_(\d+)_(\d{4})_m(\d{2})_(MSCC|MSCE)_msc_"
    r"(orcamentaria|patrimonial|controle)_classe(\d)_"
    r"(ending_balance|period_change)\.csv$", re.I)

CONTAS_LIQUIDACAO = ("622130300", "622130400", "622130700")
CONTA_NAO_EXECUTADA = "863310000"

PO_EXECUTIVO = ("10111", "10112", "60611")
MES_DO_QUADRIMESTRE = {1: 4, 2: 8, 3: 12}


@dataclass(slots=True)
class Registro:
    ano: int
    mes: int
    conta: str
    po: str
    nd: str
    nr: str
    fr: str
    compl: str
    funcao: str
    ano_inscricao: str
    valor: float
    natureza: str        # C ou D

    @property
    def liquido(self) -> float:
        """Movimento líquido: créditos positivos, débitos negativos."""
        return self.valor if self.natureza == "C" else -self.valor

    @property
    def bruto(self) -> float:
        return self.valor if self.natureza == "C" else 0.0


def _f(v: str) -> float:
    t = (v or "").strip()
    if not t:
        return 0.0
    try:
        return float(t)
    except ValueError:
        return 0.0


class Acervo:
    """Índice dos arquivos da MSC por (ano, mês, classe, tipo de saldo)."""

    def __init__(self, raiz: str) -> None:
        self.raiz = raiz
        self._indice: Dict[Tuple[int, int, int, str], str] = {}
        self._indexar()

    def _indexar(self) -> None:
        for dirpath, _, arquivos in os.walk(self.raiz):
            for nome in arquivos:
                if not nome.lower().endswith(".csv"):
                    continue
                m = PADRAO.search(nome)
                if m:
                    ano, mes, classe, tipo = (int(m.group(1)), int(m.group(2)),
                                              int(m.group(3)), m.group(4).lower())
                else:
                    m2 = PADRAO_MSC.match(nome)
                    if not m2:
                        continue
                    ano, mes, classe, tipo = (int(m2.group(2)), int(m2.group(3)),
                                              int(m2.group(6)), m2.group(7).lower())
                self._indice[(ano, mes, classe, tipo)] = os.path.join(dirpath, nome)

    # ---------- consultas ----------
    @property
    def anos(self) -> List[int]:
        return sorted({k[0] for k in self._indice})

    def meses(self, ano: int, tipo_valor: str = "period_change",
              classe: int = 6) -> List[int]:
        return sorted({k[1] for k in self._indice
                       if k[0] == ano and k[2] == classe and k[3] == tipo_valor})

    def tem(self, ano: int, mes: int, classe: int = 6,
            tipo_valor: str = "period_change") -> bool:
        return (ano, mes, classe, tipo_valor) in self._indice

    # ---------- leitura ----------
    def ler(self, ano: int, mes: int, classe: int = 6,
            tipo_valor: str = "period_change") -> Iterator[Registro]:
        caminho = self._indice.get((ano, mes, classe, tipo_valor))
        if not caminho:
            raise FileNotFoundError(
                f"sem arquivo para {ano}-{mes:02d} classe{classe} {tipo_valor}")
        with open(caminho, encoding="utf-8-sig", errors="replace", newline="") as fh:
            # O separador varia: os arquivos normalizados usam ',' e os
            # convertidos do formato antigo usam ';'. Detecta pelo cabecalho.
            cabecalho = fh.readline()
            delim = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
            fh.seek(0)
            rd = csv.DictReader(fh, delimiter=delim)
            for r in rd:
                yield Registro(
                    ano=int(r.get("exercicio") or ano),
                    mes=int(r.get("mes_referencia") or mes),
                    conta=(r.get("conta_contabil") or "").strip(),
                    po=(r.get("poder_orgao") or "").strip(),
                    nd=(r.get("natureza_despesa") or "").strip(),
                    nr=(r.get("natureza_receita") or "").strip(),
                    fr=(r.get("fonte_recursos") or "").strip(),
                    compl=(r.get("complemento_fonte") or "").strip(),
                    funcao=(r.get("funcao") or "").strip(),
                    ano_inscricao=(r.get("ano_inscricao") or "").strip(),
                    valor=_f(r.get("valor")),
                    natureza=(r.get("natureza_conta") or "").strip().upper()[:1],
                )

    def total(self, ano: int, meses: Sequence[int],
              contas: Sequence[str] = CONTAS_LIQUIDACAO,
              filtro: Optional[Callable[[Registro], bool]] = None,
              classe: int = 6,
              tipo_valor: str = "period_change") -> float:
        total = 0.0
        for mes in meses:
            if not self.tem(ano, mes, classe, tipo_valor):
                continue
            for r in self.ler(ano, mes, classe, tipo_valor):
                if r.conta not in contas:
                    continue
                if filtro and not filtro(r):
                    continue
                total += r.liquido
        return total


def periodos_janela(ano_fim: int, mes_fim: int, n: int = 12) -> List[Tuple[int, int]]:
    """Os ``n`` meses terminados em (ano_fim, mes_fim), em ordem cronológica."""
    pares: List[Tuple[int, int]] = []
    ano, mes = ano_fim, mes_fim
    for _ in range(n):
        pares.append((ano, mes))
        mes -= 1
        if mes == 0:
            ano, mes = ano - 1, 12
    return list(reversed(pares))


def janela_do_quadrimestre(ano: int, quadrimestre: int,
                           acervo: Optional[Acervo] = None) -> List[Tuple[int, int]]:
    """Janela de 12 meses do quadrimestre, ajustada ao acervo disponível."""
    mes_fim = MES_DO_QUADRIMESTRE[quadrimestre]
    pares = periodos_janela(ano, mes_fim)
    if acervo is not None:
        pares = [p for p in pares if acervo.tem(p[0], p[1])]
    return pares


if __name__ == "__main__":
    import sys
    raiz = sys.argv[1] if len(sys.argv) > 1 else \
        r"D:\Downloads\PASEP Estado\MSC_RN_2021_2026_06\MSC_RN_2021_2026_06"
    a = Acervo(raiz)
    print("raiz:", a.raiz)
    print("anos:", a.anos)
    for ano in a.anos:
        meses = a.meses(ano)
        print(f"   {ano}: {len(meses)} meses ({min(meses) if meses else '-'}..{max(meses) if meses else '-'})")
