# -*- coding: utf-8 -*-
"""Leitura das notas de empenho por célula (162011 / 162233) e separação por poder.

Cada PDF "Imprimir Nota Empenho Célula_<celula>_<MÊS>[(n)].pdf" corresponde a UM
complemento de empenho, e o complemento nomeia o poder de origem:

    162233-16233 00002 Benefícios previdenciários - P. Legislativo - Fundo ...
    162011-00001 00006 Benefícios previdenciários - MP - Capitalização ...

Portanto o valor de inativos/pensionistas de cada poder é o "Total" do PDF
daquele complemento. Como o mesmo complemento pode ter sido baixado mais de uma
vez, deduplicamos por (mês, unidade gestora, complemento).
"""
from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from leitor_pdf import ler_pdf

RE_VALOR = re.compile(r"^-?[\d.]+,\d{2}$")
RE_COMPLEMENTO = re.compile(r"(\d{6}-\d{5}\s+\d{5})\s+(.*)", re.S)

PODERES = [
    ("JUDICIARIO", [r"\bjudici", r"\btj\b", r"tribunal de justi"]),
    ("TRIBUNAL DE CONTAS", [r"\btce\b", r"tribunal de contas"]),
    ("LEGISLATIVO", [r"legislativo", r"assembleia"]),
    ("MINISTERIO PUBLICO", [r"\bmp\b", r"ministerio publico"]),
    ("DEFENSORIA", [r"defensoria", r"\bdpe\b", r"defensoria publica"]),
    ("EXECUTIVO", [r"executivo", r"\bgoverno\b"]),
]


@dataclass
class NotaCelula:
    arquivo: str
    celula: str
    mes: str
    ug: str
    complemento: str
    poder: str
    valores: List[float] = field(default_factory=list)

    @property
    def empenhado(self) -> float:
        return self.valores[0] if self.valores else 0.0

    @property
    def liquidado(self) -> float:
        return self.valores[1] if len(self.valores) > 1 else 0.0


def _num(txt: str) -> Optional[float]:
    t = txt.replace("D", "").replace("C", "").strip()
    if not RE_VALOR.match(t):
        return None
    return float(t.replace(".", "").replace(",", "."))


def _classificar_poder(complemento: str) -> str:
    baixo = complemento.lower()
    for nome, chaves in PODERES:
        for k in chaves:
            if re.search(k, baixo):
                return nome
    return "NAO IDENTIFICADO"


def ler_nota(caminho: str) -> Optional[NotaCelula]:
    try:
        paginas = ler_pdf(caminho)
    except Exception:
        return None
    if not paginas:
        return None
    linhas = [" ".join(i.texto for i in linha) for linha in paginas[0].linhas()]
    texto = "\n".join(linhas)

    m_cel = re.search(r"Célula_(\d{6})", os.path.basename(caminho))
    celula = m_cel.group(1) if m_cel else ""
    m_mes = re.search(r"_(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)", os.path.basename(caminho))
    mes = m_mes.group(1) if m_mes else ""

    ug = ""
    m_ug = re.search(r"Unidade Gestora\s*\|?\s*(\d{6})\s*([^|]*)", texto)
    if m_ug:
        ug = m_ug.group(1)

    complemento = ""
    idx = next((i for i, l in enumerate(linhas) if l.strip().startswith("Complemento")), None)
    if idx is not None:
        partes = [linhas[idx].replace("Complemento", "", 1).strip()]
        for extra in linhas[idx + 1: idx + 4]:
            if extra.strip().startswith(("Agrupamento", "Total", "1622", "1620")):
                break
            partes.append(extra.strip())
        complemento = re.sub(r"\s+", " ", " ".join(partes)).strip()

    valores: List[float] = []
    for linha in linhas:
        if linha.strip().startswith("Total"):
            for pedaco in linha.split():
                v = _num(pedaco)
                if v is not None:
                    valores.append(v)
            break

    return NotaCelula(arquivo=os.path.basename(caminho), celula=celula, mes=mes, ug=ug,
                      complemento=complemento,
                      poder=_classificar_poder(complemento), valores=valores)


def ler_pasta(pasta: str) -> List[NotaCelula]:
    notas: List[NotaCelula] = []
    for caminho in sorted(glob.glob(os.path.join(pasta, "**", "*Nota Empenho C*lula_*.pdf"), recursive=True)):
        nota = ler_nota(caminho)
        if nota and nota.valores:
            notas.append(nota)
    return notas


def consolidar(notas: List[NotaCelula]) -> Dict[tuple, NotaCelula]:
    """Deduplica por (célula, mês, UG, complemento)."""
    saida: Dict[tuple, NotaCelula] = {}
    for n in notas:
        chave = (n.celula, n.mes, n.ug, n.complemento)
        if chave not in saida:
            saida[chave] = n
    return saida


def por_poder(notas: List[NotaCelula]) -> Dict[str, Dict[str, float]]:
    """Soma liquidado por poder e por mês."""
    consolidado = consolidar(notas)
    saida: Dict[str, Dict[str, float]] = {}
    for n in consolidado.values():
        d = saida.setdefault(n.poder, {})
        d[n.mes] = d.get(n.mes, 0.0) + n.liquidado
    return saida
