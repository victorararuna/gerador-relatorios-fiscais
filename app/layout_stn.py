# -*- coding: utf-8 -*-
"""Layout oficial dos demonstrativos do RGF, transcrito do arquivo do Siconfi.

Estrutura extraída do RGF 2024 Q3 homologado (abas "RGF-Anexo 01" e
"RGF-Anexo 02") e dos rótulos do relatório impresso.
"""
from __future__ import annotations

IDENTIFICACAO = [
    ("RGF", "RELATÓRIO DE GESTÃO FISCAL"),
    ("VERSÃO", "v12"),
    ("VIGÊNCIA", "04/01/2024"),
    ("Ente", "24 - Rio Grande do Norte"),
    ("Poder", "E - Executivo"),
    ("Instituição", "171 - Governo do Estado do Rio Grande do Norte"),
    ("Exercício", "2024"),
    ("Periodicidade", "QUADRIMESTRAL"),
    ("Período", "3º quadrimestre"),
]

# ---------------------------------------------------------------------------
# RGF - Anexo 1
# ---------------------------------------------------------------------------
ANEXO1 = {
    "titulo": "RGF - ANEXO 1 (LRF, art. 55, inciso I, alínea \u201ca\u201d)",
    "grupo": "Grupo: Tabela 1.0 - Demonstrativo da Despesa com Pessoal",
    "quadro": "Quadro: Despesa com Pessoal",
    "rotulo": "Rótulo: Padrão",
    "subtitulo": "Despesa com Pessoal",
    "unidade": "R$ 1,00",
    "coluna_valor": 14,
    "colunas": [
        ("DESPESA COM PESSOAL", 56),
        ("<MR-11>", 13), ("<MR-10>", 13), ("<MR-9>", 13), ("<MR-8>", 13),
        ("<MR-7>", 13), ("<MR-6>", 13), ("<MR-5>", 13), ("<MR-4>", 13),
        ("<MR-3>", 13), ("<MR-2>", 13), ("<MR-1>", 13), ("<MR>", 13),
        ("TOTAL (ÚLTIMOS 12 MESES)", 18),
        ("INSCRITAS EM RP NÃO PROCESSADOS", 16),
    ],
    "linhas": [
        ("total", "DESPESA BRUTA COM PESSOAL (I)", "bruta", 0),
        ("linha", "Pessoal Ativo", None, 1),
        ("linha", "Vencimentos, Vantagens e Outras Despesas Variáveis", "vencimentos", 2),
        ("linha", "Obrigações Patronais", "patronal", 2),
        ("linha", "Pessoal Inativo e Pensionistas", None, 1),
        ("linha", "Aposentadorias, Reserva e Reformas", "aposentadorias", 2),
        ("linha", "Pensões", "pensoes", 2),
        ("linha", "Outras Despesas de Pessoal decorrentes de Contratos de "
                  "Terceirização ou de Contratação de Forma Indireta (§ 1º do art. 18 da LRF)",
         "terceirizacao", 1),
        ("linha", "Despesa com Pessoal não Executada Orçamentariamente", "nao_executada", 1),
        ("total", "DESPESAS NÃO COMPUTADAS (§ 1º do art. 19 da LRF) (II)", "deducoes", 0),
        ("linha", "Indenizações por Demissão e Incentivos à Demissão Voluntária",
         "indenizacoes", 1),
        ("linha", "Decorrentes de Decisão Judicial de Período Anterior ao da Apuração",
         "judiciais", 1),
        ("linha", "Despesas de Exercícios Anteriores de Período Anterior ao da Apuração",
         "exercicios_anteriores", 1),
        ("linha", "Inativos e Pensionistas com Recursos Vinculados", "vinculados", 1),
        ("linha", "Agentes Comunitários de Saúde e de Combate às Endemias com Recursos "
                  "Vinculados (CF, art. 198, § 11)", None, 1),
        ("linha", "Parcela dedutível referente ao piso salarial do Enfermeiro, Técnico de "
                  "Enfermagem, Auxiliar de Enfermagem e Parteira (ADCT, art. 38)",
         "piso_enfermagem", 1),
        ("linha", "Outras Deduções Constitucionais ou Legais", None, 1),
        ("total", "DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)", "liquida", 0),
    ],
    # quadro 2 - apuracao do limite
    "limite_titulo": "DTP e Apuração do Cumprimento do Limite Legal",
    "limite_linhas": [
        ("linha", "RECEITA CORRENTE LIQUIDA - RCL (IV)", "rcl", 0),
        ("linha", "(-) Transferências Obrigatórias da União Relativas às Emendas Individuais "
                  "(art. 166-A, § 1º, da CF)", "emendas_individuais", 1),
        ("linha", "(-) Transferências obrigatórias da União relativas às emendas de bancada "
                  "(art. 166, § 16, da CF)", "emendas_bancada", 1),
        ("linha", "(-) Transferências da União relativas à remuneração dos agentes "
                  "comunitários de saúde e de combate às endemias", None, 1),
        ("linha", "(-) Outras Deduções Constitucionais ou Legais", None, 1),
        ("total", "= RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DA "
                  "DESPESA COM PESSOAL (VI)", "rcl_ajustada", 0),
        ("total", "DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)", "dtp", 0),
        ("linha", "LIMITE MÁXIMO (VII) (incisos I, II e III, art. 20 da LRF)", "limite_max", 0),
        ("linha", "LIMITE PRUDENCIAL (VIII) = (0,95 x VII)", "limite_prudencial", 0),
        ("linha", "LIMITE DE ALERTA (IX) = (0,90 x VII)", "limite_alerta", 0),
    ],
}

# ---------------------------------------------------------------------------
# RGF - Anexo 2
# ---------------------------------------------------------------------------
ANEXO2 = {
    "titulo": "RGF - ANEXO 2 (LRF, art. 55, inciso I, alínea \u201cb\u201d)",
    "grupo": "Grupo: Tabela 2.0 - Demonstrativo da Dívida Consolidada Líquida",
    "quadro": "Quadro: Cálculo da Dívida Consolidada Líquida",
    "rotulo": "Rótulo: Padrão",
    "subtitulo": "Demonstrativo da Dívida Consolidada Líquida",
    "unidade": "Estados, DF e Municípios",
    "coluna_valor": 5,
    "colunas": [
        ("DÍVIDA CONSOLIDADA LÍQUIDA", 62),
        ("SALDO DO EXERCÍCIO ANTERIOR", 19),
        ("Até o 1º Quadrimestre", 19),
        ("Até o 2º Quadrimestre", 19),
        ("Até o 3º Quadrimestre", 19),
    ],
    "linhas": [
        ("total", "DÍVIDA CONSOLIDADA - DC (I)", "divida", 0),
        ("linha", "Dívida Mobiliária", "divida_mobiliaria", 1),
        ("linha", "Dívida Contratual", "divida_contratual", 1),
        ("linha", "Empréstimos", "emprestimos", 2),
        ("linha", "Internos", "emprestimos_internos", 3),
        ("linha", "Externos", "emprestimos_externos", 3),
        ("linha", "Reestruturação da Dívida de Estados e Municípios",
         "reestruturacao", 2),
        ("linha", "Financiamentos", None, 2),
        ("linha", "Internos", None, 3),
        ("linha", "Externos", None, 3),
        ("linha", "Parcelamento e Renegociação de Dívidas", "parcelamentos", 2),
        ("linha", "De Tributos", "parc_tributos", 3),
        ("linha", "De Contribuições Previdenciárias", "parc_previdenciarias", 3),
        ("linha", "De Demais Contribuições Sociais", None, 3),
        ("linha", "Do FGTS", None, 3),
        ("linha", "Com Instituição Não Financeira", "parc_inst_financeira", 3),
        ("linha", "Demais Dívidas Contratuais", None, 2),
        ("linha", "Precatórios Posteriores a 05/05/2000 (inclusive) Vencidos e Não Pagos",
         "precatorios", 1),
        ("linha", "Outras Dívidas", "outras_dividas", 1),
        ("total", "DEDUÇÕES (II)", "deducoes_dcl", 0),
        ("linha", "Disponibilidade de Caixa", "disp_caixa", 1),
        ("linha", "Disponibilidade de Caixa Bruta", "disp_bruta", 2),
        ("linha", "(-) Restos a Pagar Processados", "rp_processados", 2),
        ("linha", "(-) Depósitos Restituíveis e Valores Vinculados", "depositos", 2),
        ("linha", "Demais Haveres Financeiros", "haveres", 1),
        ("total", "DÍVIDA CONSOLIDADA LÍQUIDA (DCL) (III) = (I - II)", "dcl", 0),
        ("linha", "RECEITA CORRENTE LÍQUIDA - RCL (IV)", "rcl", 0),
        ("linha", "(-) Transferências Obrigatórias da União Relativas às Emendas "
                  "Individuais (art. 166-A, § 1º, da CF) (V)", "emendas_dcl", 1),
        ("total", "RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DE "
                  "ENDIVIDAMENTO (VI) = (IV - V)", "rcl_ajustada_dcl", 0),
        ("linha", "% da DC sobre a RCL AJUSTADA (I/VI)", "pct_dc", 0),
        ("linha", "% da DCL sobre a RCL AJUSTADA (III/VI)", "pct_dcl", 0),
        ("linha", "LIMITE DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL", "limite", 0),
        ("linha", "LIMITE DE ALERTA (inciso III do § 1º do art. 59 da LRF)",
         "limite_alerta", 0),
        ("total", "Outros Valores Não Integrantes da DC", None, 0),
        ("linha", "Precatórios Anteriores a 05/05/2000", None, 1),
        ("linha", "Precatórios Posteriores a 05/05/2000 (Não incluídos na DC)",
         "precatorios_fora", 1),
        ("linha", "Passivo Atuarial", "passivo_atuarial", 1),
        ("linha", "RP Não-Processados", "rp_nao_processados", 1),
        ("linha", "Antecipações de Receita Orçamentária - ARO", None, 1),
        ("linha", "Dívida Contratual de PPP", "ppp", 1),
    ],
}

# referencia do RGF 2024 Q3 homologado
REFERENCIA = {
    "Anexo 1": {
        "bruta": 13809083609.68, "vencimentos": 5727095551.73,
        "patronal": 2086640219.87, "aposentadorias": 4563063878.92,
        "pensoes": 803877241.85, "terceirizacao": 173463616.26,
        "nao_executada": 454943101.05, "deducoes": 3893336376.99,
        "indenizacoes": 25011201.14, "judiciais": 497754595.25,
        "exercicios_anteriores": 181744273.43, "vinculados": 3121824884.26,
        "piso_enfermagem": 67001422.91, "liquida": 9915747232.69,
        "rcl": 17259989216.73, "emendas_individuais": 4802839.15,
        "emendas_bancada": 22049553.00, "rcl_ajustada": 17233040024.58,
        "dtp": 9919747911.85, "limite_max": 8444189612.04,
        "limite_prudencial": 8021980131.44, "limite_alerta": 7599770650.84,
    },
    "Anexo 2": {
        "divida": 7201713061.97, "divida_mobiliaria": 0.0,
        "divida_contratual": 3565766102.01, "emprestimos": 2734195879.84,
        "emprestimos_internos": 912009325.13, "emprestimos_externos": 1822186554.71,
        "reestruturacao": 663224116.18, "parcelamentos": 168346105.99,
        "parc_tributos": 24706052.80, "parc_previdenciarias": 1190238.22,
        "parc_inst_financeira": 142449814.97, "precatorios": 3214637210.88,
        "outras_dividas": 421309749.08, "deducoes_dcl": 269271015.89,
        "disp_caixa": 0.0, "disp_bruta": 1536331084.82,
        "rp_processados": 1025632163.82, "depositos": 510698921.00,
        "haveres": 269271015.89, "dcl": 6932442046.08,
        "rcl": 17259892416.73, "emendas_dcl": 4802839.15,
        "rcl_ajustada_dcl": 17255089577.58, "pct_dc": 0.4174,
        "pct_dcl": 0.4018, "limite": 34510179155.16,
        "limite_alerta": 31059161239.64,
    },
}


# ---------------------------------------------------------------------------
# RGF - Anexo 3 - Garantias e Contragarantias
# ---------------------------------------------------------------------------
ANEXO3 = {
    "titulo": "RGF - ANEXO 3 (LRF, art. 55, inciso I, alínea \u201cc\u201d)",
    "grupo": "Grupo: Tabela 3.0 - Demonstrativo das Garantias e Contragarantias de Valores",
    "quadro": "Quadro: Saldos das Garantias Concedidas e Contragarantias Recebidas",
    "rotulo": "Rótulo: Padrão",
    "subtitulo": "Garantias Concedidas e Contragarantias Recebidas",
    "unidade": "Estados, DF e Municípios",
    "coluna_valor": 5,
    "colunas": [
        ("GARANTIAS E CONTRAGARANTIAS", 62),
        ("SALDO DO EXERCÍCIO ANTERIOR", 19),
        ("Até o 1º Quadrimestre", 19),
        ("Até o 2º Quadrimestre", 19),
        ("Até o 3º Quadrimestre", 19),
    ],
    "linhas": [
        ("total", "Garantias Concedidas", None, 0),
        ("linha", "AOS ESTADOS (I)", "gar_estados", 1),
        ("linha", "Em Operações de Crédito Externas", "gar_estados_ext", 2),
        ("linha", "Em Operações de Crédito Internas", "gar_estados_int", 2),
        ("linha", "AOS MUNICÍPIOS (II)", "gar_municipios", 1),
        ("linha", "Em Operações de Crédito Externas", "gar_municipios_ext", 2),
        ("linha", "Em Operações de Crédito Internas", "gar_municipios_int", 2),
        ("linha", "ÀS ENTIDADES CONTROLADAS (III)", "gar_controladas", 1),
        ("linha", "Em Operações de Crédito Externas", "gar_controladas_ext", 2),
        ("linha", "Em Operações de Crédito Internas", "gar_controladas_int", 2),
        ("linha", "POR MEIO DE FUNDOS E PROGRAMAS (IV)", "gar_fundos", 1),
        ("total", "TOTAL GARANTIAS CONCEDIDAS (V) = (I + II + III + IV)", "gar_total", 0),
        ("linha", "RECEITA CORRENTE LÍQUIDA - RCL (VI)", "rcl", 0),
        ("linha", "(-) Transferências Obrigatórias da União Relativas às Emendas "
                  "Individuais (art. 166-A, § 1º, da CF) (VII)", "gar_emendas", 1),
        ("total", "RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DE "
                  "ENDIVIDAMENTO (VIII) = (VI - VII)", "gar_rcl_ajustada", 0),
        ("linha", "% do TOTAL DAS GARANTIAS sobre a RCL AJUSTADA (V/VIII)", "gar_pct", 0),
        ("linha", "LIMITE DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL", "gar_limite", 0),
        ("linha", "LIMITE DE ALERTA (inciso III § 1º do art. 59 da LRF)",
         "gar_limite_alerta", 0),
        ("total", "Contragarantias Recebidas", None, 0),
        ("linha", "DOS ESTADOS (IX)", "contra_estados", 1),
        ("linha", "Em Garantia às Operações de Crédito Externas", "contra_estados_ext", 2),
        ("linha", "Em Garantia às Operações de Crédito Internas", "contra_estados_int", 2),
        ("linha", "DOS MUNICÍPIOS (X)", "contra_municipios", 1),
        ("linha", "Em Garantia às Operações de Crédito Externas", "contra_municipios_ext", 2),
        ("linha", "Em Garantia às Operações de Crédito Internas", "contra_municipios_int", 2),
        ("linha", "DAS ENTIDADES CONTROLADAS (XI)", "contra_controladas", 1),
        ("linha", "Em Garantia às Operações de Crédito Externas", "contra_controladas_ext", 2),
        ("linha", "Em Garantia às Operações de Crédito Internas", "contra_controladas_int", 2),
        ("linha", "EM GARANTIAS POR MEIO DE FUNDOS E PROGRAMAS (XII)", "contra_fundos", 1),
        ("total", "TOTAL CONTRAGARANTIAS RECEBIDAS (XIII) = (IX + X + XI + XII)",
         "contra_total", 0),
    ],
}

REFERENCIA["Anexo 3"] = {
    "gar_total": 0.0,
    "rcl": 17259892416.73,
    "gar_emendas": 4802839.15,
    "gar_rcl_ajustada": 17255089577.58,
    "gar_pct": 0.0,
    "gar_limite": 3796119707.07,
    "gar_limite_alerta": 3416507736.36,
    "contra_total": 0.0,
}


# ---------------------------------------------------------------------------
# RGF - Anexo 4 - Operacoes de Credito
# ---------------------------------------------------------------------------
ANEXO4 = {
    "titulo": "RGF - ANEXO 4 (LRF, art. 55, inciso I, alínea \u201cd\u201d)",
    "grupo": "Grupo: Tabela 4.0 - Demonstrativo das Operações de Crédito",
    "quadro": "Quadro: Valor Realizado no Período",
    "rotulo": "Rótulo: Padrão",
    "subtitulo": "Operações de Crédito",
    "unidade": "Estados, DF e Municípios",
    "coluna_valor": 3,
    "colunas": [
        ("OPERAÇÕES DE CRÉDITO", 70),
        ("No Quadrimestre de Referência", 24),
        ("Até o Quadrimestre de Referência (a)", 26),
    ],
    "linhas": [
        ("total", "Operações de Crédito", None, 0),
        ("linha", "Mobiliária", "oc_mobiliaria", 1),
        ("linha", "Interna", "oc_mobiliaria_interna", 2),
        ("linha", "Externa", "oc_mobiliaria_externa", 2),
        ("linha", "Contratual", "oc_contratual", 1),
        ("linha", "Interna", "oc_contratual_interna", 2),
        ("linha", "Empréstimos", "oc_emprestimos", 3),
        ("linha", "Aquisição Financiada de Bens e Arrendamento Mercantil Financeiro",
         "oc_aquisicao", 3),
        ("linha", "Antecipação de Receita pela Venda a Termo de Bens e Serviços",
         "oc_antecipacao", 3),
        ("linha", "Assunção, Reconhecimento e Confissão de Dívidas (LRF, art. 29, § 1º)",
         "oc_assuncao", 3),
        ("linha", "Externa", None, 2),
        ("linha", "Operações de Crédito não sujeitas ao limite para fins de contratação (I)",
         "oc_nao_sujeitas_1", 1),
        ("linha", "Externa", None, 2),
        ("linha", "Empréstimos", None, 3),
        ("linha", "Aquisição Financiada de Bens e Arrendamento Mercantil Financeiro",
         None, 3),
        ("linha", "Antecipações de Receitas pela Venda a Termo de Bens e Serviços",
         None, 3),
        ("linha", "Assunção, Reconhecimento e Confissão de Dívidas (LRF, art. 29, § 1º)",
         None, 3),
        ("linha", "Operações de crédito não sujeitas ao limite para fins de contratação (II)",
         "oc_nao_sujeitas_2", 1),
        ("total", "TOTAL (III)", "oc_total", 0),
        ("vazio", "", None, 0),
        ("total", "Apuração do Cumprimento dos Limites", None, 0),
        ("linha", "RECEITA CORRENTE LÍQUIDA - RCL (IV)", "rcl", 0),
        ("linha", "(-) Transferências Obrigatórias da União Relativas às Emendas "
                  "Individuais (art. 166-A, § 1º, da CF) (V)", "oc_emendas", 1),
        ("total", "RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DE "
                  "ENDIVIDAMENTO (VI) = (IV - V)", "oc_rcl_ajustada", 0),
        ("linha", "OPERAÇÕES VEDADAS (VII)", "oc_vedadas", 0),
        ("total", "TOTAL CONSIDERADO PARA FINS DA APURAÇÃO DO CUMPRIMENTO DO LIMITE "
                  "(VIII) = (IIIa + VII - Ia - IIa)", "oc_considerado", 0),
        ("linha", "LIMITE GERAL DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL PARA AS "
                  "OPERAÇÕES DE CRÉDITO INTERNAS E EXTERNAS", "oc_limite", 0),
        ("linha", "LIMITE DE ALERTA (inciso III do § 1º do art. 59 da LRF)",
         "oc_limite_alerta", 0),
        ("linha", "OPERAÇÕES DE CRÉDITO POR ANTECIPAÇÃO DA RECEITA ORÇAMENTÁRIA",
         "oc_aro", 0),
        ("linha", "LIMITE DEFINIDO POR RESOLUÇÃO DO SENADO FEDERAL PARA AS OPERAÇÕES "
                  "DE CRÉDITO POR ANTECIPAÇÃO DA RECEITA ORÇAMENTÁRIA", "oc_aro_limite", 0),
    ],
}


REFERENCIA["Anexo 4"] = {
    "oc_mobiliaria": 0.0,
    "oc_contratual": 429228593.51,
    "oc_contratual_interna": 429228593.51,
    "oc_emprestimos": 429228593.51,
    "oc_nao_sujeitas_1": 0.0,
    "oc_nao_sujeitas_2": 0.0,
    "oc_total": 429228593.51,
    "rcl": 17259892416.73,
    "oc_emendas": 4802839.15,
    "oc_rcl_ajustada": 17255089577.58,
    "oc_vedadas": 0.0,
    "oc_considerado": 429228593.51,
    "oc_limite": 2760814332.41,
    "oc_limite_alerta": 2484732899.17,
    "oc_aro": 0.0,
    "oc_aro_limite": 1207856270.43,
}


# ---------------------------------------------------------------------------
# RGF - Anexo 5 - Disponibilidade de Caixa e Restos a Pagar
# ---------------------------------------------------------------------------
ANEXO5 = {
    "titulo": "RGF - ANEXO 5 (LRF, art. 55, inciso III, alíneas \u201ca\u201d e \u201cb\u201d)",
    "grupo": "Grupo: Tabela 5.0 - Demonstrativo da Disponibilidade de Caixa e dos Restos a Pagar",
    "quadro": "Quadro: Disponibilidade de Caixa e Restos a Pagar",
    "rotulo": "Rótulo: Padrão",
    "subtitulo": "Disponibilidade de Caixa e Restos a Pagar",
    "unidade": "R$ 1,00",
    "coluna_valor": 2,
    "colunas": [
        ("IDENTIFICAÇÃO DOS RECURSOS", 56),
        ("Disponibilidade de Caixa Bruta (a)", 18),
        ("RP Liquidados e Não Pagos de Exercícios Anteriores (b)", 18),
        ("RP Liquidados e Não Pagos do Exercício (c)", 18),
        ("RP Empenhados e Não Liquidados (d)", 18),
        ("Demais Obrigações Financeiras (e)", 18),
        ("Consórcio Público (f)", 14),
        ("(g) = (a - (b+c+d+e) - f)", 18),
    ],
    "linhas": [
        ("total", "TOTAL DOS RECURSOS NÃO VINCULADOS (I)", "a5_nao_vinculados", 0),
        ("linha", "Recursos Não Vinculados de Impostos", "a5_impostos", 1),
        ("linha", "Outros Recursos não Vinculados", "a5_outros_nao_vinculados", 1),
        ("total", "TOTAL DOS RECURSOS VINCULADOS (EXCETO AO RPPS) (II)",
         "a5_vinculados", 0),
        ("linha", "Recursos Vinculados à Educação", "a5_educacao", 1),
        ("linha", "Transferências do FUNDEB", "a5_fundeb", 2),
        ("linha", "Outros Recursos Vinculados à Educação", "a5_outros_educacao", 2),
        ("linha", "Recursos Vinculados à Saúde", "a5_saude", 1),
        ("linha", "Transferências Fundo a Fundo de Recursos do SUS", "a5_sus", 2),
        ("linha", "Outros Recursos Vinculados à Saúde", "a5_outros_saude", 2),
        ("linha", "Recursos Vinculados à Assistência Social", "a5_assistencia", 1),
        ("linha", "Recursos Vinculados à Previdência Social (Exceto ao RPPS)",
         "a5_previdencia", 1),
        ("linha", "Demais Vinculações Decorrentes de Transferências", "a5_transferencias", 1),
        ("linha", "Transferências de Convênios e Instrumentos Congêneres (exceto "
                  "Educação, Saúde e Assistência)", "a5_convenios", 2),
        ("linha", "Outras Vinculações Decorrentes de Transferências",
         "a5_outras_transferencias", 2),
        ("linha", "Demais Vinculações Legais", "a5_legais", 1),
        ("linha", "Recursos de Operações de Crédito (exceto vinculados à Educação "
                  "e à Saúde)", "a5_op_credito", 2),
        ("linha", "Recursos de Alienação de Bens/Ativos", "a5_alienacao", 2),
        ("linha", "Recursos Vinculados a Fundos (exceto Educação, Saúde, Assistência "
                  "e Previdência)", "a5_fundos", 2),
        ("linha", "Outras Vinculações Legais", "a5_outras_legais", 2),
        ("linha", "Recursos Extraorçamentários", "a5_extraorcamentarios", 1),
        ("linha", "Outras Vinculações", "a5_outras_vinculacoes", 1),
        ("total", "TOTAL DOS RECURSOS VINCULADOS AO RPPS (III)", "a5_rpps", 0),
    ],
}

# ---------------------------------------------------------------------------
# RGF - Anexo 6 - Demonstrativo Simplificado
# ---------------------------------------------------------------------------
ANEXO6 = {
    "titulo": "RGF - ANEXO 6 (LRF, art. 55, inciso III, alínea \u201cc\u201d)",
    "grupo": "Grupo: Tabela 6.0 - Demonstrativo Simplificado do Relatório de Gestão Fiscal",
    "quadro": "Quadro: Operações de Crédito",
    "rotulo": "Rótulo: Padrão",
    "subtitulo": "Demonstrativo Simplificado do Relatório de Gestão Fiscal",
    "unidade": "R$ 1,00",
    "coluna_valor": 2,
    "colunas": [
        ("DEMONSTRATIVO SIMPLIFICADO", 64),
        ("VALOR ATÉ O QUADRIMESTRE DE REFERÊNCIA", 24),
        ("% SOBRE A RCL AJUSTADA", 20),
    ],
    "linhas": [
        ("total", "Operações de Crédito", None, 0),
        ("linha", "Operações de Crédito Internas e Externas", "a6_oc", 1),
        ("linha", "Limite Definido pelo Senado Federal para Operações de Crédito "
                  "Externas e Internas", "a6_oc_limite", 1),
        ("linha", "Operações de Crédito por Antecipação da Receita", "a6_aro", 1),
        ("linha", "Limite Definido pelo Senado Federal para Operações de Crédito por "
                  "Antecipação da Receita", "a6_aro_limite", 1),
        ("total", "Restos a Pagar e Disponibilidade de Caixa", None, 0),
        ("linha", "Restos a Pagar Empenhados e Não Liquidados do Exercício",
         "a6_rp", 1),
        ("linha", "Disponibilidade de Caixa Líquida (após a inscrição em restos a "
                  "pagar não processados do exercício)", "a6_disp", 1),
    ],
}


REFERENCIA["Anexo 5"] = {
    "a5_nao_vinculados": 189073943.32, "a5_impostos": 191572896.56,
    "a5_outros_nao_vinculados": -2498953.24, "a5_vinculados": 943599290.84,
    "a5_educacao": 215792698.02, "a5_fundeb": 13644419.38,
    "a5_outros_educacao": 202148278.64, "a5_saude": 258412337.41,
    "a5_sus": 237832004.66, "a5_outros_saude": 20580332.75,
    "a5_assistencia": 25646530.50, "a5_previdencia": 39286.58,
    "a5_transferencias": 333661474.83, "a5_convenios": 136659412.43,
    "a5_outras_transferencias": 197002062.40, "a5_legais": 89742325.07,
    "a5_op_credito": 29080994.53, "a5_alienacao": 106491.95,
    "a5_fundos": 45518517.30, "a5_outras_legais": 15036321.29,
    "a5_extraorcamentarios": 20304638.43, "a5_outras_vinculacoes": 0.0,
    "a5_rpps": 72056616.42,
}

REFERENCIA["Anexo 6"] = {
    "a6_oc": 429228593.51, "a6_oc_limite": 2760814332.41,
    "a6_aro": 0.0, "a6_aro_limite": 1207856270.43,
    "a6_rp": 344186947.20, "a6_disp": -2451355160.94,
}
