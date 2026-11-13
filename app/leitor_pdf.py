# -*- coding: utf-8 -*-
"""Leitor de texto de PDF em Python puro (suficiente para relatórios do SIAFEM).

Extrai texto com posição (x, y) para reconstruir linhas de tabela. Suporta:
  - streams de conteúdo com FlateDecode
  - operadores Tf, Td, TD, Tm, T*, Tj, TJ, '
  - fontes simples (WinAnsi/Latin-1) e diferenças básicas

Não é um renderizador: serve para ler relatórios gerados por sistema, que usam
texto real e não imagem.
"""
from __future__ import annotations

import re
import zlib
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

__all__ = ["ler_pdf", "Pagina", "ItemTexto"]

# operadores de texto que interessam
RE_OBJ = re.compile(rb"(\d+)\s+(\d+)\s+obj(.*?)endobj", re.S)
RE_STREAM = re.compile(rb"stream\r?\n(.*?)endstream", re.S)
RE_TEXTO = re.compile(
    rb"(?P<tj>\((?:[^()\\]|\\.)*\)\s*Tj)"
    rb"|(?P<tjarr>\[(?:[^\[\]]*)\]\s*TJ)"
    rb"|(?P<td>(?:[-0-9.]+\s+){2}(?:Td|TD))"
    rb"|(?P<tm>(?:[-0-9.]+\s+){6}Tm)"
    rb"|(?P<tstar>T\*)"
    rb"|(?P<tl>(?:[-0-9.]+\s+)TL)"
    rb"|(?P<bt>BT)"
    rb"|(?P<et>ET)",
    re.S,
)
RE_STRING = re.compile(rb"\((?:[^()\\]|\\.)*\)")
RE_NUM = re.compile(rb"-?\d+\.?\d*")


@dataclass
class ItemTexto:
    pagina: int
    x: float
    y: float
    texto: str


@dataclass
class Pagina:
    numero: int
    itens: List[ItemTexto]

    def linhas(self, tolerancia: float = 2.5) -> List[List[ItemTexto]]:
        """Agrupa os itens por linha (Y), da esquerda para a direita."""
        ordenados = sorted(self.itens, key=lambda i: (-i.y, i.x))
        linhas: List[List[ItemTexto]] = []
        atual: List[ItemTexto] = []
        y_ref: Optional[float] = None
        for item in ordenados:
            if y_ref is None or abs(item.y - y_ref) <= tolerancia:
                atual.append(item)
                y_ref = item.y if y_ref is None else y_ref
            else:
                linhas.append(sorted(atual, key=lambda i: i.x))
                atual = [item]
                y_ref = item.y
        if atual:
            linhas.append(sorted(atual, key=lambda i: i.x))
        return linhas

    def texto(self) -> str:
        return "\n".join(" ".join(i.texto for i in linha) for linha in self.linhas())


def _decodificar_pdfdoc(bruto: bytes) -> str:
    """Strings PDF: escapes simples e octal."""
    def troca(m: re.Match) -> bytes:
        s = m.group(0)[1:-1]
        s = s.replace(b"\\n", b"\n").replace(b"\\r", b"\r").replace(b"\\t", b"\t")
        s = s.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
        s = re.sub(rb"\\([0-7]{1,3})", lambda mm: bytes([int(mm.group(1), 8) & 0xFF]), s)
        return s
    return re.sub(rb"\((?:[^()\\]|\\.)*\)", troca, bruto).decode("latin-1", "replace")


def _streams_de_conteudo(dados: bytes) -> List[bytes]:
    saida: List[bytes] = []
    for m in RE_OBJ.finditer(dados):
        corpo = m.group(3)
        if b"/Image" in corpo or b"/FontFile" in corpo:
            continue
        if b"stream" not in corpo:
            continue
        for s in RE_STREAM.finditer(corpo):
            bruto = s.group(1)
            while bruto.endswith(b"\n") or bruto.endswith(b"\r"):
                bruto = bruto[:-1]
            if b"FlateDecode" in corpo:
                try:
                    decodificado = zlib.decompress(bruto)
                except zlib.error:
                    try:
                        decodificado = zlib.decompressobj().decompress(bruto)
                    except zlib.error:
                        continue
            else:
                decodificado = bruto
            if b"BT" in decodificado and (b"Tj" in decodificado or b"TJ" in decodificado):
                saida.append(decodificado)
    return saida


def _itens_de_stream(stream: bytes, pagina: int) -> List[ItemTexto]:
    itens: List[ItemTexto] = []
    x = y = 0.0
    pilha_x: List[float] = []
    for m in RE_TEXTO.finditer(stream):
        if m.group("bt"):
            x = y = 0.0
        elif m.group("tm"):
            nums = [float(v) for v in RE_NUM.findall(m.group("tm"))]
            if len(nums) >= 6:
                x, y = nums[4], nums[5]
                pilha_x = [x]
        elif m.group("td"):
            nums = [float(v) for v in RE_NUM.findall(m.group("td"))]
            if len(nums) >= 2:
                x += nums[0]
                y += nums[1]
        elif m.group("tstar"):
            y -= 12.0
        elif m.group("tj"):
            texto = _decodificar_pdfdoc(re.sub(rb"\s*Tj$", b"", m.group("tj")))
            if texto.strip():
                itens.append(ItemTexto(pagina, x, y, texto.strip()))
        elif m.group("tjarr"):
            partes = [_decodificar_pdfdoc(s) for s in RE_STRING.findall(m.group("tjarr"))]
            texto = "".join(partes).strip()
            if texto:
                itens.append(ItemTexto(pagina, x, y, texto))
    return itens


def ler_pdf(caminho: str) -> List[Pagina]:
    with open(caminho, "rb") as f:
        dados = f.read()
    paginas: List[Pagina] = []
    for n, stream in enumerate(_streams_de_conteudo(dados), start=1):
        itens = _itens_de_stream(stream, n)
        if itens:
            paginas.append(Pagina(n, itens))
    return paginas


def texto_completo(caminho: str) -> str:
    return "\n".join(p.texto() for p in ler_pdf(caminho))
