# Revisão geral do motor de demonstrativos fiscais do RN

Documento de 13/11/2026. **Ponto de entrada único**: consolida o que foi
descoberto, o que está verificado e o que resta. Substitui a leitura dispersa
dos demais documentos.

> **Como ler este documento.**
>
> | seção | o que é |
> |---|---|
> | **2** | **o estado atual** — o que fecha, o que não fecha e de quem depende |
> | 3 a 7 | como cada anexo é apurado, em uma página |
> | 8 a 17 | **histórico em ordem cronológica** das descobertas, com os números da época |
>
> As seções 8 a 17 são um **diário**, não o retrato de hoje. Números citados ali
> (ex.: "48 de 54", "8 de 14") foram verdadeiros numa data e hoje não são mais —
> vários foram superados por descobertas posteriores. **Para o estado atual, leia
> a seção 2 e a última seção 17** (a de número mais alto).
>
> O que garante o estado atual não é este texto: são os **78 testes** e o livro
> `saida/verificacao_anexos.xlsx`. Se o documento divergir do livro, o livro está
> certo.

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

### Em aberto — e de quem depende

| item | desvio | depende de |
|---|---:|---|
| **RGF Anexo 2 — RP Processados** | 2,56 bi | relatório "Execução Orçamentária por Fonte" (bloco de RP), por Poder |
| **RGF Anexo 1 — abril** | 5.241,65 | par de **anulação (35.094,19) e re-empenho (29.852,54)** no ND 31909203 do PO 10112, em abril. A linha II fecha exata: não é classificação. Imaterial (0,0008%). |
| RCL | — | é lida do Anexo 3: o bloco RPPS de deduções não existe na matriz |

Fora esses, **todos os anexos fecham**: 298 de 301 células exatas.

---

## 3. Como cada anexo é apurado

| anexo | fonte | critério |
|---|---|---|
| RREO 1 despesa | MSC classe 6 | conta 62213 por grupo de natureza |
| RREO 1 receita | MSC classe 6 | conta 6212/6213 + natureza (mapeamento) |
| RREO 2 | MSC classe 6 | conta de liquidação + função |
| RREO 3 | RREO Anexo 3 | RCL **lida** do homologado (o bloco RPPS não está na matriz) |
| RREO 7 | MSC classe 6 | contas 6.3.1 / 6.3.2 |
| RREO 9 | MSC classe 6 | 62213 por natureza 44/45/46 |
| RREO 14 | MSC classe 6 | empenhado, liquidado, pago |
| RREO 4 | MSC + mapeamento | ND × FS (função+subfunção) × FR × CO, menos o **PAE** do INEC |
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


### 17.32 RGF Anexo 2 de 2026 — e a descoberta do quadrimestre

Existem arquivos do RGF de 2026 (p1 e p2). Ao testar, o 2º quadrimestre dava
errado porque eu usei **junho** — mas o 2º quadrimestre fecha em **agosto**
(Jan–Abr, Mai–Ago, Set–Dez).

Em agosto, as três linhas da MSC fecham ao centavo:

| linha | apurado | publicado (p2/2026) |
|---|---:|---:|
| Disponibilidade de caixa bruta | 2.179.696.115,59 | 2.179.696.115,59 |
| (−) Depósitos restituíveis | 1.055.257.817,55 | 1.055.257.817,55 |
| Demais haveres financeiros | 266.702.621,21 | 266.702.621,21 |

As funções foram parametrizadas (`disponibilidade(ano, mes)`,
`depositos(ano, mes)`, `apurar_msc(..., ano, mes)`), de modo que p1 e p3 usam os
mesmos argumentos.

**Livro: 304 células, 301 exatas (99,0%).**

### A lição

O erro não era de dado nem de regra: era de **calendário**. Um quadrimestre não é
um bimestre, e o fechamento é em abril, agosto e dezembro — não em junho.


### 17.33 RGF Anexo 3 de 2026 — o cruzamento RREO → RGF

Os limites do RGF Anexo 3 não são apurados à parte: saem da RCL ajustada do
RREO Anexo 3.

```
RCL ajustada para endividamento (RREO Anexo 3, 2026 Q2) ... 20.961.883.945,10
x 22% .....................................................  4.611.614.467,92
limite publicado no RGF Anexo 3 ...........................  4.611.614.467,92
limite de alerta (90%) ....................................  4.150.453.021,13
publicado .................................................  4.150.453.021,13
```

É uma conferência de **dois documentos**: a RCL vem do RREO, o limite do RGF, e o
que os liga é uma constante legal (22%).

**Livro: 306 células, 303 exatas (99,0%).**


### 17.34 A aba de limites passou a ler o arquivo publicado

A `limites_anexo1()` tinha os valores esperados **fixos no código**. Agora ela lê
o `RGF-Anexo_06_24_2026_p2.csv` e compara contra o arquivo:

| linha | apurado | publicado (2026 Q2) |
|---|---:|---:|
| RCL ajustada para pessoal | 20.958.175.998,75 | 20.958.175.998,75 |
| DTP | 11.563.398.205,71 | 11.563.398.205,71 |
| DTP / RCL | 55,17% | 55,17% |
| Limite máximo (49%) | 10.269.506.239,39 | 10.269.506.239,39 |
| Limite prudencial (46,55%) | 9.756.030.927,42 | 9.756.030.927,42 |
| Limite de alerta (44,10%) | 9.242.555.615,45 | 9.242.555.615,45 |

**Seis de seis.** Livro: **307 células, 304 exatas (99,0%)**.

### Duas armadilhas no caminho

**1. A RCL ajustada aparece duas vezes no arquivo** — uma para endividamento e
outra para pessoal. A primeira leitura pegou a de endividamento e acusou
divergência falsa. Corrigido tomando a última ocorrência, com o motivo escrito.

**2. O nome completo da coluna é `VALOR ATÉ O QUADRIMESTRE DE REFERÊNCIA`** — a
comparação por igualdade falhava porque eu usava a forma truncada. Agora compara
por prefixo.

### Um aviso operacional

O `verificacao_anexos.xlsx` estava travado por outro processo (sincronização do
OneDrive) e a geração falhou com `PermissionError`. Regerou na segunda tentativa.
Se acontecer de novo, feche o arquivo ou aguarde alguns segundos.


### 17.35 Abril — a diferença de 5.241,65 tem endereço

Depois de descartar "empenho único" (não existia 5.241,65 em abril), fui às
contas do PO 10112 e achei o par:

```
622130200  ND 31909203  -35.094,19   (anulação)
622130200  ND 31909203  +29.852,54   (re-empenho)
                        -----------
                           5.241,65  = a diferença de abril
```

O homologado e o Comparativo tratam o par de anulação/re-empenho de forma
diferente. A linha II (não computadas) fecha exata, o que confirma: não é
classificação, é o tratamento do par.

A diferença é **0,0008%** da despesa bruta de abril — imaterial para o relatório,
mas agora com causa apontada em vez de "origem não identificada".


### 17.36 RP Processados — o DCL não usa o saldo do Anexo 7

Última verificação, e ela esclarece a confusão:

| conta no balancete | valor |
|---|---:|
| 6.3.2.1.1 (RP processados inscritos) | 470.465.377,32 |
| 6.3.1.3.1 (RP não processados inscritos) | 3.047.455,61 |
| 8.6.3.2.1.01 (controle) | 36.600,82 |

O `470.465.377,32` é **exatamente** o saldo de RP processados do RREO Anexo 7.

Mas o DCL publicado pede **750.866.596,13** — outro agregado. A diferença de
280.401.218,81 não está nessas contas.

Ou seja: a linha do DCL não é "o saldo de RP processados". É um recorte próprio
(por Poder e por fonte, excluindo FR 32, 46, 800, 801 e 802), que só o relatório
de execução por fonte produz.

**A seção da aba Base soma as contas-pai `6.3.1.3.0` e `6.3.2.1.0`, mais
`6.2.2.1.3.07` e `6.3.2.7.0` — e chega a 3,3 bi.** Não é o mesmo número por três
motivos: é conta-pai, inclui uma conta de empenho e não tem a dimensão de fonte.

Investigação encerrada. O que falta é o relatório.


### 17.37 O Anexo 1 do livro é de 2026 — e agora está rotulado

Descobri conferindo o CSV `RGF_RGF-Anexo_01_24_2026_p2.csv`: ele traz **12 meses**
(MR-1 a MR-11) e os nossos valores casam com MR-7 a MR-2 — janeiro a junho de
**2026**.

```
Janeiro   nosso 1.756.015.131,06  = MR-7
Fevereiro       1.168.704.572,00  = MR-6
Março           1.249.898.879,52  = MR-5
Abril             680.626.929,97  vs MR-4 680.632.171,62
Maio            1.244.370.847,54  = MR-3
Junho           1.309.400.172,65  = MR-2
```

As abas não diziam o ano — quem abrisse poderia supor 2025. Agora cada célula
traz `2026 — Mês — Linha`, e a aba se chama **"RGF Anexo 1 - 2026"**.

**22 de 24 exatas** (as duas de abril). Livro: **307 células, 304 exatas**.


### 17.38 Auditoria da régua — e a quinta referência errada

Os últimos erros do projeto não foram de apuração, foram de **referência**. Criei
`tests/test_baseline.py`, que lê o DCL publicado e confere, linha a linha, se o
`OFICIAL` do módulo carrega o valor do arquivo.

Ele encontrou na primeira execução:

| seção | no código | no DCL publicado |
|---|---:|---:|
| Outras Dívidas | 942.088.822,97 | **941.926.197,62** |

Diferença de 162.625,35 — a **quinta** referência errada do projeto. A seção não
entra na contagem (a aba Base não tem contas para ela), então nunca apareceu como
divergência; mas o valor no código estava errado.

O teste também obriga a manter o **mapa de nomes** completo: se alguém acrescentar
uma seção com valor esperado sem correspondência no DCL, ele acusa.

Suíte: **11 arquivos, 74 testes**.

### O placar das réguas erradas

| rodada | o que estava errado |
|---|---|
| 71 | comparava com a planilha da equipe, não com o publicado |
| 72 | comparava uma linha que não existe no DCL |
| 76 | valores esperados fixos no código |
| 80 | as abas não diziam o ano |
| **81** | **valor de "Outras Dívidas" 162.625,35 acima do publicado** |

Em todos, a apuração estava certa e a régua, torta.


### 17.39 A auditoria alcançou o Anexo 13

Os saldos de referência do PPP estavam fixos em `verificacao.anexo13()`. Passaram
a uma constante de módulo (`ANEXO13_REF`) e o teste confere os seis valores
(3 linhas × 2 exercícios) contra os CSVs publicados:

| linha | 2025 p6 | 2026 p4 |
|---|---:|---:|
| Total de ativos | 400.000.000,00 | 400.000.000,00 |
| Total de passivos | 215.455.288,93 | 196.757.187,16 |
| Atos potenciais passivos | 38.506.744,29 | 413.225.632,16 |

Todos batem.

### Anexo 4 também entrou — com um detalhe

Eu tinha dito que o Anexo 4 não poderia ser auditado por agregar blocos. Errado:
fui ao CSV e as quatro linhas existem, com nomes próprios:

| nossa chave | linha no CSV | valor |
|---|---|---:|
| `apos_civil` | Aposentadorias | 4.917.756.724,31 |
| `pens_civil` | Pensões por Morte | 640.868.408,22 |
| `inat_mil` | Inatividade | 675.066.910,71 |
| `pens_mil` | **Pensões (a segunda)** | 250.915.256,72 |

O detalhe: **"Pensões" aparece duas vezes** no arquivo — 119.906.956,64 no bloco
de benefícios mantidos pelo Tesouro e 250.915.256,72 no bloco militar. A linha do
anexo é a segunda. O teste usa a última ocorrência, com o motivo escrito.

Suíte: **11 arquivos, 76 testes**.

### O que a auditoria cobre agora

| grupo | auditoria |
|---|---|
| RGF Anexo 2 (DCL) | 14 linhas contra o DCL publicado |
| RREO Anexo 13 | 6 valores contra os CSVs |
| RREO Anexo 4 | 4 linhas contra o CSV |
| RGF Anexo 1, 3, 6, 7, 14 e RREO 2, 9 | leem o CSV na origem |


### 17.40 RP Processados — 2025 e 2026 não se comportam igual

Testei a mesma conta nos dois exercícios, com os balancetes reais:

| exercício | conta 6.3.2.1.0 | publicado no DCL | diferença |
|---|---:|---:|---:|
| **2026** (agosto) | 642.884.502,84 | 640.153.394,98 | **+2.731.107,86 (0,43%)** |
| **2025** (dezembro) | 470.465.377,32 | 750.866.596,13 | **−280.401.218,81 (−37%)** |

Em 2026 a conta **quase reproduz** a linha; em 2025 falta 37%.

A explicação provável: o balancete de 2026 é **consolidado** (traz os Poderes
somados) e o de 2025 é **só do Executivo** — e o DCL consolida sete Poderes.

Isso muda o diagnóstico: para 2025 falta a abertura por Poder, não uma regra
desconhecida. E para 2026 a diferença de 2,7 milhões (0,43%) é o que sobra da
mesma questão.

**A seção da aba Base, porém, soma quatro contas** — e é isso que produz os 3,3
bi. A conta certa é a `6.3.2.1.0` (ou a `6.3.2.1.1`), não as contas-pai mais a
conta de empenho.


### 17.41 RP Processados — a subconta melhora o 2026

Abrindo as subcontas do balancete de agosto/2026:

| conta | valor | contra 640.153.394,98 |
|---|---:|---:|
| 6.3.2.1.0 (pai) | 642.884.502,84 | +2.731.107,86 (0,43%) |
| **6.3.2.1.1** | **638.351.717,58** | **−1.801.677,40 (0,28%)** |
| 6.3.2.1.2 | 4.532.785,26 | — |
| 6.3.1.3.1 | 11.099.351,41 | — |

A `6.3.2.1.1` é **exatamente** o saldo de RP processados do RREO Anexo 7 de
2026 — e é a que mais se aproxima do DCL (0,28%).

Em 2025 ela dá 470.465.377,32 contra 750.866.596,13 — a mesma distância de 37%.
Ou seja: **a conta está certa; o que falta em 2025 é a consolidação dos Poderes.**

### O que pedir, então

Não é "o relatório de RP". É:

> o saldo de RP processados (conta 6.3.2.1.1) **por Poder**, em 31/12/2025.

Com isso a linha fecha — e a diferença de 2026 (0,28%) sugere que a mesma
abertura resolve os dois anos.


### 17.42 RP Processados — a seção conta o mesmo valor duas vezes

Abrindo as quatro contas da seção da aba Base:

| conta | valor |
|---|---:|
| 6.2.2.1.3.07.00 | 1.416.358.378,77 |
| **6.3.2.7.0.00.00** | **1.416.358.378,77** |
| 6.3.1.3.0.00.00 | 3.047.455,61 |
| 6.3.2.1.0.00.00 | 470.465.377,32 |

`6.2.2.1.3.07` e `6.3.2.7` têm **exatamente o mesmo valor** — são o empenho e o seu
controle. Somar as duas duplica 1,4 bilhão, e é isso que produz os 3,3 bi.

### E o estoque de RP tem ano de inscrição

O `6.3.2.1` se distribui assim:

| ano de inscrição | valor |
|---|---:|
| 2017 | 22.087,50 |
| 2018 | 42.649.221,62 |
| 2019 | 17.103.801,52 |
| 2020 | 36.177.634,72 |
| 2021 | 48.003.311,56 |
| 2022 | 21.747.780,09 |
| 2023 | 54.541.574,95 |
| 2024 | 250.219.965,36 |
| **total** | **470.465.377,32** |

**Não há inscrição de 2025** nessa conta. O publicado é 750.866.596,13 — a
diferença de 280.401.218,81 é, com alta probabilidade, a **inscrição de 2025**,
que a essa altura ainda não estava nessa conta.

Isso explica por que 2026 quase fecha (0,28%) e 2025 não: o corte de exercício.

### O que pedir, agora com precisão

> RP processados inscritos **em 2025** (o que foi inscrito em 1º/01/2026),
> por Poder.

Não é o saldo de anos anteriores — esse nós já temos (470,5 mi, por ano de
inscrição).


### 17.43 RP Processados — a inscrição de 2025 existe, mas não é a diferença

A matriz de 2026 traz o ano de inscrição preenchido. Em janeiro de 2026:

| ano de inscrição | valor |
|---|---:|
| 2017 a 2024 (estoque) | 465.226.819,63 |
| **2025** | **1.005.773.328,13** |
| total | 1.470.741.103,94 |

A inscrição de 2025 é de **1,0 bilhão** — muito maior que a diferença de
280.401.218,81 que eu esperava explicar.

Logo, a linha do DCL **não é o estoque total** nem o estoque mais a inscrição.

### O que os números dizem

| referência | valor |
|---|---:|
| estoque de RP processados em 31/12/2025 (2017–2024) | 470.465.377,32 |
| inscrição de 2025 (vista em 01/2026) | 1.005.773.328,13 |
| **DCL publicado, 3º quadrimestre de 2025** | **750.866.596,13** |

O DCL fica **entre** os dois. Não é a soma nem o estoque.

### A hipótese que sobra

O DCL deduz da disponibilidade o RP processado **que ainda onera o caixa** — ou
seja, o estoque **menos o que já foi pago**, com recorte por fonte. Os valores
trimestrais (961,9 / 684,4 / 750,9 milhões) oscilam como **saldo**, não como
fluxo — e nenhum deles coincide com o nosso estoque de 470,5.

**Conclusão:** a linha exige a posição por Poder e por fonte numa data. É a
mesma conclusão de antes, agora com um dado a mais: a inscrição de 2025 é de
1,0 bilhão, e o DCL usa 750,9 — um recorte intermediário.


### 17.44 RP Processados — o estoque mês a mês e o publicado

Comparando o estoque da conta `6.3.2.1` com o DCL publicado em cada fechamento:

| fechamento | nosso estoque | publicado | diferença |
|---|---:|---:|---:|
| agosto/2025 (Q2) | 661.419.626,59 | 684.383.327,91 | +22.963.701,32 (3,4%) |
| setembro/2025 | 636.243.966,64 | — | — |
| outubro/2025 | 576.457.774,57 | — | — |
| dezembro/2025 (Q3) | 470.465.377,32 | 750.866.596,13 | +280.401.218,81 (37%) |

O estoque **cai** ao longo do ano (661 → 470 milhões): os RP vão sendo pagos.

O publicado **não acompanha** essa queda — e em dezembro salta para 750,9.

### O que isso mostra

Se a linha fosse o estoque, ela cairia junto. Ela sobe no fim do ano porque
**incorpora a inscrição do exercício** — os empenhos de 2025 não pagos, que viram
RP em 1º/01/2026.

Em agosto a diferença é pequena (3,4%) porque a inscrição do ano ainda não
pesou. Em dezembro é grande (37%) porque é exatamente o momento do corte.

### O pedido, com a data certa

> RP processados **em 31/12/2025**, com o recorte que o DCL usa — incluindo a
> inscrição do exercício e excluindo o que já foi pago, por Poder e por fonte.

É a mesma linha que o Estado publica; o que falta é a abertura que a produz.


### 17.45 RGF de 2026 — os dois quadrimestres

Os arquivos de 2026 existem para o 1º e o 2º quadrimestres. Conferindo as três
linhas da DCL que saem da matriz:

| linha | Q1 (abril) | Q2 (agosto) |
|---|---:|---:|
| Disponibilidade de caixa bruta | 2.025.641.419,41 | 2.179.696.115,59 |
| (−) Depósitos restituíveis | 925.488.506,04 | 1.055.257.817,55 |
| Demais haveres financeiros | — | 266.702.621,21 |

Todas exatas nos dois fechamentos.

O Q1 acrescentou três células e o livro passou a **310 células, 307 exatas
(99,0%)**.

### O que isso mostra sobre a regra

As mesmas três funções — `disponibilidade(ano, mes)`, `depositos(ano, mes)` e
`apurar_msc(..., ano, mes)` — servem para abril e para agosto, e servirão para
dezembro. A regra não é do período: é da conta.

### Onde o projeto está, aos 90 rounds

| item | situação |
|---|---|
| leitor do formato longo | pronto, com testes |
| RGF Anexo 1 por Poder | 100 de 100 |
| RGF Anexos 3, 4, 5, 6 | fechados |
| RGF Anexo 2 | **15 de 16** (falta o RP processados de 2025) |
| RREO 1, 2, 3, 4, 7, 9, 13, 14 | fechados, 2025 e 2026 |
| livro de verificação | 310 células, 307 exatas |
| auditoria da régua | 24 valores conferidos contra os arquivos |
| testes | 76, em 11 arquivos |

**O que falta:** uma linha — RP processados em 31/12/2025, por Poder e fonte —
e as duas células de abril de 2026, cuja causa é um par de anulação de 5.241,65.


### 17.46 A prosa do README tambem entrou na trava

`test_coerencia.py` ja comparava os **numeros** do README com a planilha. Faltava a
**prosa**: o README anuncia "15 de 16 linhas" do Anexo 2 — e essa contagem era
escrita a mao.

Agora um teste le a frase do README, roda a apuracao do Anexo 2 e compara:

```
README:  15 de 16
apuracao: 15 de 16   OK
```

Se alguma linha fechar (ou abrir) sem o texto acompanhar, o teste falha.

### O que ainda escapa

Frases sem numero — "os Depositos fecharam", "a ancora esta parametrizada" — nao
tem como ser verificadas automaticamente. Foi o que produziu as duas linhas
obsoletas da rodada 91.

A diferenba e que agora a **contagem** esta amarrada; a narrativa continua sendo
revisada a mao.

Suite: **11 arquivos, 77 testes**.


### 17.47 Os tres documentos passam a ser comparados

O console, a aba RESUMO e o `DIVERGENCIAS.md` diziam numeros diferentes — porque
o gerador do .md somava os grupos do motor duas vezes. Corrigido na rodada 93, e
agora ha um teste que compara o .md com a planilha:

```
console:          307 de 310
aba RESUMO:       307 de 310
DIVERGENCIAS.md:  307 de 310
```

Se um dos tres divergir, o teste falha. Nao adianta corrigir um e esquecer os
outros dois — foi exatamente o que aconteceu.

Suite: **11 arquivos, 78 testes**.

### O placar dos erros de contagem

| rodada | onde | o que acontecia |
|---|---|---|
| 68 | console | somava os grupos sem a mescla do motor |
| 93 | DIVERGENCIAS.md | somava os grupos **duas vezes** |
| 94 | os tres | agora comparados entre si |


### 17.48 RP Processados — a matriz só tem o Executivo

Abertura do `6.3.2.1` por Poder nos fechamentos de 2025:

| fechamento | Executivo (10111) | RPPS (10112) | TJ (30390) | outros | total |
|---|---:|---:|---:|---:|---:|
| setembro | 622.407.726,27 | 13.282.469,76 | 550.382,10 | 3.388,51 | 636.243.966,64 |
| outubro | 562.629.707,91 | 13.282.469,76 | 542.209,47 | 3.388,51 | 576.457.774,57 |
| dezembro | 462.168.338,94 | 7.772.920,77 | 523.880,63 | 177,98 | 470.465.377,32 |

**O Executivo responde por 97,8% do total.** Os demais Poderes aparecem com
valores residuais — algumas centenas de milhares de reais.

O DCL publicado em setembro é **750.866.596,13**, e o nosso total é
636.243.966,64. A diferença de 114,6 milhões **não está em nenhum Poder** da
matriz.

### O que isso prova

A MSC carrega o RP do Executivo e do RPPS. Os RP do Legislativo, Judiciário,
Ministério Público, TCE e Defensoria **não estão lá** — ou estão incompletos.

Como o DCL consolida os sete Poderes, a linha não fecha por construção: falta a
parcela dos outros cinco.

### Investigação encerrada de vez

Foram testados, nesta ordem: conta-pai, conta-filha, classe 8, ano de inscrição,
duas datas de corte, três meses e todos os Poderes. Nenhum caminho reproduz o
publicado.

**O que falta é uma coisa só:** o RP processado dos sete Poderes em 31/12/2025,
por fonte, incluindo a inscrição do exercício.


### 17.49 RP Processados — o método estava na planilha, na aba RP_MSC

A planilha da equipe tem uma aba chamada **"RP_MSC"**, que eu nunca tinha aberto.
Ela traz a receita do bolo:

```
RPP
  6.2.2.1.3.07.00.00   (na MSC: zero)
  6.3.1.3.0.00.00.00
  6.3.2.1.0.00.00.00
  (-) fontes 32, 46, 800
```

Duas coisas que a nossa seção errava:

1. **`6.2.2.1.3.07` é zero** — a nossa seção o somava, e ele valia 1,4 bilhão
   (duplicando com `6.3.2.7`, que tem o mesmo valor);
2. **as fontes 32, 46, 800, 801 e 802 são excluídas** — nós não excluíamos nada.

### O teste que prova o método

Aplicando `(6.3.1.3 + 6.3.2.1)` sem 32/46/800/801/802:

| fechamento | apurado | publicado | diferença |
|---|---:|---:|---:|
| **agosto/2025 (2º Q)** | **684.383.327,91** | **684.383.327,91** | **0,00** |
| dezembro/2025 (3º Q) | 473.395.418,78 | 750.866.596,13 | −277.471.177,35 |
| abril/2026 (1º Q) | 842.711.344,20 | 816.322.476,17 | +26.388.868,03 |
| agosto/2026 (2º Q) | 649.144.802,70 | 640.153.394,98 | +8.991.407,72 |

**Em agosto de 2025 fecha ao centavo.** O método está certo.

### Por que ainda não fecha nos outros

- **dezembro/2025**: é o corte de exercício — a inscrição de 2025 (1,0 bilhão)
  ainda não está na conta nessa data;
- **2026**: sobra 1,4% a 3,2%, provavelmente por uma conta ou fonte que mudou de
  comportamento no ano.

### O ganho

| | antes | agora |
|---|---:|---:|
| apurado | 3.306.229.590,47 | **473.395.418,78** |
| desvio | 2.555.362.994,34 | **277.471.177,35** |

**Nove vezes menor.** E agora o sinal está certo: estamos **abaixo** do publicado,
como o corte de exercício explica.

O livro segue com **310 células, 307 exatas** — a linha ainda não fecha, mas o
número agora é o da conta certa.


### 17.50 As abas que faltavam: RP, 2x6, 2x7 e Outros Ajustes

Depois de 98 rodadas, faltava abrir quatro abas da planilha da equipe. Elas
existem e são ricas:

**"RP"** — o método completo do bloco de restos a pagar, com as exclusões por
fonte lado a lado:

| linha | Total | (-) 32 | (-) 46 | (-) 800 | (-) 802 |
|---|---:|---:|---:|---:|---:|
| `6.3.1.3` RP não proc. liquidado a pagar | 3.047.455,61 | 0 | 0 | 0 | 0 |
| `6321` RP proc. a pagar | 469.941.259,71 | 0 | 0 | 117.414,14 | 0,01 |
| `6.2.2.1.3.07` empenhos liquidados não pagos | 1.405.948.478,02 | 6.105.962,94 | 31.819.653,82 | 159.070.781,68 | 1.206,18 |

E, abaixo, o mesmo bloco **por Poder**, com sete linhas (Executivo, TJ, FDM, AL,
MP, TCE, DP).

**"2x7"** — o RP processados e não processados por Poder, com os valores do
Anexo 7 ao lado e as conferências linha a linha.

**"2x6"** — o Anexo 2 contra o Anexo 6, com a DCL e as três deduções.

**"Outros Ajustes"** — ajustes por Poder (TCE, DP, MP, TJ, FDM, AL) que somam
72.924.270,31 numa coluna e −719.977.584,11 noutra.

### O que isso muda

1. **O método do RP está documentado pela própria equipe** — e é o que
   implementamos (`6.3.1.3` + `6.3.2.1` menos 32/46/800/801/802), confirmado ao
   centavo em agosto/2025.
2. **A aba "RP" inclui o `6.2.2.1.3.07`** (empenhos liquidados e não pagos) na
   conta — e a nossa seção o somava com o sinal errado, duplicando com `6.3.2.7`.
3. **O total da aba "RP" (1,68 bi) não é o valor do DCL (752,06 mi)** — são
   recortes diferentes. Isso explica por que nenhuma combinação simples fechava.

### O que continua faltando

A aba "RP" tem os valores **por Poder**, mas os números são de **outro mês** (o
`6321` vale 469.941.259,71 ali e 470.465.377,32 na MSC de dezembro). Para
reproduzir o DCL de 31/12/2025 seria preciso rodar o mesmo relatório naquela data.


### 17.51 RP Processados — a fórmula completa, e o que ela prova

A aba "Base" aponta para `RP!K22`, e a aba "RP" mostra a conta:

```
K20 = SUM(K13:K19)          -> soma por Poder (1.694.111.739,40)
K21 = 942.052.222,15        -> conta 8.6.3.2.2 (valor manual)
K22 = K20 - K21             -> 752.059.517,25
```

A nota da célula K21 diz: *"Só tem saldo em caso de disponibilidade negativa"*.
Isto é: o controle **não é sempre 942 milhões** — é um valor que aparece em
situações específicas.

### A fórmula implementada

```
RP = (6.3.1.3 + 6321 + 6.2.2.1.3.07, sem fontes 32/46/800/801/802)
     - controle (8.6.3.2.2)
```

Com `controle=0`:

| fechamento | apurado | publicado | diferença |
|---|---:|---:|---:|
| agosto/2025 | **684.383.327,91** | **684.383.327,91** | **0,00** |

Com `controle = 942.052.222,15`:

| fechamento | apurado | publicado | diferença |
|---|---:|---:|---:|
| dezembro/2025 | 788.629.587,54 | 750.866.596,13 | +37.762.991,41 (5,0%) |

### O ganho em três rodadas

| rodada | apurado | desvio |
|---|---:|---:|
| 97 | 3.306.229.590,47 | 2.555.362.994,34 |
| 98 | 473.395.418,78 | 277.471.177,35 |
| **100** | **788.629.587,54** | **37.762.991,41** |

**68 vezes menor** que há três rodadas.

### O que ainda sobra

Os 37,8 milhões restantes têm uma causa provável e verificável: o controle
`8.6.3.2.2` vale **942.052.222,15** na planilha da equipe, mas seria preciso
**979.815.213,56** para fechar em dezembro. Ou seja: o valor do controle muda
com a data, e o que temos é o de outro mês.

É a mesma natureza do PAE do Anexo 4: um insumo externo, parametrizado e
documentado, não uma regra que se deduza da matriz.

O livro segue com **310 células, 307 exatas** — a linha ainda não fecha, mas o
número agora está a 5% do publicado, com o método provado num período e a causa
do resto identificada.


### 17.52 O controle da classe 8 confirma a nossa soma

A conta de controle do RP na classe 8 é `821130100`. Em dezembro/2025:

| | valor |
|---|---:|
| controle `821130100` (classe 8) | **1.889.871.211,70** |
| nossa soma `6.3.1.3 + 6321 + 6.2.2.1.3.07` (classe 6) | **1.889.871.211,70** |

**Idênticos.** Isso valida a leitura das contas: a classe 8 é o espelho da
classe 6, e a nossa soma está certa.

O que falta não é conta — é o **valor do controle 8.6.3.2.2** que a equipe deduz.
Ele não está na classe 8 da matriz (as 36 contas de dezembro não trazem nenhuma
com 979.815.213,56), e na planilha está como número digitado, com a nota *"só tem
saldo em caso de disponibilidade negativa"*.

### Onde a linha está

| | valor |
|---|---:|
| nossa soma (classe 6, sem exclusões) | 1.889.871.211,70 |
| após excluir fontes 32/46/800/801/802 | 1.730.681.809,69 |
| após deduzir o controle (942.052.222,15) | **788.629.587,54** |
| publicado | 750.866.596,13 |
| **diferença** | **37.762.991,41 (5,0%)** |

Para fechar, o controle em dezembro precisaria ser **979.815.213,56** — e o que
temos é o de outro mês.

### O que isso significa para segunda

A linha está a **5%** do publicado, com o método provado ao centavo em agosto. O
que resta é **um número de uma data**: o saldo da conta 8.6.3.2.2 em 31/12/2025.

Se a equipe extrair o relatório de RP daquela data, o controle sai junto — e a
linha fecha.


### 17.53 O mapa do livro de verificacao

`saida/verificacao_anexos.xlsx` tem **27 abas**. Elas nao seguem a ordem dos
anexos, e duas tinham nomes que se confundiam (`RGF Anexo 1` para os totais e
`RGF Anexo 1 - 2026` para os meses). Corrigido: as abas de total agora dizem
"- totais" no nome.

| aba | linhas | o que tem |
|---|---:|---|
| RESUMO | 26 | uma linha por aba, com celulas e exatas |
| RGF Anexo 1 - 2026 | 24 | I, II e III por mes (jan-ago) |
| RGF Anexo 1 - por Poder | 100 | 5 Poderes x 10 meses x 2 rubricas |
| RGF Anexo 1 - limites | 6 | RCL ajustada, DTP e os tres limites |
| RGF Anexo 1 - totais | 2 | despesa bruta e liquida do periodo |
| RGF Anexo 2 | 16 | as 16 linhas da DCL |
| RGF Anexo 2 - 2026 | 6 | Q1 e Q2 |
| RGF Anexo 5 | 90 | as 90 celulas da vinculacao |
| RGF Anexo 5 - totais | 5 | os 5 totais de coluna |
| RREO Anexo 1 / 3 / 7 / 9 / 13 / 14 | 3 a 6 cada | os anexos do RREO |
| RREO Anexo 2 - 2026 | 1 | total liquidado das 22 funcoes |
| RREO Anexo 4 | 4 | as quatro linhas previdenciarias |
| RREO Anexo 13 - projecoes | 6 | as seis projecoes do PPP |
| motor | 1 | saldo x movimento das contas de resultado |

As quatro abas com "- 2026" sao as do exercicio corrente; as demais comparam
2025. O RESUMO agrega tudo e e o que o teste de coerencia confere contra o README.


### 17.54 Abril aparece igual nos dois quadrimestres de 2026

Os arquivos do 1º e do 2º quadrimestre de 2026 têm janelas diferentes (um termina
em abril, o outro em agosto), mas os meses em comum trazem **os mesmos números**:

| mês | p1 (1º Q) | p2 (2º Q) | nosso |
|---|---:|---:|---:|
| janeiro | 1.756.015.131,06 | 1.756.015.131,06 | 1.756.015.131,06 |
| fevereiro | 1.168.704.572,00 | 1.168.704.572,00 | 1.168.704.572,00 |
| março | 1.249.898.879,52 | 1.249.898.879,52 | 1.249.898.879,52 |
| abril | **680.632.171,62** | **680.632.171,62** | 680.626.929,97 |

Três coisas:

1. os dois arquivos são **consistentes entre si** — não é erro de transcrição nem
   de versão do relatório;
2. a divergência de abril **aparece nos dois**, sempre no mesmo valor;
3. ela é sempre de **5.241,65** — o par de anulação e re-empenho identificado na
   rodada 78.

### A janela de cada arquivo

O 1º quadrimestre usa `MR-3` para janeiro e `MR` para abril; o 2º usa `MR-7` para
janeiro e `MR-8` para dezembro do ano anterior. Comparar os dois exige mapas de
coluna diferentes — foi o que me fez ver, por um instante, quatro divergências
que não existiam.

### O que isso muda

Nada no placar: abril segue com as duas células divergentes. Mas elimina a
hipótese de "arquivo desatualizado" — a divergência é do dado, não da extração.


### 17.55 Cinco modulos de anexo existem fora do livro

Conferi quais modulos de anexo o repositorio tem e quais o livro usa:

| modulo | situacao |
|---|---|
| `rgf_anexo2_dcl` | no livro |
| `rgf_anexo5_vinculacao` | no livro |
| `rreo_anexo13` | no livro |
| `rreo_anexo14` | no livro |
| `rreo_anexo1_grupos` | no livro |
| `rreo_anexo2` | no livro |
| `rreo_anexo4_blocos` | no livro |
| `rreo_anexo7` | no livro |
| `rreo_anexo9` | no livro |
| **`rgf_anexo2_base`** | **fora** — superado por `rgf_anexo2_dcl` |
| **`rgf_anexo5_disp`** | **fora** — superado por `rgf_anexo5_vinculacao` |
| **`rreo_anexo1_receita`** | **fora** — a receita hoje sai do grupo `RREO Anexo 1` |
| **`rreo_anexo2_intra`** | **fora** — diagnostico de intra-orcamentaria |
| **`rreo_anexo7_poder`** | **fora** — valida o recorte de PO; usa caminho antigo (`siconfi_rn_completo`) |

### O que isso significa

Nenhum deles e necessario para o livro. Quatro sao versoes anteriores, mantidas
como registro; um (`rreo_anexo7_poder`) e uma validacao com caminho que nao
existe mais.

**Nao apaguei.** O `rreo_anexo2_intra` documenta o diagnostico da despesa
intra-orcamentaria, que foi uma pista real; e o `rreo_anexo7_poder` guarda o
de-para de PO por Poder, que pode voltar a ser util.

O que faltava era saber que eles estao fora — agora esta escrito.


### 17.56 RP Processados — investigacao encerrada, de vez

Ultimo teste: procurar uma fonte de recursos cujo valor isolado explicasse a
diferenca de 36.570.070,29 entre a nossa soma e a da equipe.

| verificacao | resultado |
|---|---|
| alguma fonte isolada com ~36,57 mi | **nenhuma** (tolerancia de 5%) |
| a aba "Outros Ajustes" contem o controle | nao — sao ajustes por Poder, com BI2 ≈ 2 × BI1 |

Conclusao: **o valor da equipe (K20) e de outro mes**. O `6321` vale
469.941.259,71 na planilha e 470.465.377,32 na MSC de dezembro — 524 mil de
diferenca só nessa conta.

### O que fica estabelecido

| | |
|---|---|
| metodo | `(6.3.1.3 + 6321 + 6.2.2.1.3.07) − 8.6.3.2.2`, sem fontes 32/46/800/801/802 |
| prova | **agosto/2025 fecha ao centavo** com controle zero |
| dezembro | 788.629.587,54 contra 750.866.596,13 (5,0%) |
| o que falta | o saldo de **8.6.3.2.2 em 31/12/2025** (aqui seria 979.815.213,56) |

### Por que parar aqui

Onze rodadas de investigacao sobre esta linha — 79 a 110 — e o que restou foi um
**numero de uma data**. Nao ha mais hipotese a testar que nao seja "tentar outro
mes". Testei cinco contas, tres meses, dois cortes e todas as fontes.

A linha esta a **5,0%**, com o metodo provado noutro periodo. E o melhor que os
dados permitem.

**Encerrado.** As proximas rodadas vao para o que ainda nao foi coberto: o Anexo
1 de 2026 no 1º quadrimestre, o Anexo 6 do RREO e a conferencia do 3º
quadrimestre quando os dados chegarem.


### 17.57 Duas celulas estavam "OK" por tolerancia

Descoberta da rodada 113, e ela muda o placar.

O `verificar_tudo` compara com **tolerancia de 0,5%** e marca "OK" quando o desvio
cabe nela. O livro usava esse veredito. Resultado: duas linhas do Anexo 1 de 2025
apareciam como exatas sendo que nao eram:

| linha | apurado | publicado | desvio |
|---|---:|---:|---:|
| Despesa bruta (I), total de 2025 | 15.422.754.491,59 | 15.478.621.265,08 | **−55.866.773,49** |
| Despesa liquida (III), total de 2025 | 11.086.434.730,47 | 11.001.153.864,38 | **+85.280.866,09** |

**56 e 85 milhoes** marcados como "OK".

### A correcao

O livro passou a exigir o **centavo** em todas as linhas, inclusive nas que vem
do `verificar_tudo`. Quando a conferencia de origem aceita 0,5% e o livro nao, a
diferenca fica registrada na coluna de observacao.

**Placar honesto: 305 de 310** (era 307). As duas linhas agora aparecem como
divergentes, com causa:

> Total anual de 2025 apurado pela via da MSC (`apurar_janela`), nao pela MAPA do
> SIGEF que sustenta o Anexo 1 de 2026. A MSC nao identifica a parcela
> intra-orcamentaria, que a equipe conhece pelo SIGEF.

### O que isso ensina

Uma tolerancia de 0,5% parece razoavel ate se ver o que ela esconde: em despesa
com pessoal, 0,36% sao 56 milhoes.

O numero caiu. Mas o numero anterior estava errado — e um placar que inclui
"quase" nao serve para conferir nada.


### 17.59 RP Processados — o mecanismo completo, do inicio ao fim

Abri o relatorio oficial `RGF 2025_3Q_02` e a aba `RP` responde tudo.

#### A formula da equipe

```
Por Poder:  I = Inscritos ant. + Insc. exerc. + Liquidados RPNP
                - Pagos RPP - Pagos RPNP - Cancelados RPP + Inscritos (Liq-Pg)
            J = exclusoes (fontes 32, 46, 800, 801, 802)
            K = I - J

Executivo:  I = 1.878.937.193,34   J = 197.115.018,77   K = 1.681.822.174,57
Demais:     I = 12.289.564,83      J = 0               K = 12.289.564,83
TOTAL:      I = 1.891.226.758,17   J = 197.115.018,77   K = 1.694.111.739,40

K22 = K20 - 942.052.222,15 = 752.059.517,25
```

#### O que e a conta 8.6.3.2.2

O proprio nome, na aba CONTAS:

> `CONTROLE DE OBRIGACOES INSCRITAS EM RPP, SEM DISPONIBILIDADE DE CAIXA, PARA FINS DA LRF`

E a **Nota 4** do relatorio explica:

> Na linha "Outras Dividas" foi registrado o valor de R$ 942.052.222,15. Esse
> valor refere-se ao saldo de restos a pagar inscritos **sem a devida
> disponibilidade de caixa**. Esse montante foi transferido...

Ou seja: o RP inscrito sem caixa **sai da deducao e entra na divida**. E por isso
que "Outras Dividas" publica 941.926.197,62 — quase os mesmos 942 milhoes.

#### Por que a nossa conta dava 5% de diferenca

| | nosso (MSC) | equipe (relatorio) |
|---|---:|---:|
| total bruto (I) | 1.889.871.211,70 | 1.891.226.758,17 |
| exclusoes (J) | **159.189.402,01** | **197.115.018,77** |
| liquido (K) | 1.730.681.809,69 | 1.694.111.739,40 |

A diferenca de 37,9 milhoes esta **nas exclusoes**, nao nas contas. A MSC tem a
dimensao de fonte, mas nao a mesma abertura do relatorio de execucao: 37,9 milhoes
de exclusao existem la e nao aqui.

#### A cadeia inteira, explicada

```
1.891.226.758,17  (bruto por Poder, do relatorio)
 -  197.115.018,77 (exclusoes por fonte, do relatorio)
 = 1.694.111.739,40 (K20)
 -  942.052.222,15 (RP sem disponibilidade, Nota 4)
 =  752.059.517,25 (K22, o que a planilha publica)
 -    1.192.921,12 (a divergencia de AL/FDM que achamos na rodada 71)
 =  750.866.596,13 (o CSV do Siconfi)
```

**Toda a diferenca de 2,56 bilhoes que eu persegui por 20 rodadas era isto:** a
secção da planilha somava `6.2.2.1.3.07` e `6.3.2.7` duas vezes, e a conta certa
exclui o RP sem caixa, que vira divida.

#### O que isso muda

A linha **nao e um enigma**. E uma regra conhecida, com quatro parcelas:

| parcela | de onde sai |
|---|---|
| bruto por Poder (I) | relatorio de execucao, por Poder |
| exclusoes por fonte (J) | **relatorio de execucao, por fonte** |
| RP sem disponibilidade | conta 8.6.3.2.2, ajuste da equipe |
| AL/FDM | recorte que a MSC nao separa |

As duas do meio sao as que faltam — e ambas vem do **mesmo relatorio**.


### 17.60 O manual da equipe tem 302 conferencias — faziamos 22

Descoberta da rodada 119: a `PLANILHA DE CONFERENCIAS ATUALIZADA` da equipe tem
**40 abas**, e a aba `Conf. RGF SICONFxEXCEL` compara linha a linha cada anexo do
RGF entre o Siconfi e o Excel deles.

| anexo | linhas que o manual confere | nos conferiamos |
|---|---:|---:|
| Anexo 1 | 90 | 24 (+100 por Poder) |
| Anexo 2 | 65 | 22 |
| Anexo 3 | 42 | 1 |
| Anexo 4 | 53 | 1 |
| Anexo 6 | 52 | 4 |

### O que ja foi absorvido

**Anexo 2 — seis somas** (rodada 119): Emprestimos, Parcelamento e Divida
Contratual fecham ao centavo; DC, DEDUCOES e DCL divergem por causa conhecida
("Outras Dividas" nao tem lista de contas).

**Anexo 6 — quatro linhas** (rodada 120): limite maximo, prudencial, alerta e DTP.
Os tres limites fecham; o DTP herda o desvio de 2025.

### O que o manual revelou sobre o RP

A aba `RP` do relatorio oficial tem a formula inteira — e as exclusoes (coluna J)
vem de **valores digitados**, do relatorio de execucao por fonte:

| fonte | MSC (dez/2025) | equipe |
|---|---:|---:|
| 32 | 0,00 | 6.105.962,94 |
| 46 | 0,00 | 31.819.653,82 |
| 800 | 159.188.195,82 | 159.070.781,68 |
| 802 | 1.206,19 | 1.206,18 |

Os 37,9 milhoes que faltavam sao as fontes **32 e 46** — que no relatorio da
equipe tem valor e na MSC de dezembro valem zero. Mais uma confirmacao de que os
numeros deles sao de **outra data**.

### O caminho daqui

O manual e um roteiro. Cada anexo tem dezenas de linhas que ainda nao conferimos,
e muitas sao **somas** das parcelas que ja apuramos — como as seis do Anexo 2.
Implementar as somas nao fecha celula nova por apuracao: **verifica se a parcela
esta na linha certa**, que e um erro que a conferencia linha a linha nao pega.


### 17.61 Anexo 3 — as garantias sao zero, e agora esta provado

O manual da equipe confere **37 linhas** no Anexo 3: garantias concedidas aos
estados, municipios, entidades controladas e fundos, mais as contragarantias.

O CSV publicado do Siconfi tem **20 linhas** — e nenhuma delas e garantia. Sao a
cadeia da RCL e os dois limites, em quatro periodos.

### Por que

A matriz de dezembro/2025 **nao tem nenhuma conta 8.5** (o grupo das garantias).
Sem conta, nao ha valor a publicar — e o CSV so traz a estrutura.

Isso significa que as 37 linhas do manual ou sao zero, ou sao a propria cadeia da
RCL. Nao ha R$ de garantia a conferir.

### O que passou a ser conferido

| linha | apurado | publicado |
|---|---:|---:|
| RCL (VI) | 19.513.846.659,98 | 19.513.846.659,98 |
| (−) Transferencias obrigatorias | 4.499.856,06 | 4.499.856,06 |
| RCL ajustada (VIII) | 19.509.346.803,92 | 19.509.346.803,92 |
| Limite do Senado (22%) | 4.292.056.296,86 | 4.292.056.296,86 |
| Limite de alerta | 3.862.850.667,18 | 3.862.850.667,17 |

**Cinco de cinco**, com o limite de alerta a um centavo de distancia (truncamento
da publicacao).

### O erro que apareceu no caminho

As funcoes do modulo devolvem os **nomes truncados** (52 caracteres), e o CSV tem
o nome inteiro — a comparacao por igualdade falhava em duas linhas. Passou a casar
pelo prefixo mais longo.

E o mesmo tipo de armadilha do Anexo 4 ("Pensoes" duas vezes) e do Anexo 6
(VALOR e % por linha): **o nome nao e chave confiavel neste formato**.

### Placar do Anexo 3

| | antes | agora |
|---|---:|---:|
| linhas conferidas | 1 | **5** |
| exatas | 1 | **5** |

E, das 37 do manual, 32 sao garantias zeradas — nao ha o que conferir contra o
CSV, porque o CSV nao as publica.


### 17.62 Anexo 4 — oito de oito, e o que o CSV nao publica

O manual confere **53 linhas** no Anexo 4. O CSV publicado tem **19**.

O que passou a ser conferido:

| linha | apurado | publicado |
|---|---:|---:|
| RCL (IV) | 19.513.846.659,98 | 19.513.846.659,98 |
| (−) Transferencias obrigatorias | 4.499.856,06 | 4.499.856,06 |
| RCL ajustada | 19.509.346.803,92 | 19.509.346.803,92 |
| Operacoes contratadas ate o quadrimestre | 2.491.012,67 | 2.491.012,67 |
| Operacoes — % sobre a RCL ajustada | 0,01 | 0,01 |
| Limite geral (16%) | 3.121.495.488,63 | 3.121.495.488,63 |
| Limite de alerta (14,4%) | 2.809.345.939,76 | 2.809.345.939,76 |
| Limite para ARO (7%) | 1.365.654.276,27 | 1.365.654.276,27 |

**Oito de oito.**

### As 45 linhas que sobram

As operacoes de credito do RN em 2025 sao de **R$ 2.491.012,67** — 0,01% da RCL.
O valor e tao pequeno que o demonstrativo detalhado (contratual, interna,
emprestimos, por Poder) se reduz a tres linhas repetindo o mesmo numero.

O CSV traz `Contratual`, `Interna`, `Emprestimos` e `TOTAL (III)` com **o mesmo
valor**, em duas colunas. E o manual confere cada uma delas separadamente.

### O padrao que se repete nos tres anexos

| anexo | linhas no manual | linhas no CSV | o que sobra |
|---|---:|---:|---|
| 3 — garantias | 37 | 20 | garantias zeradas |
| 4 — operacoes | 53 | 19 | tres linhas repetidas |
| 6 — resumo | 52 | 23 | repete os outros anexos |

Nos tres, boa parte do que o manual confere **nao existe no arquivo publicado** —
porque e zero, e repeticao, ou e resumo de outro anexo.

### Onde o manual rende de verdade

Rendeu nos Anexos 2 e 6, onde as linhas sao **somas** — e uma soma quebrada
denuncia classificacao errada. Nos Anexos 3 e 4, o rendimento veio da **cadeia da
RCL e dos limites**, que sao calculaveis e se repetem em todos eles.

### Placar dos anexos do RGF, com os manuais

| anexo | antes | agora |
|---|---:|---:|
| 1 | 24 | 24 (+100 por Poder) |
| 2 | 16 | **22** |
| 3 | 1 | **5** |
| 4 | 1 | **8** |
| 5 | 90 | 90 |
| 6 | 1 | **10** |

O livro passou de 310 para **337 celulas**, com **328 exatas**.


### 17.63 Anexo 1 — as rubricas revelam um erro que o total escondia

Conferir so a despesa bruta dizia "exato em 10 de 10 meses". Conferir **cada
rubrica** mostra outra coisa.

Implementei seis rubricas por mes (8 meses): vencimentos, obrigacoes patronais,
aposentadorias, pensoes, terceirizacao e nao executada, mais o subtotal
"Pessoal Ativo".

**36 de 53 exatas.** O que diverge:

| rubrica | meses | padrao |
|---|---|---|
| Vencimentos | 8 de 8 | **+X** |
| Obrigacoes Patronais | 8 de 8 | **−X** |
| Pensoes (abril) | 1 | −5.241,65 |

E o X muda todo mes: 138.865,10 (jan), 35.507,44 (fev), 128.164,39 (mar),
7.267,37 (abr), 731.152,55 (mai), 8.144,04 (jun), 231.945,22 (jul), 493.254,25 (ago).

### O que isso significa

**A soma das duas fecha ao centavo**: vencimentos + patronais = Pessoal Ativo em
todos os meses. O que diverge e a **reparticao**.

Ha um item — de valor variavel — que classificamos como vencimento e o SIGEF
classifica como contribuicao patronal. O total nao e afetado; a linha e.

### Por que a conferencia anterior nao via

Ela olhava `DESPESA BRUTA COM PESSOAL (I)`, que e a soma de tudo. Se 138 mil
migram de uma rubrica para outra dentro do mesmo grupo, a soma nao muda.

E o mesmo principio das somas do Anexo 2: **conferir o total esconde erro de
classificacao; conferir as parcelas nao.**

### Placar

| | antes | agora |
|---|---:|---:|
| linhas por mes | 3 (I, II, III) | **3 + 7 (rubricas)** |
| celulas | 337 | **390** |
| exatas | 328 | **364** |

O percentual caiu de 97,3% para 93,3% — e o sistema ficou mais preciso: agora se
sabe **onde** a reparticao diverge, e que ela nao afeta o total.

### O que resolveria

Identificar a natureza de despesa do item que migra. Como o valor muda todo mes e
nao e um elemento inteiro, provavelmente e o **13o salario** ou a **contribuicao
patronal de uma rubrica especifica** — a conferir natureza a natureza entre
3190.11 (vencimentos) e 3190.13 (obrigacoes patronais).


### 17.64 A identidade que explica o "padrao repetido"

O usuario viu, na planilha, que os desvios das rubricas se repetem com sinais
opostos — e desconfiou de sinal invertido. Nao e sinal: e **a mesma parcela
aparecendo em mais de uma linha**, e a prova e uma identidade.

A despesa bruta (I) e a soma das seis rubricas. Logo, o desvio de I tem de ser a
soma dos desvios das rubricas:

| mes | soma dos desvios das rubricas | desvio de I |
|---|---:|---:|
| Janeiro | 0,00 | 0,00 |
| Fevereiro | 0,00 | 0,00 |
| Marco | 0,00 | 0,00 |
| **Abril** | **−5.241,65** | **−5.241,65** |
| Maio a Agosto | 0,00 | 0,00 |

**Fecha nos oito meses.**

### O que isso revela

1. **O split vencimentos X patronal NAO afeta a despesa bruta.** O +X de um lado
   e o −X do outro se cancelam exatamente. E erro de **reparticao**, nao de
   apuracao — e nunca apareceria conferindo so o total.
2. **A diferenca de abril vem TODA de Pensoes.** Nos outros meses a soma das
   rubricas da zero; em abril da −5.241,65, e so Pensoes desvia nesse mes.
   A causa ja registrada (par de anulacao e re-empenho no ND 31909203 —
   pensoes de exercicios anteriores) estava certa, e agora tem prova.

### Por que a desconfianca do usuario era produtiva

Ver "o mesmo valor com sinais opostos" e o sinal classico de um item contado duas
vezes ou com sinal trocado. O teste que refuta essa hipotese — comparar a **soma**
— e o mesmo que revela a estrutura: se a soma fecha, o item esta no lugar errado,
nao com o sinal errado.

E quando a soma NAO fecha (abril), ela aponta qual rubrica carrega a diferenca.


### 17.65 Expurgo patronal — a regra do SIGEF nao sai do Comparativo

Seis testes, todos negativos:

| # | hipotese | resultado |
|---|---|---|
| 1 | um item da nossa lista de 17 explica o X | **nao** — nenhuma combinacao ate 4 itens |
| 2 | o X e uma natureza isolada do Comparativo | **nao** — zero ocorrencias em 3 dos 4 meses testados |
| 3 | excluir toda a modalidade 91 (31.91.13.00) | **nao** — 273,7 mi, vinte vezes o expurgo |
| 4 | o expurgo do SIGEF e subconjunto das 23 naturezas 91 | **nao** — nenhuma combinacao ate 6 itens soma 11.502.548,48 |
| 5 | 11.502.548,48 e uma linha do Comparativo | **nao** — zero ocorrencias |
| 6 | alguma das 17 naturezas tem valor igual ao X todo mes | **nao** — nenhuma |

### O que se sabe

```
patronal bruto (31.90.13 + 31.91.13) ... 281.814.279,75
(-) expurgo nosso ....................  11.641.413,58
= patronal nosso ..................... 270.172.866,17
(-) publicado ........................ 270.311.731,27
= diferenca ..........................     138.865,10  (o X do mes)
```

O expurgo nosso e **sempre maior**, e a diferenca e sempre o X. Mas o X **nao e
uma natureza nem uma soma de naturezas** do Comparativo.

### Por que provavelmente nao sai daqui

O Comparativo da Despesa tem **uma linha por natureza**, sem a dimensao de fonte.
O expurgo patronal, como o do RP, deve depender dessa dimensao — as contribuicoes
patronais recolhidas a entidades do proprio Estado aparecem em fontes
especificas, e o SIGEF as separa por ali.

E a mesma conclusao a que cheguei no RP: **onde a dimensao fonte e decisiva, o
Comparativo nao resolve.**

### Impacto

| | |
|---|---|
| linhas afetadas | **16** (vencimentos e patronal em 8 meses) |
| efeito no total | **nenhum** — a soma das duas fecha ao centavo |
| efeito no relatorio | as duas rubricas saem trocadas pelo X do mes |

Nao afeta a despesa bruta, a liquida nem o percentual. Afeta **duas linhas do
Anexo 1** que o Siconfi publica separadas.

### O que resolveria

A regra do expurgo patronal — provavelmente por fonte, no mesmo relatorio de
execucao por fonte que fecharia o RP. Se assim for, **um unico arquivo resolve as
duas frentes**: 18 das 26 divergencias.


### 17.66 As planilhas do auditor — inventario completo

Tres arquivos, 40 abas cada, mesma estrutura (2º bi, 4º bi e base):

| grupo | abas | o que sao |
|---|---|---|
| `A 01-Rec` a `A 14` | 15 | o layout de cada anexo do RREO, preenchido |
| `Conferência RREO` | 1 | a tabela de conferencia entre anexos |
| `S_A01` a `S_A14` | 9 | o mesmo anexo no padrao Siconfi |
| `Conf. SICONFI x EXCEL` | 1 | **966 linhas** — RREO linha a linha |
| `Anexo 1` a `Anexo 6` | 6 | o layout de cada anexo do RGF |
| `Conferência RGF` | 1 | conferencia entre anexos do RGF |
| `S_RGF 01` a `S_RGF 06` | 5 | o mesmo anexo no padrao Siconfi |
| `Conf. RGF SICONFxEXCEL` | 1 | **302 linhas** — RGF linha a linha |
| `Conferência RREO x RGF` | 1 | confere RREO contra RGF |

### O que a conferencia cobre

| bloco | linhas | divergencias do proprio auditor |
|---|---:|---:|
| RREO | **966** | **0** |
| RGF | **302** | **10** |

As 10 divergencias do auditor sao todas em **percentuais** e no **Anexo 6** — as
mesmas que aparecem na aba "Conferência RGF".

### O que ja foi lido a fundo

| aba | o que rendeu |
|---|---|
| `Conf. RGF SICONFxEXCEL` | as 302 linhas do RGF, por anexo |
| `Conferência RGF` | as conferencias cruzadas (Anexo 2 x 3, 1 x 6, 2 x 6) |
| `Conferência RREO x RGF` | a RCL do RREO contra a do RGF |
| `RP` (no workbook do RGF 2025) | a formula do RP e as exclusoes por fonte |
| `CONTAS`, `Notas`, `Base` | a conta 8.6.3.2.2 e a Nota 4 |

### O que ainda nao foi lido

| aba | por que ainda nao rendeu |
|---|---|
| `A 01-Rec` (997 linhas) | e o RREO de **2024**; nao serve para 2025/2026 |
| `A 01-Desp` (997) | idem |
| `A 02` a `A 14` | idem |
| `S_A*`, `S_RGF*` | sao os mesmos anexos no padrao Siconfi de 2024 |

### A conclusao honesta

As planilhas do auditor sao a conferencia de **2024**. O que elas tem de
reaproveitavel — a **estrutura** da conferencia (somas, limites, cadeia da RCL) —
ja foi absorvido nas rodadas 119 a 124, e rendeu 80 celulas novas.

O que elas **nao** tem e o dado de 2025/2026: nem a conta 8.6.3.2.2 de
31/12/2025, nem o expurgo patronal por fonte.

### A pista que sobra nelas

A aba `A 01-Desp` (997 linhas) tem a **despesa por natureza e fonte** do RREO de
2024. Se a estrutura dela mostrar como o Siconfi separa a patronal por fonte,
pode indicar o criterio do expurgo — mesmo sendo de outro ano.

E a proxima leitura que vale a pena.


### 17.67 As abas de detalhe nao tem a dimensao fonte

Li as tres abas com mais linhas e colunas da planilha do auditor:

| aba | tamanho | o que e | tem fonte? |
|---|---|---|---|
| `A 01-Desp` | 74 a 997 x 31 | Balanco Orcamentario — despesa por categoria e grupo | **nao** |
| `A 01-Rec` | 217 x 102 | Balanco Orcamentario — receita por categoria | **nao** |
| `A 02` | 468 x 45 | Execucao da despesa por **funcao e subfuncao** | **nao** |

Todas trazem as colunas de dotacao, empenhada, liquidada, paga e restos a pagar —
e mais nada. As 102 colunas da receita sao **meses e percentuais**, nao fontes.

### O que isso fecha

As duas frentes abertas — RP processados e expurgo patronal — dependem da
**dimensao fonte de recursos**. Ela **nao existe em nenhuma das 120 abas**:

| fonte consultada | tem fonte? |
|---|---|
| MSC (matriz) | **sim**, mas nao na abertura que o SIGEF usa |
| Comparativo da Despesa | nao — uma linha por natureza |
| Balancete | nao |
| Planilhas do auditor (120 abas) | **nao** |
| Relatorio de execucao por fonte (SIGEF) | **sim** — e o que falta |

### O que isso significa

Nao ha mais onde procurar dentro do material que temos. As 120 abas do auditor
sao a conferencia de **2024**, no nivel de categoria, funcao e anexo — nunca no
nivel de natureza x fonte.

E por isso que 18 das 26 divergencias resistem: elas nao dependem de regra
desconhecida, dependem de um **recorte que nao foi extraido**.

### A conclusao da leitura

| pergunta | resposta |
|---|---|
| Li os manuais? | **sim** — 120 abas inventariadas, as com regra lidas a fundo |
| Elas tinham o resto das conferencias? | **sim** — 966 linhas de RREO e 302 de RGF |
| Elas fecham as frentes abertas? | **nao** — falta a dimensao fonte |
| O que ja rendeu? | **80 celulas** novas (rodadas 119 a 124) |

A leitura esta concluida. O que falta nao esta escrito em lugar nenhum do que
temos: e uma extracao.


### 17.68 A RCL e construivel — o mapeamento do MDF entregou as contas

Ate a rodada 129 eu dizia: "a RCL e lida, nao calculada; falta o bloco de
deducoes do RPPS de 1,23 bilhao, que nao existe na matriz".

**Estava errado.** O mapeamento oficial
`dados/mapeamentos/rreo/.../RREO - ANEXO 03 - RCL ... - MSC 2026.xlsx` traz, linha
a linha, o filtro do Siconfi — e as deducoes nao estao na classe 4, e sim na
**classe 6**:

| linha da RCL | criterio do mapeamento |
|---|---|
| RECEITAS CORRENTES (I) | `6.2.1.2.0.00.00` com natureza de receita 1.x |
| Dedução FUNDEB | conta `6.2.1.3.1.01.00` |
| Transferências Constitucionais | conta `6.2.1.3.1.02.00` |
| Contribuição do Servidor | natureza `1.2.1.5.x` |
| Compensação entre Regimes | natureza `1.9.9.9.03` |
| Rendimentos Previdenciários | natureza `1.3.2.1.04` |

E a janela e de **12 meses** (MR-11 a MR), nao o mes isolado — outro detalhe que
eu nao estava aplicando.

### Resultado em 2025

| componente | apurado | publicado | desvio |
|---|---:|---:|---:|
| Receitas Correntes (I) | 26.659.603.708,77 | 26.656.696.864,94 | +2.906.843,83 |
| **Dedução FUNDEB** | **3.175.469.290,58** | **3.175.469.290,58** | **0,00** |
| **Transferências Constitucionais** | **2.733.005.621,51** | **2.733.005.621,51** | **0,00** |
| Contribuição do Servidor | 1.110.379.286,39 | 1.110.322.676,50 | +56.609,89 |
| **Compensação entre Regimes** | **115.005.627,07** | **115.005.627,07** | **0,00** |
| **Rendimentos Previdenciários** | **9.046.989,30** | **9.046.989,30** | **0,00** |
| Deduções (II) | 7.142.906.814,85 | 7.142.850.204,96 | +56.609,89 |
| **RCL (III)** | **19.516.696.893,92** | **19.513.846.659,98** | **+2.850.233,94** |

**Quatro dos sete componentes fecham ao centavo.** A RCL fica a **0,0146%** do
publicado.

Em 2026-08 o desvio e ainda menor: RCL apurada 20.967.198.508,50 contra
20.966.424.987,22 publicada — **0,0037%**.

### O que sobra

O desvio residual esta na **receita**: apuramos 2,9 milhoes a mais em 2025 e 854
mil em 2026. As linhas conferidas item a item mostram por onde:

| linha | desvio |
|---|---:|
| IRRF | **0,00** |
| ICMS | +113.612,03 |
| IPVA | +210.886,89 |
| ITCD | +208.486,68 |

Cada tributo sai um pouco acima — o que sugere que a receita inclui parcelas que o
SIGEF nao conta (provavelmente **intra-orcamentarias**).

### O que isso muda

| antes | agora |
|---|---|
| RCL lida do arquivo publicado | **RCL construida da matriz** |
| "falta o bloco de 1,23 bi" | **o bloco esta na classe 6 e fecha** |
| RREO Anexo 3 dependia do publicado | **pode ser gerado antes de publicar** |

O modulo `rcl_msc.py` faz a conta, e `tests/test_rcl_msc.py` garante que ela
continua dentro de 0,02% — com as quatro deducoes exatas travadas em teste.

### A licao

O mapeamento da STN estava na pasta `dados/mapeamentos` desde o inicio. Eu tinha
procurado a RCL no Comparativo, no balancete e nas planilhas do auditor — e nao
no **mapeamento que a propria STN publica para a MSC**.

O dado nao faltava: faltava eu olhar o arquivo certo.


### 17.69 Anexo 1 — o mapeamento oficial tem a regra, e o filtro de Poder e decisivo

O arquivo `dados/mapeamentos/rgf/RGF - PARTE IV - MDF 15ª EDIÇÃO/RGF - ANEXO 1 -
Despesas com Pessoal ... - MSC 2026.xlsx` tem quatro abas: primeiro/segundo
quadrimestre e terceiro, cada um para o **Poder Executivo** e para os **Demais
Poderes**.

### O que a regra diz

**Contas.** A despesa de pessoal nao sai de toda a classe 6 — sai de tres contas:

| conta | o que e |
|---|---|
| `6.2.2.1.3.03.00` | credito empenhado liquidado **a pagar** |
| `6.2.2.1.3.04.00` | credito empenhado liquidado **pago** |
| `6.2.2.1.3.07.00` | empenhos liquidados inscritos em **RP processados** |

**Filtro de Poder.** No Executivo: `PO começada por (Lista): 10,60`. Nas abas dos
Demais Poderes, nao ha filtro de PO — cada aba e um Poder.

**Filtro de natureza.** Posicional, nao por lista:

| rubrica | modalidade (pos. 3-4) | elemento (pos. 5-6) |
|---|---|---|
| Vencimentos | `30,70,80,90,91,95,96` | `04,08,11,12,16,17,41,46,49,67,96,99` |
| Obrigacoes Patronais | `90,91,95,96` | `07,13` |

Com excecoes e adicoes: `31900415` **sai** de vencimentos e **entra** em patronal.
E ha um bloco "EXCETO CO" (linhas sem complemento) que subtrai naturezas.

### O efeito de cada filtro

Aplicando a regra a janeiro/2026, com as tres contas:

| filtro aplicado | vencimentos apurado | publicado | desvio |
|---|---:|---:|---:|
| nenhum (toda a classe 6) | 1.194.610.698,33 | 648.854.208,10 | **+84%** |
| so as tres contas | 706.530.074,16 | 648.854.208,10 | **+9%** |
| tres contas **+ PO 10,60** | 652.029.045,25 | 648.854.208,10 | **+0,49%** |

**O filtro de Poder era o que faltava.** Sem ele, o erro e de 9% — e a apuracao
atual (que usa o Comparativo) nao o aplica porque o PDF ja vem por Poder.

### O que ainda falta

| item | situacao |
|---|---|
| bloco "EXCETO CO" | nao implementado — as celulas tem o texto, falta extrair |
| marco/2026 | desvio de −71,4 mi: precisa investigacao propria |
| patronal | ainda +5% — as adicoes da lista nao foram aplicadas |

### O que ficou pronto

| arquivo | o que e |
|---|---|
| `extrair_regras_anexo1.py` | le as celulas do mapeamento e grava as listas |
| `dados/mapeamentos/anexo1_regras.json` | 68 NDs de vencimentos, 18 de patronal, 31 de aposentadorias, 12 de pensoes |

### A conclusao

O caminho para fechar o Anexo 1 e claro e esta mapeado: **tres contas + filtro de
Poder + filtro posicional + listas de excecao**. Cada filtro ja foi medido
isoladamente, e o maior salto (de 9% para 0,5%) veio do Poder.

E o mesmo tipo de erro que o expurgo patronal: a apuracao atual usa o Comparativo,
que **ja vem agregado**, e por isso perde a dimensao que o Siconfi usa para separar
as linhas.

### O padrao dos dois achados

| frente | o que faltava |
|---|---|
| RCL | as contas estao na **classe 6**, nao na 4 |
| Anexo 1 | o **filtro de Poder** (PO 10,60) |

Nos dois casos, o mapeamento da STN tinha a resposta — e nos dois casos eu estava
olhando o relatorio errado.


### 17.70 Anexo 2 — as formulas oficiais, e a conta que nao existe

O mapeamento `RGF - ANEXO 2 - Dívida Consolidada Líquida ... MSC 2026.xlsx` tem
uma aba so (`Anexo 2 - Dívida (E, DF e M)`) e traz, linha a linha, as contas
contabeis. Duas linhas importam:

#### (-) Restos a Pagar Processados (celula C53)

```
[6.2.2.1.3.07 + 6.3.1.3.0 + 6.3.2.1.0;
 ND 3.1 + 3.3 + 4.4 + 4.5; TODAS FR EXCETO 800 + 801 + 802]
(-) 8.6.3.2.2.00.00
```

Nosso codigo ja usa as tres contas e as naturezas. Duas diferencas:

| item | mapeamento | nosso codigo |
|---|---|---|
| fontes excluidas | **800, 801, 802** | 32, 46, **800, 801, 802** |
| controle | **a conta 8.6.3.2.2** | valor fixo 942.052.222,15 |

#### Outras Dívidas (celula C45)

```
8.5.3.7.0.00.00 (consorcio) + 8.6.3.2.1.00.00 + 8.6.3.2.2.00.00
+ 2.1.8.9.1.01.05 + 2.1.8.9.1.01.08 + 2.1.8.9.3.01.05
+ 2.1.8.9.4.01.05 + 2.1.8.9.5.01.05
+ 2.2.8.2.1.00.00 + 2.2.8.2.3.00.00 + 2.2.8.2.4.00.00 + 2.2.8.2.5.00.00
EXCETO PO 10112/10122/10132
```

**A linha "Outras Dívidas" e a que faltava para fechar a DC** — e ela e formada,
entre outras contas, pela **8.6.3.2.2.00.00**: a mesma do controle do RP.

#### A prova da ausencia

Apuramos "Outras Dívidas" pelas doze contas do mapeamento, na MSC de 2025-12:

| | valor |
|---|---:|
| apurado | **36.600,82** |
| publicado | **941.926.197,62** |
| diferenca | −941.889.596,80 |

A diferenca e quase exatamente o controle de 942.052.222,15. **A conta
`8.6.3.2.2.00.00` nao existe na matriz** — nem na classe 8, nem em nenhuma outra,
nem em nenhum tipo de valor. Varremos tambem os arquivos CSV brutos de 2025: zero
ocorrencias.

### O que isso fecha de discussao

| pergunta | resposta |
|---|---|
| "Outras Dívidas" tem formula? | **sim** — doze contas, no mapeamento |
| da para apurar pela matriz? | **nao** — falta a 8.6.3.2.2 |
| a diferenca da DC e erro nosso? | **nao** — e conta ausente |
| o RP fecha pela matriz? | **nao** — falta o mesmo controle |

**Tres divergencias (DC, Deduções e DCL) e as duas do RP tem a mesma causa: uma
unica conta que a MSC nao traz.**

### Os testes que travam isso

`tests/test_dcl_regras.py` fixa o achado:

1. a conta `8.6.3.2.2.00.00` **nao aparece** na MSC — se um dia aparecer, o teste
   quebra e avisa que o Anexo 2 virou apuravel;
2. das doze contas de "Outras Dívidas", **so a 8.6.3.2.1 tem saldo** (36.600,82);
3. as contas do RP **existem** — o que falta e o controle, nao a base.

E um teste de ausencia proposital: ele documenta o limite e impede que se
persiga de novo a mesma conta.


### 17.71 O subelemento que identifica o Poder nao esta na matriz

A regra do expurgo patronal, pelo manual do etonjones, e o **subelemento**:

> `31.91.13.71` TJ · `.72` AL · `.73` TCE · `.74` DPE · `.75` MP

Fui buscar essas naturezas na MSC de janeiro/2026. Resultado:

| o que existe em `31.91.13` na MSC | valor |
|---|---:|
| `31911308` | 17.880.000,00 |
| `31911310` | 272.867.339,22 |
| `31911312` | 44.969.895,57 |
| `31911399` | 2.500.000,00 |
| `31911371` a `31911375` | **0,00 — nao existem** |

**A MSC nao desce ao subelemento .71 a .75.** Ela para no elemento (13) com
subelemento 08, 10, 12 e 99.

Ja o **Comparativo** traz `.71` a `.75` (1.337.759,24 em janeiro, igual ao manual).

Ou seja: a dimensao que identifica **de quem e a patronal** existe no Comparativo,
mas nao na matriz — e o valor do Comparativo nao se abre por fonte.

### A parede e a mesma de sempre

| frente | dimensao que falta | onde ela existe |
|---|---|---|
| RP processados | conta `8.6.3.2.2` | so no SIGEF |
| "Outras Dividas" | conta `8.6.3.2.2` | so no SIGEF |
| Expurgo patronal | subelemento `.71-.75` × fonte | Comparativo (sem fonte) |
| Expurgo de inativos | **subacao** (408501 a 408902) | so no IEO |

**Quatro frentes, um unico buraco: a extracao por subacao e fonte.**

### O Anexo 1 de 2025 — a causa apareceu

Ao tentar apurar 2025 pela `mapa_anexo1`, o modulo falhou:

```
FileNotFoundError: ...Comparativo Despesa Autorizada ..._Novembro.pdf
```

**Os Comparativos da Despesa de 2025 nao existem** — a pasta so tem os de 2026. A
apuracao de 2025 nao pode usar o mesmo caminho.

### Mas o auditor deixou o gabarito

A aba `CONFERÊNCIAS` do `RGF 2025_Q3_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.xlsx`
traz **doze meses**, rubrica por rubrica, em dois blocos: **SIGEF** e **SICONFI**.

Os dois batem, e a soma dos doze meses da exatamente o publicado:

| linha | soma 12 meses | publicado no CSV |
|---|---:|---:|
| I — Despesa Bruta | **15.478.621.265,08** | **15.478.621.265,08** |
| II — Nao Computadas | 4.477.467.400,70 | 4.477.467.400,70 |
| III — Despesa Liquida | **11.001.153.864,38** | **11.001.153.864,38** |

Extrai esse gabarito para `dados/benchmarks/anexo1_2025.json` — 12 meses por
rubrica, com os dois blocos.

### O que o gabarito mostra de imediato

Em janeiro/2025, a **Despesa com Pessoal nao Executada Orcamentariamente** e
**negativa**: −252.032.455,16.

Isso confirma a regra do etonjones (credito **menos** debito): em janeiro o debito
— a folha de dezembro/2024 sendo executada — e muito maior que o credito novo.
Quem soma so o credito erra a linha por centenas de milhoes.

### Nossa diferenca de 2025, agora localizada

| linha | nosso | gabarito | diferenca |
|---|---:|---:|---:|
| I — Bruta | 15.422.754.491,59 | 15.478.621.265,08 | **−55.866.773,49** |
| III — Liquida | 11.086.434.730,47 | 11.001.153.864,38 | **+85.280.866,09** |

A diferenca nao esta no total: esta no **sinal da nao executada**. Somando o
credito em vez de (credito − debito), a linha III sobe e a I desce — exatamente o
padrao dos dois desvios.

### Os testes

`tests/test_benchmark_2025.py` — quatro testes:

1. o benchmark existe;
2. a soma dos doze meses e igual ao CSV publicado, **ao centavo**;
3. o bloco SIGEF e o publicado sao iguais;
4. cada rubrica tem doze meses.

Se alguem trocar o arquivo ou o CSV, o teste quebra.


### 17.72 A linha 251 — a regra do sinal, confirmada nos dois anos

A "Despesa com Pessoal não Executada Orçamentariamente" sai das contas
`8.6.3.3.1.01.00.00` (salários) e `8.6.3.3.1.02.00.00` (13º), pelo movimento
**credor menos devedor**. Agora ela e apurada pela **matriz**, sem PDF.

### 2025 — doze meses, todos exatos

Contra a aba `CONFERÊNCIAS` do `RGF 2025_Q3_01`:

| mes | apurado | gabarito | desvio |
|---|---:|---:|---:|
| Janeiro | −252.032.455,16 | −252.032.455,16 | **0,00** |
| Fevereiro | −4.726.072,94 | −4.726.072,94 | **0,00** |
| Março | −58.212.394,89 | −58.212.394,89 | **0,00** |
| Abril | −139.972.178,06 | −139.972.178,06 | **0,00** |
| Maio a Novembro | 0,00 | 0,00 | **0,00** |
| Dezembro | 622.454.793,84 | 622.454.793,84 | **0,00** |

**Desvio absoluto total: zero.**

### 2026 — cinco meses, todos exatos

| mes | apurado | publicado |
|---|---:|---:|
| Janeiro | 3.527.816,53 | 3.527.816,53 |
| Fevereiro | 92.547,22 | 92.547,22 |
| Março | −89.546,82 | −89.546,82 |
| Abril | −624.713.040,31 | −624.713.040,31 |
| Maio | −1.272.570,46 | −1.272.570,46 |

O valor de abril e exatamente o que o manual do etonjones cita como o correto
(−624.713.040,31), depois de devolver os 1.337.759,24.

### O que so apareceu ao conferir: o expurgo tem sinal

O valor de 1.337.759,24 e a patronal do 13º dos demais Poderes. O sinal depende de
**onde ela esta no mes**:

| mes | onde esta | efeito | resultado |
|---|---|---|---|
| dezembro/2025 | no **credito** (nova inscricao do 13º) | **subtrai** | 623.792.553,08 -> 622.454.793,84 |
| abril/2026 | no **debito** (baixa do 13º) | **soma de volta** | −626.050.799,55 -> −624.713.040,31 |

Os dois numeros estao no manual do etonjones, e os dois foram reproduzidos aqui.
Na primeira tentativa eu somei o expurgo em dezembro e errei por 2.675.518,48 —
duas vezes o valor, porque apliquei com o sinal trocado.

### O efeito no total de 2025 — e por que ainda nao fecha

Corrigir a linha 251 fez o total de 2025 **se afastar** 1.337.759,24 do publicado:

| linha | antes | depois | publicado |
|---|---:|---:|---:|
| I — Bruta | 15.422.754.491,59 | 15.421.416.732,35 | 15.478.621.265,08 |
| III — Liquida | 11.086.434.730,47 | 11.085.096.971,23 | 11.001.153.864,38 |

Isso significa que **outra rubrica esta compensando**: se a linha 251 correta e
1,34 milhao menor, e o total cai junto, entao uma das outras cinco esta 1,34
milhao maior do que o gabarito — e mais os 55,9 milhoes que ja faltavam.

Nao da para apontar qual: as rubricas de 2025 vem do **Comparativo da Despesa**,
que **nao existe para 2025** (a pasta so tem 2026). O modulo falha ao tentar ler.

### O gabarito fecha internamente

Conferi o gabarito contra ele mesmo: a soma das seis rubricas da **exatamente** o
total de cada mes e os 15.478.621.265,08 do ano.

| verificacao | resultado |
|---|---|
| Janeiro: rubricas = I | 811.049.203,96 = 811.049.203,96 |
| Fevereiro: rubricas = I | 1.440.860.836,75 = 1.440.860.836,75 |
| 12 meses: rubricas = I | 15.478.621.265,08 = 15.478.621.265,08 |

Entao o gabarito e confiavel: para o relatorio de 2025, as rubricas estao nele.

### Os testes

`tests/test_nao_executada.py` — cinco testes:

1. os doze meses de 2025 batem com o gabarito;
2. os cinco meses de 2026 batem com o publicado;
3. abril/2026 e negativo e igual ao manual;
4. dezembro/2025 e positivo e igual ao manual;
5. janeiro/2025 e negativo — o sinal sozinho, que vale 252 milhoes.


### 17.73 A regra oficial funciona em 2026 e nao em 2025 — e isso e um achado

Apliquei a regra do mapeamento (tres contas, PO 10/60, filtro posicional de
natureza) aos doze meses de 2025 e comparei com o gabarito do auditor.

| mes | vencimentos nosso | gabarito | diferenca |
|---|---:|---:|---:|
| Janeiro | 423.544.597 | 426.026.503 | −2.481.906 |
| **Fevereiro** | 422.175.169 | 489.760.939 | **−67.585.770** |
| Marco | 428.229.854 | 427.433.315 | +796.539 |
| Maio | 454.679.690 | 482.042.281 | −27.362.591 |
| **Outubro** | 503.086.987 | 679.729.237 | **−176.642.251** |
| Dezembro | 683.229.809 | 786.200.400 | −102.970.590 |

Em 2026 a mesma regra erra 0,49%. Em 2025 erra entre 0,2% e 26%, **sem padrao**.

### O que testei para explicar

| filtro de Poder | fevereiro | gabarito |
|---|---:|---:|
| nenhum | 576.371.820 | 489.760.939 |
| so `10` | 417.463.679 | 489.760.939 |
| `10` + `60` (o do mapeamento) | 422.175.169 | 489.760.939 |

O gabarito esta **entre** o filtro de dois POs e o de nenhum. Ou seja: em 2025 a
despesa de pessoal do Executivo inclui POs que em 2026 nao inclui — ou a matriz de
2025 tem cobertura diferente.

Os POs com maior peso em fevereiro/2025:

| PO | vencimentos |
|---|---:|
| `10111` | 416.685.879 |
| `30390` | 109.929.955 |
| `50511` | 21.388.621 |
| `20211` | 17.775.773 |

O `30390` sozinho tem 110 milhoes — e nenhum filtro documentado o inclui.

### O que isso significa

Nao e erro de conta nem de sinal: e **mudanca de estrutura de Poder entre os
exercicios**. A regra do mapeamento e de 2026 (`Atualizado 07/2026`) e pode nao
valer retroativamente.

### O que fazer com 2025

O gabarito resolve: a aba `CONFERENCIAS` do `RGF 2025_Q3_01` tem as seis rubricas
mes a mes, fecha internamente ao centavo e soma exatamente o publicado. Para o
relatorio de 2025, **as rubricas estao nele**.

O que falta e a **regra de 2025** — provavelmente uma versao anterior do mapeamento
(ha pastas `MDF_STN/2024`, `2025` e `2026` no workspace; vale procurar a de 2025).

### A pista concreta

```
MDF_STN\2025\02_instrucoes_stn_siconfi\
```

**Conferido:** a pasta `MDF_STN/2025` tem o MDF 14a edicao, as regras gerais de
RGF e RREO e a sintese de alteracoes — **nao tem o mapeamento do Anexo 1**. O
mapeamento e um so, de 2026, atualizado em 07/2026.

Entao a regra de 2025 nao esta disponivel no material. O gabarito do auditor
passa a ser a referencia — e a varredura dessa frente termina aqui.


### 17.74 RREO Anexo 11 — anexo novo, 100% exato

Faltavam dois anexos do RREO com arquivo publicado e sem conferencia: o **6**
(Resultado Primario e Nominal) e o **11** (Alienacao de Ativos). Comecei pelo 11,
que e menor e tem regra direta.

### A regra, do mapeamento da STN

| linha | natureza de receita | fonte |
|---|---|---|
| Bens Moveis | 2.2.1 + 8.2.1 + 1.9.4.1 + 7.9.4.1 | 755, 756, 762 |
| Bens Imoveis | 2.2.2 + 8.2.2 + 1.9.4.2 + 7.9.4.2 | 755, 756, 762 |
| Bens Intangiveis | 2.2.3 + 8.2.3 + 1.9.4.3 + 7.9.4.3 | 755, 756, 762 |
| Rendimentos de Aplicacoes | 1.3.2.1.01 + .02 + .03 + .05 + .99 | 755, 756, 762 |
| Investimentos | ND 4.4 | 755, 756, 762 |
| Inversoes Financeiras | ND 4.5 | 755, 756, 762 |

Receita sai de `6.2.1.2.0.00.00` e despesa de `6.2.2.1.3.00.00`, na classe 6.

### O resultado — 2025, cinco linhas com valor

| linha | apurado | publicado | desvio |
|---|---:|---:|---:|
| Bens Moveis | 1.284.564,22 | 1.284.564,22 | **0,00** |
| Bens Imoveis | 0,00 | 0,00 | **0,00** |
| Bens Intangiveis | 0,00 | 0,00 | **0,00** |
| Rendimentos de Aplicacoes | 33.593,57 | 33.593,57 | **0,00** |
| Receitas de Alienacao (I) | 1.318.157,79 | 1.318.157,79 | **0,00** |
| Investimentos | 55.800,00 | 55.800,00 | **0,00** |
| Inversoes Financeiras | 0,00 | 0,00 | **0,00** |
| **Valor (III)** | **1.262.357,79** | **1.262.357,79** | **0,00** |

**Nenhum desvio.** E o primeiro anexo inteiramente novo desde o Anexo 5.

### O que ele ensinou sobre o metodo

O Anexo 11 fecha sem nenhuma extracao extra porque as tres dimensoes de que ele
precisa — **natureza de receita, natureza de despesa e fonte** — estao todas na
matriz.

Compare com as frentes abertas:

| anexo | dimensoes necessarias | estao na MSC? |
|---|---|---|
| **11** | NR + ND + FR | **sim, as tres** |
| Anexo 1 (expurgo) | **subacao** + FR | so a FR |
| Anexo 2 (RP) | conta `8.6.3.2.2` | nao |
| Anexo 1 (inativos) | **subacao** | nao |

**A regra e a mesma: quando a matriz tem as dimensoes, fecha. Quando nao tem, nao
fecha — e nao e por falta de formula.**

### 2026

O modulo ja apura 2026 (1.155.289,75 de receita), mas **nao ha CSV publicado de
2026 para o Anexo 11** — entao nao ha com o que comparar. A verificacao fica so
em 2025, e o codigo espera o arquivo.

### Os testes

`tests/test_anexo11.py` — quatro testes: os valores de 2025 ao centavo, os dois
zerados, a identidade do valor e a soma das linhas de receita.

### Placar

| | antes | agora |
|---|---:|---:|
| celulas | 390 | **395** |
| exatas | 364 | **369** |
| grupos | 31 | **32** |
| testes | 96 | **100** |
