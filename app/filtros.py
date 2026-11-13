# -*- coding: utf-8 -*-
"""Interpretador dos filtros dos mapeamentos da STN.

Os mapeamentos descrevem cada linha do anexo em linguagem natural. Este módulo
transforma essas descrições em predicados aplicáveis aos registros da MSC.

Expressões encontradas:

    NR começada por 1,2 EXCETO NR (Lista): 211102,211255
    NR começada com (Lista): 1
    NR começada por 111
    ND começada por 3.1.90.01
    FR (Lista): 1605
    Resultado de fórmula
    Mapeamento na célula

Regra: prefixo ("começada por" / "começada com") e lista ("(Lista): a,b").
O "EXCETO" remove itens.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence

CAMPOS = {"NR": "nr", "ND": "nd", "FR": "fr", "CO": "compl",
          "PO": "po", "AI": "ano_inscricao", "FS": "fs",
          "CC": "conta", "CONTA": "conta"}

RE_PREFIXO = re.compile(
    r"\b(NR|ND|FR|CO|PO|AI|CC)\s+come[çc]ad[ao]s?\s+(?:por|com)\s*"
    r"(?:\(Lista\)\s*)?[=:]?\s*([0-9.,\s]+)", re.I)
RE_LISTA = re.compile(r"\b(NR|ND|FR|CO|PO|AI|CC)\s*\(Lista\)\s*:\s*([0-9.,\s]+)", re.I)
RE_EXCETO = re.compile(r"EXCETO\s+(?:NR|ND|FR|CO|PO|AI|CC)\s*(?:\(Lista\))?\s*:\s*([0-9.,\s]+)",
                       re.I)


def _itens(texto: str) -> List[str]:
    return [t.strip() for t in re.split(r"[,\s]+", texto) if t.strip()]


@dataclass
class Filtro:
    """Predicado sobre um registro da MSC."""
    descricao: str
    prefixos: dict      # campo -> lista de prefixos
    exceto: dict        # campo -> lista de valores exatos
    invalido: bool = False

    def aplicar(self, reg) -> bool:
        if self.invalido:
            return False
        for campo, prefixos in self.prefixos.items():
            valor = getattr(reg, campo, "") or ""
            if not any(valor.startswith(p) for p in prefixos):
                return False
        for campo, valores in self.exceto.items():
            valor = getattr(reg, campo, "") or ""
            if any(valor.startswith(v) for v in valores):
                return False
        return True


def interpretar(texto: str) -> Filtro:
    """Converte a descrição em Filtro."""
    if not texto:
        return Filtro(texto or "", {}, {}, invalido=True)
    if re.search(r"Resultado de f[óo]rmula|Mapeamento na c[ée]lula", texto, re.I):
        return Filtro(texto, {}, {}, invalido=True)

    prefixos: dict = {}
    for m in RE_PREFIXO.finditer(texto):
        campo = CAMPOS.get(m.group(1).upper())
        if not campo:
            continue
        itens = _itens(m.group(2))
        if itens:
            prefixos.setdefault(campo, []).extend(itens)
    for m in RE_LISTA.finditer(texto):
        campo = CAMPOS.get(m.group(1).upper())
        if not campo:
            continue
        itens = _itens(m.group(2))
        if itens and campo not in prefixos:
            prefixos.setdefault(campo, []).extend(itens)

    exceto: dict = {}
    for m in RE_EXCETO.finditer(texto):
        # descobre de que campo é o EXCETO (o último campo citado antes)
        campo = "nr"
        for candidato in ("NR", "ND", "FR", "CO"):
            if re.search(candidato + r"\b", texto[:m.start()], re.I):
                campo = CAMPOS[candidato]
        itens = _itens(m.group(1))
        if itens:
            exceto.setdefault(campo, []).extend(itens)

    invalido = not prefixos and not exceto
    return Filtro(texto, prefixos, exceto, invalido=invalido)


def aplicar_linhas(linhas: Sequence, filtro_texto: str) -> List:
    f = interpretar(filtro_texto)
    return [r for r in linhas if f.aplicar(r)]


def total(linhas: Sequence, filtro_texto: str) -> float:
    f = interpretar(filtro_texto)
    return sum(r.liquido for r in linhas if f.aplicar(r))


if __name__ == "__main__":
    exemplos = [
        "NR começada por 1,2 EXCETO NR (Lista): 211102,211255",
        "NR começada com (Lista): 1",
        "NR começada por 111",
        "Resultado de fórmula",
        "ND começada por 3.1.90.01",
    ]
    for e in exemplos:
        f = interpretar(e)
        print(f"{e[:52]:52} -> prefixos={f.prefixos} exceto={f.exceto} invalido={f.invalido}")
