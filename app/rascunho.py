# -*- coding: utf-8 -*-
"""
Leitura dos RASCUNHOS do Siconfi (planilhas .xls exportadas por anexo).

Formato observado (SICONFI_RREO/RGF v14, vigencia 05/01/2026):

    linha 3   RELATORIO RESUMIDO ... / RELATORIO DE GESTAO FISCAL
    linha 4   VERSAO: v14
    linha 5   VIGENCIA: 05/01/2026
    linha 7   Ente: 24 - Rio Grande do Norte
    linha 8   Poder: E - Executivo
    linha 9   Instituicao: 171 - Governo do Estado ...
    linha 10  Exercicio: 2026
    linha 11  Periodicidade: BIMESTRAL
    linha 12  Periodo: 2o bimestre
    linha N   Grupo: Tabela 1.0 - ...
    linha N+1 Quadro: Despesa com Pessoal
    linha N+2 Rotulo: Padrao
    linha N+3.. cabecalho de colunas
    ...       dados (coluna A = rotulo; demais = valores)

Todo o reconhecimento textual e feito sobre uma versao sem acento, para nao
depender de codificacao nem de variacao de grafia.
"""
from __future__ import annotations

import os
import re
import unicodedata
from typing import Dict, List, Optional, Tuple

from leitor_xls import Aba, ler_xls
from modelo import Anexo, Bloco, Coluna, Documento, Ente, Linha, Periodo

RE_ABA = re.compile(r"^(RREO|RGF)\s*-\s*Anexo\s*(\d+)", re.I)
RE_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u00ad\u200b\ufeff]")
MARCADOR = re.compile(r"\(([a-z])\)")
LIMITE_META = 20


def _semacento(t: str) -> str:
    base = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in base if not unicodedata.combining(c))


def _limpar(t: str) -> str:
    """Normaliza espacos e remove caracteres de controle que quebram o Excel."""
    return re.sub(r"\s+", " ", RE_CTRL.sub("", t or "")).strip()


def _norm(t: str) -> str:
    return _semacento(_limpar(t)).lower()


def _num(v) -> Optional[float]:
    return float(v) if isinstance(v, (int, float)) else None


# ---------------------------------------------------------------------------
# metadados
# ---------------------------------------------------------------------------
def _ler_metadados(aba: Aba) -> Tuple[Ente, Optional[Periodo], str, str]:
    ente = Ente()
    versao = vigencia = ""
    exercicio: Optional[int] = None
    periodicidade = ""
    numero_periodo: Optional[int] = None

    for lin in range(1, min(aba.max_lin, LIMITE_META) + 1):
        bruto = _limpar(aba.texto(lin, 1))
        if not bruto:
            continue
        txt = _norm(bruto)
        m = re.match(r"^(ente|poder|instituicao|exercicio|periodicidade|periodo|versao|vigencia)"
                     r"\s*:\s*(.*)$", txt)
        if not m:
            continue
        chave, resto = m.group(1), m.group(2)
        valor = _limpar(bruto.split(":", 1)[1]) if ":" in bruto else ""
        if chave == "ente":
            partes = re.match(r"^(\d*)\s*-?\s*(.*)$", resto)
            ente.codigo = (partes.group(1) or "").strip()
            ente.nome = valor.split("-", 1)[-1].strip()
        elif chave == "poder":
            ente.poder = valor
        elif chave == "instituicao":
            ente.instituicao = valor
        elif chave == "exercicio":
            d = re.search(r"(\d{4})", resto)
            exercicio = int(d.group(1)) if d else None
        elif chave == "periodicidade":
            periodicidade = resto.upper()
        elif chave == "periodo":
            d = re.search(r"(\d+)", resto)
            numero_periodo = int(d.group(1)) if d else None
        elif chave == "versao":
            versao = valor
        elif chave == "vigencia":
            vigencia = valor

    periodo = None
    if exercicio and numero_periodo:
        periodo = Periodo(exercicio, periodicidade or "BIMESTRAL", numero_periodo)
    return ente, periodo, versao, vigencia


# ---------------------------------------------------------------------------
# blocos
# ---------------------------------------------------------------------------
def _abre_bloco(linha_norm: str) -> bool:
    return linha_norm.startswith("rotulo:")


def _contexto_bloco(aba: Aba, linha_rotulo: int) -> Tuple[str, str]:
    grupo = quadro = ""
    for lin in range(linha_rotulo - 1, max(0, linha_rotulo - 5), -1):
        txt = _norm(aba.texto(lin, 1))
        valor = _limpar(aba.texto(lin, 1)).split(":", 1)[-1].strip()
        if txt.startswith("grupo:"):
            grupo = valor
        elif txt.startswith("quadro:"):
            quadro = valor
    return grupo, quadro


def _inicios_blocos(aba: Aba) -> List[int]:
    return [lin for lin in range(1, aba.max_lin + 1) if _abre_bloco(_norm(aba.texto(lin, 1)))]


def _primeira_linha_com_valor(aba: Aba, inicio: int, fim: int, max_col: int) -> Optional[int]:
    for lin in range(inicio, fim + 1):
        if any(isinstance(aba.valor(lin, c), (int, float)) for c in range(2, max_col + 1)):
            return lin
    return None


def _colunas_do_cabecalho(aba: Aba, ini: int, fim: int, cols: List[int]) -> List[Coluna]:
    colunas: List[Coluna] = []
    for c in cols:
        partes: List[str] = []
        for lin in range(ini, fim + 1):
            t = _limpar(aba.texto(lin, c))
            if t and t not in partes:
                partes.append(t)
        titulo = partes[-1] if partes else f"Coluna {c}"
        superior = " / ".join(partes[:-1]) if len(partes) > 1 else ""
        marc = ""
        for p in reversed(partes):
            m = MARCADOR.search(p.lower())
            if m:
                marc = m.group(1)
                break
        tipo = "percentual" if "%" in " ".join(partes) else "moeda"
        colunas.append(Coluna(chave=f"c{c}", titulo=titulo, superior=superior,
                              marcador=marc, tipo=tipo))
    return colunas


def _nivel_rotulo(rotulo_bruto: str) -> int:
    """Indentacao em pares de espacos: 2->1, 4->2, 6->3, 8->4 ..."""
    bruto = len(rotulo_bruto) - len(rotulo_bruto.lstrip(" "))
    return min(bruto // 2, 6)


def _eh_total(rotulo: str) -> bool:
    t = _norm(rotulo)
    if re.search(r"\((i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s*$", t):
        return True
    return t.rstrip().endswith("total")


def _ler_bloco(aba: Aba, linha_rotulo: int, fim: int, max_col: int) -> Optional[Bloco]:
    grupo, quadro = _contexto_bloco(aba, linha_rotulo)
    primeira = _primeira_linha_com_valor(aba, linha_rotulo + 1, fim, max_col)
    if primeira is None:
        return None

    cab_ini, cab_fim = linha_rotulo + 1, primeira - 1

    cols_valor: List[int] = []
    for c in range(2, max_col + 1):
        if any(isinstance(aba.valor(lin, c), (int, float)) for lin in range(primeira, fim + 1)):
            cols_valor.append(c)
    if not cols_valor:
        return None

    colunas = _colunas_do_cabecalho(aba, cab_ini, cab_fim, cols_valor)
    por_col = {c: col.chave for c, col in zip(cols_valor, colunas)}

    titulo_tabela = ""
    if cab_ini <= cab_fim:
        titulo_tabela = _limpar(aba.texto(cab_ini, 1)) or _limpar(aba.texto(cab_ini, 2))

    linhas: List[Linha] = []
    ultimo_nivel = 0
    for lin in range(primeira, fim + 1):
        valor_bruto = aba.valor(lin, 1)
        bruto = "" if valor_bruto is None else str(valor_bruto)
        rotulo = _limpar(bruto)
        nivel = _nivel_rotulo(RE_CTRL.sub("", bruto))
        if rotulo:
            ultimo_nivel = nivel
        else:
            nivel = ultimo_nivel
        valores: Dict[str, Optional[float]] = {}
        tem = False
        for c, chave in por_col.items():
            v = _num(aba.valor(lin, c))
            valores[chave] = v
            tem = tem or (v is not None)
        if not rotulo and not tem:
            continue
        linhas.append(Linha(
            rotulo=rotulo,
            valores=valores,
            nivel=nivel,
            negrito=_eh_total(rotulo),
            total=_eh_total(rotulo),
            linha_origem=lin,
        ))

    if not linhas:
        return None
    return Bloco(grupo=grupo, quadro=quadro, titulo_tabela=titulo_tabela,
                 colunas=colunas, linhas=linhas)


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
def ler_rascunho(caminho: str) -> Documento:
    wb = ler_xls(caminho)
    doc: Optional[Documento] = None

    for nome_aba in wb.nomes:
        m = RE_ABA.match(nome_aba.strip())
        if not m:
            continue
        tipo, numero = m.group(1).upper(), int(m.group(2))
        aba = wb.abas[nome_aba]
        ente, periodo, versao, vigencia = _ler_metadados(aba)

        if doc is None:
            doc = Documento(tipo=tipo, ente=ente, periodo=periodo,
                            versao_layout=versao, vigencia_layout=vigencia,
                            arquivo_origem=os.path.basename(caminho))
        elif periodo and not doc.periodo:
            doc.periodo = periodo

        inicios = _inicios_blocos(aba)
        blocos: List[Bloco] = []
        for i, ini in enumerate(inicios):
            fim = (inicios[i + 1] - 1) if i + 1 < len(inicios) else aba.max_lin
            b = _ler_bloco(aba, ini, fim, aba.max_col)
            if b:
                blocos.append(b)
        doc.anexos.append(Anexo(documento=tipo, numero=numero, blocos=blocos))

    if doc is None:
        raise ValueError(f"nenhum anexo RREO/RGF reconhecido em {caminho}")

    # anexos que o Siconfi exporta sem rotulos recebem o catalogo minerado
    try:
        import catalogo
        catalogo.aplicar_em(doc.anexos)
    except Exception:
        pass
    return doc


def ler_pasta(pasta: str) -> List[Documento]:
    docs: List[Documento] = []
    for nome in sorted(os.listdir(pasta)):
        if not nome.lower().endswith((".xls", ".xlsx")):
            continue
        caminho = os.path.join(pasta, nome)
        try:
            docs.append(ler_rascunho(caminho))
        except Exception:
            continue
    return docs




