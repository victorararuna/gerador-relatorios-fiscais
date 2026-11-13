# -*- coding: utf-8 -*-
"""Interpretador dos filtros dos mapeamentos da STN — versão 2.

Acrescenta dois recursos que o Anexo 5 exige:

1. **Filtro composto** — partes separadas por ``///``, aplicadas em E:
   ``PO começada por (Lista): 10  /// FR Pos. inicial= 2 ; Tamanho= 3; Lista= 500``

2. **Substring de fonte de recurso** — ``FR Pos. inicial= 2 ; Tamanho= 3``
   significa os caracteres da posição 2 ao 4 (1-indexado). A FR ``1500`` dá
   ``500``.

Expressões simples continuam iguais:

    NR começada por 1,2 EXCETO NR (Lista): 211102,211255
    CC começada por (Lista)= 2121101,2121301
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

CAMPOS = {"NR": "nr", "ND": "nd", "FR": "fr", "CO": "compl",
          "PO": "po", "AI": "ano_inscricao", "FS": "fs",
          "CC": "conta", "CONTA": "conta"}

RE_PREFIXO = re.compile(
    r"\b(NR|ND|FR|CO|PO|AI|CC)\s+come[çc]ad[ao]s?\s+(?:por|com)\s*"
    r"(?:\(?Lista\)?\s*)?[=:]?\s*([0-9.,\s]+)", re.I)
RE_LISTA = re.compile(r"\b(NR|ND|FR|CO|PO|AI|CC)\s*\(?Lista\)?\s*[=:]?\s*([0-9.,\s]+)",
                      re.I)
RE_EXCETO = re.compile(
    r"EXCETO\s+(NR|ND|FR|CO|PO|AI|CC)\s*"
    r"(?:come[çc]a\s+por\s+lista|na\s+lista|\(Lista\))?\s*[=:]?\s*([0-9.,\s]+)",
    re.I)
RE_SUBSTR = re.compile(
    r"(FR|ND|NR|CC)\s+Pos\.?\s*inicial\s*=\s*(\d+)\s*;?\s*Tamanho\s*=\s*(\d+)"
    r"(?:\s*;?\s*Lista\s*[=:]\s*([0-9.,\s]+))?", re.I)


def _itens(texto: str) -> List[str]:
    return [t.strip() for t in re.split(r"[,\s]+", texto or "") if t.strip()]


@dataclass
class Condicao:
    """Uma condição sobre um registro."""
    campo: str
    prefixos: List[str] = field(default_factory=list)
    posicao: Optional[int] = None
    tamanho: Optional[int] = None
    valores: List[str] = field(default_factory=list)
    exceto: List[str] = field(default_factory=list)

    def casar(self, reg) -> bool:
        valor = getattr(reg, self.campo, "") or ""
        if self.posicao is not None and self.tamanho:
            pedaco = valor[self.posicao - 1:self.posicao - 1 + self.tamanho]
            if self.valores:
                return pedaco in self.valores
            return True
        if self.prefixos:
            if not any(valor.startswith(p) for p in self.prefixos):
                return False
        if self.valores:
            if not any(valor.startswith(v) for v in self.valores):
                return False
        if self.exceto:
            if any(valor.startswith(e) for e in self.exceto):
                return False
        return True


@dataclass
class Filtro:
    descricao: str
    condicoes: List[Condicao] = field(default_factory=list)
    invalido: bool = False

    def aplicar(self, reg) -> bool:
        if self.invalido or not self.condicoes:
            return False
        return all(c.casar(reg) for c in self.condicoes)

    @property
    def prefixos(self):
        """Compatibilidade: primeiro campo/prefixos encontrados."""
        for c in self.condicoes:
            if c.prefixos:
                return {c.campo: c.prefixos}
        return {}

    @property
    def exceto(self):
        for c in self.condicoes:
            if c.exceto:
                return {c.campo: c.exceto}
        return {}


RE_CONTA_PONTUADA = re.compile(r"\b(\d\.\d\.\d\.\d\.\d+\.\d+\.\d+)\b")


def conta_para_prefixo(conta: str) -> str:
    """6.2.1.2.0.00.00 -> 621200000 (formato da MSC)."""
    return conta.replace(".", "")


def _parte(texto: str) -> List[Condicao]:
    """Converte um trecho (sem ///) em condições."""
    saida: List[Condicao] = []

    # conta contábil pontuada (formato do mapeamento)
    for m in RE_CONTA_PONTUADA.finditer(texto):
        saida.append(Condicao(campo="conta",
                              prefixos=[conta_para_prefixo(m.group(1))]))

    # substring de FR
    for m in RE_SUBSTR.finditer(texto):
        campo = CAMPOS.get(m.group(1).upper(), "fr")
        saida.append(Condicao(
            campo=campo,
            posicao=int(m.group(2)),
            tamanho=int(m.group(3)),
            valores=_itens(m.group(4) or ""),
        ))

    # prefixos
    for m in RE_PREFIXO.finditer(texto):
        campo = CAMPOS.get(m.group(1).upper())
        itens = _itens(m.group(2))
        if campo and itens:
            saida.append(Condicao(campo=campo, prefixos=itens))
    for m in RE_LISTA.finditer(texto):
        campo = CAMPOS.get(m.group(1).upper())
        itens = _itens(m.group(2))
        if campo and itens:
            # evita duplicar o que o prefixo já capturou
            if not any(c.campo == campo and c.prefixos for c in saida):
                saida.append(Condicao(campo=campo, prefixos=itens))

    # exceto
    for m in RE_EXCETO.finditer(texto):
        campo = CAMPOS.get(m.group(1).upper(), "nr")
        itens = _itens(m.group(2))
        if itens:
            if saida:
                saida[-1].exceto.extend(itens)
            else:
                saida.append(Condicao(campo=campo, exceto=itens))
    return saida


def interpretar(texto: str) -> Filtro:
    if not texto or not texto.strip():
        return Filtro(texto or "", [], invalido=True)
    if re.search(r"Resultado de f[óo]rmula|Mapeamento na c[ée]lula|FILTROS SICONFI",
                 texto, re.I) and "come" not in texto.lower() and "pos" not in texto.lower():
        return Filtro(texto, [], invalido=True)

    condicoes: List[Condicao] = []
    import re as _re
    for parte in _re.split(r"/{2,3}", texto):
        condicoes.extend(_parte(parte))
    invalido = not condicoes
    return Filtro(texto, condicoes, invalido=invalido)


def total(linhas, filtro_texto: str) -> float:
    f = interpretar(filtro_texto)
    return sum(r.liquido for r in linhas if f.aplicar(r))


if __name__ == "__main__":
    exemplos = [
        "PO começada por (Lista): 10  /// FR Pos. inicial= 2 ; Tamanho= 3; Lista= 500",
        "NR começada por 1,2 EXCETO NR (Lista): 211102,211255",
        "CC começada por (Lista)= 2121101,2121301",
        "Resultado de fórmula",
    ]
    for e in exemplos:
        f = interpretar(e)
        print(f"{e[:60]:60} -> inv={f.invalido} conds={len(f.condicoes)}")
        for c in f.condicoes:
            print(f"      {c}")
