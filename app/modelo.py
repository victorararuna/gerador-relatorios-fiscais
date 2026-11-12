# -*- coding: utf-8 -*-
"""Modelo de dominio dos demonstrativos fiscais (MDF/Siconfi).

Terminologia:
  Documento  = um RREO ou RGF de um ente, poder, exercicio e periodo.
  Anexo      = um dos anexos do RREO (1..14) ou do RGF (1..6).
  Bloco      = um quadro dentro do anexo (ex.: "Receitas Orcamentarias",
               "Apuracao do Cumprimento do Limite Legal").
  Linha      = um rotulo com seus valores nas colunas do bloco.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Periodo:
    exercicio: int
    periodicidade: str          # BIMESTRAL / QUADRIMESTRAL
    numero: int                 # 1..6 (bimestre) ou 1..3 (quadrimestre)

    @property
    def rotulo(self) -> str:
        if self.periodicidade.upper().startswith("BIM"):
            return f"{self.numero}º bimestre"
        return f"{self.numero}º quadrimestre"

    @property
    def meses(self) -> int:
        """Meses acumulados ate o fim do periodo."""
        if self.periodicidade.upper().startswith("BIM"):
            return 2 * self.numero
        return 4 * self.numero

    @property
    def mes_final(self) -> int:
        return self.meses

    def __str__(self) -> str:
        return f"{self.exercicio} · {self.rotulo}"


@dataclass
class Ente:
    codigo: str = ""
    nome: str = ""
    poder: str = ""
    instituicao: str = ""

    @property
    def nome_curto(self) -> str:
        return self.nome.replace("Rio Grande do Norte", "RN")


@dataclass
class Coluna:
    chave: str
    titulo: str
    superior: str = ""          # titulo do grupo de colunas (linha de cima)
    marcador: str = ""          # (a), (b), (c)...
    tipo: str = "moeda"         # moeda | percentual | texto


@dataclass
class Linha:
    rotulo: str
    valores: Dict[str, Optional[float]] = field(default_factory=dict)
    nivel: int = 0              # indentacao (0 = sem)
    negrito: bool = False
    total: bool = False
    linha_origem: int = 0

    @property
    def vazia(self) -> bool:
        return not self.rotulo.strip() and not any(v is not None for v in self.valores.values())

    def valor(self, chave: str) -> Optional[float]:
        return self.valores.get(chave)


@dataclass
class Bloco:
    grupo: str = ""
    quadro: str = ""
    titulo_tabela: str = ""
    colunas: List[Coluna] = field(default_factory=list)
    linhas: List[Linha] = field(default_factory=list)

    @property
    def nome(self) -> str:
        return self.quadro or self.titulo_tabela or self.grupo


@dataclass
class Anexo:
    documento: str              # RREO | RGF
    numero: int
    blocos: List[Bloco] = field(default_factory=list)

    @property
    def chave(self) -> str:
        return f"{self.documento}-Anexo {self.numero:02d}"


@dataclass
class Documento:
    tipo: str                   # RREO | RGF
    ente: Ente = field(default_factory=Ente)
    periodo: Optional[Periodo] = None
    versao_layout: str = ""
    vigencia_layout: str = ""
    anexos: List[Anexo] = field(default_factory=list)
    arquivo_origem: str = ""

    def anexo(self, numero: int) -> Optional[Anexo]:
        for a in self.anexos:
            if a.numero == numero:
                return a
        return None

    @property
    def identificacao(self) -> str:
        return f"{self.tipo} {self.periodo}"

    def resumo(self) -> str:
        partes = [self.tipo, str(self.periodo), f"{len(self.anexos)} anexos"]
        if self.versao_layout:
            partes.append(f"layout {self.versao_layout}")
        return " · ".join(partes)
