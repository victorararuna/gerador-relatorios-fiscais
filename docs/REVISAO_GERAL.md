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
| RREO Anexo 2 — função | 23 funções | **0,00** |
| RREO Anexo 3 — RCL | 5 linhas, 2025 e 2026 | **0,00** |
| RREO Anexo 7 — restos a pagar | 5 linhas | **0,00** |
| RREO Anexo 9 — despesa de capital | 4 linhas | **0,00** |
| RREO Anexo 14 — simplificado | 6 linhas | **0,00** |
| RGF Anexo 3 — garantias | 5 linhas | **0,00** |
| RGF Anexo 4 — limites | 3 limites | **0,00** |
| RGF Anexo 6 — limites | 3 limites | **0,00** |

### Apurado com desvio pequeno e documentado

| anexo | situação |
|---|---|
| **RGF Anexo 1 — pessoal** | bruta a −0,36% (2025 Q3); a líquida desvia pela dedução |
| **RREO Anexo 4 — previdenciário** | 4/4: inatividade e pensões militares **exatas**; civis a +0,02% e +0,15% |
| **RGF Anexo 2 — DCL** | **8 de 14 linhas exatas**; as demais com causa identificada |
| **RGF Anexo 5 — disponibilidade** | (b) +0,11%, (c) +0,74%, (f) exata; (a) explicada; (e) a 0,7% |

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
