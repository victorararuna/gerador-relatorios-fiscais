# -*- coding: utf-8 -*-
"""Identidade dos relatórios do SIGEF/RN — ano e mês de referência.

Uma extração do exercício errado (ou de outro mês) somaria em silêncio e
contaminaria a apuração. Este módulo lê o cabeçalho do relatório e valida a
identidade antes de qualquer soma.
"""
from __future__ import annotations

import re
from typing import Optional, Tuple

MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

RE_ANO = re.compile(r"Ano Base:\s*(\d{4})")
RE_MES = re.compile(r"M[êe]s Refer[êe]ncia\s+([A-Za-zÀ-ÿ]+)")


class ErroFonte(ValueError):
    """O relatório não é do exercício ou do mês esperado."""


def ler_cabecalho(texto: str) -> Tuple[Optional[int], Optional[str]]:
    """Extrai (ano, mês) do cabeçalho de um relatório do SIGEF/RN."""
    m_ano = RE_ANO.search(texto)
    m_mes = RE_MES.search(texto)
    ano = int(m_ano.group(1)) if m_ano else None
    mes = m_mes.group(1).capitalize() if m_mes else None
    # a expressão da tela às vezes vem antes do valor; normaliza pelo calendário
    if mes not in MESES:
        for nome in MESES:
            if mes and nome.lower().startswith(mes.lower()[:4]):
                mes = nome
                break
    return ano, mes


def validar(ano: Optional[int], mes: Optional[str],
            ano_esperado: int, mes_esperado: Optional[str] = None,
            origem: str = "") -> None:
    """Levanta ErroFonte quando o relatório não é do período esperado."""
    onde = f" ({origem})" if origem else ""
    if ano is None:
        raise ErroFonte(f"ano base não identificado no relatório{onde}")
    if ano != ano_esperado:
        raise ErroFonte(
            f"exercício errado{onde}: relatório é de {ano}, esperado {ano_esperado}")
    if mes_esperado is not None:
        if mes is None:
            raise ErroFonte(f"mês de referência não identificado{onde}")
        if mes.lower() != mes_esperado.lower():
            raise ErroFonte(
                f"mês errado{onde}: relatório é de {mes}, esperado {mes_esperado}")


def validar_arquivo(caminho: str, ano_esperado: int,
                    mes_esperado: Optional[str] = None) -> Tuple[int, str]:
    """Abre o PDF, lê o cabeçalho e valida. Devolve (ano, mês)."""
    import os
    import sys

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.join(raiz, "app") not in sys.path:
        sys.path.insert(0, os.path.join(raiz, "app"))
    import leitor_pdf as LP

    texto = re.sub(r"\s+", " ", LP.ler_pdf(caminho)[0].texto())
    ano, mes = ler_cabecalho(texto)
    validar(ano, mes, ano_esperado, mes_esperado, os.path.basename(caminho))
    return ano, mes
