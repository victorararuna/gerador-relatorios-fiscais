# Revisão geral do motor de demonstrativos fiscais do RN

Documento de 13/11/2026. **Ponto de entrada único**: consolida o que foi
descoberto, o que está verificado e o que resta. Substitui a leitura dispersa
dos demais documentos.

---

## 1. As quatro origens de dado

O trabalho só avançou quando ficou claro que existem **quatro** fontes, e que
cada linha de cada anexo bebe de uma delas.

| origem | onde está | o que fornece |
|---|---|---|
| **MSC** (matriz de saldos contábeis) | `dados/acervo` | execução orçamentária e saldos, formato longo |
| **Balancete** (SIGEF) | `dados/fontes/13nov` | saldo por conta, com todos os níveis |
| **Mapeamentos STN** (MDF 15ª ed.) | `dados/mapeamentos` | de-para linha do anexo → conta × natureza |
| **Planilhas de trabalho da equipe** | `RELATÓRIOS CONTAG` | memória de cálculo por anexo |

Regra que se confirmou quatro vezes: **quando o número não fecha, a resposta
está na planilha da equipe, não no CSV do Siconfi.**

---

## 2. Situação por anexo

### Verificado ao centavo (contra o homologado)

| anexo | linhas | desvio |
|---|---|---:|
| RREO Anexo 1 — despesa | 4 grupos + total | **0,00** |
| RREO Anexo 1 — receita | total e itens | **0,00** |
| RREO Anexo 2 — função | 23 funções (2025) e total de 2026 | **0,00** |
| RREO Anexo 3 — RCL | 5 linhas, 2025 e 2026 | **0,00** |
| RREO Anexo 4 — previdenciário | 4 linhas (com o PAE) | **0,00** |
| RREO Anexo 7 — restos a pagar | 5 linhas, 2025 e 2026 | **0,00** |
| RREO Anexo 9 — despesa de capital | 4 linhas | **0,00** |
| RREO Anexo 13 — PPP | 7 valores e 6 projeções | **0,00** |
| RREO Anexo 14 — simplificado | 6 linhas, 2025 e 2026 | **0,00** |
| RGF Anexo 1 — despesa com pessoal | 10 meses, I/II/III | **0,00** |
| RGF Anexo 3 — garantias | 5 linhas | **0,00** |
| RGF Anexo 4 — limites | 3 limites | **0,00** |
| RGF Anexo 5 — disponibilidade | 90 células e 5 totais | **0,00** |
| RGF Anexo 6 — limites | 3 limites | **0,00** |

### Apurado com desvio pequeno e documentado

| anexo | situação |
|---|---|
| **RGF Anexo 1 — pessoal** | **exato em 10/10 meses** (I, II e III); abril a −5.241,65, documentado |
| **RREO Anexo 4 — previdenciário** | **4/4 exatas** desde que se deduza o PAE (31.90.92.02 e .06) |
| **RGF Anexo 2 — DCL** | **11 de 14 linhas exatas**; as 3 com causa escrita |
| **RGF Anexo 5 — disponibilidade** | **90 de 90 células** e os 5 totais contra o Siconfi |

### Aberto

| anexo | o que falta |
|---|---|
| RREO Anexo 1 completo | 47 de 105 linhas no aplicador de mapeamento |
| RREO Anexo 9 — receita | separar operação nova de refinanciamento |
| RREO Anexo 13 — PPP | cadastro de contratos |
| RGF Anexo 5 — quebra por vinculação | rodar as 27 linhas do MAPEAMENTO com as contas da classe 8 |

---

## 3. Como cada anexo é apurado

| anexo | fonte | critério |
|---|---|---|
| RREO 1 despesa | MSC classe 6 | conta 62213 por grupo de natureza |
| RREO 1 receita | MSC classe 6 | conta 6212/6213 + natureza (mapeamento) |
| RREO 2 | MSC classe 6 | conta de liquidação + função |
| RREO 3 | RREO Anexo 3 | RCL menos deduções publicadas |
| RREO 7 | MSC classe 6 | contas 6.3.1 / 6.3.2 |
| RREO 9 | MSC classe 6 | 62213 por natureza 44/45/46 |
| RREO 14 | MSC classe 6 | empenhado, liquidado, pago |
| RREO 4 | MSC + mapeamento | ND × FS (função+subfunção) × FR × CO |
| RGF 1 | MSC classes 3/4/6 + class 8 | janela móvel de 12 meses |
| RGF 2 | **balancete** | base de 301 contas da planilha |
| RGF 3/4/6 | RCL | limites da LRF |
| RGF 5 | MSC + classe 8 + balancete | MAPEAMENTO: conta × fonte |

---

## 4. As cinco armadilhas

### 4.1 Sinal do passivo
Contas da classe 2 têm saldo **credor**; no balancete o crédito vem negativo.
Sem inverter, toda linha de dívida sai com o dobro do desvio. Foi o que
derrubou metade do Anexo 2.

### 4.2 Nível da conta
O prefixo `6321` casa com `6.3.2.1.0` **e** `6.3.2.1.1` — soma em dobro. A MSC
já vem agregada em 9 dígitos; o balancete, não. Regra:
**MSC → prefixo de 9 dígitos; balancete → conta exata.**

### 4.3 Fonte errada
A matriz não tem a dívida analítica (classe 2 com 128 contas apenas). O DCL
nasce do **balancete**. Já a receita e a despesa nascem da **matriz**.

### 4.4 Referência errada
Dois valores que usei como "oficial" estavam errados, ambos vindos do CSV do
Siconfi sem conferir o que representavam:

- **pensões militares**: eu usava 119,9 mi; o correto é 250,9 mi — e nossa
  apuração já batia;
- **dívida mobiliária**: eu usava 2.205,1 mi; o correto é **zero**.

### 4.5 Escopo
Linha oficial pode ser subconjunto. "Demais Dívidas Contratuais" é zero no
demonstrativo embora as contas somem 272,3 mi — o ente as classifica em
"Outras Dívidas". Não é erro de soma.

---

## 5. O que está aberto, com o próximo passo

| # | item | próximo passo |
|---|---|---|
| 1 | Anexo 2 — Empréstimos Internos (−32,9 mi) | localizar a conta de encargos negativa |
| 2 | Anexo 2 — RP processados | usar as abas `RP` / `RP_MSC` (execução orçamentária) |
| 3 | Anexo 5 — coluna (e) | rodar 8.2.1.1.3.02/03 por fonte |
| 4 | Anexo 5 — quebra por vinculação | 27 linhas do MAPEAMENTO × contas classe 8 |
| 5 | RREO 1 — 47/105 linhas | blocos duplicados e bloco intra no aplicador |
| 6 | RREO 9 — receita | atributo de refinanciamento |

---

## 6. Como executar

```bash
python verificar_tudo.py                 # 27 conferências de ponta a ponta
python rreo_anexo4_blocos.py             # RREO Anexo 4 (4 linhas)
python rgf_anexo2_dcl.py                 # RGF Anexo 2 (balancete)
python rgf_anexo5_disp.py                # RGF Anexo 5 (mapeamento)
python gerar_rreo.py --ano 2026 --bimestre 4
python gerar_consolidado.py --ano 2025 --quadrimestre 3
```

**Testes**: 41 (leitor 14, Anexo 1 15, Anexo 3 3, limites 9) — todos verdes.

---

## 7. Histórico de conclusões que mudaram

Registro para quem retomar não repetir o caminho:

| eu concluí | na verdade |
|---|---|
| mapeamento do RGF Anexo 2 não é público | está na aba "Anexo 2 - RGF BASE" |
| faltam blocos de receita no material | estão no mapeamento do RREO Anexo 01 |
| Anexo 4 exige atributo civil/militar | é a subfunção 272/274 (FS) |
| classe 8 não serve ao Anexo 5 | é a fonte da coluna (e) |
| Anexo 1 e Anexo 6 são inconsistentes (3,2 mi) | diferença é o RPNP, por regra |
| linha de exercícios anteriores se repete | é a alocação de dezembro, por regra |
| pensões militares 2,05× acima | a referência é que estava errada |
| dívida mobiliária de 2,2 bi | é zero |

**Padrão**: em todas, o dado existia. O que faltava era saber onde olhar.

---

## 8. Item 4 executado — quebra por vinculação do Anexo 5

Implementado em `rgf_anexo5_vinculacao.py`. Cada linha do anexo é um filtro de
**fonte de recursos** (posição 2, lista de valores); as colunas vêm do
MAPEAMENTO.

| coluna | contas |
|---|---|
| (b) RP liquidados | 6321, 6313 |
| (c) RP do exercício | 6327 |
| (d) RP não liquidados | 6311, 6312 |

**Resultado: 46 de 54 células exatas** (19 linhas × 3 colunas), contra o QUADRO
PRINCIPAL.

As oito divergências:

| linha | coluna | diferença |
|---|---|---:|
| Recursos Não Vinculados de Impostos | b | +524.118 |
| Recursos Não Vinculados de Impostos | c | +1.769.977 |
| Recursos Não Vinculados de Impostos | d | +1.548.101 |
| Outros Recursos não Vinculados | c | +15.137 |
| Outros Recursos não Vinculados | d | +751.849 |
| Recursos Vinculados a Fundos | c | +8.624.787 |
| Outras Vinculações Legais | b | +594.952 |
| Outras Vinculações Legais | c | +13.522.393 |

Todas são **para mais** e concentradas em três linhas. O padrão sugere que o
anexo desconta algo que o filtro de fonte sozinho não captura — provavelmente os
RP cancelados, que aparecem em coluna própria do demonstrativo.

### 8.1 A fonte 759 e o salto para 48 de 54

"Recursos Vinculados a Fundos" e "Outras Vinculações Legais" **compartilham a
fonte 759**. O anexo a atribui somente à primeira:

```
FR 759 ... 6321 = 581.150,15 | 6313 = 13.801,55 | 6327 = 13.522.392,88
```

Removendo 759 de "Outras Vinculações Legais":

| célula | nosso | oficial |
|---|---:|---:|
| Outras — (b) | 7.213,51 | 7.213,81 |
| Outras — (c) | 13.318.440,16 | 13.318.440,16 |

**48 de 54 células exatas** (89%).

Restam seis, todas concentradas em duas linhas:

| linha | coluna | diferença |
|---|---|---:|
| Recursos Não Vinculados de Impostos | b | +524.118 |
| Recursos Não Vinculados de Impostos | c | +1.769.977 |
| Recursos Não Vinculados de Impostos | d | +1.548.101 |
| Outros Recursos não Vinculados | c | +15.137 |
| Outros Recursos não Vinculados | d | +751.849 |
| Recursos Vinculados a Fundos | c | +8.624.787 |

A hipótese dos RP cancelados **não se confirmou**: subtrair 6329/6319 produz
valores negativos em várias linhas. O caminho agora é a coluna (H) do arquivo,
que trata dos cancelados separadamente.

---

## 9. Validação em 2026 contra a planilha da equipe

A pasta `Arquivos etonjones` trouxe o que faltava: o `Quadro_e_Mapa_Janeiro_a_
Outubro_2026.xlsx` (a planilha de trabalho), os IEO mensais das UGs 162233 e
162011, os Comparativos mensais e o **RGF Q2/2026 homologado**.

### O falso alarme dos 3,25 bi

Eu havia apontado que o painel mostrava 12,86 bi para Jan–Out e o Siconfi 16,11
bi para Jan–Ago — o que parecia contradição. **Não é:** nossa apuração usa
**janela móvel de 12 meses** (set/2025 a ago/2026), e o painel usa o **ano
calendário** (jan a out/2026). Janelas diferentes, números diferentes.

### O confronto com a janela certa

Nosso motor, jan–set/2026, recorte Executivo, contra a soma dos meses da planilha:

| linha | nosso | planilha | desvio |
|---|---:|---:|---:|
| Despesa Bruta (I) | 11.528.161.353,65 | 11.489.313.966,33 | **+0,34%** |
| Despesas Não Computadas (II) | 3.026.980.959,05 | 3.083.374.098,61 | −1,83% |
| Despesa Líquida (III) | 8.501.180.394,60 | 8.405.939.867,72 | +1,13% |

**A despesa bruta fecha a 0,34%** — calculada pelo motor a partir da matriz,
sem usar a planilha em nada. É a validação independente que faltava para 2026.

### O que a planilha confirma

| regra | evidência |
|---|---|
| DEA (elemento 92) concentrada em dezembro | coluna Dez/26 de II = **61.416.717,30** |
| Enfermagem a 72% em 2026 | aplicada na composição de II |
| Expurgo por UG 162233/162011 | R$ 466,2 mi (inat 276,4 + pens 93,2 + pat 96,6) |

### O que resta

A diferença em II (−1,83%) é o único ponto: deduzimos R$ 56,4 mi menos que a
planilha. Com os IEO mensais em mãos, dá para decompor mês a mês e localizar
exatamente onde a dedução diverge.

---

## 10. O expurgo dos demais Poderes — regra identificada

Lendo o IEO da UG 162233 (FUNFIRN) visualmente, os cinco Poderes aparecem com
estes códigos:

| subação | Poder | aposentadorias 0.8.00 | pensões 0.8.00 | patronal 0.5.00 |
|---|---|---:|---:|---:|
| 218401 | Defensoria | 104.948,47 | — | 21.466,73 |
| 221201 | TJRN | 12.629.016,99 | 2.387.869,11 | 3.402.724,06 |
| 222201 | ALRN | 8.562.226,99 | 493.412,13 | 2.707.863,35 |
| 222401 | MPRN | — | 337.476,89 | 1.002.121,32 |
| 222501 | TCE | 3.198.821,82 | 310.632,74 | 1.467.070,97 |

**Setembro/2026:**

| componente | valor |
|---|---:|
| aposentadorias 0.8.00 | 24.495.014,27 |
| pensões 0.8.00 | 3.529.390,87 |
| patronal 0.5.00 | 8.601.246,43 |
| **total** | **36.625.651,57** |
| planilha | 36.447.985,52 |
| **desvio** | **+0,49%** |

A regra é: **aposentadorias e pensões na fonte 0.8.00 + patronal na fonte
0.5.00, dos cinco Poderes.**

### Aplicação aos nove meses

`expurgo_poderes.py` lê o IEO pela geometria do PDF. A aposentadoria sai exata;
as pensões ainda não são capturadas (os blocos usam outra codificação de
subação — 408901, 410401 — e vêm descritos por extenso).

| mês | nosso (apos+patr) | planilha | desvio |
|---|---:|---:|---:|
| jan | 36.779.918,07 | 47.435.203,37 | −22% |
| fev | 28.741.825,43 | 28.155.853,57 | +2,1% |
| mar | 28.993.657,03 | 22.327.549,36 | +30% |
| abr | 28.100.268,07 | 653.864.492,01 | −96% |
| mai | 30.055.132,70 | 29.772.727,55 | +0,9% |
| jun | 30.269.728,68 | 36.249.744,22 | −16% |
| jul | 29.617.936,84 | 29.546.096,39 | **+0,24%** |
| ago | 24.219.219,46 | 25.936.622,87 | −6,6% |
| set | 33.201.209,17 | 36.447.985,52 | −8,9% |
| out | 29.909.152,52 | 29.476.494,85 | +1,5% |

Julho fecha a 0,24% e maio a 0,9% **mesmo sem as pensões** — o que confirma a
regra. Os meses com desvio maior têm causa: falta o componente de pensões
(~3,5 mi/mês) e, em abril, a planilha embute o ajuste de −R$ 624,7 mi da conta
8.6.3.3.1.

### 10.1 O leitor por blocos e o resultado nos nove meses

`expurgo_poderes.py` foi reescrito para separar em blocos: os identificados por
código de subação rendem aposentadorias e patronal; os identificados pela
descrição ("pensionistas - Tribunal de Justiça" etc.) rendem pensões.

**Setembro/2026:**

| componente | apurado | planilha |
|---|---:|---:|
| aposentadorias 0.8.00 | 24.495.014,27 | — |
| pensões 0.8.00 | 3.494.674,89 | — |
| patronal 0.5.00 | 8.706.194,90 | — |
| **total** | **36.695.884,06** | **36.447.985,52** |
| **desvio** | **+0,68%** | |

### Os nove meses — só setembro fecha

| mês | apurado | planilha | desvio |
|---|---:|---:|---:|
| jan | 39.842.750,07 | 47.435.203,37 | −16% |
| fev | 31.929.124,04 | 28.155.853,57 | +13% |
| mar | 32.162.974,01 | 22.327.549,36 | +44% |
| abr | 31.318.076,56 | 653.864.492,01 | −95% |
| mai | 33.349.378,77 | 29.772.727,55 | +12% |
| jun | 33.636.991,04 | 36.249.744,22 | −7% |
| jul | 33.172.076,64 | 29.546.096,39 | +12% |
| ago | 27.766.563,97 | 25.936.622,87 | +7% |
| **set** | **36.695.884,06** | **36.447.985,52** | **+0,68%** |
| out | 33.278.070,64 | 29.476.494,85 | +13% |

**1 de 10 meses dentro de 2%.**

### A leitura honesta

A apuração do motor é **estável** (ronda R$ 33 mi todo mês); a da planilha
**varia** (de 22 a 47 mi). Se a regra fosse só aposentadorias + pensões +
patronal, as duas deveriam variar juntas.

Conclusão: existe um **componente mensal variável** que ainda não identifiquei.
Os candidatos: 13º salário (só em alguns meses), patronal sobre a folha de
inativos em meses específicos, ou exercícios anteriores.

Setembro fechou porque ali os componentes coincidiram.

### 10.2 Março lido e as combinações testadas

Lendo o IEO de março visualmente, o bloco da ALRN mostra o que varia:

| conta | setembro | março |
|---|---:|---:|
| ALRN 31.90.01 na fonte 0.5.00 | 11.548.881,70 | **5.044.555,49** |
| ALRN 31.90.01 na fonte 0.8.00 | 8.562.226,99 | 4.895.720,17 |

A mesma conta varia 2,3× de um mês para o outro. É aí que mora o componente
mensal que faltava identificar.

### Combinações testadas nos dez meses

| mês | apos | apos+patr | apos+pens | tudo | planilha |
|---|---:|---:|---:|---:|---:|
| jan | 24,7 | 36,8 | 27,8 | 39,8 | **47,4** |
| fev | 20,5 | **28,7** | 23,7 | 31,9 | 28,2 |
| mar | 20,6 | 29,0 | **23,8** | 32,2 | 22,3 |
| mai | 21,7 | **30,1** | 25,0 | 33,3 | 29,8 |
| jun | 21,6 | 30,3 | 25,0 | 33,6 | 36,2 |
| jul | 21,0 | **29,6** | 24,6 | 33,2 | 29,5 |
| ago | 15,9 | 24,2 | 19,4 | 27,8 | 25,9 |
| set | 24,5 | 33,2 | 28,0 | **36,7** | 36,4 |
| out | 21,3 | **29,9** | 24,7 | 33,3 | 29,5 |

**`apos + patronal` é a melhor combinação geral: fecha em 5 dos 10 meses**
(fev, mai, jul, out e quase ago). Mas não explica janeiro (+10,7 acima de
qualquer combinação) nem março (−6,7 abaixo de apos+patr).

Isso reforça: o expurgo tem os três componentes identificados **mais um fator
mensal** que não é constante — provavelmente 13º, atrasados ou exercícios
anteriores lançados em 31.90.92/94.

---

## 11. A especificação da MAPA e a validação do expurgo

Com a especificação em mãos (`docs/MANUAL_MAPA_ANEXO1.md`), a regra do expurgo
dos inativos ficou explícita: **fonte 0.5.00 + fonte 0.8.00**, por subação.

Confronto da nossa linha de aposentadorias com a do QUADRO, mês a mês:

| mês | nosso | planilha | lacuna | expurgo (5 Poderes) | resíduo |
|---|---:|---:|---:|---:|---:|
| jan | 765.918.836,02 | 738.721.841,06 | 27.196.995 | 24.747.756 | 2.449.239 |
| fev | 446.913.643,30 | 424.405.986,78 | 22.507.657 | 20.466.415 | 2.041.242 |
| mar | 449.748.959,12 | 423.850.718,32 | 25.898.241 | 20.623.004 | 5.275.237 |
| abr | 468.373.953,02 | 441.617.489,06 | 26.756.464 | 19.807.320 | 6.949.144 |
| mai | 464.122.939,89 | 437.285.993,34 | 26.836.947 | 21.682.248 | 5.154.698 |
| jun | 472.906.541,62 | 446.393.073,41 | 26.513.468 | 21.635.864 | 4.877.604 |
| jul | 469.835.105,50 | 442.302.059,10 | 27.533.046 | 21.044.835 | 6.488.212 |
| ago | 372.474.018,80 | 355.311.963,91 | 17.162.055 | 15.898.299 | 1.263.756 |
| set | 567.565.402,86 | 529.872.067,22 | 37.693.336 | 24.495.014 | 13.198.321 |

### Leitura

O expurgo explica **80% a 93% da lacuna** em oito dos nove meses. O resíduo
(1,3 a 6,9 mi) é o componente de classificação — naturezas que a planilha põe
em outra linha.

Setembro é o caso fora da curva: resíduo de 13,2 mi, o dobro dos demais.

### Conclusão

A regra está certa e o valor está certo. Falta **aplicá-la**: hoje o motor não
deduz os inativos dos demais Poderes da sua linha de aposentadorias.

---

## 12. A MAPA reconstruída — aposentadorias fecham ao centavo

Aplicando o manual aos arquivos da pasta, com o **Comparativo** como fonte do
bruto (3º número da linha = Liquidada no mês) e o **IEO** como fonte da dedução:

**Trava de conferência (manual, item 4):** a soma das naturezas do grupo 31 no
Comparativo dá **1.659.015.263,31** — exatamente o GND 31 da planilha.

**Seção 2.3 — Aposentadorias (setembro/2026):**

| parcela | valor |
|---|---:|
| bruto (20 naturezas das linhas 183-202) | 567.729.412,24 |
| (−) IEO 0.8.00 (DPRN 104.948,47 + TJRN 12.629.016,99 + ALRN 8.562.226,99 + TCE 3.198.821,82) | 24.495.014,27 |
| (−) IEO 0.5.00 (ALRN 11.548.881,70 + TCE 1.813.449,05) | 13.362.330,75 |
| **líquido** | **529.872.067,22** |
| planilha | **529.872.067,22** |
| **diferença** | **0,00** |

**A linha fecha ao centavo.**

O que faltava era exatamente a parcela de **fonte 0.5.00** da ALRN e do TCE —
a "regra de ouro" do manual. Sem ela, a diferença era de R$ 13,36 mi.

### Pendência de implementação

`expurgo_poderes.py` captura a fonte 0.8.00 mas ainda não a 0.5.00 (bug de
atribuição no bloco do IEO). O valor está provado à mão; falta o parser.

---

## 13. Seção 2.3 fechada — aposentadorias em 8 de 10 meses

A parcela que faltava era a **fonte 0.5.00**. Ela não é lida diretamente no
IEO: no bloco da 0.5.00 o relatório imprime o **total da fonte** e, abaixo, os
elementos. Como o total é a soma dos elementos, a aposentadoria paga pelo
Tesouro é obtida por diferença:

    aposentadorias 0.5.00 = total da fonte 0.5.00 − patronal 0.5.00

### Resultado por Poder (setembro/2026)

| Poder | 0.8.00 | 0.5.00 (por diferença) |
|---|---:|---:|
| DPRN | 104.948,47 | 0,00 |
| TJRN | 12.629.016,99 | 0,00 |
| ALRN | 8.562.226,99 | 11.548.881,70 |
| MPRN | 0,00 | 0,00 |
| TCE | 3.198.821,82 | 1.813.449,05 |
| **total** | **24.495.014,27** | **13.362.330,75** |

E a linha fecha: `567.729.412,24 − 24.495.014,27 − 13.362.330,75 = 529.872.067,22`.

### Os dez meses

| mês | apurado | planilha | diferença |
|---|---:|---:|---:|
| janeiro | 686.312.230,70 | 738.721.841,06 | **−52.409.610,36** |
| fevereiro | 424.371.697,98 | 424.405.986,78 | −34.288,80 |
| março | 423.850.718,32 | 423.850.718,32 | **0,00** |
| abril | 441.617.489,06 | 441.617.489,06 | **0,00** |
| maio | 437.285.993,34 | 437.285.993,34 | **0,00** |
| junho | 446.393.073,41 | 446.393.073,41 | **0,00** |
| julho | 442.302.059,10 | 442.302.059,10 | **0,00** |
| agosto | 355.311.963,91 | 355.311.963,91 | **0,00** |
| setembro | 529.872.067,22 | 529.872.067,22 | **0,00** |
| outubro | 442.352.625,45 | 442.352.625,45 | **0,00** |

**8 de 10 exatos ao centavo.**

### Janeiro: causa identificada

No Comparativo de janeiro:

```
31.90.01.00 (agregado) ..... 765.918.836,02
31.90.01.01 ................ 658.074.916,41
31.90.01.21 ................. 55.434.309,25
soma dos subelementos ...... 713.509.225,66
diferença ................... 52.409.610,36  <- igual à lacuna
```

Há um subelemento executado só em janeiro que o relatório não abre na listagem
— provavelmente aposentadorias intra-orçamentárias (31.91.01). É o único ponto
aberto da seção.

### 13.1 Pensões — o IPERN entrou

As pensões especiais e o montepio são executados na **UG 162011 (IPERN)**, com
códigos próprios: 412301 (ALRN), 412401 (MPRN), 412501 (TCE), 412601 e 412701
(TJRN). Somando as duas UGs e incluindo as fontes 0.5.00 e 0.8.04:

| mês | apurado | planilha | diferença |
|---|---:|---:|---:|
| janeiro | 74.267.123,37 | 94.440.794,10 | −20.173.670,73 |
| fevereiro | 76.131.864,76 | 75.695.508,43 | 436.356,33 |
| março | 76.348.551,34 | 76.238.461,25 | 110.090,09 |
| abril | 76.269.203,03 | 76.124.731,24 | 144.471,79 |
| maio | 76.160.520,54 | 76.058.020,54 | **102.500,00** |
| junho | 76.388.908,67 | 76.286.408,67 | **102.500,00** |
| julho | 76.552.217,40 | 76.442.836,31 | 109.381,09 |
| agosto | 76.309.794,85 | 76.207.294,85 | **102.500,00** |
| setembro | 77.272.761,35 | 77.112.359,14 | 160.402,21 |
| outubro | 78.472.225,82 | 78.369.725,82 | **102.500,00** |

O desvio caiu de R$ 5,9 mi para **R$ 102.500,00 constantes** em quatro meses —
um item fixo que ainda não é capturado. Janeiro continua fora da curva
(−20,17 mi), provavelmente pelo mesmo subelemento que afetou as aposentadorias.

### 13.2 Os R$ 102.500 eram DEA de pensões

O desvio constante de R$ 102.500,00 por mês tinha endereço exato na aba MAPA:
as linhas de **DEA de pensões (31.90.92.03)** — R$ 23.000,00 no MPRN (linha
234) e R$ 79.500,00 no TJRN (linha 244).

Conferindo a soma das dez linhas de dedução da MAPA em maio:

| linha | Poder | natureza | valor |
|---|---|---|---:|
| 228 | ALRN | 31.90.03.01 | 960.076,62 |
| 229 | ALRN | 31.90.03.05 | 479.198,94 |
| 232 | MPRN | 31.90.03.01 | 662.939,10 |
| 233 | MPRN | 31.90.03.05 | 382.276,58 |
| 234 | MPRN | 31.90.92.03 | 23.000,00 |
| 237 | TCE | 31.90.03.01 | 605.907,80 |
| 238 | TCE | 31.90.03.05 | 185.511,48 |
| 240 | TJRN | 31.90.03.01 | 3.702.290,56 |
| 241 | TJRN | 31.90.03.05 | 2.122.761,12 |
| 244 | TJRN | 31.90.92.03 | 79.500,00 |
| | | **total** | **9.203.462,20** |

Idêntico à dedução da planilha.

### Placar das pensões

| mês | diferença |
|---|---:|
| janeiro | −20.427.820,81 |
| fevereiro a outubro | **0,00** (9 meses) |

**9 de 10 exatos.** O único desvio é janeiro, o mesmo mês que resiste nas
aposentadorias.

---

## 14. DESPESA BRUTA FECHADA — 10 de 10 meses exatos

Aplicando a especificação da MAPA aos relatórios do SIGEF/RN, a despesa bruta
com pessoal do Poder Executivo foi reconstruída do zero e confere com a
planilha da equipe **ao centavo, em todos os dez meses de 2026**.

| mês | apurado | planilha | diferença |
|---|---:|---:|---:|
| janeiro | 1.756.015.131,06 | 1.756.015.131,06 | **0,00** |
| fevereiro | 1.168.704.572,00 | 1.168.704.572,00 | **0,00** |
| março | 1.249.898.879,52 | 1.249.898.879,52 | **0,00** |
| abril | 680.626.929,97 | 680.626.929,97 | **0,00** |
| maio | 1.244.370.847,54 | 1.244.370.847,54 | **0,00** |
| junho | 1.309.400.172,65 | 1.309.400.172,65 | **0,00** |
| julho | 1.261.103.623,98 | 1.261.103.623,98 | **0,00** |
| agosto | 1.196.626.531,82 | 1.196.626.531,82 | **0,00** |
| setembro | 1.622.567.277,79 | 1.622.567.277,79 | **0,00** |
| outubro | 1.372.795.749,49 | 1.372.795.749,49 | **0,00** |

### As seis seções, todas fechadas

| seção | linhas | fonte |
|---|---|---|
| 2.1 Vencimentos | 8-101 | Comparativo |
| 2.2 Patronal | 102-180 | Comparativo (expurgo por 31.91.13.xx) |
| 2.3 Aposentadorias | 182-208 | Comparativo + IEO (0.8.00 e 0.5.00) |
| 2.4 Pensões | 209-244 | Comparativo + IEO 162233 e 162011 |
| 2.5 Terceirização | 245-249 | Comparativo (33.90.34.00) |
| 2.6 Não executada | 250-251 | Balancetes 8.6.3.3.1 |

### O último item: o estorno de fevereiro

O IEO imprime o valor do MPRN em fevereiro como **positivo** (17.144,40), mas
é um **cancelamento de empenho**: o "Disponível" (46.343.855,60) é maior que o
"Atualizado" (46.361.000,00). O manual registra o caso expressamente. Sem
tratá-lo, a despesa bruta de fevereiro ficava R$ 34.288,80 acima.

---

## 15. ANEXO 1 APURADO DO ZERO — I, II e III exatos nos dez meses

Com o Quadro II montado, a despesa líquida (III = I − II) fecha em todos os
meses.

### Despesas Não Computadas (II) — composição

| componente | linhas | regra |
|---|---|---|
| Indenizações | 253-261 | 31.XX.94.00 bruto |
| Decisão judicial | 262-273 | 31.XX.91.00 bruto |
| Exercícios anteriores | 274-285 | **só em dezembro**; no mês entra apenas a parcela da FR 0.8.00 |
| Inativos vinculados | 286-328 | 31.XX.01.00 e 03.00 nas fontes 8.00-8.04, menos os demais Poderes |
| ACS (FR 604) | 329-333 | 100% do liquidado |
| Enfermagem (FR 605) | 334-338 | **72% em 2026** |

### Resultado

| mês | Despesa Líquida (III) | diferença |
|---|---:|---:|
| janeiro | 1.449.033.494,41 | **0,00** |
| fevereiro | 904.030.766,32 | **0,00** |
| março | 872.968.664,12 | **0,00** |
| abril | 303.562.294,70 | **0,00** |
| maio | 934.354.741,80 | **0,00** |
| junho | 929.475.861,77 | **0,00** |
| julho | 905.691.808,26 | **0,00** |
| agosto | 1.072.483.241,96 | **0,00** |
| setembro | 1.095.755.711,68 | **0,00** |
| outubro | 879.576.307,01 | **0,00** |

**I, II e III exatos ao centavo nos dez meses de 2026.**

### O detalhe da fonte 0.8.00

A DEA (elemento 92) é deduzida apenas em dezembro, mas a parcela executada na
**fonte 0.8.00** entra deduzida no próprio mês (MAPA linha 276): R$ 1.681,65 em
janeiro e R$ 2.509,77 em junho — exatamente os valores que o manual registra.

---

## 16. Ajustes aplicados em 13/11/2026 (sem depender de dado novo)

| anexo | antes | depois |
|---|---|---|
| **RGF Anexo 5** | 48 de 54 células | **90 de 90 exatas** |
| **RREO Anexo 9 — receita** | não implementada | **exata** (2.491.012,67) |
| **RGF Anexo 2** | 8 de 14 linhas | **9 de 14** (empréstimos internos) |
'| **RCL fixa no código** | valores de 2024 sem aviso | **trava que impede o uso em outro exercício** |
| **RREO Anexo 13** | não existia | **módulo criado — 7 de 7 valores exatos** |
| **Limites do Anexo 1** | peças soltas | **função `limites()` — 55,17% conferido** |'

### RGF Anexo 5

Três correções em `rgf_anexo5_vinculacao.py`:

1. filtro de Poder (`po` começando por "10") — a causa das 6 células residuais;
2. coluna (e) pela **classe 8** (`821130200`/`821130300`) mais `863310000` na
   linha de não vinculados;
3. coluna (a) pela classe 1 com sinal D−C, excluindo a conta-espelho `111120000`.

Resultado: **90 de 90 células exatas** (2025 Q3).

### RREO Anexo 9 — receita

O módulo não tinha o lado da receita. Implementado com a natureza de receita
(prefixo "21" e "81") sobre `6.2.1.2` + `6.2.1.3`, separando refinanciamento
pelos códigos `211102/211255/212102/212255`. Realizado: **2.491.012,67**, igual
ao homologado; refinanciamento zero.

### RGF Anexo 2

`USAR_PAI` restrito a `2.1.2.1.1.02` e `2.1.2.1.3.02`: usa a conta-pai de nível 7
em vez do filho terminal. Em 31/12/2025, Empréstimos Internos fecha em
**849.909.956,58** — exato. As outras linhas não foram afetadas.

A primeira tentativa aplicou o pai a todas as contas e **quebrou três linhas**
(Contribuições Previdenciárias, Instituição Não Financeira, Demais Haveres) —
por isso a regra ficou restrita.

### Trava da RCL

`app/layout_stn.py` tinha a cadeia da RCL fixa para 2024 (`17.259.989.216,73`).
Agora há `EXERCICIO_REFERENCIA = 2024` e `referencia(exercicio)`, que **levanta
erro** para qualquer outro exercício. Teste em `tests/test_layout_stn.py`.

### O que continua pendente

- RGF Anexo 2: as 5 linhas por Poder (disponibilidade, depósitos, haveres) e os
  RP processados dependem do relatório por fonte.
- Anexo 13: módulo ainda não criado.
- RCL/limites: ligar o Anexo 3 ao bloco de limites.



---

## 17. Aba de verificação por anexo

`verificacao.py` gera `saida/verificacao_anexos.xlsx` com uma aba por
demonstrativo (apurado, referência, desvio, situação) e uma aba de resumo.

| anexo | células | exatas | divergentes |
|---|---:|---:|---:|
| RGF Anexo 1 (jan–ago vs homologado) | 24 | 22 | 2 |
| RGF Anexo 2 | 14 | 9 | 5 |
| RGF Anexo 5 | 90 | **90** | 0 |
| RREO Anexo 9 | 5 | **5** | 0 |
| RREO Anexo 13 | 7 | **7** | 0 |
| **total** | **140** | **133** | **7** |

### As sete divergências, todas com causa

| anexo | item | desvio | causa |
|---|---|---:|---|
| 1 | Abril — I | −5.241,65 | empenho de março liquidado em abril sem complemento (documentado no manual) |
| 1 | Abril — III | −5.241,65 | idem |
| 2 | Demais Dívidas Contratuais | +272.293.396,59 | o RN publica zero nessa linha (decisão de classificação, não erro) |
| 2 | Disponibilidade de Caixa Bruta | +1.850.637,57 | exige os blocos por Poder |
| 2 | (−) Restos a Pagar Processados | −4.058.289.107,72 | exige o relatório por fonte |
| 2 | (−) Depósitos Restituíveis | +54.946.195,61 | exige os blocos por Poder |
| 2 | Demais Haveres Financeiros | +7.505.813,73 | exige os blocos por Poder |

Nenhuma divergência está "arredondada para zero": todas aparecem com o valor e a
causa.


### 17.1 O livro agora cobre tudo

`verificacao.py` incorporou as 27 conferências do `verificar_tudo.py`, agrupadas
por anexo. O livro passou a ter **16 abas** e **166 células**:

| grupo | células | exatas |
|---|---:|---:|
| RGF Anexo 1 (jan–ago) | 24 | 22 |
| RGF Anexo 1 — limites | 5 | **5** |
| RGF Anexo 2 | 14 | 9 |
| RGF Anexo 3 / 4 / 6 | 3 | **3** |
| RGF Anexo 5 | 90 | **90** |
| RREO Anexo 1 / 2 / 3 / 7 / 9 / 13 / 14 | 27 | **27** |
| motor | 1 | **1** |
| **total** | **166** | **159** |

### 17.2 A cadeia RCL → limites

`mapa_anexo1.limites_do_rreo(dtp_12m)` fecha o caminho:

```
RREO Anexo 3 (CSV homologado) -> RCL ajustada 20.958.175.998,75
                              -> limites( RCL , DTP 12 meses )
                              -> 55,17% e os três limites em reais
```

Conferido contra o publicado: 55,17%; máximo 10.269.506.239,39; prudencial
9.756.030.927,42; alerta 9.242.555.615,45.


### 17.3 Anexo 1 por Poder — 100 de 100

A aba "RGF Anexo 1 - por Poder" confronta o que o motor apura no IEO para cada
Poder com as linhas de dedução da MAPA (289-293 para aposentadorias na fonte
0.8.00; 296-300 para pensões nas fontes 0.8.00 e 0.8.04).

**Cinco Poderes × dez meses × dois componentes = 100 células, todas exatas.**

| Poder | aposentadorias (set) | pensões (set) |
|---|---:|---:|
| ALRN | 8.562.226,99 | 653.945,20 |
| DPRN | 104.948,47 | 0,00 |
| MPRN | 0,00 | 516.454,36 |
| TCE/RN | 3.198.821,82 | 370.274,76 |
| TJRN | 12.629.016,99 | 3.072.814,87 |

O livro de verificação passou a **266 células, 259 exatas**.


### 17.4 Anexo 13 — projeções implementadas

A projeção do contrato é geométrica e sai de **uma âncora** mais dois índices
publicados na nota do próprio demonstrativo:

```
despesa(EC+n) = 60.190.422,53 x (IPCA / SELIC)^(n-1)      IPCA 3,5% | SELIC 10,68%
RCL(EC+n)     = RCL_EC x 1,02031208231^n
```

Conferido nas seis colunas publicadas: **todas exatas** (uma com 1 centavo de
arredondamento).

A âncora é `ANCORA_ARENA` em `rreo_anexo13.py` — o único dado que não vem da
matriz, e é o mesmo nos quatro bimestres do exercício.


### 17.5 RREO Anexo 4 no livro — e uma referência errada corrigida

O módulo dos blocos previdenciários comparava as pensões militares com
**119.906.956,64** — que é a linha do bloco principal, não o total. O total
publicado é **250.915.256,72**, e é ele que o motor apura.

| linha | apurado | oficial | desvio |
|---|---:|---:|---:|
| Aposentadorias civis | 4.918.972.380,24 | 4.917.756.724,31 | +1.215.656 (0,02%) |
| Pensões por morte civis | 641.798.204,93 | 640.868.408,22 | +929.797 (0,15%) |
| **Inatividade militar** | 675.066.910,71 | 675.066.910,71 | **0** |
| **Pensões militares** | 250.915.256,72 | 250.915.256,72 | **0** |

Duas exatas, duas com desvio documentado abaixo de 0,15%.

O livro de verificação passou a **276 células, 267 exatas**.


### 17.6 Relatório de divergências gerado do livro

`verificacao.relatorio_divergencias()` escreve `docs/DIVERGENCIAS.md` a partir do
próprio livro de verificação. Não é escrito à mão: se o livro mudar, o relatório
muda junto — e não há como um divergência "desaparecer" da documentação.

Estado atual: **267 de 276 células exatas**; as 9 divergentes estão listadas com
valor, referência, desvio e causa.

| anexo | divergentes | situação |
|---|---:|---|
| RGF Anexo 1 | 2 | abril: empenho de março liquidado em abril (−5.241,65) |
| RGF Anexo 2 | 5 | blocos por Poder e RP por fonte — depende de extração |
| RREO Anexo 4 | 2 | 0,02% e 0,15% — classificação fina de naturezas, em investigação |

Sobre as duas do Anexo 4: testei o mapeamento por sufixo de natureza e o desvio
**não** corresponde a uma natureza isolada (o sufixo 9403 vale 926.078,43 e o
desvio das pensões é 929.796,71). É diferença de classificação dentro do
conjunto, não uma linha trocada.


### 17.7 Trava de regressão dos anexos fechados

`tests/test_verificacao.py` falha se qualquer célula dos anexos fechados voltar a
divergir: Anexo 13 (saldos e projeções), Anexo 9, limites do Anexo 1 e Anexo 5.
São 7 testes em 4,6 segundos.

Também verifica que **toda divergência conhecida tem causa escrita** em
`CAUSAS` — e que um item desconhecido não inventa causa ("sem causa
identificada").

Motivo: a regra que fecha um anexo hoje pode ser alterada amanhã por quem achar
que está corrigindo outra coisa. O teste avisa antes de o relatório sair.

### 17.8 Anexo 4 — o que foi testado

Tentei isolar o desvio de 0,02% (aposentadorias civis) e 0,15% (pensões civis)
pelo complemento de fonte. O complementar se distribui em três COs:

| linha | CO 1111 | CO 1121 | CO 1122 |
|---|---:|---:|---:|
| aposentadorias civis | 1.739.994.707,43 | 66.413.050,21 | 20.468.496,52 |
| pensões civis | 49.754.089,37 | 1.103.670,02 | 474.282,69 |

Nenhum deles corresponde ao desvio (1.215.655,93 e 929.796,71). É diferença de
classificação dentro do conjunto, não um complemento inteiro a mais.


### 17.9 Anexo 5 conferido contra o Siconfi, não só contra a planilha

Até aqui o Anexo 5 era conferido célula por célula contra a planilha da equipe.
Agora há também a conferência dos **totais das colunas contra o CSV publicado**
(`RGF_RGF-Anexo_05_24_2025_p3.csv`, TOTAL IV):

| coluna | apurado | publicado |
|---|---:|---:|
| (a) Disponibilidade bruta | 1.088.399.547,00 | 1.088.399.547,00 |
| (b) RP processados | 472.988.715,32 | 472.988.715,32 |
| (c) RPNP inscritos no exercício | 1.405.948.478,02 | 1.405.948.478,02 |
| (d) RPNP a liquidar | 11.871.954,46 | 11.871.954,46 |
| (e) Demais obrigações financeiras | 2.230.614.991,10 | 2.230.614.991,10 |

**Cinco de cinco.** É a primeira vez que um anexo do RGF é conferido contra o
arquivo publicado além da planilha de trabalho.

O livro passou a **281 células, 272 exatas** (95,9%).


### 17.10 Anexo 4 — o desvio está no bloco 31.90.92

Decompus as duas linhas por família de natureza. O resultado é conclusivo:

| linha | família | apurado | esperado | diferença |
|---|---|---:|---:|---:|
| Aposentadorias civis | 31.90.01 | 4.648.107.547,94 | 4.648.217.285,93 | **−109.737,99** |
| Aposentadorias civis | 31.90.92 | 270.864.832,30 | 269.539.438,38 | **+1.325.393,92** |
| Pensões civis | 31.90.03 | 634.718.036,81 | 634.718.040,12 | −3,31 |
| Pensões civis | 31.90.92 | 7.080.168,12 | 6.150.368,10 | **+929.800,02** |

**A família 01 e a 03 praticamente fecham.** Todo o desvio está no **31.90.92
(DEA)**, e a soma dos dois excessos — 1.325.393,92 + 929.800,02 = 2.255.193,94 —
menos a falta de 109.737,99 e os 3,31, dá exatamente o desvio das duas linhas.

A memória da equipe mostra, no bloco 92, uma linha `b` de **−2.145.718,19**
(lançada como `31.90.92 b` e composta em `31.90.92 (a−b)`), que o motor não
reproduz. Não é uma fonte inteira: testei as oito fontes que executam 92 em 2025
e nenhuma vale esse montante.

Fica localizado: o que falta é **a natureza de despesa** que compõe esse `b`, não
o bloco.


### 17.11 ANEXO 4 FECHADO — as quatro linhas exatas

O desvio estava todo no bloco 31.90.92. A linha do anexo **não é o bruto**: é o
bruto **menos o PAE** (Parcela de Ajuste Previdenciário):

| linha | natureza do PAE | valor |
|---|---|---:|
| Aposentadorias civis | 31.90.92.02 | 1.215.655,93 |
| Pensões por morte civis | 31.90.92.06 | 929.796,71 |

Conferindo:

```
4.918.972.380,24 - 1.215.655,93 = 4.917.756.724,31   (publicado)
  641.798.204,93 -   929.796,71 =   640.868.408,22   (publicado)
```

| linha | apurado | oficial | desvio |
|---|---:|---:|---:|
| Aposentadorias civis | 4.917.756.724,31 | 4.917.756.724,31 | **0** |
| Pensões por morte civis | 640.868.408,22 | 640.868.408,22 | **0** |
| Inatividade militar | 675.066.910,71 | 675.066.910,71 | **0** |
| Pensões militares | 250.915.256,72 | 250.915.256,72 | **0** |

### O PAE não vem da matriz

Testei: o 31.90.92.02 e o .06 **não existem** na MSC de 2025. O PAE é informado
pelo **INEC** a cada bimestre e transcrito na aba "PAE" da planilha da equipe
("PREENCHER TODO BIMESTRE. FONTE: INEC").

É o segundo insumo exógeno do projeto, ao lado da âncora do PPP. Fica
parametrizado em `PAE_2025` e documentado como tal — não deduzido.

**O livro passou a 281 células, 274 exatas (97,5%).**


### 17.12 Anexo 2 — as três linhas por Poder, localizadas

Testando as abas "Disponibilidade", "Depósitos" e "D+ Haveres" contra a MSC, por
Poder:

| linha | Poderes que batem ao centavo | onde está a diferença |
|---|---|---|
| Disponibilidade | TCE, MP, DP | Executivo |
| Depósitos | TCE, TJ, MP, DP | Executivo (54.946.195,61) |
| Demais Haveres | — | não fecha por prefixo: 73 contas-folha |

Nas duas primeiras, **quatro ou três Poderes fecham exatamente** e a diferença
inteira está no Executivo. O valor é o mesmo que o balancete produz — logo, não é
erro de leitura: é **escopo de conta no Executivo**.

"Demais Haveres" resiste a outro método: a aba lista 73 contas-folha, e o prefixo
de 6 dígitos captura 22 vezes o valor oficial (6,02 bi contra 269,3 mi). Precisa
do critério de conta exato, não de prefixo.


### 17.13 Anexo 2 — a linha de Depósitos exclui a fonte 800

A aba "CONTAS" mostra que a coluna usada é `E = C - D`, rotulada **"VALOR SEM
RPPS"**. Testando a hipótese na MSC:

| escopo | valor | contra o oficial |
|---|---:|---:|
| todas as fontes | 852.068.043,72 | +54.946.195,61 |
| **sem a fonte 800** | **798.507.904,34** | **+1.386.056,23 (0,17%)** |

A fonte 800 soma 53.560.139,38 — praticamente toda a diferença.

Ou seja: a linha não é o saldo bruto das contas 2.1.8.8/2.2.8.8 — é o saldo
**sem a parcela do RPPS**, que a equipe soma em separado (bloco IPERN, fontes 800
e 802, linhas 16 a 22 da aba).

Restam R$ 1.386.056,23 (0,17%), provavelmente a fonte 802 ou uma sub-conta
específica.


### 17.14 Anexo 2 — as linhas têm escopos diferentes

Descobri por que a mesma regra não servia para as três linhas. Lendo o cabeçalho
das abas da equipe:

| aba | cabeçalho da coluna do Executivo | escopo |
|---|---|---|
| Disponibilidade | "Executivo" | consolidado, com os demais Poderes |
| Depósitos | "EXECUTIVO" | consolidado + bloco IPERN |
| D+ Haveres | **"EXECUTIVO (SEM RPPS)"** | **só o Executivo, sem o RPPS** |

Testando na MSC:

| linha | escopo | valor | contra o oficial |
|---|---|---:|---:|
| Demais Haveres | todos os POs | 276.769.780,89 | +7.455.265,00 |
| **Demais Haveres** | **PO 10111** | **269.273.793,89** | **−40.722,00 (0,015%)** |
| Disponibilidade | PO 10111 só | 1.075.235.890,80 | −473.945.474,56 |
| Disponibilidade | todos os POs | 1.559.285.389,89 | +10.104.024,53 |

**Demais Haveres é Executivo sem RPPS** — em PO 10111 o valor passa de 7,4
milhões de desvio para **40.722,00**. A linha é 100% Executivo: a aba mostra zero
em MP, TCE, DP, AL, FDM e TJ.

**Disponibilidade é consolidada** — restringir ao Executivo a derruba para menos
da metade. O escopo dela é o oposto.


### 17.15 Demais Haveres fechou — e a causa era uma conta agregada

A linha "Demais Haveres Financeiros" é **Executivo sem RPPS** (73 contas-folha,
PO 10111). Implementada assim, o desvio caiu de 7.505.813,73 para **40.722,00**.

O resíduo era **uma conta só**: a aba lista `1.2.1.3.1.01.00.00`, mas a MSC
agrega esse valor no sufixo `.99` — a conta que existe é **`121310199`** com
exatamente R$ 40.722,00. Com o mapa `EQUIVALENTES = {"121310100": "121310199"}`:

| | valor | contra o oficial |
|---|---:|---:|
| balancete (Executivo + RPPS) | 276.820.329,62 | +7.505.813,73 |
| MSC, todos os POs | 276.769.780,89 | +7.455.265,00 |
| **MSC, PO 10111** | 269.273.793,89 | −40.722,00 |
| **MSC, PO 10111 + conta .99** | **269.314.515,89** | **0** |

**RGF Anexo 2: 10 de 14 linhas exatas.** O livro passou a **275 de 281**.


### 17.16 Depósitos — a dedução e o Poder que sobra

A aba "Depósitos" tem, abaixo das 8 contas, um bloco **IPERN** (linhas 16-42)
com 24 sub-contas em FR 800/802. A aba "CONTAS" subtrai esse bloco do total
(`D253 = Depósitos!D42`):

```
C 834.666.683,98   (as 8 contas do Executivo — igual ao nosso valor da MSC)
D  53.753.274,49   (o bloco IPERN)
E 780.913.409,49   (o que vai para a linha)
```

O total da linha, então, é **todas as contas menos o bloco IPERN**:

| escopo | valor | contra o oficial |
|---|---:|---:|
| todas as contas | 852.068.043,72 | +54.946.195,61 |
| menos o bloco IPERN | 798.314.769,23 | **+1.192.921,12** |

### E o resíduo é de outro Poder

O Executivo fecha: `834.666.683,98 − 53.753.274,49 = 780.913.409,49`. O que sobra
está nos demais Poderes:

| | nosso | da aba | diferença |
|---|---:|---:|---:|
| AL + FDM | 2.531.909,68 | 1.338.988,56 | **1.192.921,12** |

É exatamente o resíduo. O AL (PO 20211) concentra o FDM, e a diferença é de
escopo de conta entre a MSC e o balancete da AL.

Tentei implementar a dedução do bloco IPERN e o resultado não convergiu (erro de
sinal e de prefixo das sub-contas). **Revertido** — a linha segue pelo balancete,
com o desvio de 54,9 mi documentado aqui, em vez de um número pior.


### 17.17 Depósitos — por que não fecha hoje

Tentei reproduzir o bloco IPERN (as 24 sub-contas em FR 800/802) e **não há
fonte no projeto com a granularidade necessária**:

| fonte | granularidade | resultado |
|---|---|---|
| MSC | 7 segmentos (9 dígitos: `218810102`) | o bloco não existe — a conta mais fina é `2.1.8.8.1.01.02`, não `2.1.8.8.1.01.08.01` |
| balancete | 8 segmentos | só **9 das 24** contas casam, e somam **657.898.469,56** contra 53.753.274,49 da aba (12× o valor) |

A MSC para no sétimo segmento; o balancete desce ao oitavo, mas não na mesma
abertura que a aba — 15 contas não casam e as que casam capturam o pai, não a
folha.

Confirmado no balancete: a conta mais fina da família é `2.1.8.8.1.01.08.00`
(sete segmentos, R$ 128.568,23); o oitavo — `.08.01` — não existe em nenhuma
fonte. O pai `2.1.8.8.1.01.00.00` soma R$ 531.484.361,86 e não serve: é a família
inteira.

**Conclusão:** a linha de Depósitos depende de uma abertura de 8 segmentos **por
fonte** que não existe em nenhuma das nossas fontes — nem na MSC, nem no
balancete. Não é falta de esforço: é falta de dado.

Duas implementações tentadas e revertidas. A linha segue pelo balancete, com o
desvio de 54.946.195,61 documentado — e a regra conhecida (total menos bloco
IPERN) registrada para quando o insumo existir.


### 17.18 Disponibilidade fechou — e a regra é a mesma dos Depósitos

A aba "CONTAS" (linha 243) faz `C - D`, com D vindo da aba "Disponibilidade".
O rótulo é o mesmo de antes: **"VALOR SEM RPPS"**.

Testando na MSC as 13 contas da disponibilidade:

| escopo | valor | contra o oficial |
|---|---:|---:|
| todas as fontes | 1.559.285.389,89 | +10.104.024,53 |
| **sem 800, 801 e 802** | **1.549.181.365,36** | **0** |

**RGF Anexo 2: 11 de 14 linhas exatas.** O livro passou a **276 de 281**.

### O padrão que se repetiu três vezes

| linha | regra |
|---|---|
| Depósitos | total − bloco IPERN (800/802) |
| Disponibilidade | total sem 800/801/802 |
| Demais Haveres | PO 10111 (sem o RPPS) |

Nas três, o que sai é o **RPPS**. A diferença é só a forma de tirar: por bloco de
contas numa, por fonte noutra, por Poder na terceira.


### 17.19 Depósitos — o resíduo é uma conta do AL

Com a Disponibilidade fechada pelo mesmo critério, sobrou uma única conta nos
Depósitos. A composição do AL (PO 20211):

| conta | fonte | valor |
|---|---|---:|
| 218830102 | 1500 | 2.512.993,42 |
| 218850108 | 1500 | 17.718,59 |
| 218830102 | 2501 | 567,67 |
| 218810401 | 1869 | 440,00 |
| 218819900 | 1869 | 190,00 |
| **total** | | **2.531.909,68** |

A aba da equipe traz AL 1.252.392,72 + FDM 86.595,84 = **1.338.988,56**.

A diferença é **1.192.921,12** e está concentrada na `218830102` da fonte 1500 —
a MSC não separa o que a equipe atribui ao AL e ao FDM.

Como no caso do bloco IPERN, é **falta de granularidade**, não de regra.


### 17.20 Trava do Anexo 2

`tests/test_rgf_anexo2.py` confere as 11 linhas exatas e mantém uma lista
explícita das 3 pendentes, com o motivo de cada uma:

| pendente | motivo |
|---|---|
| Demais Dívidas Contratuais | o RN publica zero e aloca em Outras Dívidas |
| (−) Depósitos Restituíveis | falta granularidade (8º segmento e AL × FDM) |
| (−) Restos a Pagar Processados | exige o relatório por fonte, por Poder |

O teste falha em dois sentidos: se uma linha que fechava voltar a divergir **e**
se uma pendente passar a fechar sem que a lista seja atualizada. A segunda trava
é a que evita a documentação envelhecer sem avisar.

Suíte completa: **9 arquivos, 69 testes**.


### 17.21 RREO Anexo 2 de 2026

As verificações do RREO usavam arquivos de 2025. Acrescentei a conferência de
**2026, 4º bimestre**, contra o CSV do Siconfi:

```
total liquidado (22 funções) ... 16.013.488.241,73
publicado ...................... 16.013.488.241,73   exato
```

O cruzamento **por função** não foi incluído: o mapa código → nome do módulo não
alinha com os rótulos do CSV de 2026, e 18 das 22 funções apareceram com desvio
igual ao próprio valor (sinal de que o código não foi encontrado, não de erro de
apuração). Confiar nesse cruzamento seria publicar 18 falsos divergentes.

O total é robusto e é o que está no livro. **282 células, 277 exatas.**


### 17.22 RREO Anexo 7 de 2026 — cinco de cinco

Parametrizei `rreo_anexo7` por ano/mês e conferi os dois exercícios:

| linha | 2025 | 2026 |
|---|---|---|
| RP processados pagos | 1.009.808.236,48 | 1.182.340.948,71 |
| RP processados cancelados | 49.997.069,58 | 69.178.545,41 |
| RP processados — saldo | 470.465.377,32 | 638.351.717,58 |
| RP não processados pagos | 217.231.892,52 | 221.477.718,89 |
| RP não processados cancelados | 188.293.949,99 | 264.195.701,11 |

**Todas exatas nos dois anos.** O livro passou a **287 células, 282 exatas
(98,3%)**.

O mesmo parâmetro (`matriz(ano, mes)`) serve para o 3º quadrimestre, quando os
dados chegarem.


### 17.23 RREO Anexo 14 de 2026 — seis de seis

Mesmo tratamento do Anexo 7: parametrizado por ano, mês e caminho do Anexo 3.

| linha | 2025 | 2026 |
|---|---|---|
| Despesas empenhadas | 23.874.415.460,69 | 20.405.779.981,56 |
| Despesas liquidadas | 23.361.499.529,63 | 16.013.488.241,73 |
| Despesas pagas | 21.945.141.150,86 | 15.316.721.257,95 |
| RCL | 19.513.846.659,98 | 20.966.424.987,22 |
| RCL ajustada — endividamento | 19.509.346.803,92 | 20.961.883.945,10 |
| RCL ajustada — pessoal | 19.507.449.078,52 | 20.958.175.998,75 |

**Seis de seis nos dois exercícios.** O livro passou a **293 células, 288 exatas
(98,3%)**.

Os três anexos do RREO de 2026 agora conferidos — 2, 7 e 14 — compartilham o
mesmo padrão de parametrização, e o 3º quadrimestre usará os mesmos argumentos.


### 17.24 A RCL — até onde a matriz alcança

`app/anexo3_msc.py::ler_rcl()` **lê** a RCL do CSV do Siconfi; não a calcula. Isso
é uma dependência real, e testei se a matriz a reproduz.

**RECEITAS CORRENTES (I)** — sim, quase:

| | valor |
|---|---:|
| MSC: 6.2.1.2 com natureza de receita prefixo "1", 12 meses de 2025 | 26.659.603.708,77 |
| publicado (Anexo 3, 2025) | 26.656.696.864,94 |
| diferença | **+2.906.843,83 (0,011%)** |

**DEDUÇÕES (II)** — não fecha:

| | valor |
|---|---:|
| MSC: 6.2.1.3 (sinal invertido, é conta redutora) | 5.943.961.755,92 |
| publicado | 7.142.850.204,96 |
| diferença | **−1.198.888.449,04** |

A diferença deve estar na **dedução do FUNDEB** (R$ 3.175.469.290,58), que pode
ser registrada em outra conta ou natureza.

**Situação:** a RCL é o último item do projeto que ainda é lido em vez de
apurado. As receitas correntes — 73% do caminho — já se reproduzem; falta o
mapeamento das deduções.


### 17.25 A RCL — os componentes das deduções

Decompus o 6.2.1.3 e **dois dos cinco componentes aparecem exatos**:

| componente | conta | MSC | publicado |
|---|---|---:|---:|
| Dedução para formação do FUNDEB | `621310100` | 3.175.469.290,58 | 3.175.469.290,58 |
| Transferências constitucionais e legais | `621310200` | 2.733.005.621,51 | 2.733.005.621,51 |
| outros | `621390000` | 35.486.843,83 | — |
| **total do 6.2.1.3** | | **5.943.961.755,92** | **7.142.850.204,96** |

O que falta é o **bloco do RPPS**, que não está no 6.2.1.3:

| componente | publicado |
|---|---:|
| Contribuição do servidor para o plano de previdência | 1.110.322.676,50 |
| Compensações financeiras entre regimes | 115.005.627,07 |
| Rendimentos de aplicações previdenciárias | 9.046.989,30 |
| **total** | **1.234.375.292,87** |

5.943.961.755,92 + 1.234.375.292,87 = 7.178.337.048,79 — um pouco acima do
publicado (7.142.850.204,96), porque o `621390000` provavelmente já contém parte
desses itens.

**Situação da RCL:** 4 dos 7 componentes identificados (receitas correntes, FUNDEB
e transferências exatos; o bloco RPPS localizado em valor, não em conta).


### 17.26 A RCL — o bloco RPPS não está na matriz

Procurei o bloco de 1,23 bi em todos os lugares plausíveis:

| verificação | resultado |
|---|---|
| `621390000` por natureza | só itens pequenos; o maior é 32.580.000,00 (NR 7215) |
| `6213` por Poder | Executivo 5,91 bi, RPPS 32,6 mi, demais < 55 mil |
| total do `6213` | **5.943.961.755,92** contra 7.142.850.204,96 publicados |

O bloco de 1.234.375.292,87 (contribuição do servidor, compensações e rendimentos
previdenciários) **não tem contrapartida no 6.2.1.3**. Não é soma errada: a
matriz não registra essas deduções ali.

**Conclusão:** a RCL não é integralmente apurável da MSC. Quatro componentes são
(receitas correntes a 0,011%, FUNDEB e transferências exatos); três não são, e a
demonstração os busca em outra fonte.

Isso fecha a investigação da RCL. Ela continua sendo **lida** do Anexo 3 — e
agora se sabe exatamente por quê.


### 17.27 Anexo 2 — por que o RP Processados exige o relatório

A seção da aba "Base" usa quatro contas, todas somadas com sinal positivo:

```
6.2.2.1.3.07.00   6.3.1.3.0.00.00   6.3.2.1.0.00.00   6.3.2.7.0.00.00
```

No balancete só as **contas-pai** existem (as filhas `6.3.1.3.1` e `6.3.2.1.1`
não estão lá), e elas somam **3.306.229.590,47** contra **752.059.517,25**
publicados.

A composição publicada, pela memória da equipe, é:

```
RP bruto dos sete Poderes .......... 1.694.111.739,40
(-) conta 8.6.3.2.2 ................   942.052.222,15
= RP processados ...................   752.059.517,25
```

Mesmo descontando a conta de controle dos nossos R$ 3,3 bi, chegaríamos a
R$ 2,36 bi — **três vezes** o publicado. As contas-pai do balancete agregam
inscritos, cancelados e o que já foi pago, sem a dimensão de fonte que a equipe
usa para excluir FR 32, 46, 800, 801 e 802.

**Conclusão:** não é conta trocada nem sinal. É a dimensão **fonte de recursos por
Poder**, que só o relatório do SIGEF tem.


### 17.28 Um bug no próprio relatório — e a causa dentro da planilha

Duas correções que a rodada 68 trouxe:

**1. A causa agora está na aba.** As linhas divergentes do livro passaram a trazer
o motivo na coluna "observação", gerado do mesmo `CAUSAS` que alimenta o
`DIVERGENCIAS.md`. Quem abrir a planilha vê o motivo sem precisar do markdown.
Conferido: **5 divergentes, 0 sem causa escrita**.

**2. O console contava menos que a planilha.** Ele somava os grupos de `FONTES` e
depois os do motor que não estivessem ali — mas `gerar()` **mescla** as linhas do
motor nos grupos existentes. Resultado: console dizia 288 de 293; a aba RESUMO
dizia **299 células, 294 exatas**.

Corrigido com uma função `_grupos()` usada pelos dois. Agora os dois dizem
294 de 299.


### 17.29 Trava de coerência entre README e livro

`tests/test_coerencia.py` compara o número declarado no README com o total da aba
RESUMO e falha se divergirem. Também verifica que **nenhuma divergência fica sem
causa escrita** na planilha.

É a trava que faltava: o bug da rodada 68 nasceu de o console contar diferente da
planilha. Agora, se o README mentir sobre o que a planilha contém, o teste avisa.

Suíte: **10 arquivos, 72 testes**.


### 17.30 A base de comparação do Anexo 2 estava errada — e o Depósitos fechou

O `OFICIAL` do módulo foi montado a partir da **aba Base da planilha da equipe**.
Fui ao **DCL publicado** (CSV do Siconfi, 3º quadrimestre de 2025) e ele traz
valores diferentes em duas linhas:

| linha | planilha da equipe | **DCL publicado** | nossa apuração |
|---|---:|---:|---:|
| (−) Depósitos Restituíveis | 797.121.848,11 | **798.314.769,23** | **798.314.769,23** |
| (−) Restos a Pagar Processados | 752.059.517,25 | **750.866.596,13** | 3.306.229.590,47 |

Na linha de Depósitos, **a planilha é que diverge** — a nossa apuração bate com o
publicado ao centavo.

A regra, afinal, era simples: as 8 contas **sem as fontes 800 e 802**.

```
todas as fontes ....... 852.068.043,72
sem 800 e 802 ......... 798.314.769,23   = DCL publicado
```

**RGF Anexo 2: 12 de 14 linhas exatas.** Livro: **295 de 299**.

### O que eu errei antes

Na rodada 56 concluí que a linha "não era apurável" porque o bloco IPERN exigia o
8º segmento. O bloco IPERN era um caminho; a exclusão por fonte era outro, mais
simples, e funcionava. Eu parei no primeiro que falhou em vez de testar o segundo.

E o mais grave: eu comparava contra a planilha da equipe — que **não é** o
publicado. A conferência só vale contra o arquivo homologado.


### 17.31 ANEXO 2 EM 15 DE 16 — três linhas que estavam fora da conferência

O DCL publicado tem 30 linhas; o módulo conferia 13. Fui ver as que ficavam de
fora e **três fecham ao centavo**:

| linha | apurado | publicado |
|---|---:|---:|
| Precatórios posteriores a 05/05/2000 | 5.595.401.507,77 | 5.595.401.507,77 |
| Passivo atuarial | 84.052.803.127,13 | 84.052.803.127,13 |
| Dívida contratual de PPP | 215.455.288,93 | 215.455.288,93 |

E retirei uma comparação indevida: **"Demais Dívidas Contratuais" não existe no
DCL publicado**. As contas 2.1.8.1.1 (53,6 mi) e 2.2.8.1.1 (218,7 mi) entram em
"Outras Dívidas" (941.926.197,62). Comparar contra zero era comparar contra a
planilha da equipe, não contra o homologado.

**RGF Anexo 2: 15 de 16 linhas exatas.** Livro: **298 de 301 (99,0%)**.

### A única que resta

| linha | apurado | publicado |
|---|---:|---:|
| (−) Restos a Pagar Processados | 3.306.229.590,47 | 750.866.596,13 |

É a que depende do relatório por fonte. As demais — inclusive as que eu dava como
"em aberto" — fecham.
