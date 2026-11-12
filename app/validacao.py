# -*- coding: utf-8 -*-
"""Motor de conferencia dos demonstrativos.

Tres familias de checagem, todas derivadas do proprio layout do rascunho:

1. ARITMETICA EXPLICITA - colunas cujo titulo traz a formula entre parenteses
   ("% (b/a)", "SALDO (a-c)"). As letras sao resolvidas pelos marcadores das
   colunas. Divergencia = ERRO (a formula e inequivoca).
2. TOTAL x SUBORDINADOS - linha de total deve fechar com a soma dos itens
   subordinados (pela indentacao). Aceita a soma dos filhos diretos ou a de
   todos os descendentes; se nenhuma fechar, gera ALERTA (pode ser formula de
   subtracao, ex.: despesa liquida = bruta - deducoes).
3. TOTAL MENSAL - em blocos com colunas mensais (<MR-11>.. <MR>), a coluna
   TOTAL deve ser a soma dos meses. Divergencia = ALERTA, porque a legislacao
   admite ajustes (ex.: despesa nao executada, inscricao em RP nao processados).

Tolerancias: 1 centavo para moeda, 0,05 p.p. para percentual.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from modelo import Bloco, Coluna, Documento, Linha

TOL_MOEDA = 0.01
TOL_PCT = 0.05

RE_FORMULA_MOEDA = re.compile(r"\(\s*([a-z])\s*-\s*([a-z])\s*\)")
RE_FORMULA_PCT = re.compile(r"\(\s*([a-z])\s*/\s*([a-z])\s*\)")
RE_MENSAL = re.compile(r"^<MR(-\d+)?>$")


@dataclass
class Achado:
    severidade: str          # erro | alerta | info
    anexo: str
    bloco: str
    linha: str
    regra: str
    mensagem: str
    esperado: Optional[float] = None
    encontrado: Optional[float] = None

    @property
    def diferenca(self) -> Optional[float]:
        if self.esperado is None or self.encontrado is None:
            return None
        return self.encontrado - self.esperado

    def __str__(self) -> str:
        dif = f" (dif. {self.diferenca:,.2f})" if self.diferenca is not None else ""
        return (f"[{self.severidade.upper()}] {self.anexo} / {self.bloco} / "
                f"{self.linha}: {self.mensagem}{dif}")


def _col_por_marcador(bloco: Bloco) -> Dict[str, Coluna]:
    return {c.marcador: c for c in bloco.colunas if c.marcador}


def _descendentes(linhas: List[Linha], indice: int) -> List[Linha]:
    """Todas as linhas subordinadas (qualquer nivel maior), ate voltar ao nivel."""
    base = linhas[indice].nivel
    saida = []
    for j in range(indice + 1, len(linhas)):
        atual = linhas[j]
        if not atual.rotulo.strip():
            continue
        if atual.nivel <= base:
            break
        saida.append(atual)
    return saida


def _folhas(desc: List[Linha]) -> List[Linha]:
    """Itens finais da hierarquia (sem subordinados proprios)."""
    saida = []
    for k, d in enumerate(desc):
        prox = desc[k + 1] if k + 1 < len(desc) else None
        if prox is None or prox.nivel <= d.nivel:
            saida.append(d)
    return saida


def _somar(linhas: List[Linha], chave: str) -> Optional[float]:
    vals = [x.valor(chave) for x in linhas if x.valor(chave) is not None]
    return sum(vals) if vals else None


def _fecha(valor: float, candidatos: List[Optional[float]]) -> bool:
    for c in candidatos:
        if c is None:
            continue
        if abs(valor - c) <= max(TOL_MOEDA, abs(valor) * 1e-9):
            return True
    return False


def _comparar(linha: Linha, col: Coluna, esperado: float, tol: float,
              chave_anexo: str, bloco: Bloco, regra: str, rotulo_col: str) -> List[Achado]:
    atual = linha.valor(col.chave)
    if atual is None or abs(atual - esperado) <= tol:
        return []
    return [Achado(severidade="erro", anexo=chave_anexo, bloco=bloco.nome,
                   linha=linha.rotulo.strip() or "(sem rotulo)", regra=regra,
                   mensagem=f"{rotulo_col} nao confere no item",
                   esperado=esperado, encontrado=atual)]


def validar_bloco(bloco: Bloco, chave_anexo: str) -> List[Achado]:
    achados: List[Achado] = []
    marcadores = _col_por_marcador(bloco)

    # ---- 1. aritmetica explicita ----------------------------------------
    for col in bloco.colunas:
        titulo = f"{col.titulo} {col.superior}"
        m_pct = RE_FORMULA_PCT.search(titulo)
        m_sub = RE_FORMULA_MOEDA.search(titulo)
        if m_pct:
            a, b = m_pct.group(1), m_pct.group(2)
            ca, cb = marcadores.get(a), marcadores.get(b)
            if not ca or not cb:
                continue
            for linha in bloco.linhas:
                va, vb = linha.valor(ca.chave), linha.valor(cb.chave)
                if va is None or not vb:
                    continue
                achados.extend(_comparar(linha, col, va / vb * 100.0, TOL_PCT,
                                         chave_anexo, bloco, "percentual",
                                         f"% ({a}/{b})"))
        elif m_sub:
            a, b = m_sub.group(1), m_sub.group(2)
            ca, cb = marcadores.get(a), marcadores.get(b)
            if not ca or not cb:
                continue
            for linha in bloco.linhas:
                va, vb = linha.valor(ca.chave), linha.valor(cb.chave)
                if va is None or vb is None:
                    continue
                achados.extend(_comparar(linha, col, va - vb, TOL_MOEDA,
                                         chave_anexo, bloco, "saldo", f"saldo ({a}-{b})"))

    # ---- 2. total x subordinados ----------------------------------------
    for i, linha in enumerate(bloco.linhas):
        if not (linha.total or linha.negrito) or not linha.rotulo.strip():
            continue
        desc = _descendentes(bloco.linhas, i)
        if len(desc) < 2:
            continue
        menor = min(x.nivel for x in desc)
        filhos = [d for d in desc if d.nivel == menor]
        for col in bloco.colunas:
            if col.tipo == "percentual":
                continue
            valor = linha.valor(col.chave)
            if valor is None:
                continue
            diretos = _somar(filhos, col.chave)
            folhas = _somar(_folhas(desc), col.chave)
            if _fecha(valor, [diretos, folhas]):
                continue
            referencia = diretos if diretos is not None else folhas
            if referencia is None:
                continue
            achados.append(Achado(
                severidade="alerta", anexo=chave_anexo, bloco=bloco.nome,
                linha=linha.rotulo.strip(), regra="total x subordinados",
                mensagem=(f"total nao fecha com a soma dos itens subordinados "
                          f"na coluna '{col.titulo}' (pode ser formula de subtracao)"),
                esperado=referencia, encontrado=valor))

    # ---- 3. total mensal -------------------------------------------------
    mensais = [c for c in bloco.colunas if RE_MENSAL.match(c.titulo.strip())]
    totais = [c for c in bloco.colunas if "TOTAL" in c.titulo.upper()]
    if len(mensais) >= 6 and totais:
        col_total = totais[0]
        for linha in bloco.linhas:
            valor = linha.valor(col_total.chave)
            if valor is None:
                continue
            soma = sum(linha.valor(c.chave) or 0.0 for c in mensais)
            if abs(valor - soma) > TOL_MOEDA:
                achados.append(Achado(
                    severidade="alerta", anexo=chave_anexo, bloco=bloco.nome,
                    linha=linha.rotulo.strip() or "(sem rotulo)", regra="total mensal",
                    mensagem=(f"coluna '{col_total.titulo}' difere da soma dos meses "
                              f"(verificar ajustes, ex.: RP nao processados)"),
                    esperado=soma, encontrado=valor))
    return achados


def validar_documento(doc: Documento) -> List[Achado]:
    achados: List[Achado] = []
    for anexo in doc.anexos:
        for bloco in anexo.blocos:
            achados.extend(validar_bloco(bloco, anexo.chave))
    ordem = {"erro": 0, "alerta": 1, "info": 2}
    achados.sort(key=lambda a: (ordem.get(a.severidade, 3), a.anexo))
    return achados


def resumo(achados: List[Achado]) -> Dict[str, int]:
    r = {"erro": 0, "alerta": 0, "info": 0}
    for a in achados:
        r[a.severidade] = r.get(a.severidade, 0) + 1
    return r

