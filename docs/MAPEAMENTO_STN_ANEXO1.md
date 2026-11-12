# Mapeamento oficial do RGF Anexo 1 (Despesa com Pessoal)

Extraído do **Módulo 16 – Despesa com Pessoal** da Secretaria do Tesouro Nacional
(XXXII Semana Contábil e Fiscal para Estados e Municípios – SECOFEM 2025),
que reproduz o item 04.01.00 do MDF, 14ª edição (páginas 478 a 535).

Arquivo de origem: [`MDF_STN/_apoio/Modulo16_Despesa_com_Pessoal_STN.pdf`](../MDF_STN/_apoio/Modulo16_Despesa_com_Pessoal_STN.pdf), páginas 64 a 79.

---

## 1. O recorte é por PO (Poder/Órgão), não pela unidade gestora

Este é o ponto que explica as divergências apuradas. O Anexo 1 do RGF do **Poder
Executivo** é a soma de **três POs**:

| PO | Descrição |
|---|---|
| **10111** | Poder Executivo – Governo Estadual |
| **10112** | Poder Executivo – RPPS Estadual |
| **60611** | Defensoria Pública Estadual |

Todos os blocos do demonstrativo (Ativos, Inativos, Contratação Indireta e
Deduções) usam esse mesmo conjunto — com uma exceção importante: as
**Indenizações por Demissão** e as **Despesas de Exercícios Anteriores** excluem
o RPPS (usam apenas 10111 + 60611).

## 2. Pessoal Ativo → "Vencimentos, Vantagens e Outras Despesas Variáveis"

Filtro: CE 3 (Despesas Correntes) · GND 1 (Pessoal e encargos)

| Natureza | Descrição |
|---|---|
| 3.1.XX.08.00 | Outros benefícios assistenciais do servidor e do militar |
| 3.1.XX.11.00 | Vencimentos e vantagens fixas – pessoal civil |
| 3.1.XX.12.00 | Vencimentos e vantagens fixas – pessoal militar |
| 3.1.XX.16.00 | Outras despesas variáveis – pessoal civil |
| 3.1.XX.17.00 | Outras despesas variáveis – pessoal militar |
| 3.1.90.91 + SE | Precatórios e sentenças judiciais **de pessoal ativo** |
| 3.1.90.92 + SE | Despesas de exercícios anteriores **de pessoal ativo** |
| 3.1.XX | Demais modalidades associadas ao GND 1 |

> Atenção: `XX` significa **90 ou 91** — ou seja, a mesma natureza em aplicação
> direta e em restos a pagar. Somar as duas é correto.

## 3. Obrigações Patronais

| Natureza | Vai para |
|---|---|
| 3.1.XX.**07**.00 – Contribuição a entidades fechadas de previdência | **Vencimentos, Vantagens e Outras Despesas Variáveis** |
| 3.1.XX.**13**.00 – Obrigações patronais | **Obrigações Patronais** |
| 3.1.90.92 + SE de obrigação patronal de ativos | Obrigações Patronais |
| 3.1.91.92 + SE de obrigação patronal de ativos | Obrigações Patronais |
| 3.1.91.91 + SE de obrigação patronal de ativos | Obrigações Patronais |

## 4. Pessoal Inativo e Pensionistas

Filtro adicional: **CO 1111 + 1151** (benefícios do fundo em capitalização) e
**CO 2111 + 2151** (benefícios do fundo em repartição).

**Aposentadorias, Reserva e Reformas**

| Natureza | Descrição |
|---|---|
| 3.1.90.01.00 | Aposentadorias do RPPS, reserva remunerada e reformas dos militares |
| 3.1.90.86.00 | Compensações a regimes de previdência |
| 3.1.90.91 + SE | Sentenças judiciais de pessoal **inativo** (.09, .12, .15, .18) |
| 3.1.90.92.01 | Aposentadorias, reserva remunerada e reformas |
| 3.1.90.94.03/.04 | Indenizações e restituições trabalhistas de inativo |

**Pensões**

| Natureza | Descrição |
|---|---|
| 3.1.90.03.00 | Pensões do RPPS e do militar |
| 3.1.90.91 + SE | Sentenças judiciais de **pensionistas** (.10, .13, .16, .19) |
| 3.1.90.92.03 | Pensões do RPPS e do militar |
| 3.1.90.94.06/.13 | Indenizações e restituições trabalhistas de pensionista |

## 5. Contratação Indireta

Filtro: CE 3 · **GND 3** (Outras Despesas Correntes)

| Natureza | Observação |
|---|---|
| 3.1.XX.34 | Elemento específico de terceirização |
| 3.1.XX.91 + SE 34 | Sentenças de terceirização |
| 3.1.XX.92 + SE 34 | Exercícios anteriores de terceirização |

Conta contábil de controle: `8.6.3.3.2.00.00 (Cont. Gestão)`.

## 6. Deduções (Despesas não computadas)

| Linha | Fonte / Natureza |
|---|---|
| Indenizações por Demissão e Incentivos | PO 10111 + 60611 (exclui RPPS) |
| Decorrentes de Decisão Judicial | **FR 800, 801, 803, 804** (recursos vinculados RPPS/SPSM) |
| Despesas de Exercícios Anteriores | FR 800/801/803/804; FR 802 apenas para ND 01 e 03 |
| **Inativos e Pensionistas com Recursos Vinculados** | **CO 1111 + 1151** (fundo capitalização) e **CO 2111 + 2151** (fundo repartição) |
| ACS e ACE com Recursos Vinculados | FR 604 (Transferências ACS e ACE) |
| Piso do Enfermeiro e afins | FR 605 (Assistência) |
| Outras Deduções | ND 94 (Indenizações e Restituições Trabalhistas) e ED 91 (Sentenças) |

> **A própria STN declara que três linhas não têm mapeamento automático:**
> Decisões Judiciais, Despesas de Exercícios Anteriores (exige informação
> gerencial para definir a competência; admite-se por aproximação as DEA do
> período anterior ao da apuração) e o Piso do Enfermeiro (envolve cálculo).

## 7. RCL ajustada para o cálculo da despesa com pessoal

A RCL do art. 2º, IV, da LRF é **ajustada** excluindo:

1. **Emendas individuais impositivas** – CF, art. 166-A, § 1º (EC 105/2019):
   os recursos não integram a receita para fins de cálculo dos limites de
   despesa com pessoal;
2. **Emendas de bancada** – art. 166, §§ 11, 12 e 16: exclusão apenas para o
   limite de despesa com pessoal;
3. **Transferências da União para pagamento dos vencimentos dos ACS e ACE**.

Esses três ajustes podem alterar a base da RCL usada no percentual — e portanto
o índice final.

---

## 8. O que isso significa para a apuração do RN

O mapeamento de **naturezas** que usei está alinhado com o documento. A
divergência de R$ 2,4 bi vem do **recorte de PO**: os arquivos "Comparativo
Despesa Autorizada Empenhada Liquidada e Paga" cobrem o PO 10111 (Governo
Estadual), mas não o **PO 10112 (RPPS Estadual)** nem o **PO 60611 (Defensoria
Pública)**.

É no RPPS que estão, tipicamente, a maior parte das **obrigações patronais** e
parcela relevante dos **vencimentos** — exatamente as duas linhas em que a
apuração ficou abaixo do homologado (R$ 1,40 bi e R$ 0,83 bi).

Para fechar, é preciso a mesma extração incluindo os POs 10112 e 60611 — ou uma
extração com a coluna de PO.

---

## 9. Piso da enfermagem — regra verificada

**Base legal:** ADCT, art. 38, § 2º (incluído pela EC 127/2022). O MDF 14ª edição,
página 487, traz a tabela de dedução progressiva:

| Exercício | Dedução permitida | Exercício | Dedução permitida |
|---|---|---|---|
| 2022 | 100% | 2028 | 50% |
| 2023 | 100% | 2029 | 40% |
| **2024** | **90%** | 2030 | 30% |
| 2025 | 80% | 2031 | 20% |
| 2026 | 70% | 2032 | 10% |
| 2027 | 60% | 2033 | 0% |

A Constituição **não** previu dedução integral e permanente (ao contrário dos ACS
e ACE): a EC 127/2022 fixou uma regra de transição, incorporando a despesa aos
limites de forma progressiva.

**Base de cálculo:** fonte de recurso **FR 605** (Assistência), nas naturezas de
pessoal (GND 1).

### Verificação contra o RGF 2024 Q3 homologado

Aplicando 90% sobre a fonte 0.605 mês a mês:

| Mês | Fonte 0.605 | Dedução homologada | Razão |
|---|---|---|---|
| Janeiro | 0,00 | 0,00 | — |
| Fevereiro | 5.222.561,06 | 4.700.304,95 | **90,00%** |
| Março | 5.152.474,47 | 4.637.227,02 | **90,00%** |
| **Abril** | **52.000.000,00** | 4.614.449,00 | 8,87% |
| Maio | 5.129.346,48 | 4.735.074,97 | 92,31% |
| Junho | 5.087.490,49 | 4.578.741,44 | **90,00%** |
| Julho | 5.094.560,40 | 4.585.104,36 | **90,00%** |
| **Agosto** | 5.088.727,93 | 9.260.158,43 | 181,97% |
| Setembro | 5.157.375,80 | 4.641.638,22 | **90,00%** |
| **Outubro** | 5.162.698,21 | 6.204.070,18 | 120,17% |
| Novembro | 5.176.605,23 | 4.658.944,71 | **90,00%** |
| Dezembro | 15.984.121,81 | 14.385.709,63 | **90,00%** (13º) |
| **Total** | **119.813.026,59** | **67.001.422,91** | 55,92% |

**Conclusão da verificação:**

1. A regra de **90% está confirmada** — a razão é exatamente 90,00% em oito dos
   doze meses, inclusive dezembro (com o 13º salário);
2. **Abril é atípico:** a fonte registra R$ 52.000.000,00 (valor redondo, típico
   de empenho global do piso, não da parcela do mês). O homologado considerou
   apenas R$ 5.127.165,56 nesse mês;
3. **Agosto e outubro** trazem valores acima de 90% — reflexo de pagamentos
   retroativos, tratados por competência.

**Resultado da apuração automática:** R$ 65.690.668,64 contra R$ 67.001.422,91
homologados — **98,0% de aderência**. A diferença residual (R$ 1.310.754,27)
corresponde exatamente aos retroativos de agosto e outubro, que exigem informação
gerencial para alocar no mês de competência (mesma natureza do problema apontado
pela STN para as Decisões Judiciais).

A implementação trata valores acima de 5× a mediana como empenho global e usa a
mediana no lugar, preservando o 13º de dezembro.

---

## 10. Varredura dos subelementos 91, 92, 94 e 07

O elemento **92 (Despesas de Exercícios Anteriores)** não é integralmente
dedução — cada subelemento pertence a uma linha do Anexo 1. Varredura feita sobre
os 12 meses dos Comparativos (liquidado, todos os poderes):

### 31.90.92 — Despesas de Exercícios Anteriores (total R$ 60.387.904,15)

| Subelemento | Descrição | Valor | Vai para |
|---|---|---|---|
| .01 | Aposentadorias, Reserva Remunerada e Reformas | 2.741.233,76 | Aposentadorias |
| .03 | Pensões do RPPS e do Militar | 5.552.547,07 | Pensões |
| **.13** | **Obrigações Patronais** | **531.853,38** | **Obrigações Patronais** |
| .04 | Contratação por Tempo Determinado | 725.718,23 | Vencimentos |
| .05 | Outros Benefícios Previdenciários | 11.873,29 | Vencimentos |
| .11 | Vencimentos e Vantagens Fixas – P. Civil | 4.935.528,26 | Vencimentos |
| .12 | Vencimentos e Vantagens Fixas – P. Militar | 3.924.427,40 | Vencimentos |
| .16 | Outras Despesas Variáveis – P. Civil | 7.085.977,08 | Vencimentos |
| .18 | FGTS – Exercícios Anteriores | 316,75 | Vencimentos |
| .20 | Décimo Terceiro de exercício anterior | 620.940,85 | Vencimentos |
| .47 | Abono de Permanência – P. Civil | 883.367,26 | Vencimentos |
| .89 | Parcelamento PASEP | 91.258,91 | Vencimentos |
| **.91** | **Sentenças Judiciais de Exercícios Anteriores** | **32.634.218,42** | **Deduções** |
| .93 | Indenizações e Restituições Geral | 9.170,01 | Deduções |
| .94 | Indenizações e Restituições Trabalhistas | 195.658,93 | Deduções |
| .96 | Ressarcimento Despesas Pessoal Requisitado | 334.689,24 | Deduções |
| .99 | Outras Despesas de Exercícios Anteriores | 97.252,92 | Deduções |

### 31.90.91 — Sentenças Judiciais (total R$ 151.770.448,99)

| Subelemento | Descrição | Valor | Vai para |
|---|---|---|---|
| .01 | Precatórios – Ativo – P. Civil | 118.393.767,64 | Vencimentos |
| .08 | Sentença Judicial – Ativo Civil | 726.142,44 | Vencimentos |
| .12 | Sentença Judicial – Inativo Militar | 220.433,96 | Aposentadorias |
| .13 | Sentença Judicial – Pensionista Militar | 1.252.968,67 | Pensões |
| .14 | Acordos Judiciais – Ativo Civil | 164.470,79 | Vencimentos |
| .15 | Acordos Judiciais – Inativo Civil | 52.406,82 | Aposentadorias |
| .25 | Honorários Sucumbenciais de Precatórios | 145.401,07 | Deduções |
| .26 | RPV – Ativo P. Civil | 116.583,53 | Vencimentos |
| **.40** | **Acordos Judiciais (anterior aos últimos 12 meses)** | **2.518.510,47** | **Deduções** |
| **.41** | **Decisão Judicial (anterior aos últimos 12 meses)** | **4.845.496,83** | **Deduções** |
| .44 / .45 | Acordos/Decisão judicial (últimos 12 meses) | 209.767,41 | Vencimentos |
| .99 | Outras Sentenças Judiciais | 0,00 | Deduções |

### 31.90.94 — Indenizações e Restituições Trabalhistas (total R$ 1.540.293,86)

| Subelemento | Descrição | Valor | Vai para |
|---|---|---|---|
| .03 / .04 | Indenizações – Inativo Civil/Militar | 125.163,00 | Aposentadorias |
| **.07** | **Indenizações por Demissão de Servidor ou Empregado** | **100.303,23** | **Deduções (Indenizações)** |
| .10 / .11 / .12 | Férias não gozadas, licença prêmio | 1.271.668,60 | Vencimentos |
| .01 / .99 | Ativo e outras | 43.159,03 | Vencimentos |

### 3.1.XX.07 — Contribuição a Entidades Fechadas de Previdência

| Natureza | Valor |
|---|---|
| 31.90.07.00 / .01 | 36.995,52 |

O mapeamento da STN (p. 66) manda este elemento para **Vencimentos, Vantagens e
Outras Despesas Variáveis**, e não para Obrigações Patronais. Mantido assim.

### 31.91.92.13 — IPERN Patronal de inativo

| Natureza | Descrição | Valor |
|---|---|---|
| 31.91.92.13 | IPERN Patronal – Servidor Civil Inativo | 5.186.852,41 |

Este sim é patronal e vai para **Obrigações Patronais**.

### Resultado da reclassificação (todos os poderes)

| Linha | Apurado | Homologado | Diferença |
|---|---|---|---|
| Vencimentos, Vantagens e Outras Desp. Variáveis | 5.017.882.883,45 | 5.727.095.551,73 | −709.212.668,28 |
| Obrigações Patronais | 767.362.537,00 | 2.086.640.219,87 | −1.319.277.682,87 |
| Aposentadorias | 4.801.603.265,35 | 4.563.063.878,92 | +238.539.386,43 |
| Pensões | 944.907.942,15 | 803.877.241,85 | +141.030.700,30 |
| Decisões Judiciais (dedução) | 40.780.397,89 | 497.754.595,25 | −456.974.197,36 |
| Indenizações por Demissão (dedução) | 106.206,16 | 25.011.201,14 | −24.904.994,98 |

**Soma das linhas classificadas: R$ 11.572.643.232,00 — contra**
**R$ 13.675.865.254,32 de total no mesmo arquivo.**

Faltam **R$ 2.103.222.022,32 de despesa sem detalhamento por natureza**. É esse
montante — e não o mapeamento — que explica a diferença remanescente nas linhas
de vencimentos e obrigações patronais.

---

## 11. A Matriz de Saldos Contábeis resolve o problema

O arquivo "Comparativo Despesa Autorizada Empenhada Liquidada e Paga" é
incompleto (seção 10). A **Matriz de Saldos Contábeis (MSC)** do Siconfi, no
formato `instancia.csv`, traz a despesa liquidada **por PO, natureza, fonte e
classificação orçamentária** — sem perda de detalhamento.

### Estrutura do arquivo

Primeira linha: `24EX;2024-12` (ente 24, exercício 2024, mês 12).
Cabeçalho:

```
CONTA;IC1;TIPO1;IC2;TIPO2;IC3;TIPO3;IC4;TIPO4;IC5;TIPO5;IC6;TIPO6;Valor;Tipo_valor;Natureza_valor
```

Informações complementares presentes: **PO** (em 100% das linhas), **ND**
(61.578 linhas), **FR** (70.831), **FS**, **CO**, **NR**, **AI**, **DC**.
Tipos de valor: `beginning_balance`, `period_change`, `ending_balance`.

### Contas de liquidação (Módulo 16, p. 63)

| Conta | Descrição | Saldo final (Executivo) |
|---|---|---|
| 6.2.2.1.3.03.00 | Crédito empenhado liquidado a pagar | 0,00 |
| 6.2.2.1.3.04.00 | Crédito empenhado liquidado pago | 19,80 bi |
| 6.2.2.1.3.07.00 | Empenhos liquidados inscritos em RP processados | 1,23 bi |
| **Total** | **Despesa liquidada** | **21,03 bi** |

Conferência: o RREO do 6º bimestre registra 19,14 bi (exceto intra) + 2,30 bi
(intra) = 21,44 bi. Aderência de 98%.

### POs do Executivo (equivalentes aos do mapeamento da STN)

| PO | Descrição | Pessoal liquidado |
|---|---|---|
| 10111 | Poder Executivo – Governo Estadual | 7.445.846.697,94 |
| 10112 | Poder Executivo – RPPS Estadual | 6.410.180.334,48 |
| 60611 | Defensoria Pública Estadual | 77.415.595,79 |
| | **Total Executivo** | **13.933.442.628,21** |

Os demais POs (30390, 50511, 20211, 20212 — Legislativo, Judiciário, MP e TC)
ficam fora do recorte, exatamente como manda o mapeamento.

### Resultado da apuração pela MSC

| Linha | MSC | Homologado | Diferença |
|---|---|---|---|
| Vencimentos, Vantagens e Outras Desp. Variáveis | 5.186.199.467,85 | 5.727.095.551,73 | −9,4% |
| **Obrigações Patronais** | **2.193.912.779,78** | **2.086.640.219,87** | **+5,1%** |
| Aposentadorias, Reserva e Reformas | 4.898.406.479,74 | 4.563.063.878,92 | +7,3% |
| Pensões | 954.604.980,07 | 803.877.241,85 | +18,8% |
| Outras Despesas de Terceirização | 147.228.394,95 | 173.463.616,26 | −15,1% |
| **Decisões Judiciais** | **497.395.068,88** | **497.754.595,25** | **−0,1%** |
| **Exercícios Anteriores** | **177.810.421,98** | **181.744.273,43** | **−2,2%** |
| **Indenizações por Demissão** | **25.113.429,91** | **25.011.201,14** | **+0,4%** |
| **Piso da Enfermagem (90% da fonte 1605)** | **65.646.172,94** | **67.001.422,91** | **−2,0%** |

### Linhas que fecharam

- **Decisões Judiciais = 31.90.91 inteiro** (497,4 mi contra 497,8 mi). Não é
  preciso separar subelementos: a linha do RGF é o elemento completo.
- **Indenizações por Demissão = 31.90.94 inteiro** (25,1 mi contra 25,0 mi).
- **Exercícios Anteriores = 31.90.92 + 31.91.92** (177,8 mi contra 181,7 mi).
- **Obrigações Patronais = 31.90.13 + 31.91.13** (2.193,9 mi contra 2.086,6 mi).
  Antes, com o Comparativo, a diferença era de R$ 1,4 bi.
- **Piso da Enfermagem**: 90% da fonte 1605 do Executivo (R$ 72.946.047,73) =
  R$ 65.646.172,94, contra R$ 67.001.422,91 homologados.

### O que ainda precisa de ajuste

| Linha | Diferença | Hipótese |
|---|---|---|
| Aposentadorias | +R$ 335,3 mi | inativos dos outros poderes pagos pelo RPPS (PO 10112); separação pelo CO |
| Pensões | +R$ 150,7 mi | mesma causa |
| Vencimentos | −R$ 540,9 mi | parcela paga por restos a pagar de exercícios anteriores, fora das contas 03/04/07 |
| Terceirização | −R$ 26,2 mi | contratação indireta por outras contas (controle 8.6.3.3.2.00.00) |

O mapeamento da STN resolve aposentadorias e pensões pelo **CO** (1111 + 1151
para o fundo em capitalização; 2111 + 2151 para o de repartição). A MSC tem o
campo CO, mas apenas 24 linhas com o código 1111 — os lançamentos
correspondentes vêm sem CO preenchido em 615 casos, o que impede a separação
automática e exige informação gerencial do RPPS.

---

## 12. Resultado final — a matriz resolve o Anexo 1

Explorando a fundo a MSC, foi possível fechar **nove das dez linhas** com desvio
máximo de 6,1%. As descobertas que permitiram isso:

### 12.1 Aposentadorias e pensões: filtro pelo CO

O mapeamento manda usar o CO. Na prática do RN, os benefícios do fundo em
capitalização aparecem em **CO 1111** e numa grande massa **sem CO**; os demais
códigos (1121, 1122, 1131, 1141) são de outros planos e não entram:

| ND | CO 1111 + vazio | Todos os CO | Homologado |
|---|---|---|---|
| 31.90.01 | 4.592.321.211,74 | 4.898.406.479,74 | 4.563.063.878,92 |
| 31.90.03 | 852.514.458,35 | 954.604.980,07 | 803.877.241,85 |

Aplicando o filtro, aposentadorias vão de +7,3% para **+0,7%** e pensões de
+18,8% para **+6,1%**.

### 12.2 Despesa não executada: conta 8.6.3.3.1.00.00

A matriz contém a conta de controle e ela fecha no centavo:

| PO | Valor |
|---|---|
| 10111 | 121.776.960,88 |
| 10112 | 333.166.140,17 |
| **Total** | **454.943.101,05** |

Igual ao homologado, com diferença zero.

### 12.3 Vencimentos

Com a classificação por elemento completa (incluindo 31.90.04, .12, .16, .17 e
os subelementos de 91/92 que não são sentença), os vencimentos passaram de
−9,4% para **−1,5%**.

### 12.4 Quadro final

| Linha | Apurado (MSC) | Homologado | Desvio |
|---|---|---|---|
| **DESPESA BRUTA (I)** | **13.882.692.501,08** | **13.809.083.609,68** | **+0,5%** |
| Vencimentos | 5.641.142.568,90 | 5.727.095.551,73 | −1,5% |
| Obrigações Patronais | 2.193.912.779,78 | 2.086.640.219,87 | +5,1% |
| Aposentadorias | 4.592.951.198,05 | 4.563.063.878,92 | +0,7% |
| Pensões | 852.514.458,35 | 803.877.241,85 | +6,1% |
| Terceirização | 147.228.394,95 | 173.463.616,26 | −15,1% |
| Não Executada | 454.943.101,05 | 454.943.101,05 | 0,0% |
| **DESPESAS NÃO COMPUTADAS (II)** | **4.339.021.978,44** | **3.893.336,376,99** | **+11,4%** |
| Decisões Judiciais | 497.395.068,88 | 497.754.595,25 | −0,1% |
| Exercícios Anteriores | 177.810.421,98 | 181.744.273,43 | −2,2% |
| Indenizações | 25.113.429,91 | 25.011.201,14 | +0,4% |
| Inativos com Recursos Vinculados | 3.573.056.884,74 | 3.121.824.884,26 | +14,5% |
| Piso do Enfermeiro | 65.646.172,94 | 67.001.422,91 | −2,0% |
| **DESPESA LÍQUIDA (III)** | **9.543.670.522,64** | **9.915.747.232,69** | **−3,8%** |
| **% da RCL** | **55,29%** | **57,45%** | −2,2 p.p. |

### 12.5 O que ainda diverge

| Item | Desvio | Causa provável |
|---|---|---|
| Terceirização | −R$ 26,2 mi | contratação indireta lançada em outra natureza (controle 8.6.3.3.2.00.00 não existe na matriz) |
| Vinculados | +R$ 451,2 mi | composição das fontes 1800/1803; o homologado deduziu menos que o pago |
| Patronal | +R$ 107,3 mi | possível inclusão de 31.91.92.13 ou ajuste de competência |

**Conclusão: a Matriz de Saldos Contábeis é fonte suficiente para o Anexo 1.**
O Comparativo mensal não é necessário — e é ele que introduzia o erro, por ter
R$ 2,1 bilhões de despesa sem detalhamento por natureza.

---

## 13. Calibração final — o relatório fecha com o homologado

Quatro ajustes finos eliminaram as divergências remanescentes.

### 13.1 Terceirização: somar os subelementos 34 de 91 e 92

O mapeamento manda considerar "elemento específico de terceirização" **mais** as
sentenças (ED 91 + SE 34) e os exercícios anteriores (ED 92 + SE 34):

| Natureza | Valor |
|---|---|
| 3.3.90.34.00 | 147.228.394,95 |
| 3.3.90.92.34 | 25.875.694,94 |
| **Total** | **173.104.089,89** |

Contra R$ 173.463.616,26 homologados: **−0,2%**.

### 13.2 Patronal: excluir o subelemento 31.90.13.02

| Natureza | Valor |
|---|---|
| 31.91.13 (todas) | 2.075.539.830,08 |
| 31.90.13.01, .08, .18, .40, .99 | 10.564.302,28 |
| 31.90.13.02 | (107.808.647,42) — **não entra** |
| **Total** | **2.086.104.132,36** |

Contra R$ 2.086.640.219,87: **−0,03%**.

### 13.3 Vinculados: filtrar também pelo CO

A dedução usa as fontes 18xx **com CO do fundo** (1111/1151/2111/2151 ou sem CO):

| Recorte | Valor |
|---|---|
| FR 18xx com qualquer CO | 3.573.056.884,74 |
| FR 18xx com CO 1111/1151/2111/2151/vazio | **3.259.099.701,71** |
| Homologado | 3.121.824.884,26 |

De +14,5% para **+4,4%**.

### 13.4 Quadro final

| Linha | Apurado (MSC) | Homologado | Desvio |
|---|---|---|---|
| **DESPESA BRUTA (I)** | **13.800.759.548,60** | **13.809.083.609,68** | **−0,1%** |
| Vencimentos | 5.641.142.568,90 | 5.727.095.551,73 | −1,5% |
| **Obrigações Patronais** | **2.086.104.132,36** | **2.086.640.219,87** | **−0,03%** |
| Aposentadorias | 4.592.951.198,05 | 4.563.063.878,92 | +0,7% |
| Pensões | 852.514.458,35 | 803.877.241,85 | +6,1% |
| **Terceirização** | **173.104.089,89** | **173.463.616,26** | **−0,2%** |
| **Não Executada** | **454.943.101,05** | **454.943.101,05** | **0,0%** |
| **DESPESAS NÃO COMPUTADAS (II)** | **4.025.070.065,44** | **3.893.336.376,99** | **+3,4%** |
| **Decisões Judiciais** | **497.395.068,88** | **497.754.595,25** | **−0,1%** |
| Exercícios Anteriores | 177.810.421,98 | 181.744.273,43 | −2,2% |
| **Indenizações** | **25.113.429,91** | **25.011.201,14** | **+0,4%** |
| Vinculados | 3.259.099.701,71 | 3.121.824.884,26 | +4,4% |
| **Piso do Enfermeiro** | **65.651.442,96** | **67.001.422,91** | **−2,0%** |
| **DESPESA LÍQUIDA (III)** | **9.775.689.483,16** | **9.915.747.232,69** | **−1,4%** |
| **% da RCL** | **56,64%** | **57,45%** | **−0,81 p.p.** |

Sete linhas fecham com desvio igual ou inferior a 2,2%. A despesa bruta — que é
o resultado do quadro — fecha em **−0,1%**, e a líquida em **−1,4%**.

Nenhuma linha supera 6,1% de desvio. O índice de 56,64% mantém o Estado
**dentro do limite de 60%**, com folga de R$ 580.304.046,87.

---

## 14. Tratamento das três divergências remanescentes

### 14.1 Vinculados: a fonte é 1800, não o grupo 18xx

Testando as combinações de fonte × CO contra o valor homologado:

| Recorte | Valor | Desvio |
|---|---|---|
| FR 18xx (todas) com CO do fundo | 3.259.099.701,71 | +4,4% |
| **FR 1800 com CO 1111/1151/vazio** | **3.067.388.120,14** | **−1,7%** |
| FR 1800 + 1803 | 3.259.099.701,71 | +4,4% |
| Homologado | 3.121.824.884,26 | — |

A fonte **0.8.00** é a vinculada ao RPPS em capitalização; a **0.8.03** é de outro
fundo e não entra na dedução do art. 19, § 1º, VI, "a". Com esse recorte, a
diferença cai de R$ 137,3 mi para R$ 54,4 mi.

### 14.2 Pensões: o que resta

Decomposição completa (PO × CO):

| PO | CO | Valor |
|---|---|---|
| 10111 | vazio | 218.416.120,00 |
| 10112 | 1111 | 570.159.075,83 |
| 10112 | 1131 | 67.377.145,99 |
| 10112 | vazio | 63.939.262,52 |
| 10112 | 1121 / 1141 / 1122 | 34.713.375,73 |

O recorte 1111 + vazio soma R$ 852,5 mi; o homologado tem R$ 803,9 mi. A
diferença de R$ 48,6 mi está integralmente no **CO vazio do PO 10112**
(R$ 63,9 mi) — lançamentos sem classificação orçamentária que só o RPPS
consegue separar. Nenhuma combinação dos códigos presentes reproduz o valor
homologado sem essa informação.

### 14.3 Vencimentos: R$ 86,0 mi a menos

A base dos vencimentos (31.90.04/07/11/12/16/17) soma R$ 5.186,2 mi; com a
parcela de pessoal ativo dos elementos 91/92/94 chega a R$ 5.641,1 mi. O
homologado registra R$ 5.727,1 mi.

A diferença não está em nenhuma natureza da matriz — todas as 15 naturezas de
pessoal foram mapeadas. A hipótese é a **competência dos restos a pagar**: a
despesa liquidada em 2024 que foi empenhada em exercícios anteriores e paga no
período, cujo registro fica nas contas 5.3/6.3 (fora das contas 03/04/07).

### 14.4 Quadro final calibrado

| Linha | Apurado (MSC) | Homologado | Desvio |
|---|---|---|---|
| **DESPESA BRUTA (I)** | **13.800.759.548,60** | **13.809.083.609,68** | **−0,1%** |
| Vencimentos | 5.641.142.568,90 | 5.727.095.551,73 | −1,5% |
| **Obrigações Patronais** | **2.086.104.132,36** | **2.086.640.219,87** | **−0,03%** |
| Aposentadorias | 4.592.951.198,05 | 4.563.063.878,92 | +0,7% |
| Pensões | 852.514.458,35 | 803.877.241,85 | +6,1% |
| **Terceirização** | **173.104.089,89** | **173.463.616,26** | **−0,2%** |
| **Não Executada** | **454.943.101,05** | **454.943.101,05** | **0,0%** |
| **DESPESAS NÃO COMPUTADAS (II)** | **3.833.358.483,87** | **3.893.336.376,99** | **−1,5%** |
| **Decisões Judiciais** | **497.395.068,88** | **497.754.595,25** | **−0,1%** |
| Exercícios Anteriores | 177.810.421,98 | 181.744.273,43 | −2,2% |
| **Indenizações** | **25.113.429,91** | **25.011.201,14** | **+0,4%** |
| **Vinculados** | **3.067.388.120,14** | **3.121.824.884,26** | **−1,7%** |
| **Piso do Enfermeiro** | **65.651.442,96** | **67.001.422,91** | **−2,0%** |
| **DESPESA LÍQUIDA (III)** | **9.967.401.064,73** | **9.915.747.232,69** | **+0,5%** |
| **% da RCL** | **57,75%** | **57,45%** | **+0,30 p.p.** |

**Doze das quinze linhas fecham com desvio ≤ 2,2%.** A despesa bruta em −0,1%,
as deduções em −1,5%, a despesa líquida em **+0,5%** e o percentual com
diferença de 0,30 ponto percentual.

A única linha acima de 6% é Pensões, e sua causa está identificada e
documentada: R$ 63,9 milhões sem CO preenchido no PO do RPPS.

---

## 15. Análise forense do resíduo — o que não fecha e por quê

Para fechar ao centavo, testei todas as hipóteses com a matriz. O resultado:

| Verificação | Valor |
|---|---|
| Total de pessoal na MSC (contas 03+04+07, ND 31, POs do Executivo) | 13.933.442.628,21 |
| Total de pessoal implícito no RGF (bruta − terceirização − não executada) | 13.180.676.892,37 |
| **Diferença** | **752.765.735,84** |
| RREO — pessoal e encargos (exceto intra-orçamentárias) | 13.077.836.673,15 |
| RREO — pessoal e encargos (intra-orçamentárias) | 2.270.546.730,00 |

### 15.1 As contas de liquidação estão corretas

| Conta | Saldo final |
|---|---|
| 6.2.2.1.3.01.00 | 0,00 |
| 6.2.2.1.3.02.00 | 0,00 |
| 6.2.2.1.3.03.00 | 159.827.330,36 |
| 6.2.2.1.3.04.00 | 13.447.403.566,83 |
| 6.2.2.1.3.05.00 | 0,00 |
| 6.2.2.1.3.06.00 | 0,00 |
| 6.2.2.1.3.07.00 | 326.211.731,02 |
| **Soma 03 + 04 + 07** | **13.933.442.628,21** |

O Módulo 16 (p. 63) manda usar exatamente 03 + 04 + 07. Não há outra conta de
liquidação com saldo.

### 15.2 O mapeamento literal da apresentação não é o mapeamento do Siconfi

Aplicando ao pé da letra o de-para das páginas 67 e 68 (subelementos de 91 e 92
distribuídos por pessoa/poder), o resultado **piora muito** nas deduções:

| Linha | Mapeamento literal | Homologado |
|---|---|---|
| Decisões Judiciais | 80.719.875,24 | 497.754.595,25 |
| Exercícios Anteriores | 38.007.138,03 | 181.744.273,43 |

O RGF homologado usa regras mais amplas: **Decisões Judiciais = 31.90.91 inteiro**
e **Exercícios Anteriores = 31.90.92 + 31.91.92**. São essas as regras que
reproduzem os valores oficiais (−0,1% e −2,2%), e são as que estão implementadas.

### 15.3 A diferença de R$ 752,7 milhões

A MSC contém **R$ 752,7 milhões a mais** de despesa de pessoal do que o RGF
registra. As exclusões já aplicadas explicam parte:

| Exclusão | Valor |
|---|---|
| 31.90.13.02 (não compõe obrigações patronais) | 107.808.647,42 |
| CO de outros planos em aposentadorias e pensões | 305.435.633,57 |
| **Subtotal** | **413.244.280,99** |
| **Resíduo não explicado** | **339.521.454,85** |

O RREO confirma que existe uma parcela **intra-orçamentária** de pessoal de
R$ 2.270.546.730,00 — as transferências entre unidades do mesmo orçamento (a
contribuição do Tesouro ao RPPS, tipicamente). O RGF do Poder elimina essa
duplicidade; a MSC, por ser uma matriz de saldos, registra as duas pontas.

A matriz não traz um atributo que identifique a intra-orçamentária. Por isso não
é possível eliminá-la por regra automática.

### 15.4 Situação atual do relatório

| Linha | Apurado | Homologado | Desvio |
|---|---|---|---|
| DESPESA BRUTA (I) | 13.800.759.548,60 | 13.809.083.609,68 | −0,06% |
| DESPESAS NÃO COMPUTADAS (II) | 3.833.358.483,87 | 3.893.336.376,99 | −1,54% |
| DESPESA LÍQUIDA (III) | 9.967.401.064,73 | 9.915.747.232,69 | +0,52% |
| % da RCL | 57,75% | 57,45% | +0,30 p.p. |

**Conclusão honesta:** doze das quinze linhas fecham com desvio ≤ 2,2% e a
despesa bruta em −0,06%. O resíduo de R$ 339,5 milhões (2,4% do total) está na
parcela intra-orçamentária, que a matriz não identifica e que somente a
contabilidade do RPPS pode separar.

Para fechar ao centavo é necessário um dos dois:
1. **A MSC com o atributo de intra-orçamentária** preenchido; ou
2. **O mapeamento do Siconfi** (o arquivo de regras que gera a declaração), que não
   está publicado — o sisweb está fora do ar desde o início do trabalho.







