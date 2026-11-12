# -*- coding: utf-8 -*-
"""Extração das linhas de detalhe das notas de empenho por célula.

Cada PDF "Imprimir Nota Empenho Célula_<celula>_<mês>" lista as notas de UM
complemento de empenho. A coluna "Célula Orçamentária" traz, numa só string,
a fonte de recurso e a natureza da despesa:

    16233 222201 0.8.00.000000 31.90.01.01
                   ^fonte        ^natureza

Com isso conseguimos, para cada poder (que vem do complemento):
  - quanto de inativos/pensões foi pago com recursos vinculados (fonte 0.8);
  - quanto foi pago com recursos do Tesouro (fonte 0.5).
"""
from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from leitor_pdf import ler_pdf

RE_CELULA = re.compile(r"(\d\.\d\.\d{2}\.\d{6})\s+(\d{2}\.\d{2}\.\d{2}\.\d{2})")
RE_NUMERO = re.compile(r"^-?[\d.]+,\d{2}$")


@dataclass
class Detalhe:
    arquivo: str
    celula: str
    mes: str
    complemento: str
    poder: str
    fonte: str
    natureza: str
    liquidado: float


def _classificar_poder(complemento: str) -> str:
    from fontes_empenho import _classificar_poder as base
    return base(complemento)


def _valor(txt: str) -> Optional[float]:
    t = txt.replace("D", "").replace("C", "").strip()
    if not RE_NUMERO.match(t):
        return None
    try:
        return float(t.replace(".", "").replace(",", "."))
    except ValueError:
        return None


def _colunas(pagina) -> Optional[List[float]]:
    """Posições X dos cabeçalhos da tabela."""
    for linha in pagina.linhas():
        textos = [it.texto for it in linha]
        if textos and textos[0].startswith("Agrupamento"):
            return [it.x for it in linha]
    return None


def _atribuir(linha, xs: List[float]) -> Dict[int, str]:
    """Mapeia cada item para a coluna cujo X é o mais próximo à esquerda."""
    saida: Dict[int, str] = {}
    for item in linha:
        idx = 0
        for k, x in enumerate(xs):
            if item.x >= x - 5:
                idx = k
        saida[idx] = (saida.get(idx, "") + " " + item.texto).strip()
    return saida


def ler_detalhes(caminho: str) -> List[Detalhe]:
    try:
        paginas = ler_pdf(caminho)
    except Exception:
        return []
    if not paginas:
        return []
    pagina = paginas[0]
    xs = _colunas(pagina)

    nome = os.path.basename(caminho)
    m_cel = re.search(r"Célula_(\d{6})", nome)
    celula = m_cel.group(1) if m_cel else ""
    m_mes = re.search(r"_(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)", nome)
    mes = m_mes.group(1) if m_mes else ""

    linhas = pagina.linhas()
    complemento = ""
    for i, linha in enumerate(linhas):
        t = " ".join(it.texto for it in linha)
        if t.strip().startswith("Complemento"):
            partes = [t.replace("Complemento", "", 1).strip()]
            for extra in linhas[i + 1: i + 4]:
                tt = " ".join(it.texto for it in extra).strip()
                if tt.startswith(("Agrupamento", "Total", "1622", "1620")):
                    break
                partes.append(tt)
            complemento = re.sub(r"\s+", " ", " ".join(partes)).strip()
            break
    poder = _classificar_poder(complemento)

    detalhes: List[Detalhe] = []
    if not xs:
        return detalhes
    for linha in linhas:
        celulas = _atribuir(linha, xs)
        texto_celula = ""
        for v in celulas.values():
            m = RE_CELULA.search(v)
            if m:
                texto_celula = v
                break
        if not texto_celula:
            continue
        m = RE_CELULA.search(texto_celula)
        fonte, natureza = m.group(1), m.group(2)
        liquidado = 0.0
        for k, v in celulas.items():
            if 0 < k < len(xs) and k >= 8:      # colunas de valor ficam à direita
                val = _valor(v.split()[0]) if v.split() else None
                if val is not None:
                    liquidado = val
                    break
        detalhes.append(Detalhe(arquivo=nome, celula=celula, mes=mes, complemento=complemento,
                                poder=poder, fonte=fonte, natureza=natureza,
                                liquidado=liquidado))
    return detalhes


def ler_pasta(pasta: str) -> List[Detalhe]:
    saida: List[Detalhe] = []
    for caminho in sorted(glob.glob(os.path.join(pasta, "**", "*Nota Empenho C*lula_*.pdf"), recursive=True)):
        saida.extend(ler_detalhes(caminho))
    return saida


def por_poder_fonte(detalhes: List[Detalhe]) -> Dict[Tuple[str, str], float]:
    """Soma liquidada por (poder, fonte), deduplicando por arquivo/natureza."""
    vistos = set()
    saida: Dict[Tuple[str, str], float] = {}
    for d in detalhes:
        chave = (d.arquivo, d.natureza, d.liquidado)
        if chave in vistos:
            continue
        vistos.add(chave)
        k = (d.poder, d.fonte)
        saida[k] = saida.get(k, 0.0) + d.liquidado
    return saida
