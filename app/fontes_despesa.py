# -*- coding: utf-8 -*-
"""Consolida as séries mensais de despesa a partir dos Comparativos mensais.

Entrada: os 12 arquivos
    "Comparativo Despesa Autorizada Empenhada Liquidada e Paga_<MÊS>.xls"
Cada um traz, por linha: Natureza da Despesa | Fonte Recurso | Especificação |
Empenhada no Mês | Liquidada no Mês | Paga no Mês.

Regras aprendidas na análise (todas verificadas nos arquivos):

1. Os valores são DO MÊS (não acumulados) — confirmado pela série de folha.
2. A MESMA natureza aparece uma vez por FONTE DE RECURSO.
3. A fonte "1.0" é o TOTAL da natureza e é exatamente igual à soma das demais
   fontes. Somar tudo (como numa tabela comum) duplica o valor. Regra: se a
   linha "1.0" existe no mês, ela é o valor; senão somam-se as fontes.
   (Este foi o erro que inflava os totais em 2x.)
4. Natureza "XX.XX.XX.00" é o total do elemento; as "XX.XX.XX.NN" são
   desdobramentos e NÃO devem ser somadas junto.
5. Algumas linhas têm a classificação ilegível (caracteres de controle) e são
   isoladas em vez de somadas a um elemento errado.
"""
from __future__ import annotations

import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from leitor_xls import ler_xls

MESES = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
         "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

RE_NAT = re.compile(r"\d{2}\.\d{2}\.\d{2}\.\d{2}")
RE_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

COL_EMPENHADA, COL_LIQUIDADA, COL_PAGA = 4, 5, 6
FONTE_TOTAL = "1.0"


@dataclass
class SerieMensal:
    """Valores de uma natureza (ou elemento) ao longo dos 12 meses."""
    liquidada: List[Optional[float]] = field(default_factory=lambda: [None] * 12)
    empenhada: List[Optional[float]] = field(default_factory=lambda: [None] * 12)
    paga: List[Optional[float]] = field(default_factory=lambda: [None] * 12)
    por_fonte: Dict[str, float] = field(default_factory=dict)
    por_fonte_mensal: Dict[str, List[float]] = field(default_factory=dict)

    def total(self, campo: str = "liquidada") -> float:
        return sum(v for v in getattr(self, campo) if v is not None)

    def somar(self, outra: "SerieMensal") -> None:
        for campo in ("liquidada", "empenhada", "paga"):
            destino = getattr(self, campo)
            origem = getattr(outra, campo)
            for i in range(12):
                if origem[i] is None:
                    continue
                destino[i] = (destino[i] or 0.0) + origem[i]
        for k, v in outra.por_fonte.items():
            self.por_fonte[k] = self.por_fonte.get(k, 0.0) + v
        for k, serie in outra.por_fonte_mensal.items():
            destino_f = self.por_fonte_mensal.setdefault(k, [0.0] * 12)
            for i in range(12):
                destino_f[i] += serie[i]


@dataclass
class Resultado:
    por_natureza: Dict[str, SerieMensal]
    ilegiveis: List[dict]
    arquivos_lidos: List[str]
    meses_ausentes: List[str]

    def elemento(self, prefixo: str) -> SerieMensal:
        """Soma o elemento (XX.XX.XX) usando a linha .00 quando existir."""
        chave00 = f"{prefixo}.00"
        if chave00 in self.por_natureza:
            return self.por_natureza[chave00]
        saida = SerieMensal()
        for nat, s in self.por_natureza.items():
            if nat.startswith(prefixo + "."):
                saida.somar(s)
        return saida

    def grupo(self, prefixo: str) -> SerieMensal:
        """Soma o grupo (XX.XX) usando a linha XX.XX.00.00 quando existir."""
        chave = f"{prefixo}.00.00"
        if chave in self.por_natureza:
            return self.por_natureza[chave]
        saida = SerieMensal()
        for nat, s in self.por_natureza.items():
            if nat.startswith(prefixo + ".") and nat.endswith(".00"):
                saida.somar(s)
        return saida

    def somar_naturezas(self, naturezas: List[str]) -> SerieMensal:
        saida = SerieMensal()
        for nat in naturezas:
            s = self.por_natureza.get(nat)
            if s:
                saida.somar(s)
        return saida


def ler_comparativos(pasta: str) -> Resultado:
    bruto: Dict[tuple, Dict[str, List[float]]] = defaultdict(
        lambda: defaultdict(lambda: [0.0, 0.0, 0.0]))
    ilegiveis: List[dict] = []
    lidos: List[str] = []
    ausentes: List[str] = []

    for i, mes in enumerate(MESES):
        caminho = os.path.join(pasta, f"Comparativo Despesa Autorizada Empenhada Liquidada e Paga_{mes}.xls")
        if not os.path.exists(caminho):
            ausentes.append(mes)
            continue
        wb = ler_xls(caminho)
        aba = wb.abas[wb.nomes[0]]
        lidos.append(mes)

        for lin in range(2, aba.max_lin + 1):
            bruto_nat = aba.valor(lin, 1)
            if bruto_nat is None:
                continue
            texto = str(bruto_nat)
            emp = aba.valor(lin, COL_EMPENHADA)
            liq = aba.valor(lin, COL_LIQUIDADA)
            pag = aba.valor(lin, COL_PAGA)
            if not any(isinstance(v, (int, float)) for v in (emp, liq, pag)):
                continue

            if RE_CTRL.search(texto) or len(RE_NAT.findall(texto)) > 1:
                ilegiveis.append(dict(mes=mes, linha=lin, fonte=aba.texto(lin, 2),
                                      empenhada=emp, liquidada=liq, paga=pag,
                                      texto=RE_CTRL.sub(" ", texto)[:80]))
                continue

            m = RE_NAT.search(texto)
            if not m:
                continue
            nat = m.group(0)
            fonte = aba.texto(lin, 2) or "(sem fonte)"
            acumulado = bruto[(nat, i)][fonte]
            for k, valor in enumerate((liq, emp, pag)):
                if isinstance(valor, (int, float)) and not isinstance(valor, bool):
                    acumulado[k] += float(valor)

    por_natureza: Dict[str, SerieMensal] = {}
    campo_idx = (("liquidada", 0), ("empenhada", 1), ("paga", 2))
    for (nat, i), fontes in bruto.items():
        s = por_natureza.setdefault(nat, SerieMensal())
        if FONTE_TOTAL in fontes:
            usado = {FONTE_TOTAL: fontes[FONTE_TOTAL]}
        else:
            usado = fontes
        for _nome, valores in usado.items():
            for campo, k in campo_idx:
                atual = getattr(s, campo)[i] or 0.0
                getattr(s, campo)[i] = atual + valores[k]
        for nome_fonte, valores in fontes.items():
            if nome_fonte == FONTE_TOTAL:
                continue
            s.por_fonte[nome_fonte] = s.por_fonte.get(nome_fonte, 0.0) + valores[0]
            lista = s.por_fonte_mensal.setdefault(nome_fonte, [0.0] * 12)
            lista[i] += valores[0]

    return Resultado(por_natureza=por_natureza, ilegiveis=ilegiveis,
                     arquivos_lidos=lidos, meses_ausentes=ausentes)


# ---------------------------------------------------------------------------
# mapa MDF 14a edicao - RGF Anexo 1 (Despesa com Pessoal)
# ---------------------------------------------------------------------------
MAPA_MDF = [
    ("Pessoal Ativo", None, []),
    ("Vencimentos, Vantagens e Outros", "31.90.04 + .07 + .11 + .12 + .16 + .17",
     ["31.90.04", "31.90.07", "31.90.11", "31.90.12", "31.90.16", "31.90.17"]),
    ("Obrigações Patronais", "31.90.13 + 31.91.13", ["31.90.13", "31.91.13"]),
    ("Pessoal Inativo e Pensionistas", None, []),
    ("Aposentadorias, Reserva e Reformas", "31.90.01", ["31.90.01"]),
    ("Pensões", "31.90.03", ["31.90.03"]),
    ("Outras Despesas de Pessoal decorrentes de Contratos de Terceirização", "31.90.34", ["31.90.34"]),
    ("Despesa com Pessoal não Executada Orçamentariamente", None, []),
    ("DESPESAS NÃO COMPUTADAS (II)", None, []),
    ("Indenizações por Demissão e Incentivos à Demissão Voluntária", "31.90.14", ["31.90.14"]),
    ("Decorrentes de Decisão Judicial", "31.90.91", ["31.90.91"]),
    ("Despesas de Exercícios Anteriores", "31.90.92", ["31.90.92"]),
    ("Inativos e Pensionistas com Recursos Vinculados", None, []),
    ("Agentes Comunitários de Saúde e de Combate a Endemias", None, []),
    ("Parcela dedutível do RPPS", None, []),
]


def quadro1(res: Resultado) -> List[dict]:
    linhas: List[dict] = []
    for rotulo, chave, elementos in MAPA_MDF:
        if not elementos:
            linhas.append(dict(rotulo=rotulo, serie=SerieMensal(), pendente=True,
                               detalhe=chave or ""))
            continue
        serie = SerieMensal()
        encontrados = []
        for el in elementos:
            s = res.elemento(el)
            if s.total() != 0:
                encontrados.append(el)
            serie.somar(s)
        linhas.append(dict(rotulo=rotulo, serie=serie, pendente=False,
                           detalhe=", ".join(encontrados) or "sem movimento"))
    return linhas


def totais(linhas: List[dict]) -> dict:
    bruta = sum(l["serie"].total() for l in linhas[:7] if not l["pendente"])
    deducao = sum(l["serie"].total() for l in linhas[8:] if not l["pendente"])
    return dict(bruta=bruta, deducao=deducao, liquida=bruta - deducao)


# ---------------------------------------------------------------------------
# classificacao por subelemento (91, 92, 94) - linhas do Anexo 1
# ---------------------------------------------------------------------------
# cada chave e um prefixo de natureza; o valor e a linha do demonstrativo
SUBELEMENTO_LINHA = {
    # Despesas de Exercicios Anteriores (92)
    "31.90.92.01": "aposentadorias",
    "31.91.92.01": "aposentadorias",
    "31.90.92.03": "pensoes",
    "31.91.92.03": "pensoes",
    "31.90.92.13": "patronal",
    "31.91.92.13": "patronal",
    "31.90.92.91": "judiciais",
    "31.91.92.91": "judiciais",
    "31.90.92.93": "judiciais",
    "31.90.92.94": "judiciais",
    "31.90.92.96": "judiciais",
    "31.90.92.99": "judiciais",
    # Sentencas judiciais (91)
    "31.90.91.40": "judiciais",
    "31.90.91.41": "judiciais",
    "31.91.91.40": "judiciais",
    "31.91.91.41": "judiciais",
    "31.90.91.10": "pensoes",
    "31.90.91.13": "pensoes",
    "31.90.91.12": "aposentadorias",
    "31.90.91.15": "aposentadorias",
    "31.90.91.20": "judiciais",
    "31.90.91.25": "judiciais",
    "31.90.91.99": "judiciais",
    # Indenizacoes e restituicoes (94)
    "31.90.94.07": "indenizacoes",
    "31.90.94.03": "aposentadorias",
    "31.90.94.04": "aposentadorias",
    "31.90.94.13": "pensoes",
    "31.90.94.93": "indenizacoes",
    "31.90.94.99": "indenizacoes",
}


def natureza_linha(nat: str) -> str:
    """Classifica uma natureza (subelemento) na linha do Anexo 1."""
    if nat in SUBELEMENTO_LINHA:
        return SUBELEMENTO_LINHA[nat]
    elem = nat[:8]
    if elem in ("31.90.91", "31.91.91"):
        return "vencimentos"      # demais sentencas = pessoal ativo
    if elem in ("31.90.92", "31.91.92"):
        return "vencimentos"      # demais DEA = pessoal ativo
    if elem in ("31.90.93", "31.90.94", "31.90.95", "31.90.96"):
        return "vencimentos"
    if elem == "31.90.01":
        return "aposentadorias"
    if elem == "31.90.03":
        return "pensoes"
    if elem in ("31.90.13", "31.91.13"):
        return "patronal"
    if elem in ("31.90.07", "31.91.07"):
        return "vencimentos"      # contrib. a entidade fechada de previdencia
    if elem in ("31.90.04", "31.90.11", "31.90.12", "31.90.16", "31.90.17"):
        return "vencimentos"
    return "vencimentos"


def somar_por_linha(res: "Resultado") -> Dict[str, SerieMensal]:
    """Soma as naturezas ja classificadas por linha do Anexo 1."""
    linhas: Dict[str, SerieMensal] = {k: SerieMensal() for k in
                                      ("vencimentos", "patronal", "aposentadorias", "pensoes",
                                       "judiciais", "indenizacoes")}
    # agrupa por elemento (31.90.XX); usa os subelementos quando existirem,
    # senao o proprio elemento (.00) - sem duplicar
    elementos = {}
    for nat in res.por_natureza:
        if not nat.startswith("31.") or nat.count(".") != 3:
            continue
        if nat in ("31.00.00.00", "31.90.00.00", "31.91.00.00"):
            continue
        elementos.setdefault(nat[:8], {})[nat] = res.por_natureza[nat]

    for elemento, naturezas in elementos.items():
        subelementos = {n: s for n, s in naturezas.items() if not n.endswith(".00")}
        if subelementos:
            for nat, serie in subelementos.items():
                linhas[natureza_linha(nat)].somar(serie)
        else:
            for nat, serie in naturezas.items():
                linhas[natureza_linha(nat)].somar(serie)
    return linhas
