# -*- coding: utf-8 -*-
"""Leitura dos mapeamentos oficiais da STN (MDF 15ª edição — MSC 2026).

Os arquivos `Mapeamentos Parte III (RREO)` e `Parte IV (RGF)` trazem, para cada
linha de cada anexo, os **critérios de apuração**:

    coluna 1 — ESPECIFICAÇÃO (o rótulo da linha do anexo)
    coluna 2 — FILTROS SICONFI (o filtro, em linguagem natural)
    coluna 3 — Critérios (Informações Complementares / Contas Contábeis)

Exemplos de filtro:

    "NR começada por lista: 1114501,1114502"
    "Resultado de fórmula"
    "Mapeamento na célula"

E de critério:

    "NR: 1.1.1.4.50.1.0 + NR: 1.1.1.4.50.2.0"
    "Conta contábil: (6.2.1.3.1.02.00) e (6.2.2.1.3.03.00 + ...)"

Uso:

    python mapeamento.py --listar
    python mapeamento.py --anexo "RREO - ANEXO 03"
"""
from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import openpyxl

RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "dados", "mapeamentos")


@dataclass
class LinhaMapeamento:
    linha: int
    especificacao: str
    filtro: str
    criterio: str

    @property
    def naturezas_receita(self) -> List[str]:
        """NRs citadas no filtro ou no critério."""
        texto = f"{self.filtro} {self.criterio}"
        return sorted(set(re.findall(r"\b(\d{7,8})\b", texto)))

    @property
    def contas(self) -> List[str]:
        """Contas contábeis citadas (formato 6.2.1.2.0.00.00)."""
        texto = f"{self.filtro} {self.criterio}"
        achados = re.findall(r"\b(\d\.\d\.\d\.\d(?:\.\d+)*)\b", texto)
        return sorted(set(achados))


@dataclass
class Anexo:
    nome: str
    abas: List[str] = field(default_factory=list)
    linhas: List[LinhaMapeamento] = field(default_factory=list)


def _arquivos(parte: str = "") -> List[str]:
    padrao = os.path.join(RAIZ, "**", "*.xlsx")
    todos = glob.glob(padrao, recursive=True)
    if parte:
        todos = [p for p in todos if parte.lower() in p.lower()]
    return sorted(todos)


def listar() -> List[str]:
    return [os.path.basename(p) for p in _arquivos()]


def ler(caminho: str, aba: Optional[str] = None) -> Anexo:
    wb = openpyxl.load_workbook(caminho, data_only=True)
    nome = os.path.basename(caminho)
    abas = wb.sheetnames
    # prefere a aba de Estados
    alvo = aba
    if alvo is None:
        for a in abas:
            if "estado" in a.lower():
                alvo = a
                break
        else:
            alvo = abas[0]
    ws = wb[alvo]

    anexo = Anexo(nome=nome, abas=abas)
    for l in range(1, ws.max_row + 1):
        esp = ws.cell(l, 1).value
        filtro = ws.cell(l, 2).value
        criterio = ws.cell(l, 3).value
        if esp is None:
            continue
        esp = str(esp).strip()
        if not esp or len(esp) < 3:
            continue
        anexo.linhas.append(LinhaMapeamento(
            linha=l,
            especificacao=esp,
            filtro=str(filtro or "").strip(),
            criterio=str(criterio or "").strip(),
        ))
    return anexo


def por_anexo(chave: str) -> Optional[Anexo]:
    """Primeiro arquivo cujo nome contém a chave (ex.: 'ANEXO 03')."""
    for p in _arquivos():
        if chave.upper() in os.path.basename(p).upper():
            return ler(p)
    return None


def resumo() -> Dict[str, int]:
    saida = {}
    for p in _arquivos():
        try:
            a = ler(p)
            saida[os.path.basename(p)[:60]] = len(a.linhas)
        except Exception:  # noqa: BLE001
            saida[os.path.basename(p)[:60]] = -1
    return saida


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Mapeamentos STN dos anexos.")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--anexo", help="ex.: 'RREO - ANEXO 03'")
    a = ap.parse_args()
    if a.listar or not a.anexo:
        print("arquivos de mapeamento:")
        for nome, n in resumo().items():
            print(f"   {nome:62} {n:>4} linhas")
    if a.anexo:
        an = por_anexo(a.anexo)
        if not an:
            print(f"não encontrado: {a.anexo}")
        else:
            print(f"\n{an.nome}  (abas: {', '.join(an.abas[:3])})")
            for lm in an.linhas[:40]:
                print(f"   {lm.especificacao[:44]:44} | {lm.filtro[:52]}")
