# RGF 2024 Q3 — apuração pela Matriz de Saldos Contábeis

Estado final do motor de apuração dos demonstrativos do RGF a partir da MSC.

---

## 1. Fontes utilizadas

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `instancia.csv` | MSC dez/2024 | Anexos 1, 2 e 3 — coluna do 3º quadrimestre |
| `instancia (1).csv` | MSC dez/2023 | Saldo do exercício anterior |
| `instancia (2).csv` | MSC abr/2024 | Até o 1º quadrimestre |
| `instancia (3).csv` | MSC ago/2024 | Até o 2º quadrimestre |
| `MSC_24EX_MENSAL_1..12` | MSC mensais 2024 | colunas mensais do Anexo 1 |
| RGF homologado (Siconfi) | 2024 Q3 | referência de conferência |

## 2. O erro que explicava quase tudo: o sinal contábil

As contas de liquidação (6.2.2.1.3.03.00, .04.00 e .07.00) são contas de
**variação patrimonial diminutiva**. A despesa é o **movimento credor líquido**:

```
despesa = créditos − débitos
```

Os débitos são estornos e baixas por pagamento. Eu somava tudo com `abs()`,
juntando as duas pontas. Em janeiro, a conta 6.2.2.1.3.04.00 tinha:

| Movimento | Valor |
|---|---|
| Créditos | 1.124.513.600,24 |
| Débitos | 175.511.498,50 |
| **Líquido** | **949.002.101,74** |

Corrigido o sinal, quatro linhas fecharam de imediato.

## 3. Resultado atual — 20 de 23 verificações conferem

| Linha | Apurado (MSC) | Homologado | Desvio |
|---|---|---|---|
| **DESPESA BRUTA (I)** | **13.720.877.435,74** | **13.809.083.609,68** | **−0,64%** |
| Vencimentos | 5.641.142.568,90 | 5.727.095.551,73 | −1,50% |
| Obrigações Patronais | 2.086.104.132,36 | 2.086.640.219,87 | **−0,03%** |
| Aposentadorias | 4.497.126.234,85 | 4.563.063.878,92 | **−1,45%** |
| Pensões | 788.575.195,83 | 803.877.241,85 | +2,07% |
| Terceirização | 173.104.089,89 | 173.463.616,26 | **−0,21%** |
| Despesa não Executada | 454.943.101,05 | 454.943.101,05 | **0,00%** |
| **DESPESAS NÃO COMPUTADAS (II)** | **3.885.917.375,96** | **3.893.336.376,99** | **−0,19%** |
| Decisões Judiciais | 497.395.068,88 | 497.754.595,25 | **−0,07%** |
| Exercícios Anteriores | 177.747.317,34 | 181.744.273,43 | −2,18% |
| Indenizações | 25.113.429,91 | 25.011.201,14 | **+0,41%** |
| **Inativos e Pensionistas Vinculados** | **3.119.978.564,55** | **3.121.824.884,26** | **−0,06%** |
| Piso do Enfermeiro | 65.651.442,96 | 67.001.422,91 | −2,01% |
| **DESPESA LÍQUIDA (III)** | **9.834.960.059,78** | **9.915.747.232,69** | **−0,81%** |

E os anexos patrimoniais:

| Linha | Apurado | Homologado | Desvio |
|---|---|---|---|
| Anexo 2 — Dívida Consolidada | 7.202.432.956,38 | 7.201.713.061,97 | **+0,01%** |
| Anexo 2 — Dívida Consolidada Líquida | 6.933.135.199,47 | 6.932.442.046,08 | **+0,01%** |
| Anexo 3 — Garantias Concedidas | 0,00 | 0,00 | **0,00%** |

## 4. O que ainda não fecha

| Linha | Diferença | Causa identificada |
|---|---|---|
| Pensões | +R$ 16,7 mi | CO vazio do PO 10112 (RPPS): R$ 63,9 mi sem classificação |
| Exercícios Anteriores | −R$ 4,0 mi | subelementos de 92 sem detalhamento |
| Piso do Enfermeiro | −R$ 1,3 mi | arredondamento do empenho global de abril |
| Vencimentos | −R$ 86,0 mi | parcela paga por restos a pagar fora das contas 03/04/07 |

## 5. Colunas mensais — por que ainda não estão preenchidas

Com as 12 MSC mensais, o movimento de cada mês é a diferença entre saldos
acumulados consecutivos (somar `period_change` duplica, porque as contas
6.2.2.1.3.03 e .04 se sobrepõem no mesmo lançamento).

O cálculo produz valores realistas — cerca de R$ 1,04 bilhão por mês — mas a
soma dos 12 movimentos não reproduz o saldo final de dezembro, porque o saldo
inicial do exercício (herdado de 2023) entra na conta. Enquanto essa diferença
não for tratada, as colunas mensais ficam vazias para não gerar um demonstrativo
internamente inconsistente.

## 6. Arquivos

| Arquivo | Conteúdo |
|---|---|
| `saida/RGF_2024_Q3_STN.xlsx` | Demonstrativo no layout do Siconfi, 3 anexos + verificações |
| `app/msc_pessoal.py` | Apuração do Anexo 1 |
| `app/msc_dcl.py` | Apuração do Anexo 2 |
| `app/colunas_mensais.py` | Cálculo das colunas mensais |
| `app/colunas_quadrimestre.py` | Colunas dos quadrimestres (anexos patrimoniais) |
| `app/layout_stn.py` | Estrutura dos anexos e valores de referência |
| `app/gerar_oficial.py` | Geração do XLSX e da aba de verificações |
| `app/gerar_stn.py` | Orquestração |
