# -*- coding: utf-8 -*-
"""RREO Anexo 4 (Previdência Social) apurado na Matriz de Saldos Contábeis.

O Anexo 4 não usa o par exceto-intra / intra do resto do RREO: o demonstrativo
é dividido pela **fonte de recursos** do RPPS, e cada bloco tem receita,
despesa e resultado próprios:

    bloco  fonte  seções    conteúdo
    ------ -----  --------  --------------------------------------------------
    1800   1800   I a VI    Fundo em Capitalização (plano previdenciário)
    1801   1801   VII a XI   Fundo em Repartição (plano financeiro)
    1802   1802   XII a XVI  Administração do RPPS
    1803   1803   XX a XXII  Inativos e pensionistas militares
    1804   1804   XVII a XIX Benefícios mantidos pelo Tesouro (só no molde do RN)

O identificador usado na chave é o ``cod_conta`` do CSV publicado — e não o
rótulo, que se repete dentro do mesmo bloco ("Ativo" aparece para segurados e
para patronal; "Caixa e Equivalentes de Caixa" aparece nos três fundos) e não
serve de chave de dicionário.

    from rreo_anexo4_completo import celulas
    cel = celulas(r"...\\dados\\rr_msc", 2026, 4)
    cel[("TotalDasDespesasRPPSPrevidenciario",
         "DESPESAS EMPENHADAS ATÉ O BIMESTRE (d)", 1800)]

O que sai da matriz (e o que não sai)
-------------------------------------
Receita: conta 6.2.1.2 (6212) em ``period_change`` do exercício. A previsão
atualizada é a conta 5.2.1.1 (5211) em ``ending_balance`` — usar 6211+6212
acerta o total do bloco mas erra linha a linha (o 6211 traz ajustes que só
fazem sentido agregados).

Despesa — as três colunas de execução saem das contas 6.2.2.1.3 na matriz:

    empenhado = movimento líquido de **todas** as 62213*
    liquidado = 622130300 + 622130400 + 622130700
    pago      = 622130400

e a dotação, da conta 5.2.2.1 (5221) em ``ending_balance``. A conta 5222 é
espelho da 5221 e não entra (dobraria a dotação).

Duas regras de seleção que a validação contra o publicado de RR (2026 B4)
obrigou:

1. ``nd 3.3.91.39`` fica fora do anexo. Em RR são R$ 20,1 mi de dotação no
   Fundo em Capitalização que, somados, estouram o bloco.
2. Os benefícios do plano financeiro pagos **direto pelo Tesouro** (fonte
   1500, nd 3.1.90.01/03) entram no Fundo em Repartição. Sem eles o bloco
   fecha R$ 4.342.505,99 abaixo do publicado (empenhado) e R$ 5.402.707,00
   abaixo na dotação; com eles fecha ao centavo nas quatro colunas.

A reserva orçamentária do RPPS não é uma linha de despesa: é o `nd 99` da
dotação somado nas quatro fontes, e sai na coluna "PREVISÃO ORÇAMENTÁRIA"
(R$ 171.900.837,00 em RR 2026 B4, igual ao publicado).

Linhas que não saem da matriz
-----------------------------
* os saldos patrimoniais (Caixa, Investimentos, Outros Bens e Direitos) — a
  MSC não atribui a fonte de recursos a esses saldos (classe 1 sem fr);
* os APORTES do molde do RN e o PAE informado pelo INEC;
* o bloco 1804 (Benefícios mantidos pelo Tesouro), que só existe no molde do
  RN e não tem fonte 1804 na matriz de RR.

Para essas, e para as linhas zeradas que o Siconfi imprime, aceite
``publicado=`` — um dict ``{(cod_conta, coluna): valor}`` (ou o caminho do CSV
publicado) que preenche as linhas replicáveis.

A Compensação Financeira entre os Regimes (despesa) sai **só** na dotação,
onde a matriz a identifica (nd 3.1.90.86: R$ 500.000,00 no Fundo em
Capitalização e R$ 480.000,00 no de Repartição, exatamente como no publicado).
Na execução ela não é identificável — o nd não tem empenho — e por isso não é
emitida; o valor correspondente fica em "Demais Despesas Previdenciárias",
que é o que o publicado mostra.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

RAIZ = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.join(RAIZ, "app")
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from acervo import Acervo  # noqa: E402

# ---------------------------------------------------------------- colunas
P_ATU = "PREVISÃO ATUALIZADA (a)"
R_REAL = "RECEITAS REALIZADAS ATÉ O BIMESTRE (b)"
D_ATU = "DOTAÇÃO ATUALIZADA (c)"
E_ATE = "DESPESAS EMPENHADAS ATÉ O BIMESTRE (d)"
L_ATE = "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (e)"
P_ATE = "DESPESAS PAGAS ATÉ O BIMESTRE (f)"
P_ORC = "PREVISÃO ORÇAMENTÁRIA"
SALDO = "SALDO ATUAL"

COLUNAS_RECEITA = (P_ATU, R_REAL)
COLUNAS_DESPESA = (D_ATU, E_ATE, L_ATE, P_ATE)

# ---------------------------------------------------------------- MSC
CONTA_PAGA = "622130400"
CONTAS_LIQUIDACAO = ("622130300", "622130400", "622130700")
CONTA_PREVISAO = "5211"          # 5.2.1.1 — previsão atualizada da receita
CONTA_DOTACAO = "5221"           # 5.2.2.1 — dotação atualizada da despesa
CONTA_RECEITA = "6212"           # 6.2.1.2 — receita realizada
CONTA_DESPESA = "62213"          # 6.2.2.1.3 — execução da despesa

#: naturezas de despesa de benefícios (3.1.90.01/91/92 e 3.1.90.03)
ND_APOSENTADORIAS = frozenset({"319001", "319091", "319092"})
ND_PENSOES = frozenset({"319003"})
ND_COMPENSACAO = frozenset({"319086"})
#: benefícios do plano financeiro que o Tesouro paga direto (fonte 1500):
#: só 3.1.90.01 e 3.1.90.03 — o 3.1.90.91/92 dessas mesmas fontes é despesa
#: do Tesouro (aposentadorias do RGPS), não do fundo.
ND_TESOURO = frozenset({"319001", "319003"})
#: fora do anexo: reserva orçamentária (99) e 3.3.91.39
ND_RESERVA = "99"
ND_EXCLUIDAS = frozenset({"339139"})
#: em 1802 (administração) estas naturezas não são "Pessoal e Encargos"
ND_NAO_PESSOAL = frozenset({"319091", "319092", "319094"})

#: fontes de recursos que são os fundos do RPPS
FONTES = ("1800", "1801", "1802", "1803")
#: fontes que podem ser replicadas do publicado quando a matriz não as tem
FONTES_PUBLICADO = ("1804",)

#: fonte de recursos do Tesouro — cobre os benefícios do plano financeiro
FONTE_TESOURO = "1500"

TESOURO_NO_REPARTICAO = True
"""Os benefícios do plano financeiro pagos pelo Tesouro (fonte 1500, nd
3.1.90.01/03) entram no bloco 1801. Calibrado contra o RREO de RR 2026 B4."""

# ---------------------------------------------------------------- linhas
#: (cod_conta, bloco, chave) — receita. A chave é resolvida em `_receita`.
RECEITA: Tuple[Tuple[str, int, str], ...] = (
    ("ReceitasCorrentesRPPSBrutasPrevidenciario", 1800, "correntes"),
    ("ReceitaDeContribuicoesDosSeguradosBrutaPrevidenciario", 1800, "seg"),
    ("ReceitaDeContribuicoesDosSeguradoslAtivoPrevidenciario", 1800, "seg_ativo"),
    ("ReceitaDeContribuicoesDosSeguradosInativoPrevidenciario", 1800, "seg_inativo"),
    ("ReceitaDeContribuicoesDosSeguradosPensionistaPrevidenciario", 1800, "seg_pensionista"),
    ("ReceitaDeContribuicoesPatronalPrevidenciario", 1800, "pat"),
    ("ReceitaDeContribuicoesPatronalAtivoPrevidenciario", 1800, "pat_ativo"),
    ("ReceitaDeContribuicoesPatronalInativoPrevidenciario", 1800, "pat_inativo"),
    ("ReceitaDeContribuicoesPatronalPensionistaPrevidenciario", 1800, "pat_pensionista"),
    ("ReceitaPatrimonialRPPSBrutaPrevidenciario", 1800, "patrimonial"),
    ("ReceitasDeValoresMobiliariosPrevidenciariasBrutasPrevidenciario", 1800, "patrimonial"),
    ("ReceitasDeCapitalRPPSBrutasPrevidenciario", 1800, "capital"),
    ("AmortizacaoDeEmprestimosPrevidenciariaBrutaPrevidenciario", 1800, "amortizacao"),
    ("OutrasReceitasCorrentesRPPSBrutasPrevidenciario", 1800, "outras"),
    ("ReceitasCompensacaoFinanceiraEntreOsRegimes", 1800, "compensacao"),
    ("DemaisReceitasCorrentesRPPSBrutasPrevidenciario", 1800, "demais"),
    ("TotalReceitasRPPSPrevidenciario", 1800, "total"),

    ("ReceitasCorrentesRPPSBrutasFinanceiro", 1801, "correntes"),
    ("ReceitaDeContribuicoesDosSeguradosBrutaFinanceiro", 1801, "seg"),
    ("ReceitaDeContribuicoesDosSeguradosAtivoFinanceiro", 1801, "seg_ativo"),
    ("ReceitaDeContribuicoesDosSeguradosInativoFinanceiro", 1801, "seg_inativo"),
    ("ReceitaDeContribuicoesDosSeguradosPensionistaFinanceiro", 1801, "seg_pensionista"),
    ("ReceitaDeContribuicoesPatronalFinanceiro", 1801, "pat"),
    ("ReceitaDeContribuicoesPatronalAtivoFinanceiro", 1801, "pat_ativo"),
    ("ReceitaDeContribuicoesPatronalInativoFinanceiro", 1801, "pat_inativo"),
    ("ReceitaDeContribuicoesPatronalPensionistaFinanceiro", 1801, "pat_pensionista"),
    ("ReceitaPatrimonialRPPSBrutaFinanceiro", 1801, "patrimonial"),
    ("ReceitasDeValoresMobiliariosPrevidenciariasBrutasFinanceiro", 1801, "patrimonial"),
    ("OutrasReceitasCorrentesRPPSBrutasFinanceiro", 1801, "outras"),
    ("ReceitasCompensacaoFinanceiraEntreOsRegimesFundoEmReparticao", 1801, "compensacao"),
    ("DemaisReceitasCorrentesRPPSBrutasFinanceiro", 1801, "demais"),
    ("TotalReceitasRPPSFinanceiro", 1801, "total"),

    ("ReceitasCorrentesDaAdministracaoRPPS", 1802, "total"),
    ("TotalDasReceitasDaAdministracaoRPPS", 1802, "total"),

    ("ContribuicaoSobreARemuneracaoDosMilitaresAtivos", 1803, "mil_ativo"),
    ("ContribuicaoSobreARemuneracaoDosMilitaresInativos", 1803, "mil_inativo"),
    ("ContribuicaoSobreARemuneracaoDosPensionistas", 1803, "mil_pensionista"),
    ("OutrasContribuicoesMilitares", 1803, "mil_outras"),
    ("TotalDasContribucoesDosMilirares", 1803, "total"),
)

#: (cod_conta, bloco, chave) — despesa. A chave é resolvida em `_despesa`.
DESPESA: Tuple[Tuple[str, int, str], ...] = (
    ("DespesasPrevidenciariasExcetoIntraOrcamentariasBeneficiosPrevidenciario", 1800, "benef"),
    ("DespesasPrevidenciariasExcetoIntraOrcamentariasAposentadoriasPrevidenciario", 1800, "apos"),
    ("DespesasExcetoIntraOrcamentariasPessoalCivilPensoesRPPSPrevidenciario", 1800, "pens"),
    ("DespesasExcetoIntraOrcamentariasOutrasDepesasRPPSPrevidenciario", 1800, "outras"),
    ("DespesasCompensacaoFinanceiraEntreOsRegimes", 1800, "comp_dotacao"),
    ("DespesasExcetoIntraOrcamentariasDemaisDespesasRPPSPrevidenciario", 1800, "demais"),
    ("TotalDasDespesasRPPSPrevidenciario", 1800, "total"),
    ("RREO4ResultadoRPPSPrevidenciario", 1800, "resultado"),

    ("DespesasPrevidenciariasExcetoIntraOrcamentariasBeneficiosFinanceiro", 1801, "benef"),
    ("DespesasPrevidenciariasExcetoIntraOrcamentariasAposentadoriasFinanceiro", 1801, "apos"),
    ("DespesasExcetoIntraOrcamentariasPessoalCivilPensoesRPPSFinanceiro", 1801, "pens"),
    ("DespesasExcetoIntraOrcamentariasOutrasDepesasRPPSFinanceiro", 1801, "outras"),
    ("DespesasCompensacaoFinanceiraEntreOsRegimesFundoEmReparticao", 1801, "comp_dotacao"),
    ("DespesasExcetoIntraOrcamentariasDemaisDespesasRPPSFinanceiro", 1801, "demais"),
    ("TotalDasDespesasRPPSFinanceiro", 1801, "total"),
    ("RREO4ResultadoRPPSFinanceiro", 1801, "resultado"),

    ("DespesasCorrentesDaAdministracaoRPPS", 1802, "correntes"),
    ("PessoalEEncargosSociaisDaAdministracaoRPPS", 1802, "pessoal"),
    ("DemaisDespesasCorrentesDaAdministracaoRPPS", 1802, "demais"),
    ("DespesasDeCapitalDaAdministracaoRPPS", 1802, "capital"),
    ("TotalDasDespesasDaAdministracaoRPPS", 1802, "total"),
    ("ResultadoDaAdministracaoRPPS", 1802, "resultado"),

    ("DespesasMilitaresInatividade", 1803, "apos"),
    ("DespesasMilitaresPensoes", 1803, "pens"),
    ("DespesasMilitaresOutrasDespesas", 1803, "outras"),
    ("TotalDasDespesasComInativosEPensionistasMilirares", 1803, "total"),
    ("ResultadoAssociadoAInativosEPensionistasMilirares", 1803, "resultado"),
)

#: linhas que não saem da matriz: (cod_conta, bloco, coluna)
REPLICAVEIS: Tuple[Tuple[str, int, str], ...] = (
    ("RREO4CaixaDoRPPSPrevidenciario", 1800, SALDO),
    ("InvestimentosDoRPPSPrevidenciario", 1800, SALDO),
    ("OutrosBensEDireitosDoRPPSPrevidenciario", 1800, SALDO),
    ("CaixaEEquivalenteDeCaixaFundoEmReparticao", 1801, SALDO),
    ("InvestimentosEAplicacoesFundoEmReparticao", 1801, SALDO),
    ("OutrosBensEDireitosFundoEmReparticao", 1801, SALDO),
    ("CaixaEEquivalenteDeCaixaAdministracaoDoRPPS", 1802, SALDO),
    ("InvestimentosEAplicacoesAdministracaoDoRPPS", 1802, SALDO),
    ("ReservaOrcamentariaDoRPPSPrevidenciario", 0, P_ORC),
    # molde do RN (bloco 1804 e aportes)
    ("ContribuicoesDosServidoresBeneficiosMantidosPeloTesouro", 1804, P_ATU),
    ("ContribuicoesDosServidoresBeneficiosMantidosPeloTesouro", 1804, R_REAL),
    ("DemaisReceitasPrevidenciariasBeneficiosMantidosPeloTesouro", 1804, P_ATU),
    ("DemaisReceitasPrevidenciariasBeneficiosMantidosPeloTesouro", 1804, R_REAL),
    ("TotalDasReceitasBeneficiosMantidosPeloTesouro", 1804, P_ATU),
    ("TotalDasReceitasBeneficiosMantidosPeloTesouro", 1804, R_REAL),
    ("PensoesBeneficiosMantidosPeloTesouro", 1804, D_ATU),
    ("PensoesBeneficiosMantidosPeloTesouro", 1804, E_ATE),
    ("PensoesBeneficiosMantidosPeloTesouro", 1804, L_ATE),
    ("PensoesBeneficiosMantidosPeloTesouro", 1804, P_ATE),
    ("TotalDasDespesasBeneficiosMantidosPeloTesouro", 1804, D_ATU),
    ("TotalDasDespesasBeneficiosMantidosPeloTesouro", 1804, E_ATE),
    ("TotalDasDespesasBeneficiosMantidosPeloTesouro", 1804, L_ATE),
    ("TotalDasDespesasBeneficiosMantidosPeloTesouro", 1804, P_ATE),
    ("ResultadoDosBeneficiosMantidosPeloTesouro", 1804, D_ATU),
    ("ResultadoDosBeneficiosMantidosPeloTesouro", 1804, E_ATE),
    ("ResultadoDosBeneficiosMantidosPeloTesouro", 1804, L_ATE),
    ("ResultadoDosBeneficiosMantidosPeloTesouro", 1804, P_ATE),
    ("AportesParaAPrevidenciaPlanoPrevidenciarioDeficitFinanceiroPrevidenciario",
     1800, "APORTES REALIZADOS"),
)

#: rótulo de cada cod_conta (para aceitar `publicado` com chave = rótulo)
ROTULOS: Dict[str, str] = {
    "RREO4CaixaDoRPPSPrevidenciario": "Caixa e Equivalentes de Caixa",
    "InvestimentosDoRPPSPrevidenciario": "Investimentos e Aplicações",
    "OutrosBensEDireitosDoRPPSPrevidenciario": "Outros Bens e Direitos",
    "CaixaEEquivalenteDeCaixaFundoEmReparticao": "Caixa e Equivalentes de Caixa",
    "InvestimentosEAplicacoesFundoEmReparticao": "Investimentos e Aplicações",
    "OutrosBensEDireitosFundoEmReparticao": "Outros Bens e Direitos",
    "CaixaEEquivalenteDeCaixaAdministracaoDoRPPS": "Caixa e Equivalentes de Caixa",
    "InvestimentosEAplicacoesAdministracaoDoRPPS": "Investimentos e Aplicações",
    "ReservaOrcamentariaDoRPPSPrevidenciario": "VALOR",
}

_CHAVE = Tuple[str, str, int]


def _mapa_blocos() -> Dict[str, int]:
    mapa = {cod: bloco for cod, bloco, _chave in RECEITA + DESPESA}
    for cod, bloco, _coluna in REPLICAVEIS:
        mapa.setdefault(cod, bloco)
    return mapa


#: cod_conta -> bloco, para conferir um Anexo 4 publicado
BLOCO_DE = _mapa_blocos()


# ---------------------------------------------------------------- utilidades
def _ler(ac: Acervo, ano: int, mes: int, classe: int,
         tipo_valor: str) -> List:
    """Linhas de um arquivo da matriz; lista vazia se o arquivo não existe."""
    try:
        return list(ac.ler(ano, mes, classe=classe, tipo_valor=tipo_valor))
    except (FileNotFoundError, ValueError, KeyError):
        return []


def _grupo_nr(nr: str) -> Tuple[str, str]:
    """(grupo, vínculo) de uma natureza de receita do RPPS.

    A natureza tem 8 dígitos, ``1.2.1.5.xx.y.z`` nas contribuições do RPPS:

    * ``xx = 01`` segurados e ``03`` outras contribuições dos servidores;
    * ``xx = 02`` contribuição patronal dos ativos;
    * ``xx = 50`` contribuição patronal dos inativos (y=1) e pensionistas (y=2);
    * ``xx = 52/53/55/56`` contribuições dos militares, com y=1/4 ativo,
      y=2 inativo e y=3 pensionista.

    As naturezas intra-orçamentárias são as mesmas com o prefixo 7.
    """
    n = nr or ""
    if len(n) < 8:
        return "outras", ""
    if n[:4] in ("1215", "7215"):
        familia = n[4:6]
        if familia == "50":
            return "pat", {"1": "inativo", "2": "pensionista"}.get(n[6], "inativo")
        if familia == "02":
            return "pat", "ativo"
        if familia in ("01", "03"):
            vinculo = {"1": "ativo", "4": "ativo", "0": "ativo",
                       "2": "inativo", "3": "pensionista"}.get(n[6], "ativo")
            return "seg", vinculo
        if n[4] == "5":                                    # militares
            vinculo = {"1": "ativo", "4": "ativo",
                       "2": "inativo", "3": "pensionista"}.get(n[6], "ativo")
            return "mil", vinculo
        return "outras", ""
    if n.startswith("132"):
        return "patrimonial", ""
    if n.startswith("1999"):
        return "compensacao", ""
    return "outras", ""


def _fora(nd: str) -> bool:
    """Naturezas que o Anexo 4 não leva: reserva orçamentária e 3.3.91.39."""
    return nd[:2] == ND_RESERVA or nd[:6] in ND_EXCLUIDAS


def _recorte(fonte, fr: str, extras: Iterable[str] = (),
             so_nds: frozenset = frozenset()):
    """Somas de uma fonte restritas a um bloco (e às fontes extras do bloco)."""
    extras = tuple(extras)
    saida: Dict[str, float] = defaultdict(float)
    for (f, chave), valor in fonte.items():
        if f == fr:
            saida[chave] += valor
        elif f in extras and chave[:6] in so_nds:
            saida[chave] += valor
    return saida


# ---------------------------------------------------------------- apuração
def _receita(prev, real, fr: str) -> Dict[str, Dict[str, float]]:
    """{coluna: {chave: valor}} das linhas de receita do bloco."""
    saida: Dict[str, Dict[str, float]] = {}
    for coluna, fonte in ((P_ATU, prev), (R_REAL, real)):
        d: Dict[str, float] = defaultdict(float)
        for nr, valor in _recorte(fonte, fr).items():
            d["total"] += valor
            if nr[:1] in ("1", "7"):
                d["correntes"] += valor
            elif nr[:1] in ("2", "8"):
                d["capital"] += valor
            grupo, vinculo = _grupo_nr(nr)
            d[grupo] += valor
            if vinculo:
                d[f"{grupo}_{vinculo}"] += valor
        # "Outras" é o resíduo do bloco: o que não é contribuição nem
        # receita patrimonial. Assim nenhuma natureza nova fica de fora.
        d["outras"] = d["total"] - d["seg"] - d["pat"] - d["patrimonial"]
        d["demais"] = d["outras"] - d["compensacao"]
        d["amortizacao"] = sum(v for nr, v in _recorte(fonte, fr).items()
                               if nr[:2] in ("23", "83"))
        d["mil_outras"] = (d["total"] - d["mil_ativo"] - d["mil_inativo"]
                           - d["mil_pensionista"])
        saida[coluna] = d
    return saida


def _despesa_beneficios(fonte, fr: str,
                        extras: Iterable[str] = ()) -> Dict[str, float]:
    """{chave: valor} de um bloco de benefícios (1800, 1801, 1803)."""
    nds = _recorte(fonte, fr, extras, ND_TESOURO)
    d: Dict[str, float] = defaultdict(float)
    for nd, valor in nds.items():
        if _fora(nd):
            continue
        d["total"] += valor
        if nd[:6] in ND_APOSENTADORIAS:
            d["apos"] += valor
        elif nd[:6] in ND_PENSOES:
            d["pens"] += valor
        elif nd[:6] in ND_COMPENSACAO:
            d["compensacao"] += valor
    d["benef"] = d["apos"] + d["pens"]
    d["outras"] = d["total"] - d["benef"]
    # na execução a compensação não é identificável: o publicado mostra o
    # valor inteiro em "Demais Despesas Previdenciárias".
    d["demais"] = d["outras"] - d["compensacao"]
    return d


def _despesa_administracao(fonte, fr: str) -> Dict[str, float]:
    """{chave: valor} do bloco 1802 (Administração do RPPS)."""
    d: Dict[str, float] = defaultdict(float)
    for nd, valor in _recorte(fonte, fr).items():
        if _fora(nd):
            continue
        if nd[:2] == "31":
            if nd[:6] not in ND_NAO_PESSOAL:
                d["pessoal"] += valor
        elif nd[:2] in ("32", "33"):
            d["demais"] += valor
        elif nd[:1] == "4":
            d["capital"] += valor
    d["correntes"] = d["pessoal"] + d["demais"]
    d["total"] = d["correntes"] + d["capital"]
    return d


def ler_publicado(caminho: str) -> Dict[Tuple[str, str], float]:
    """{(cod_conta, coluna): valor} de um Anexo 4 publicado.

    Aceita o CSV do Siconfi (separador ';') e, na falta da coluna
    ``cod_conta``, cai para o rótulo (``conta``).
    """
    saida: Dict[Tuple[str, str], float] = {}
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        cabecalho = fh.readline()
        delim = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
        fh.seek(0)
        for r in csv.DictReader(fh, delimiter=delim):
            chave = (r.get("cod_conta") or r.get("conta") or "").strip()
            try:
                valor = float(r.get("valor") or 0.0)
            except ValueError:
                continue
            if chave:
                saida.setdefault((chave, (r.get("coluna") or "").strip()), valor)
    return saida


def _replicaveis(publicado: Dict[Tuple[str, str], float],
                 cel: Dict[_CHAVE, float]) -> int:
    """Sobrepõe as linhas que se replicam do publicado. Devolve quantas."""
    if not publicado:
        return 0
    por_rotulo = {rot: cod for cod, rot in ROTULOS.items()}
    cods = {cod for cod, _bloco, _col in REPLICAVEIS}
    n = 0
    for (cod, coluna), valor in publicado.items():
        if cod not in cods:
            cod = por_rotulo.get(cod, "")
        if not cod:
            continue
        alvo = [b for c, b, col in REPLICAVEIS if c == cod and col == coluna]
        if not alvo:
            continue
        cel[(cod, coluna, alvo[0])] = round(float(valor), 2)
        n += 1
    return n


def celulas(raiz: str, ano: int, bimestre: int, **kwargs) -> Dict[_CHAVE, float]:
    """{(cod_conta, coluna, bloco): valor} do Anexo 4 apurado na matriz.

    ``raiz``      pasta da MSC (a mesma dos outros módulos do repo)
    ``ano``       exercício
    ``bimestre``  1 a 6 (o RREO é cumulativo: 4 => janeiro a agosto)
    ``publicado`` opcional, ``{(cod_conta, coluna): valor}`` ou o caminho do
                  CSV publicado; preenche os saldos, a reserva e o bloco 1804.
    ``tesouro_no_reparticao`` força/desliga a fonte 1500 no bloco 1801.

    O ``bloco`` é o código da fonte de recursos (1800 a 1804); a reserva
    orçamentária, que não pertence a um fundo, sai com ``bloco=0``. Célula de
    valor zero não entra no dicionário — é o que o Siconfi faz no arquivo
    publicado (não imprime linha zerada).
    """
    publicado = kwargs.get("publicado")
    if isinstance(publicado, str):
        publicado = ler_publicado(publicado)
    tesouro = kwargs.get("tesouro_no_reparticao", TESOURO_NO_REPARTICAO)
    ac = Acervo(raiz)
    if not 1 <= bimestre <= 6:
        raise ValueError(f"bimestre deve estar entre 1 e 6: {bimestre}")
    mes_fim = 2 * bimestre
    faltando = [m for m in range(1, mes_fim + 1)
                if not ac.tem(ano, m, classe=6, tipo_valor="period_change")]
    if faltando:
        raise FileNotFoundError(
            f"MSC sem movimento (classe 6, period_change) em {ano}: faltam os "
            f"meses {faltando}. O RREO é cumulativo desde janeiro — apurar com "
            f"meses faltando daria valor menor que o devido. Raiz: {raiz}")
    if not ac.tem(ano, mes_fim, classe=5, tipo_valor="ending_balance"):
        raise FileNotFoundError(
            f"MSC sem dotação/previsão (classe 5, ending_balance) em "
            f"{ano}-{mes_fim:02d}: {raiz}")
    meses = list(range(1, mes_fim + 1))

    prev: Dict[Tuple[str, str], float] = defaultdict(float)
    real: Dict[Tuple[str, str], float] = defaultdict(float)
    dot: Dict[Tuple[str, str], float] = defaultdict(float)
    emp: Dict[Tuple[str, str], float] = defaultdict(float)
    liq: Dict[Tuple[str, str], float] = defaultdict(float)
    pag: Dict[Tuple[str, str], float] = defaultdict(float)

    for r in _ler(ac, ano, mes_fim, 5, "ending_balance"):
        if not r.fr:
            continue
        # 5211 = previsão da receita; 5221 = dotação da despesa (5222 é espelho)
        if r.conta.startswith(CONTA_PREVISAO) and r.nr:
            prev[(r.fr, r.nr)] += -r.liquido
        elif r.conta.startswith(CONTA_DOTACAO) and r.nd:
            dot[(r.fr, r.nd)] += -r.liquido

    for m in meses:
        for r in _ler(ac, ano, m, 6, "period_change"):
            if not r.fr:
                continue
            if r.conta.startswith(CONTA_RECEITA):
                if r.nr:
                    real[(r.fr, r.nr)] += r.liquido
                continue
            if not r.conta.startswith(CONTA_DESPESA):
                continue
            emp[(r.fr, r.nd)] += r.liquido
            if r.conta in CONTAS_LIQUIDACAO:
                liq[(r.fr, r.nd)] += r.liquido
            if r.conta == CONTA_PAGA:
                pag[(r.fr, r.nd)] += r.liquido

    cel: Dict[_CHAVE, float] = {}

    def put(conta: str, coluna: str, bloco: int, valor: float) -> None:
        """Grava a célula; valor zerado não entra (o Siconfi não imprime)."""
        arredondado = round(valor, 2)
        if abs(arredondado) >= 0.005:
            cel[(conta, coluna, bloco)] = arredondado

    # ---- receita
    receitas = {fr: _receita(prev, real, fr) for fr in FONTES}
    for fr in FONTES:
        bloco = int(fr)
        for conta, b, chave in RECEITA:
            if b != bloco:
                continue
            for coluna in COLUNAS_RECEITA:
                put(conta, coluna, bloco, receitas[fr][coluna].get(chave, 0.0))

    # ---- despesa
    # os benefícios do plano financeiro pagos pelo Tesouro não têm a fonte do
    # fundo na matriz; o publicado os leva no bloco 1801 (ver docstring).
    if tesouro is True:
        extras: Tuple[str, ...] = (FONTE_TESOURO,)
    elif not tesouro:
        extras = ()
    elif isinstance(tesouro, str):
        extras = (tesouro,)
    else:
        extras = tuple(tesouro)

    for fr in FONTES:
        bloco = int(fr)
        receita = receitas[fr]
        # a fonte do Tesouro só entra no Fundo em Repartição (1801)
        extras_bloco = extras if bloco == 1801 else ()
        if bloco == 1802:
            valores = {col: _despesa_administracao(fonte, fr)
                       for col, fonte in ((D_ATU, dot), (E_ATE, emp),
                                          (L_ATE, liq), (P_ATE, pag))}
        else:
            valores = {col: _despesa_beneficios(fonte, fr, extras_bloco)
                       for col, fonte in ((D_ATU, dot), (E_ATE, emp),
                                          (L_ATE, liq), (P_ATE, pag))}

        for conta, b, chave in DESPESA:
            if b != bloco:
                continue
            if chave == "resultado":
                for coluna in COLUNAS_DESPESA:
                    fonte_rec = P_ATU if coluna == D_ATU else R_REAL
                    put(conta, coluna, bloco,
                        receita[fonte_rec].get("total", 0.0)
                        - valores[coluna].get("total", 0.0))
                continue
            if chave == "comp_dotacao":
                # só a dotação identifica a compensação entre regimes
                put(conta, D_ATU, bloco, valores[D_ATU].get("compensacao", 0.0))
                continue
            for coluna in COLUNAS_DESPESA:
                put(conta, coluna, bloco, valores[coluna].get(chave, 0.0))

    # ---- reserva orçamentária (nd 99 de todas as fontes do RPPS)
    reserva = sum(v for (f, nd), v in dot.items()
                  if nd[:2] == ND_RESERVA and f in FONTES + FONTES_PUBLICADO)
    put("ReservaOrcamentariaDoRPPSPrevidenciario", P_ORC, 0, reserva)

    # ---- linhas replicadas do publicado
    _replicaveis(publicado or {}, cel)
    return cel


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="RREO Anexo 4 (Previdência) na MSC")
    ap.add_argument("--raiz", default=os.path.join(RAIZ, "dados", "rr_msc"))
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--bimestre", type=int, default=4)
    ap.add_argument("--publicado", default=None,
                    help="CSV do Anexo 4 publicado, para as linhas replicáveis")
    ap.add_argument("--conferir", action="store_true",
                    help="compara célula a célula com o publicado de --publicado")
    args = ap.parse_args()

    cel = celulas(args.raiz, args.ano, args.bimestre, publicado=args.publicado)
    print(f"{len(cel)} células apuradas em {args.raiz} ({args.ano} B{args.bimestre})")
    por_bloco: Dict[int, int] = defaultdict(int)
    for (_conta, _coluna, bloco) in cel:
        por_bloco[bloco] += 1
    for bloco in sorted(por_bloco):
        print(f"   bloco {bloco or '-':>4}: {por_bloco[bloco]:>3} células")
    total = sum(v for v in cel.values())
    print(f"   soma dos valores: {total:,.2f}")

    if args.conferir and args.publicado:
        oficial = ler_publicado(args.publicado)
        exatas = divergentes = ausentes = 0
        piores = []
        for (conta, coluna), valor in oficial.items():
            bloco = BLOCO_DE.get(conta)
            nosso = cel.get((conta, coluna, bloco)) if bloco is not None else None
            if nosso is None:
                ausentes += 1
            elif abs(nosso - valor) < 0.011:
                exatas += 1
            else:
                divergentes += 1
                piores.append((conta, coluna, nosso, valor))
        print(f"\npublicado: {len(oficial)} células | exatas {exatas} | "
              f"divergentes {divergentes} | não emitidas {ausentes}")
        replicadas = sum(1 for cod, _bloco, col in REPLICAVEIS
                         if (cod, col) in oficial)
        if replicadas:
            print(f"   ({replicadas} dessas células são linhas replicáveis — "
                  f"saldos patrimoniais, reserva, aportes — preenchidas pelo "
                  f"próprio publicado)")
        for conta, coluna, nosso, valor in sorted(
                piores, key=lambda x: -abs(x[2] - x[3]))[:10]:
            print(f"   {conta[:48]:<50}{coluna[:28]:<30}"
                  f"{nosso:>16,.2f}{valor:>16,.2f}{nosso - valor:>14,.2f}")
