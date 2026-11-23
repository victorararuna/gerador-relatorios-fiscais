# -*- coding: utf-8 -*-
"""RREO Anexo 06 — Resultados Primário e Nominal — apurado na Matriz de Saldos Contábeis.

O Anexo 06 **não** é o de Restos a Pagar (esse é o Anexo 07): aqui os restos a pagar
aparecem em três pontos — as colunas ``RESTOS A PAGAR PROCESSADOS PAGOS (b)``,
``LIQUIDADOS`` e ``PAGOS (c)`` e a linha ``(-) Restos a Pagar Processados (XLI)`` do
quadro da dívida consolidada.

Recorte do anexo
----------------
Diferente dos Anexos 01/07/09, o Anexo 06 **não tem blocos intra-orçamentários**
``(I)/(II)/(III)``. O corte é por **fonte de recursos**:

    exceto fontes RPPS  ->  fr[1:4] não está em {800, 801, 802}
    com fontes RPPS     ->  fr[1:4] está em {800, 801, 802}

Não é 800-804: com o 804 a linha "Pessoal e Encargos Sociais" dá R$ 12.987.104,42 a
mais. O filtro de modalidade ``nd[2:4] == "91"`` **não** se aplica a este anexo (não
há linha intra aqui). Na receita, as naturezas intra-orçamentárias (categoria 7)
entram no bloco corrente junto com a categoria 1 — é a chave que faz a linha
"Contribuições" fechar (sem a categoria 7 sobram R$ 26,79 mi contra R$ 58,31 mi
publicados, porque o estado lança 121.5.5.x e 721.5.5.x na mesma linha).

Contas da MSC usadas (todas de ``period_change`` acumulado do exercício, salvo nota):
    621200000                          receita bruta (natureza C)
    621310100, 621310200, 621390000    deduções da receita (natureza D)
    5221*                              dotação atualizada (classe 5, valor = -liquido)
    622130100 + 622130200 + 622130300 + 622130400   despesa empenhada
    622130300 + 622130400              despesa liquidada
    622130400                          despesa paga
    632200000                          restos a pagar processados pagos (b)
    631400000                          restos a pagar não processados pagos (c)
    631300000 + 631400000              "LIQUIDADOS" (saldos de fechamento do mês)
    632100000 + 631300000              saldo de RPP (linha XLI), saldos de fechamento
    1.1.2.*                            "Demais Haveres Financeiros" (classe 1)

A conta 622130700 (que o acervo lista entre as de liquidação) **não** entra aqui: com
ela a despesa empenhada e a liquidada de RR ficam R$ 37,7 mi acima do publicado. Só
6.2.2.1.3.01/.03/.04 formam as três colunas de execução.

Identidade que destrava a coluna de despesa (conferida ao centavo):

    (XXXIIa + XXXIIb + XXXIIc) = DESPESAS PAGAS (a) + RPP PAGOS (b) + PAGOS (c)

Ou seja: a despesa primária total é medida pelos **três fluxos de pagamento**, não
por empenho/liquidação.

O que sai da MSC e o que não sai
--------------------------------
Apurado: toda a receita realizada (coluna ``RECEITAS REALIZADAS (a)``), as sete
colunas de execução da despesa, o resultado primário acima da linha (XXXIV/XXXV),
a receita de alienação de investimentos permanentes (XLV) e, no quadro da dívida, o
saldo de RPP (XLI) e os demais haveres financeiros — coluna ``Até o Bimestre``.

Não sai da MSC (fica **fora** do dicionário, nunca zero):
    - metas da LDO (resultado primário e nominal) — ato normativo;
    - ``SALDO DE EXERCÍCIOS ANTERIORES`` e ``Superávit Financeiro Utilizado...`` — LOA;
    - juros/encargos ativos e passivos (XXXVI/XXXVII) — regime de competência, sem conta;
    - variação cambial (XLVI) e outros ajustes (XLIX);
    - dívida consolidada (XXXIX), deduções (XL), disponibilidade de caixa (bruta e
      líquida) e depósitos restituíveis — o conjunto de contas das classes 1/2 que o
      ente usa nesse quadro não é reproduzível pela MSC sem o relatório por fonte
      (testado: a lista do Anexo 2 do RGF deixa R$ 859,3 mi de fora em RR). Por isso a
      coluna ``Até o Bimestre`` dessas linhas também fica fora, e com ela XLII(b) e
      XLIII;
    - variações de precatórios e das demais obrigações (XLVII/XLVIII) — exigem o saldo
      de 31/12 do exercício anterior, que não está no acervo;
    - toda a coluna ``Em 31/12/<ano-1> (a)`` do quadro da dívida — o acervo do
      exercício anterior só tem as classes 5 e 6.

Parâmetro ``publicado`` (opcional)
----------------------------------
Recebe ``{(conta, coluna): valor}`` e serve **apenas** para as células que a MSC não
produz por natureza (não é gabarito de valor): as colunas ``PREVISÃO ATUALIZADA``
(LOA), ``VALOR CORRENTE`` (metas da LDO), ``PREVISÃO ORÇAMENTÁRIA`` (abertura) e a
coluna ``Em 31/12/<ano-1> (a)``. Aceita a chave ``conta`` tanto pelo **rótulo**
quanto pelo **cod_conta** do Siconfi — necessário porque o rótulo da meta da LDO
aparece duas vezes (primário e nominal). A coluna ``Até o Bimestre`` **não** é
replicada: ela é apurada (ou não sai), nunca copiada.

Calibração por ente (opcional)
------------------------------
O padrão é o de RR. Um ente com classificação local diferente tem um JSON em
``dados/mapeamentos/anexo6_<uf>.json``, carregado automaticamente a partir do nome
da pasta da MSC (``al_msc`` -> AL); ``celulas(..., uf=...)``/``calibracao=...``
forçam outra origem. O JSON traz o de-para ``rotulos`` (cod_conta -> rótulo
publicado) e os prefixos de natureza da receita do ente (``receita``). No Anexo 06
de AL a meta da LDO primária e a nominal usam o **mesmo** rótulo e a mesma coluna:
para comparar sem ambiguidade use ``celulas(..., chaves_cod=True)`` com
``ler_publicado(..., por_cod=True)``.

Desvios conhecidos contra o publicado de RR 2026 B4
---------------------------------------------------
Nenhum desvio de total: XXXII, XXXIII, XXXIV, XXXV e as somas por bloco fecham ao
centavo. Os desvios são todos de **abertura por linha**, e vêm da classificação que
o ente usa, não da MSC:

1. ``RESTOS A PAGAR PROCESSADOS PAGOS (b)``: total exato (R$ 91.814.252,65), mas a
   abertura Pessoal x Outras Correntes difere R$ 2.966.620,10 — o ente classifica
   como pessoal um valor que a MSC traz na natureza 33.
2. ``PAGOS (c)`` e ``LIQUIDADOS``: mesma coisa em R$ 8.800.553,79 (Outras Correntes
   que o ente reporta em Pessoal) e R$ 1.170.070,35 (Outras Correntes que o ente
   reporta em Investimentos). Como os dois lados se compensam, XVIII+XXIII, XX+XXVIII
   e os resultados primários permanecem exatos; só a abertura por linha oscila.
3. ``Alienação de Bens``: o estado repete o total na linha "Outras Alienações de
   Bens" e não isola a alienação de investimentos permanentes (XI). Com
   ``alienacao_isolada=True`` a linha (XI) passa a ser apurada e subtraída de (XIII),
   como manda o rótulo da fórmula — nesse modo XI/XIII/XVI/XVII e os resultados
   mudam em R$ 584.700,20 (o valor de 2.2.1.3.01.01 em RR).
4. ``LIQUIDADOS``: a linha é o **saldo de fechamento** de 6.3.1.3 somado ao de
   6.3.1.4, não o movimento do período.
5. O rótulo da meta da LDO nominal sai com o sufixo ``(nominal)``, porque no layout
   oficial as duas metas usam exatamente o mesmo rótulo e a mesma coluna.

Linhas que o ente não movimenta (``Operações de Crédito (VIII)``, ``Outras Receitas
de Capital``, ``Receitas Não Primárias de Capital com Fontes RPPS``, restos a pagar
de juros e de inversões) saem com **0,00**: é apuração de soma vazia, não valor
ausente — as linhas verdadeiramente não apuráveis ficam fora do dicionário.

Uso:
    >>> from rreo_anexo6_completo import celulas
    >>> c = celulas(r"...\\dados\\rr_msc", 2026, 4)
    >>> c[("Pessoal e Encargos Sociais", "DESPESAS PAGAS (a)", 0)]
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

RAIZ = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.join(RAIZ, "app")
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from acervo import Acervo  # noqa: E402

# ---------------------------------------------------------------------------
# colunas do layout
# ---------------------------------------------------------------------------
PREV_ATU = "PREVISÃO ATUALIZADA"
REC_A = "RECEITAS REALIZADAS (a)"
DOT = "DOTAÇÃO ATUALIZADA"
EMP = "DESPESAS EMPENHADAS"
LIQ = "DESPESAS LIQUIDADAS"
PAG_A = "DESPESAS PAGAS (a)"
RPP_B = "RESTOS A PAGAR PROCESSADOS PAGOS (b)"
LIQ_RP = "LIQUIDADOS"
PAG_C = "PAGOS (c)"
VALOR = "VALOR"
VALOR_CORRENTE = "VALOR CORRENTE"
VALOR_INCORRIDO = "VALOR INCORRIDO"
PREV_ORC = "PREVISÃO ORÇAMENTÁRIA"

#: colunas de execução da despesa, na ordem do layout
COLS_DESPESA = (DOT, EMP, LIQ, PAG_A, RPP_B, LIQ_RP, PAG_C)


def col_abertura(ano: int) -> str:
    """Rótulo da coluna de saldo de abertura (muda de ano para ano)."""
    return f"Em 31/12/{ano - 1} (a)"


def col_bimestre(ano: int) -> str:
    return f"Até o Bimestre {ano} (b)"


# ---------------------------------------------------------------------------
# contas e recortes
# ---------------------------------------------------------------------------
CONTAS_RECEITA = ("621200000", "621310100", "621310200", "621390000")
CONTAS_EMPENHO = ("622130100", "622130200", "622130300", "622130400")
CONTAS_LIQUIDACAO = ("622130300", "622130400")
CONTA_PAGA = "622130400"
CONTA_RPP_PAGO = "632200000"
CONTA_RPP_SALDO = "632100000"
CONTA_RPNP_PAGO = "631400000"
CONTA_RPNP_LIQUIDADO = "631300000"
PREFIXO_DOTACAO = "5221"
PREFIXO_HAVERES = "112"

#: fontes RPPS no Anexo 06 (não inclui 803/804)
FONTES_RPPS = ("800", "801", "802")
#: elemento da ND que isola "Concessão de Empréstimos e Financiamentos" (XXIV)
ELEMENTO_CONCESSAO = "66"

GRUPO_PESSOAL = "31"
GRUPO_JUROS = "32"
GRUPO_OUTRAS_CORRENTES = "33"
GRUPO_INVESTIMENTOS = "44"
GRUPO_INVERSOES = "45"
GRUPO_AMORTIZACAO = "46"

#: naturezas intra-orçamentárias -> categoria equivalente (receita)
_CATEGORIA_INTERNA = {"7": "1", "8": "2"}


def _rpps(fr: str) -> bool:
    """A fonte é vinculada ao RPPS?"""
    return len(fr) >= 4 and fr[1:4] in FONTES_RPPS


def _fonte_rpps_ampla(fr: str) -> bool:
    """Fonte 8xx — usada para separar a reserva orçamentária do RPPS."""
    return len(fr) >= 2 and fr[1:2] == "8"


def _norm_nr(nr: str) -> str:
    """Natureza da receita com a categoria intra-orçamentária normalizada.

    7.x (correntes intra) -> 1.x; 8.x (capital intra) -> 2.x. É o que faz as linhas
    de detalhe da receita fecharem: a categoria 7 entra no bloco corrente.
    """
    if not nr:
        return ""
    return _CATEGORIA_INTERNA.get(nr[0], nr[0]) + nr[1:]


def _grupo(nd: str) -> str:
    return nd[:2]


def _elemento(nd: str) -> str:
    return nd[4:6]


# ---------------------------------------------------------------------------
# rótulos (cod_conta -> rótulo do Siconfi)
# ---------------------------------------------------------------------------
ROTULOS: Dict[str, str] = {
    # ---- receitas
    "ReceitasCorrentesExcetoFontesRPPS": "RECEITAS CORRENTES (EXCETO FONTES RPPS) (I)",
    "RREO6ReceitasTributarias": "Impostos, Taxas e Contribuições de Melhoria",
    "RREO6ICMS": "ICMS",
    "RREO6IPVA": "IPVA",
    "RREO6ITCD": "ITCD",
    "RREO6IRRF": "IRRF",
    "RREO6OutrasReceitasTributarias": "Outros Impostos, Taxas e Contribuições de Melhoria",
    "RREO6ReceitasDeContribuicoes": "Contribuições",
    "RREO6ReceitaPatrimonial": "Receita Patrimonial",
    "RREO6AplicacoesFinanceiras": "Aplicações Financeiras (II)",
    "OutrasReceitasPatrimoniais": "Outras Receitas Patrimoniais",
    "RREO6TransferenciasCorrentes": "Transferências Correntes",
    "RREO6CotaParteDoFPE": "Cota-Parte do FPE",
    "TransferenciasDaLCn611989": "Transferências da LC nº 61/1989",
    "TransferenciasDoFUNDEB": "Transferências do FUNDEB",
    "RREO6OutrasTransferenciasCorrentes": "Outras Transferências Correntes",
    "RREO6DemaisReceitasCorrentes": "Demais Receitas Correntes",
    "OutrasReceitasFinanceiras": "Outras Receitas Financeiras (III)",
    "RREO6DiversasReceitasCorrentes": "Receitas Correntes Restantes",
    "ReceitasPrimariasCorrentesExcetoFontesRPPS":
        "RECEITAS PRIMÁRIAS CORRENTES (EXCETO FONTES RPPS) (IV) = (I - (II + III))",
    "ReceitasPrimariasCorrentesComFontesRPPS":
        "RECEITAS PRIMÁRIAS CORRENTES (COM FONTES RPPS) (V)",
    "ReceitasNaoPrimariasCorrentesComFontesRPPS":
        "RECEITAS NÃO PRIMÁRIAS CORRENTES (COM FONTES RPPS) (VI)",
    "ReceitasDeCapitalExcetoFontesRPPS": "RECEITAS DE CAPITAL (EXCETO FONTES RPPS) (VII)",
    "RREO6OperacoesDeCredito": "Operações de Crédito (VIII)",
    "RREO6AmortizacaoDeEmprestimos": "Amortização de Empréstimos (IX)",
    "RREO6AlienacaoDeBens": "Alienação de Bens",
    "ReceitasDeAlienacaoDeInvestimentosPermanentes":
        "Receitas de Alienação de Investimentos Permanentes (XI)",
    "OutrasAlienacoesDeBens": "Outras Alienações de Bens",
    "RREO6TransferenciasDeCapital": "Transferências de Capital",
    "RREO6ConveniosCapital": "Convênios",
    "RREO6OutrasTransferenciasDeCapital": "Outras Transferências de Capital",
    "RREO6OutrasReceitasDeCapital": "Outras Receitas de Capital",
    "OutrasReceitasDeCapitalPrimarias": "Outras Receitas de Capital Primárias",
    "ReceitasPrimariasDeCapitalExcetoFontesRPPS":
        "RECEITAS PRIMÁRIAS DE CAPITAL (EXCETO FONTES RPPS) (XIII) = "
        "(VII - (VIII + IX + X + XI + XII))",
    "ReceitasNaoPrimariasDeCapitalComFontesRPPS":
        "RECEITAS NÃO PRIMÁRIAS DE CAPITAL (COM FONTES RPPS) (XV)",
    "RREO6TotalReceitaPrimaria": "RECEITA PRIMÁRIA TOTAL (XVI) = (IV + V + XIII + XIV)",
    "ReceitaPrimariaTotalExcetoFontesRPPS":
        "RECEITA PRIMÁRIA TOTAL (EXCETO FONTES RPPS) (XVII) = (IV + XIII)",
    # ---- despesas
    "DespesasCorrentesExcetoFontesRPPS": "DESPESAS CORRENTES (EXCETO FONTES RPPS) (XVIII)",
    "RREO6PessoalEEncargosSociais": "Pessoal e Encargos Sociais",
    "RREO6JurosEEncargosDaDivida": "Juros e Encargos da Dívida (XIX)",
    "RREO6OutrasDespesasCorrentes": "Outras Despesas Correntes",
    "RREO6DemaisDespesasCorrentes": "Demais Despesas Correntes",
    "DespesasPrimariasCorrentesExcetoFontesRPPS":
        "DESPESAS PRIMÁRIAS CORRENTES (EXCETO FONTES RPPS) (XX) = (XVIII - XIX)",
    "DespesasPrimariasCorrentesComFontesRPPS":
        "DESPESAS PRIMÁRIAS CORRENTES (COM FONTES RPPS) (XXI)",
    "DespesasDeCapitalExcetoFontesRPPS": "DESPESAS DE CAPITAL (EXCETO FONTES RPPS) (XXIII)",
    "RREO6Investimentos": "Investimentos",
    "RREO6InversoesFinanceiras": "Inversões Financeiras",
    "RREO6ConcessaoDeEmprestimos": "Concessão de Empréstimos e Financiamentos (XXIV)",
    "RREO6DemaisInversoesFinanceiras": "Demais Inversões Financeiras",
    "RREO6AmortizacaoDaDivida": "Amortização da Dívida (XXVII)",
    "DespesasPrimariasDeCapitalExcetoFontesRPPS":
        "DESPESAS PRIMÁRIAS DE CAPITAL (EXCETO FONTES RPPS) (XXVIII) = "
        "(XXIII - (XXIV + XXV + XXVI + XXVII))",
    "RREO6ReservaDeContingencia": "RESERVA DE CONTINGÊNCIA (XXIX)",
    "DespesasPrimariasDeCapitalComFontesRPPS":
        "DESPESAS PRIMÁRIAS DE CAPITAL (COM FONTES RPPS) (XXX)",
    "RREO6TotalDespesaPrimaria":
        "DESPESA PRIMÁRIA TOTAL (XXXII) = (XX + XXI + XXVIII + XXIX + XXX)",
    "DespesaPrimariaTotalExcetoFontesRPPS":
        "DESPESA PRIMÁRIA TOTAL (EXCETO FONTES RPPS) (XXXIII) = (XX + XXVIII + XXIX)",
    # ---- resultados
    "ResultadoPrimarioComRPPSAcimaDaLinha":
        "RESULTADO PRIMÁRIO (COM RPPS) - Acima da Linha (XXXIV) = "
        "(XVIa - (XXXIIa +XXXIIb + XXXIIc))",
    "ResultadoPrimarioSemRPPSAcimaDaLinha":
        "RESULTADO PRIMÁRIO (SEM RPPS) - Acima da Linha (XXXV) = "
        "(XVIIa - (XXXIIIa +XXXIIIb + XXXIIIc))",
    "RREO6MetaDeResultadoPrimarioFixadaNoAnexoDeMetasFiscaisDaLDOParaOExercicioDeReferencia":
        "Meta fixada no Anexo de Metas Fiscais da LDO para o exercício de referência",
    "MetaDeResultadoNominalFixadaNoAnexoDeMetasFiscaisDaLDOParaOExercicioDeReferencia":
        "Meta fixada no Anexo de Metas Fiscais da LDO para o exercício de referência "
        "(nominal)",
    "JurosEncargosEVariacoesMonetariasAtivosExcetoRPPS":
        "Juros, Encargos e Variações Monetárias Ativos (Exceto RPPS) (XXXVI)",
    "JurosEncargosEVariacoesMonetariasPassivosExcetoRPPS":
        "Juros, Encargos e Variações Monetárias Passivos (Exceto RPPS) (XXXVII)",
    "ResultadoNominalAcimaDaLinhaSemRPPS":
        "RESULTADO NOMINAL (SEM RPPS) - Acima da Linha (XXXVIII) = XXXV + (XXXVI - XXXVII)",
    # ---- dívida consolidada líquida
    "DividaConsolidada": "DÍVIDA CONSOLIDADA (XXXIX)",
    "DeducoesDaDividaConsolidada": "DEDUÇÕES (XL)",
    "RREO5DisponibilidadeDeCaixa": "Disponibilidade de Caixa",
    "DisponibilidadeDeCaixaBruta": "Disponibilidade de Caixa Bruta",
    "RestosAPagarProcessadosExcetoPrecatorios": "(-) Restos a Pagar Processados (XLI)",
    "DepositosRestituiveisEValoresVinculados":
        "(-) Depósitos Restituíveis e Valores Vinculados",
    "DemaisHaveresFinanceiros": "Demais Haveres Financeiros",
    "DividaConsolidadaLiquida": "DÍVIDA CONSOLIDADA LÍQUIDA (XLII) = (XXXIX - XL)",
    "ResultadoNominalAbaixoDaLinhaSemRPPS":
        "RESULTADO NOMINAL (SEM RPPS) - Abaixo da Linha (XLIII) = (XLIIa - XLIIb)",
    "VariacaoSaldoRPP": "VARIAÇÃO DO SALDO DE RPP (XLIV) = (XLIb - XLIa)",
    "ReceitaDeAlienacaoDeInvestimentosPermanentes":
        "RECEITA DE ALIENAÇÃO DE INVESTIMENTOS PERMANENTES (XLV) = (XI)",
    "VariacaoCambial": "VARIAÇÃO CAMBIAL (XLVI)",
    "VariacaoDoSaldoDePrecatoriosIntegrantesDaDC":
        "VARIAÇÃO DO SALDO DE PRECATÓRIOS INTEGRANTES DA DC (XLVII)",
    "VariacaoDoSaldoDasDemaisObrigacoesIntegrantesDaDC":
        "VARIAÇÃO DO SALDO DAS DEMAIS OBRIGAÇÕES INTEGRANTES DA DC (XLVIII)",
    "OutrosAjustes": "OUTROS AJUSTES (XLIX)",
    "ResultadoNominalAbaixoDaLinhaSemRPPSAjustado":
        "RESULTADO NOMINAL (SEM RPPS) AJUSTADO - Abaixo da Linha (L) = "
        "(XLIII + (XLIV - XLV - XLVI + XLVII + XLVIII) +/- (XLIX))",
    "ResultadoPrimarioAbaixoDaLinhaSemRPPS":
        "RESULTADO PRIMÁRIO (SEM RPPS) - Abaixo da Linha (LI) = (L) - (XXXVI - XXXVII)",
    # ---- abertura orçamentária
    "RREO6SaldoDeExerciciosAnteriores": "SALDO DE EXERCÍCIOS ANTERIORES",
    "SuperavitFinanceiro":
        "Superávit Financeiro Utilizado para Abertura e Reabertura de Créditos Adicionais",
    "ReservaOrcamentariaDoRPPSPrevidenciario": "RESERVA ORÇAMENTÁRIA DO RPPS",
}

#: linhas do bloco de receita (a coluna PREVISÃO ATUALIZADA delas é LOA, não MSC)
LINHAS_RECEITA = (
    "ReceitasCorrentesExcetoFontesRPPS",
    "RREO6ReceitasTributarias",
    "RREO6ICMS",
    "RREO6IPVA",
    "RREO6ITCD",
    "RREO6IRRF",
    "RREO6OutrasReceitasTributarias",
    "RREO6ReceitasDeContribuicoes",
    "RREO6ReceitaPatrimonial",
    "RREO6AplicacoesFinanceiras",
    "OutrasReceitasPatrimoniais",
    "RREO6TransferenciasCorrentes",
    "RREO6CotaParteDoFPE",
    "TransferenciasDaLCn611989",
    "TransferenciasDoFUNDEB",
    "RREO6OutrasTransferenciasCorrentes",
    "RREO6DemaisReceitasCorrentes",
    "OutrasReceitasFinanceiras",
    "RREO6DiversasReceitasCorrentes",
    "ReceitasPrimariasCorrentesExcetoFontesRPPS",
    "ReceitasPrimariasCorrentesComFontesRPPS",
    "ReceitasNaoPrimariasCorrentesComFontesRPPS",
    "ReceitasDeCapitalExcetoFontesRPPS",
    "RREO6OperacoesDeCredito",
    "RREO6AmortizacaoDeEmprestimos",
    "RREO6AlienacaoDeBens",
    "ReceitasDeAlienacaoDeInvestimentosPermanentes",
    "OutrasAlienacoesDeBens",
    "RREO6TransferenciasDeCapital",
    "RREO6ConveniosCapital",
    "RREO6OutrasTransferenciasDeCapital",
    "RREO6OutrasReceitasDeCapital",
    "OutrasReceitasDeCapitalPrimarias",
    "ReceitasPrimariasDeCapitalExcetoFontesRPPS",
    "ReceitasNaoPrimariasDeCapitalComFontesRPPS",
    "RREO6TotalReceitaPrimaria",
    "ReceitaPrimariaTotalExcetoFontesRPPS",
)

#: linhas do quadro da dívida (usam as colunas de abertura e do bimestre)
LINHAS_DIVIDA = (
    "DividaConsolidada",
    "DeducoesDaDividaConsolidada",
    "RREO5DisponibilidadeDeCaixa",
    "DisponibilidadeDeCaixaBruta",
    "RestosAPagarProcessadosExcetoPrecatorios",
    "DepositosRestituiveisEValoresVinculados",
    "DemaisHaveresFinanceiros",
    "DividaConsolidadaLiquida",
)

#: células que a MSC não produz por natureza e que podem vir do último publicado
REPLICAVEIS: Dict[str, Tuple[str, ...]] = {cod: (PREV_ATU,) for cod in LINHAS_RECEITA}
REPLICAVEIS[
    "RREO6MetaDeResultadoPrimarioFixadaNoAnexoDeMetasFiscaisDaLDOParaOExercicioDeReferencia"
] = (VALOR_CORRENTE,)
REPLICAVEIS[
    "MetaDeResultadoNominalFixadaNoAnexoDeMetasFiscaisDaLDOParaOExercicioDeReferencia"
] = (VALOR_CORRENTE,)
REPLICAVEIS["RREO6SaldoDeExerciciosAnteriores"] = (PREV_ORC,)
REPLICAVEIS["SuperavitFinanceiro"] = (PREV_ORC,)
# no quadro da dívida a MSC só apura a coluna do bimestre (e apenas XLI e haveres);
# a coluna de abertura é o fechamento do exercício anterior, que não está no acervo
for _cod in LINHAS_DIVIDA:
    REPLICAVEIS[_cod] = ("{abertura}",)
del _cod

#: pasta dos JSONs de calibração por ente
DIR_MAPEAMENTOS = os.path.join(RAIZ, "dados", "mapeamentos")

#: cod IBGE -> UF (só os entes calibrados; os demais seguem sem calibração)
UF_POR_COD = {"27": "AL"}

#: ``al_msc`` / ``rr_msc`` -> UF
_RE_RAIZ = re.compile(r"(?:^|[\\/])([a-z]{2})_msc(?:[\\/]|$)", re.I)


def uf_da_raiz(raiz: str) -> Optional[str]:
    """UF deduzida do nome da pasta da MSC (``...\\dados\\al_msc`` -> ``AL``)."""
    m = _RE_RAIZ.search(os.path.abspath(raiz) + os.sep)
    return m.group(1).upper() if m else None


def carregar_calibracao(raiz: Optional[str] = None,
                        uf: Optional[str] = None,
                        caminho: Optional[str] = None) -> Dict:
    """JSON de calibração do ente (``dados/mapeamentos/anexo6_<uf>.json``).

    Sem ``uf``/``caminho``, a UF é deduzida do nome da pasta da MSC. Se não
    houver JSON para o ente, devolve ``{}`` — o comportamento é o de sempre.
    """
    if caminho is None:
        uf = (uf or (uf_da_raiz(raiz) if raiz else None) or "").upper() or None
        if not uf:
            return {}
        uf = UF_POR_COD.get(uf, uf)
        caminho = os.path.join(DIR_MAPEAMENTOS, f"anexo6_{uf.lower()}.json")
    if not os.path.exists(caminho):
        return {}
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# coleta na MSC
# ---------------------------------------------------------------------------
def _periodo(ac: Acervo, ano: int, bimestre: int, mes: Optional[int],
             meses: Optional[Sequence[int]]) -> Tuple[List[int], int]:
    """(meses acumulados, mês de referência dos saldos) do bimestre."""
    if mes is None:
        if not 1 <= bimestre <= 6:
            raise ValueError("bimestre deve estar entre 1 e 6")
        mes = 2 * bimestre
    if meses is None:
        disponiveis = [m for m in range(1, mes + 1)
                       if ac.tem(ano, m, 6, "period_change")]
        if not disponiveis:
            raise FileNotFoundError(
                f"sem MSC de classe 6 para {ano} até o mês {mes:02d}")
        meses = disponiveis
    else:
        meses = [m for m in meses if ac.tem(ano, m, 6, "period_change")]
        if not meses:
            raise FileNotFoundError(
                f"sem MSC de classe 6 em {ano} para os meses pedidos")
    return list(meses), max(meses)


def _receita(ac: Acervo, ano: int, meses: Sequence[int]
             ) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Receita líquida por natureza, separada entre exceto-RPPS e RPPS."""
    exc: Dict[str, float] = defaultdict(float)
    rp: Dict[str, float] = defaultdict(float)
    for m in meses:
        for r in ac.ler(ano, m, 6, "period_change"):
            if r.conta not in CONTAS_RECEITA:
                continue
            nr = _norm_nr(r.nr)
            if _rpps(r.fr):
                rp[nr] += r.liquido
            else:
                exc[nr] += r.liquido
    return exc, rp


def _despesa(ac: Acervo, ano: int, meses: Sequence[int], mes_ref: int
             ) -> Dict[str, Dict[tuple, float]]:
    """As sete colunas de execução, por (grupo de ND, elemento, RPPS)."""
    cols: Dict[str, Dict[tuple, float]] = {c: defaultdict(float) for c in COLS_DESPESA}

    # dotação: classe 5, contas 5221*, valor positivo (o líquido é negativo)
    for m in meses:
        if not ac.tem(ano, m, 5, "period_change"):
            continue
        for r in ac.ler(ano, m, 5, "period_change"):
            if not r.conta.startswith(PREFIXO_DOTACAO) or r.nd.startswith("99"):
                continue          # reservas: apuradas à parte, ver `_reservas`
            cols[DOT][(_grupo(r.nd), _elemento(r.nd), _rpps(r.fr))] -= r.liquido

    # empenho, liquidação, pagamento do exercício e pagamento de restos a pagar
    for m in meses:
        for r in ac.ler(ano, m, 6, "period_change"):
            chave = (_grupo(r.nd), _elemento(r.nd), _rpps(r.fr))
            if r.conta in CONTAS_EMPENHO:
                cols[EMP][chave] += r.liquido
                if r.conta in CONTAS_LIQUIDACAO:
                    cols[LIQ][chave] += r.liquido
                if r.conta == CONTA_PAGA:
                    cols[PAG_A][chave] += r.liquido
            elif r.conta == CONTA_RPP_PAGO:
                cols[RPP_B][chave] += r.liquido
            elif r.conta == CONTA_RPNP_PAGO:
                cols[PAG_C][chave] += r.liquido

    # "LIQUIDADOS": saldo de fechamento de 6.3.1.3 + 6.3.1.4
    if ac.tem(ano, mes_ref, 6, "ending_balance"):
        for r in ac.ler(ano, mes_ref, 6, "ending_balance"):
            if r.conta in (CONTA_RPNP_LIQUIDADO, CONTA_RPNP_PAGO):
                cols[LIQ_RP][(_grupo(r.nd), _elemento(r.nd), _rpps(r.fr))] += r.liquido
    return cols


def _reservas(ac: Acervo, ano: int, meses: Sequence[int]) -> Tuple[float, float]:
    """(reserva de contingência, reserva orçamentária do RPPS) na dotação."""
    contingencia = reserva_rpps = 0.0
    for m in meses:
        if not ac.tem(ano, m, 5, "period_change"):
            continue
        for r in ac.ler(ano, m, 5, "period_change"):
            if not r.conta.startswith(PREFIXO_DOTACAO) or not r.nd.startswith("99"):
                continue
            if _fonte_rpps_ampla(r.fr):
                reserva_rpps -= r.liquido
            else:
                contingencia -= r.liquido
    return contingencia, reserva_rpps


def _haveres(ac: Acervo, ano: int, mes_ref: int) -> Optional[float]:
    """Demais haveres financeiros: classe 1, prefixo 1.1.2."""
    if not ac.tem(ano, mes_ref, 1, "ending_balance"):
        return None
    total = 0.0
    for r in ac.ler(ano, mes_ref, 1, "ending_balance"):
        if r.conta.startswith(PREFIXO_HAVERES):
            total += r.liquido
    return -total


def _saldos_rp(ac: Acervo, ano: int, mes_ref: int) -> Optional[float]:
    """Saldo de RPP: 6.3.2.1 + 6.3.1.3 (saldos de fechamento)."""
    if not ac.tem(ano, mes_ref, 6, "ending_balance"):
        return None
    total = 0.0
    for r in ac.ler(ano, mes_ref, 6, "ending_balance"):
        if r.conta in (CONTA_RPP_SALDO, CONTA_RPNP_LIQUIDADO):
            total += r.liquido
    return total


def _soma(col: Dict[tuple, float], grupos: Iterable[str],
          rpps: Optional[bool] = None, elemento: Optional[str] = None) -> float:
    """Soma uma coluna filtrando grupo de ND, elemento e recorte de fonte."""
    grupos = set(grupos)
    total = 0.0
    for (grupo, elem, fonte_rpps), valor in col.items():
        if grupo not in grupos:
            continue
        if elemento is not None and elem != elemento:
            continue
        if rpps is True and not fonte_rpps:
            continue
        if rpps is False and fonte_rpps:
            continue
        total += valor
    return total


# ---------------------------------------------------------------------------
# apuração
# ---------------------------------------------------------------------------
def celulas(raiz: str, ano: int, bimestre: int, *,
            publicado: Optional[Dict[tuple, float]] = None,
            mes: Optional[int] = None,
            meses: Optional[Sequence[int]] = None,
            acervo: Optional[Acervo] = None,
            alienacao_isolada: bool = False,
            rotulos: Optional[Dict[str, str]] = None,
            calibracao: Optional[Dict] = None,
            uf: Optional[str] = None,
            chaves_cod: bool = False) -> Dict[tuple, float]:
    """Células do Anexo 06 apuradas na MSC: ``{(conta, coluna, bloco): valor}``.

    Args:
        raiz: pasta com os arquivos da Matriz de Saldos Contábeis (formato longo).
        ano: exercício.
        bimestre: 1..6; o mês de referência é ``2 * bimestre`` (B4 -> agosto).
        publicado: ``{(conta, coluna): valor}`` usado **só** nas células que a MSC não
            produz (previsão da LOA, metas da LDO, abertura e saldo de 31/12 do ano
            anterior). Aceita ``conta`` por rótulo ou por ``cod_conta``.
        mes: força o mês de referência (default ``2 * bimestre``).
        meses: força os meses acumulados.
        acervo: reaproveita um ``Acervo`` já indexado.
        alienacao_isolada: separa a alienação de investimentos permanentes (XI) —
            ver nota 2 do módulo.
        rotulos: de-para opcional ``{cod_conta: rótulo publicado}``; sobrepõe o de
            RR. Também aceito pelo JSON ``dados/mapeamentos/anexo6_<uf>.json``.
        calibracao: dicionário de calibração já carregado (default: o JSON do ente,
            detectado pelo nome da pasta da MSC).
        uf: força a UF da calibração (``AL``, ``RR``...).
        chaves_cod: devolve ``conta`` como **cod_conta** do Siconfi em vez do
            rótulo. É o modo necessário quando o publicado tem rótulo ambíguo
            (no Anexo 06 de AL a meta da LDO primária e a nominal usam o mesmo
            texto e a mesma coluna) — use com ``ler_publicado(..., por_cod=True)``.

    Returns:
        Dict com chave ``(conta, coluna, bloco)``; ``coluna`` é o cabeçalho do
        layout e ``bloco`` sempre 0 (este anexo não tem blocos
        intra-orçamentários: o corte é por fonte e cada recorte tem linha
        própria, então não há repetição de conta entre blocos).
    """
    ac = acervo if acervo is not None else Acervo(raiz)
    meses, mes_ref = _periodo(ac, ano, bimestre, mes, meses)
    cal = calibracao if calibracao is not None else carregar_calibracao(raiz, uf)
    rot = dict(ROTULOS)
    rot.update(cal.get("rotulos") or {})
    rot.update(rotulos or {})
    recorte = cal.get("receita") or {}

    def _pref(chave: str, padrao: Sequence[str]) -> Tuple[str, ...]:
        """Prefixos de natureza da receita: calibração do ente ou o padrão."""
        item = recorte.get(chave)
        if isinstance(item, dict):
            item = item.get("prefixos")
        return tuple(item) if item else tuple(padrao)

    def _excluir(chave: str) -> Tuple[str, ...]:
        item = recorte.get(chave)
        return tuple(item.get("excluir") or ()) if isinstance(item, dict) else ()

    v: Dict[Tuple[str, str], float] = {}

    def definir(cod: str, coluna: str, valor: Optional[float]) -> None:
        if valor is not None:
            v[(cod, coluna)] = valor

    def comb(*termos: Tuple[float, str, str]) -> Optional[float]:
        """Soma algébrica de (sinal, cod, coluna); None se faltar alguma célula."""
        total = 0.0
        for sinal, cod, coluna in termos:
            x = v.get((cod, coluna))
            if x is None:
                return None
            total += sinal * x
        return total

    # ---------------- receita ----------------
    exc, rp = _receita(ac, ano, meses)

    def tot(fonte: Dict[str, float], *prefixos: str) -> float:
        return sum(x for nr, x in fonte.items() if nr.startswith(prefixos))

    corr_exc, corr_rp = tot(exc, "1"), tot(rp, "1")
    cap_exc, cap_rp = tot(exc, "2"), tot(rp, "2")

    impostos = tot(exc, "11")
    icms = tot(exc, "11145")
    ipva = tot(exc, "111251")
    itcd = tot(exc, "111252")
    irrf = tot(exc, *_pref("irrf", ("11130311",)))
    contribuicoes = tot(exc, "12")
    patrimonial = tot(exc, "13")
    aplicacoes = (tot(exc, *_pref("aplicacoes_financeiras", ("132",)))
                  - tot(exc, *_excluir("aplicacoes_financeiras")))
    transferencias = tot(exc, "17")
    fpe = tot(exc, "17115001")
    lc61 = tot(exc, "17115301")
    fundeb = tot(exc, *_pref("fundeb", ("17515001", "17155301")))
    financeiras = tot(exc, "16410101")
    demais_correntes = tot(exc, "19") + tot(exc, "16")

    definir("ReceitasCorrentesExcetoFontesRPPS", REC_A, corr_exc)
    definir("RREO6ReceitasTributarias", REC_A, impostos)
    definir("RREO6ICMS", REC_A, icms)
    definir("RREO6IPVA", REC_A, ipva)
    definir("RREO6ITCD", REC_A, itcd)
    definir("RREO6IRRF", REC_A, irrf)
    definir("RREO6OutrasReceitasTributarias", REC_A,
            impostos - (icms + ipva + itcd + irrf))
    definir("RREO6ReceitasDeContribuicoes", REC_A, contribuicoes)
    definir("RREO6ReceitaPatrimonial", REC_A, patrimonial)
    definir("RREO6AplicacoesFinanceiras", REC_A, aplicacoes)
    definir("OutrasReceitasPatrimoniais", REC_A, patrimonial - aplicacoes)
    definir("RREO6TransferenciasCorrentes", REC_A, transferencias)
    definir("RREO6CotaParteDoFPE", REC_A, fpe)
    definir("TransferenciasDaLCn611989", REC_A, lc61)
    definir("TransferenciasDoFUNDEB", REC_A, fundeb)
    definir("RREO6OutrasTransferenciasCorrentes", REC_A,
            transferencias - (fpe + lc61 + fundeb))
    definir("RREO6DemaisReceitasCorrentes", REC_A, demais_correntes)
    definir("OutrasReceitasFinanceiras", REC_A, financeiras)
    definir("RREO6DiversasReceitasCorrentes", REC_A, demais_correntes - financeiras)

    # (VI) é a parcela não primária das fontes RPPS: rendimentos de aplicações
    nao_prim_corr_rp = tot(rp, "13210401")
    definir("ReceitasNaoPrimariasCorrentesComFontesRPPS", REC_A, nao_prim_corr_rp)
    definir("ReceitasPrimariasCorrentesComFontesRPPS", REC_A,
            corr_rp - nao_prim_corr_rp)

    operacoes = tot(exc, *_pref("operacoes_credito", ("211",)))
    amortizacoes = tot(exc, "23110601")
    alienacao = tot(exc, "22")
    alienacao_invest = tot(exc, "22130101")
    transferencias_capital = tot(exc, "24")
    convenios = tot(exc, "2414")
    outras_capital = cap_exc - (operacoes + alienacao + amortizacoes
                                + transferencias_capital)

    definir("ReceitasDeCapitalExcetoFontesRPPS", REC_A, cap_exc)
    definir("RREO6OperacoesDeCredito", REC_A, operacoes)
    definir("RREO6AmortizacaoDeEmprestimos", REC_A, amortizacoes)
    definir("RREO6AlienacaoDeBens", REC_A, alienacao)
    definir("RREO6TransferenciasDeCapital", REC_A, transferencias_capital)
    definir("RREO6ConveniosCapital", REC_A, convenios)
    definir("RREO6OutrasTransferenciasDeCapital", REC_A,
            transferencias_capital - convenios)
    definir("RREO6OutrasReceitasDeCapital", REC_A, outras_capital)
    definir("OutrasReceitasDeCapitalPrimarias", REC_A, outras_capital)
    definir("ReceitasNaoPrimariasDeCapitalComFontesRPPS", REC_A, cap_rp)

    if alienacao_isolada:
        definir("ReceitasDeAlienacaoDeInvestimentosPermanentes", REC_A, alienacao_invest)
        definir("OutrasAlienacoesDeBens", REC_A, alienacao - alienacao_invest)
    else:
        # convenção do publicado de RR: o total fica em "Outras Alienações de Bens"
        definir("OutrasAlienacoesDeBens", REC_A, alienacao)

    definir("ReceitasPrimariasCorrentesExcetoFontesRPPS", REC_A,
            comb((1, "ReceitasCorrentesExcetoFontesRPPS", REC_A),
                 (-1, "RREO6AplicacoesFinanceiras", REC_A),
                 (-1, "OutrasReceitasFinanceiras", REC_A)))

    termos_capital = [(1, "ReceitasDeCapitalExcetoFontesRPPS", REC_A),
                      (-1, "RREO6OperacoesDeCredito", REC_A),
                      (-1, "RREO6AmortizacaoDeEmprestimos", REC_A)]
    if alienacao_isolada:
        termos_capital.append(
            (-1, "ReceitasDeAlienacaoDeInvestimentosPermanentes", REC_A))
    definir("ReceitasPrimariasDeCapitalExcetoFontesRPPS", REC_A, comb(*termos_capital))

    definir("RREO6TotalReceitaPrimaria", REC_A,
            comb((1, "ReceitasPrimariasCorrentesExcetoFontesRPPS", REC_A),
                 (1, "ReceitasPrimariasCorrentesComFontesRPPS", REC_A),
                 (1, "ReceitasPrimariasDeCapitalExcetoFontesRPPS", REC_A),
                 (1, "ReceitasNaoPrimariasDeCapitalComFontesRPPS", REC_A)))
    definir("ReceitaPrimariaTotalExcetoFontesRPPS", REC_A,
            comb((1, "ReceitasPrimariasCorrentesExcetoFontesRPPS", REC_A),
                 (1, "ReceitasPrimariasDeCapitalExcetoFontesRPPS", REC_A)))

    # ---------------- despesa ----------------
    cols = _despesa(ac, ano, meses, mes_ref)

    def desp(cod: str, grupos: Iterable[str], rpps: Optional[bool] = None,
             elemento: Optional[str] = None) -> None:
        """Preenche as sete colunas de execução de uma linha de despesa."""
        for coluna in COLS_DESPESA:
            definir(cod, coluna, _soma(cols[coluna], grupos, rpps, elemento))

    desp("DespesasCorrentesExcetoFontesRPPS",
         (GRUPO_PESSOAL, GRUPO_JUROS, GRUPO_OUTRAS_CORRENTES), rpps=False)
    desp("RREO6PessoalEEncargosSociais", (GRUPO_PESSOAL,), rpps=False)
    desp("RREO6JurosEEncargosDaDivida", (GRUPO_JUROS,), rpps=False)
    desp("RREO6OutrasDespesasCorrentes", (GRUPO_OUTRAS_CORRENTES,), rpps=False)
    desp("DespesasPrimariasCorrentesComFontesRPPS",
         (GRUPO_PESSOAL, GRUPO_OUTRAS_CORRENTES), rpps=True)
    desp("DespesasDeCapitalExcetoFontesRPPS",
         (GRUPO_INVESTIMENTOS, GRUPO_INVERSOES, GRUPO_AMORTIZACAO), rpps=False)
    desp("RREO6Investimentos", (GRUPO_INVESTIMENTOS,), rpps=False)
    desp("RREO6InversoesFinanceiras", (GRUPO_INVERSOES,), rpps=False)
    desp("RREO6ConcessaoDeEmprestimos", (GRUPO_INVERSOES,), rpps=False,
         elemento=ELEMENTO_CONCESSAO)
    desp("RREO6AmortizacaoDaDivida", (GRUPO_AMORTIZACAO,), rpps=False)
    desp("DespesasPrimariasDeCapitalComFontesRPPS", (GRUPO_INVESTIMENTOS,), rpps=True)

    # linhas espelho: repetem a linha de cima no layout oficial
    for coluna in COLS_DESPESA:
        definir("RREO6DemaisDespesasCorrentes", coluna,
                v.get(("RREO6OutrasDespesasCorrentes", coluna)))

    # reservas: só existem na coluna de dotação
    reserva_contingencia, reserva_rpps = _reservas(ac, ano, meses)
    definir("RREO6ReservaDeContingencia", DOT, reserva_contingencia)
    definir("ReservaOrcamentariaDoRPPSPrevidenciario", PREV_ORC, reserva_rpps)

    for coluna in COLS_DESPESA:
        definir("RREO6DemaisInversoesFinanceiras", coluna,
                comb((1, "RREO6InversoesFinanceiras", coluna),
                     (-1, "RREO6ConcessaoDeEmprestimos", coluna)))
        definir("DespesasPrimariasCorrentesExcetoFontesRPPS", coluna,
                comb((1, "DespesasCorrentesExcetoFontesRPPS", coluna),
                     (-1, "RREO6JurosEEncargosDaDivida", coluna)))
        definir("DespesasPrimariasDeCapitalExcetoFontesRPPS", coluna,
                comb((1, "DespesasDeCapitalExcetoFontesRPPS", coluna),
                     (-1, "RREO6ConcessaoDeEmprestimos", coluna),
                     (-1, "RREO6AmortizacaoDaDivida", coluna)))

        termos_total = [(1, "DespesasPrimariasCorrentesExcetoFontesRPPS", coluna),
                        (1, "DespesasPrimariasCorrentesComFontesRPPS", coluna),
                        (1, "DespesasPrimariasDeCapitalExcetoFontesRPPS", coluna),
                        (1, "DespesasPrimariasDeCapitalComFontesRPPS", coluna)]
        termos_exceto = [(1, "DespesasPrimariasCorrentesExcetoFontesRPPS", coluna),
                         (1, "DespesasPrimariasDeCapitalExcetoFontesRPPS", coluna)]
        if ("RREO6ReservaDeContingencia", coluna) in v:
            termos_total.append((1, "RREO6ReservaDeContingencia", coluna))
            termos_exceto.append((1, "RREO6ReservaDeContingencia", coluna))
        definir("RREO6TotalDespesaPrimaria", coluna, comb(*termos_total))
        definir("DespesaPrimariaTotalExcetoFontesRPPS", coluna, comb(*termos_exceto))

    # resultado primário acima da linha: receita primária menos os três pagamentos
    pagamentos = comb((1, "RREO6TotalDespesaPrimaria", PAG_A),
                      (1, "RREO6TotalDespesaPrimaria", RPP_B),
                      (1, "RREO6TotalDespesaPrimaria", PAG_C))
    pagamentos_exc = comb((1, "DespesaPrimariaTotalExcetoFontesRPPS", PAG_A),
                          (1, "DespesaPrimariaTotalExcetoFontesRPPS", RPP_B),
                          (1, "DespesaPrimariaTotalExcetoFontesRPPS", PAG_C))
    receita_primaria = v.get(("RREO6TotalReceitaPrimaria", REC_A))
    receita_primaria_exc = v.get(("ReceitaPrimariaTotalExcetoFontesRPPS", REC_A))
    if pagamentos is not None and receita_primaria is not None:
        definir("ResultadoPrimarioComRPPSAcimaDaLinha", VALOR,
                receita_primaria - pagamentos)
    if pagamentos_exc is not None and receita_primaria_exc is not None:
        definir("ResultadoPrimarioSemRPPSAcimaDaLinha", VALOR,
                receita_primaria_exc - pagamentos_exc)

    # ---------------- quadro da dívida consolidada líquida ----------------
    definir("RestosAPagarProcessadosExcetoPrecatorios", col_bimestre(ano),
            _saldos_rp(ac, ano, mes_ref))
    definir("DemaisHaveresFinanceiros", col_bimestre(ano),
            _haveres(ac, ano, mes_ref))
    definir("ReceitaDeAlienacaoDeInvestimentosPermanentes", VALOR, alienacao_invest)

    # ---------------- células replicáveis do último publicado ----------------
    if publicado:
        abertura, bimestre_col = col_abertura(ano), col_bimestre(ano)
        for cod, colunas in REPLICAVEIS.items():
            for coluna in colunas:
                coluna = coluna.format(abertura=abertura, bimestre=bimestre_col)
                valor = _do_publicado(publicado, cod, coluna, rot)
                if valor is not None:
                    v[(cod, coluna)] = valor

    # ---------------- fórmulas que dependem do publicado ----------------
    for coluna in (col_abertura(ano), col_bimestre(ano)):
        definir("DividaConsolidadaLiquida", coluna,
                comb((1, "DividaConsolidada", coluna),
                     (-1, "DeducoesDaDividaConsolidada", coluna)))
    definir("ResultadoNominalAbaixoDaLinhaSemRPPS", VALOR,
            comb((1, "DividaConsolidadaLiquida", col_abertura(ano)),
                 (-1, "DividaConsolidadaLiquida", col_bimestre(ano))))
    definir("VariacaoSaldoRPP", VALOR,
            comb((1, "RestosAPagarProcessadosExcetoPrecatorios", col_bimestre(ano)),
                 (-1, "RestosAPagarProcessadosExcetoPrecatorios",
                  col_abertura(ano))))

    if chaves_cod:
        return {(cod, coluna, 0): valor for (cod, coluna), valor in v.items()}

    # rótulo: se o ente usa o mesmo texto em duas linhas (AL: metas da LDO),
    # a segunda ocorrência recebe um sufixo para não ser sobrescrita.
    saida: Dict[tuple, float] = {}
    for (cod, coluna), valor in v.items():
        conta = rot[cod]
        chave = (conta, coluna, 0)
        n = 2
        while chave in saida:
            chave = (f"{conta} ({n})", coluna, 0)
            n += 1
        saida[chave] = valor
    return saida


def _do_publicado(publicado: Dict[tuple, float], cod: str,
                  coluna: str, rotulos: Optional[Dict[str, str]] = None
                  ) -> Optional[float]:
    """Valor de ``publicado`` por cod_conta ou por rótulo (nessa ordem)."""
    rot = rotulos or ROTULOS
    for chave in ((cod, coluna), (rot.get(cod, cod), coluna)):
        if chave in publicado:
            try:
                return float(publicado[chave])
            except (TypeError, ValueError):
                return None
    return None


# ---------------------------------------------------------------------------
# leitura e conferência do publicado
# ---------------------------------------------------------------------------
def ler_publicado(caminho: str, por_cod: bool = False
                  ) -> Dict[Tuple[str, str], float]:
    """``{(conta, coluna): valor}`` de um CSV do Siconfi.

    ``por_cod=True`` devolve a chave ``(cod_conta, coluna)`` em vez do rótulo —
    necessário quando o rótulo se repete (Anexo 06 de AL, metas da LDO).
    """
    saida: Dict[Tuple[str, str], float] = {}
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for linha in csv.DictReader(fh, delimiter=";"):
            conta = linha.get("cod_conta") if por_cod else linha.get("conta")
            try:
                saida[(conta, linha["coluna"])] = float(linha["valor"] or 0)
            except (TypeError, ValueError, KeyError):
                continue
    return saida


def conferir(apurado: Dict[tuple, float], publicado: Dict[Tuple[str, str], float],
             tolerancia: float = 0.01):
    """Compara o apurado com o publicado.

    Returns:
        ``(iguais, divergentes, ausentes)`` — ``divergentes`` traz
        ``(conta, coluna, apurado, publicado, diferença)`` e ``ausentes`` traz
        ``(conta, coluna, publicado)`` para as células fora do dicionário.
    """
    iguais: List[tuple] = []
    divergentes: List[tuple] = []
    ausentes: List[tuple] = []
    for (conta, coluna), esperado in publicado.items():
        valor = apurado.get((conta, coluna, 0))
        if valor is None:
            ausentes.append((conta, coluna, esperado))
        elif abs(valor - esperado) <= tolerancia:
            iguais.append((conta, coluna, esperado))
        else:
            divergentes.append((conta, coluna, valor, esperado, valor - esperado))
    return iguais, divergentes, ausentes


# ---------------------------------------------------------------------------
def main(argv: Optional[Sequence[str]] = None) -> int:
    import io

    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    argv = list(sys.argv[1:] if argv is None else argv)
    raiz = argv[0] if argv else os.path.join(RAIZ, "dados", "rr_msc")
    ano = int(argv[1]) if len(argv) > 1 else 2026
    bimestre = int(argv[2]) if len(argv) > 2 else 4
    # o publicado de AL repete o rótulo das metas da LDO: nesse ente a
    # conferência é feita por cod_conta
    por_cod = (uf_da_raiz(raiz) or "RR") != "RR"

    apurado = celulas(raiz, ano, bimestre, chaves_cod=por_cod)
    print(f"MSC: {raiz}")
    print(f"exercício {ano} — {bimestre}º bimestre")
    print(f"células apuradas na MSC: {len(apurado)}")

    candidatos = [argv[3]] if len(argv) > 3 else []
    candidatos.append(os.path.join(RAIZ, "dados", "rr_rreo_pub", str(ano),
                                   f"RREO_14_{ano}_bim{bimestre}_anexo06.csv"))
    publicado = next((ler_publicado(c, por_cod=por_cod)
                      for c in candidatos if c and os.path.exists(c)), None)
    if not publicado:
        return 0

    completo = celulas(raiz, ano, bimestre, publicado=publicado,
                       chaves_cod=por_cod)
    print(f"células com o publicado (previsão/metas/abertura/saldo anterior): "
          f"{len(completo)}")
    iguais, divergentes, ausentes = conferir(completo, publicado)
    print(f"conferência: {len(iguais)} iguais, {len(divergentes)} divergentes, "
          f"{len(ausentes)} fora do dicionário")
    for conta, coluna, valor, esperado, dif in sorted(
            divergentes, key=lambda x: -abs(x[4]))[:20]:
        print(f"  DIV {conta[:54]:<56} {coluna[:22]:<24} "
              f"apurado={valor:>16,.2f} publicado={esperado:>16,.2f} "
              f"dif={dif:>14,.2f}")
    for conta, coluna, esperado in sorted(ausentes)[:25]:
        print(f"  --- {conta[:54]:<56} {coluna[:22]:<24} "
              f"publicado={esperado:>16,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
