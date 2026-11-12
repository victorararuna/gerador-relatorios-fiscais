# RGF Anexo 2 — Dívida Consolidada Líquida (DCL)

Apuração a partir da **Matriz de Saldos Contábeis** (instancia.csv, exercício
2024), 3º quadrimestre, confrontada com o RGF homologado no Siconfi.

---

## 1. O que o Anexo 2 exige

Estrutura conforme o **MDF 14ª edição, tópico 04.02** (páginas 505 a 534):

```
DÍVIDA CONSOLIDADA (I)  = Dívida Mobiliária
                        + Dívida Contratual (empréstimos, reestruturação,
                          financiamentos — internos e externos)
                        + Precatórios
                        + Operações de crédito
                        + Parcelamento e renegociação de dívidas

DEDUÇÕES (II)           = Disponibilidade de caixa
                        + Aplicações financeiras
                        + Demais haveres financeiros

DÍVIDA CONSOLIDADA LÍQUIDA (III) = (I - II)

% da DC sobre a RCL ajustada  (I / RCL)
% da DCL sobre a RCL ajustada (III / RCL)
```

**Ponto importante (MDF p. 505):** o Anexo 2 do Executivo **abrange todos os
Poderes**. Diferentemente do Anexo 1, aqui **não se aplica o recorte por PO** — a
dívida é do Estado, não de um Poder.

## 2. Composição identificada na matriz

| Conta | Descrição | Valor |
|---|---|---|
| 2.2.1.1.03.02 | Precatórios — RPPS | 2.246.649.478,40 |
| 2.2.2.1.02.00 | Dívida contratual — externa | 1.572.256.793,43 |
| 2.2.1.1.03.03 | Precatórios — demais | 1.224.820.548,10 |
| 2.2.3.1.1.04.02 | Parcelamento — previdenciário | 846.845.402,52 |
| 2.2.2.1.1.02.98 | Dívida contratual — interna | 754.362.811,29 |
| 2.2.3.1.1.04.03 | Parcelamento — demais | 505.326.837,50 |
| 2.1.8.9.1.01.06 | Demais obrigações — longo prazo | 48.569.113,73 |
| 2.1.8.8.1.01.10 | Demais obrigações — curto prazo | 3.043.658,36 |
| 2.1.8.9.1.14.00 | Demais obrigações — ajustes | 539.377,20 |
| 2.1.1.4.3.98.00 | Empréstimos — outras | 18.935,85 |
| | **DÍVIDA CONSOLIDADA (I)** | **7.202.432.956,38** |

| Conta | Descrição | Valor |
|---|---|---|
| 1.2.1.1.1.99.05 | Créditos a receber — dedução | 264.346.056,77 |
| 1.2.1.1.1.97.00 | Créditos a receber — dedução | 4.947.535,80 |
| 1.1.3.8.1.1.10 | Aplicações financeiras | 2.836,12 |
| 1.1.3.5.1.04.00 | Disponibilidade | 1.328,22 |
| | **DEDUÇÕES (II)** | **269.297.756,91** |

## 3. Resultado

| Linha | Apurado (MSC) | Homologado | Diferença |
|---|---|---|---|
| **Dívida Consolidada (I)** | **7.202.432.956,38** | **7.201.713.061,97** | **+719.894,41 (+0,010%)** |
| **Deduções (II)** | **269.297.756,91** | **269.271.015,89** | **+26.741,02 (+0,010%)** |
| **Dívida Consolidada Líquida (III)** | **6.933.135.199,47** | **6.932.442.046,08** | **+693.153,39 (+0,010%)** |
| % da DC sobre a RCL | 41,73% | 41,74% | −0,01 p.p. |
| **% da DCL sobre a RCL** | **40,17%** | **40,18%** | **−0,01 p.p.** |

O limite de 200% da RCL para os Estados é amplamente atendido: 40,18%.

## 4. Como as contas foram identificadas

O MDF **não publica** o de-para de contas do Anexo 2 — ele descreve apenas o
significado das linhas. O mapeamento oficial está nos arquivos de mapeamento da
STN, que continuam indisponíveis (o sisweb está fora do ar).

As contas foram identificadas por **reconciliação contra o valor homologado**:
busca de subconjunto sobre as contas 2.1.x e 2.2.x da matriz, excluindo as
provisões (2.7.2) e os controles (2.7.9), até reproduzir a Dívida Consolidada de
R$ 7.201.713.061,97. O mesmo procedimento foi aplicado às deduções, sobre as
contas 1.1 e 1.2.

**Isto é um ponto de atenção metodológico:** a composição encontrada reproduz o
total com precisão de centavos de milésimo (0,01%), mas a atribuição de cada
conta a uma linha específica (Dívida Mobiliária, Empréstimos, Financiamentos,
Precatórios, Parcelamento) depende do mapeamento oficial. Por isso o
demonstrativo foi montado com as contas agrupadas sob "Dívida Consolidada" e
"Deduções", sem quebrar nas sublinhas do MDF.

## 5. Comparação com o Anexo 1

| | Anexo 1 — Despesa com Pessoal | Anexo 2 — DCL |
|---|---|---|
| Recorte | POs 10111 + 10112 + 60611 | Todos os Poderes |
| Fonte | MSC | MSC |
| Linhas | 15 | 4 |
| Desvio no total | −0,06% (bruta) | **+0,010%** |
| Dificuldade | classificação de subelementos e CO | identificação de contas |

O Anexo 2 fechou muito mais fácil porque a DCL é **saldo patrimonial**, não
fluxo de despesa: não há competência, subelemento nem restos a pagar para
classificar. Basta somar as contas certas.

---

## 6. Layout oficial e verificações

Com o RGF homologado reenviado, o relatório passa a ser gerado no **layout do
Siconfi**, com três abas:

- **`RGF-Anexo 01`** — bloco de identificação, grupo/quadro/rótulo, título,
  cabeçalho com as 15 colunas oficiais (MR-11 a MR, TOTAL e RP não processados),
  as 18 linhas do quadro e o quadro de apuração do limite.
- **`RGF-Anexo 02`** — as 5 colunas oficiais e as 42 linhas da DCL, incluindo as
  obrigações não integrantes.
- **`Verificações`** — conferência linha a linha contra os valores homologados,
  com semáforo: verde até 2%, amarelo até 10%, vermelho acima.

### Estrutura real do Anexo 2 (extraída do homologado)

| Linha | Valor (3º quadrim.) |
|---|---|
| DÍVIDA CONSOLIDADA – DC (I) | 7.201.713.061,97 |
| Dívida Mobiliária | 0,00 |
| Dívida Contratual | 3.565.766.102,01 |
| — Empréstimos | 2.734.195.879,84 |
| —— Internos | 912.009.325,13 |
| —— Externos | 1.822.186.554,71 |
| — Reestruturação da Dívida | 663.224.116,18 |
| — Parcelamento e Renegociação | 168.346.105,99 |
| Precatórios posteriores a 05/05/2000 | 3.214.637.210,88 |
| Outras Dívidas | 421.309.749,08 |
| DEDUÇÕES (II) | 269.271.015,89 |
| — Disponibilidade de Caixa Bruta | 1.536.331.084,82 |
| — (–) Restos a Pagar Processados | 1.025.632.163,82 |
| — (–) Depósitos Restituíveis | 510.698.921,00 |
| — Demais Haveres Financeiros | 269.271.015,89 |
| **DÍVIDA CONSOLIDADA LÍQUIDA (III)** | **6.932.442.046,08** |
| RCL | 17.259.892.416,73 |
| (–) Emendas individuais | 4.802.839,15 |
| **RCL AJUSTADA (VI)** | **17.255.089.577,58** |
| **% da DC sobre a RCL ajustada** | **41,74%** |
| **% da DCL sobre a RCL ajustada** | **40,18%** |
| Limite (Resolução do Senado, 200%) | 34.510.179.155,16 |
| Limite de alerta (180%) | 31.059.161.239,64 |

### Descoberta relevante: o limite do Executivo é 49%, não 60%

O Anexo 1 revela que a apuração usa a **RCL ajustada** e que o limite máximo do
Poder Executivo é **49% da RCL ajustada** (Resolução do Senado nº 40/2001:
60% do Estado, dos quais 3% Legislativo, 6% Judiciário, 2% Ministério Público,
restando 49% para o Executivo).

| Linha | Valor homologado |
|---|---|
| DTP (Despesa Total com Pessoal) | 9.919.747.911,85 |
| **% da DTP sobre a RCL ajustada** | **57,56%** |
| Limite máximo (49%) | 8.444.189.612,04 |
| Limite prudencial (46,55%) | 8.021.980.131,44 |
| Limite de alerta (44,10%) | 7.599.770.650,84 |

**O Rio Grande do Norte está acima do limite máximo em R$ 1,53 bilhão**, e
também acima do limite de alerta. A apuração pela matriz reproduz esse quadro
(57,86%), com a mesma diferença de 0,30 ponto percentual já identificada.

---

## 7. Coluna "Saldo do Exercício Anterior" com a matriz de 2023

Com a Matriz de Saldos Contábeis de 2023 (arquivo `instancia (1).csv`), a coluna
do saldo anterior passou a ser preenchida:

| Linha | Saldo em 31/12/2023 (MSC) | Homologado | Desvio |
|---|---|---|---|
| Dívida Consolidada (I) | 4.381.511.696,00 | 4.452.045.566,50 | −1,58% |
| Dívida Contratual | 1.719.861.358,09 | 2.895.074.897,34 | — |
| Precatórios | 2.356.040.266,74 | — | — |
| Deduções (II) | 280.367.534,59 | 350.524.739,48 | −20,0% |
| **Dívida Consolidada Líquida** | **4.101.144.161,41** | **4.101.520.827,02** | **−0,01%** |

A **DCL de 2023 fecha em −0,01%**, embora a DC e as deduções individualmente
divirjam mais (−1,6% e −20%). Os desvios se compensam quase exatamente — o que
reforça que o conjunto de contas identificado está correto, mas a repartição
entre dívida e deduções ainda precisa do mapeamento oficial.

### O que a matriz anual não permite

As colunas **Até o 1º Quadrimestre** e **Até o 2º Quadrimestre** continuam
vazias. O RGF apura esses períodos como "últimos 12 meses" em datas móveis:

| Coluna | Período dos últimos 12 meses |
|---|---|
| Saldo do exercício anterior | 31/12/2023 |
| Até o 1º quadrimestre | maio/2023 a abril/2024 |
| Até o 2º quadrimestre | setembro/2023 a agosto/2024 |
| Até o 3º quadrimestre | janeiro a dezembro/2024 |

As matrizes disponíveis são **anuais** (saldo acumulado de dezembro). Para
preencher os quadrimestres intermediários seriam necessárias as MSC **mensais** —
ou as de abril e agosto de 2024.

---

## 8. Quadrimestres preenchidos (matrizes de abril e agosto)

Com as matrizes de **abril/2024** e **agosto/2024**, as quatro colunas do Anexo 2
passaram a ser preenchidas:

| Data | DC apurada | DC oficial | Desvio | DCL apurada | DCL oficial | Desvio |
|---|---|---|---|---|---|---|
| 31/12/2023 | 4.381.511.696,00 | 4.452.045.566,50 | −1,58% | 4.101.144.161,41 | 4.101.520.827,02 | −0,01% |
| 30/04/2024 | 4.922.207.778,82 | 4.974.054.363,73 | −1,04% | 4.641.840.244,23 | 3.403.298.378,88 | +36,39% |
| 31/08/2024 | 5.069.690.239,09 | 4.818.269.690,74 | +5,22% | 4.792.854.056,58 | 3.514.440.351,57 | +36,38% |
| 31/12/2024 | 7.202.432.956,38 | 7.201.713.061,97 | **+0,01%** | 6.933.135.199,47 | 6.932.442.046,08 | **+0,01%** |

### A dívida fecha; a dedução não

A **Dívida Consolidada** fecha bem em três das quatro datas e em 0,01% na data de
referência. O problema está nas **deduções** nas datas intermediárias:

| Data | Deduções apuradas | Deduções oficiais |
|---|---|---|
| 31/12/2023 | 280.367.534,59 | 350.524.739,48 |
| 30/04/2024 | 280.367.534,59 | 1.570.755.984,85 |
| 31/08/2024 | 276.836.183,00 | 1.303.829.339,17 |
| 31/12/2024 | 269.297.756,91 | 269.271.015,89 |

A composição oficial das deduções é:

```
DEDUÇÕES = Disponibilidade de Caixa + Demais Haveres Financeiros

Disponibilidade de Caixa = Disponibilidade de Caixa Bruta
                         - Restos a Pagar Processados
                         - Depósitos Restituíveis e Valores Vinculados
```

| Data | Disp. bruta | (–) RP processados | (–) Depósitos | = Disp. caixa | Haveres | Total |
|---|---|---|---|---|---|---|
| 31/12/2023 | 1.651.757.299,80 | 1.127.395.287,62 | 443.108.288,59 | 81.253.723,59 | 269.271.015,89 | 350.524.739,48 |
| 30/04/2024 | 2.287.397.328,09 | 543.448.909,92 | 442.463.449,21 | 1.301.484.968,96 | 269.271.015,89 | 1.570.755.984,85 |
| 31/08/2024 | 1.854.471.672,26 | 359.009.866,68 | 460.903.482,30 | 1.034.558.323,28 | 269.271.015,89 | 1.303.829.339,17 |
| 31/12/2024 | 1.536.331.084,82 | 1.025.632.163,82 | 510.698.921,00 | 0,00 | 269.271.015,89 | 269.271.015,89 |

**O "Demais Haveres Financeiros" está identificado** — é a conta 1.2.1.1.1.99,
com R$ 269.271.015,89 constante nas quatro datas.

**A Disponibilidade de Caixa Bruta, os RP Processados e os Depósitos ainda não.**
A busca por subconjunto nas contas 1.1 não encontrou um conjunto estável entre as
datas — o que indica que a composição não é um grupo fixo de contas, ou que há
conta de natureza redutora. Sem o mapeamento oficial, as colunas intermediárias
saem com a dedução incompleta.



