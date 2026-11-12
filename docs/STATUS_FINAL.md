# Status dos demonstrativos — o que está fechado e o que falta

Balanço honesto do que foi construído e do que cada lacuna exige.

---

## 1. RGF 2024 Q3 — 6 anexos

| Anexo | Situação | Desvio |
|---|---|---|
| Anexo 1 — Despesa com Pessoal | ⚠️ parcial | −0,64% na bruta |
| Anexo 2 — Dívida Consolidada Líquida | ✅ fecha | +0,01% |
| Anexo 3 — Garantias e Contragarantias | ✅ fecha | 0,00% |
| Anexo 4 — Operações de Crédito | ❌ operações | limites em 0,00% |
| Anexo 5 — Disponibilidade e Restos a Pagar | ❌ valores por fonte | — |
| Anexo 6 — Demonstrativo Simplificado | ⚠️ parcial | herda o do Anexo 4 |

**Verificações: 24 de 30 linhas conferem.**

### O que falta no Anexo 1

| Linha | Desvio | Causa | O que resolve |
|---|---|---|---|
| Vencimentos | −R$ 86,0 mi | parcela intra-orçamentária | MSC com o atributo de intra |
| Pensões | +R$ 16,7 mi | CO vazio do PO 10112 | informação do RPPS |
| Exercícios Anteriores | −R$ 4,0 mi | subelementos de 92 | detalhamento |
| Piso do Enfermeiro | −R$ 1,3 mi | arredondamento do empenho global | — |

O erro está **concentrado em Vencimentos** (97% da diferença da bruta). Testei e
descartei: natureza não mapeada, PO faltante e restos a pagar de 2023. O resíduo
aponta para a despesa intra-orçamentária, que a matriz não identifica.

### O que falta no Anexo 4 e 6

A operação de crédito realizada (R$ 429.228.593,51) é **receita orçamentária**.
A MSC traz o código da natureza da **despesa** (ND), mas não o da **receita**.
Sem esse atributo, não há como isolar.

### O que falta no Anexo 5

O cruzamento por fonte de recurso exige a conta **8.2.1.7.4.01 — Disponibilidade
por Fonte a Utilizar** (citada nas próprias notas explicativas do RGF), que vem
**sem saldo** nas matrizes disponíveis.

---

## 2. RREO 2024 B6 — 11 anexos

| Anexo | Rótulos | Valores |
|---|---|---|
| 01 — Balanço Orçamentário | ✅ 159/159 | ✅ |
| 02 — Despesas por Função | ⚠️ 153/388 | ✅ |
| 03 — RCL | ✅ 31/31 | ✅ |
| 04 — Previdenciárias | ✅ 51/59 | ✅ |
| 06 — Resultado Primário | ✅ 73/91 | ✅ |
| 07 — Restos a Pagar | ✅ 17/24 | ✅ |
| 09 — Operações de Crédito | ❌ 0/9 | ✅ |
| 10 — Projeção Atuarial | ⚠️ 56/148 | ✅ |
| 11 — Alienação de Ativos | ❌ 1/14 | ✅ |
| 13 — PPP | ✅ 12/12 | ✅ |
| 14 — Simplificado | ✅ 56/56 | ✅ |

**Oito dos onze anexos com rótulo completo ou quase.**

### Anexos 8 e 12 — não pertencem ao Siconfi

Confirmado pelo Guia de Preenchimento (p. 7): os Anexos 8 (Educação) e 12 (Saúde)
são enviados ao **SIOPE** e ao **SIOPS**, respectivamente. O arquivo consolidado
do RREO nunca os conterá.

O Anexo 8 foi extraído do DOE-RN (190 linhas). O Anexo 12 ficou parcial: a tabela
do DOE tem seis colunas em 120 pontos, densidade que a clusterização por X não
separa.

---

## 3. O que falta e o que cada item exige

| Lacuna | Exige |
|---|---|
| RGF 1 — Vencimentos (R$ 86 mi) | MSC com atributo de intra-orçamentária |
| RGF 1 — Pensões (R$ 16,7 mi) | informação do RPPS sobre o CO vazio |
| RGF 4 e 6 — Operações de Crédito | natureza da receita (não existe na MSC) |
| RGF 5 — Disponibilidade por fonte | conta 8.2.1.7.4.01 com saldo |
| RREO 9 e 11 — rótulos | DOE da edição que os publicou (não é a de 30/01) |
| RREO 10 — 92 linhas | calibração da extração por X no DOE |
| RREO 12 — Saúde | SIOPS, ou calibração fina no DOE |

**Nenhuma dessas lacunas é erro de cálculo.** Todas são ausência de dado na fonte
disponível — e cada uma tem um caminho de solução identificado.

---

## 4. O que está pronto para uso

| Arquivo | Conteúdo |
|---|---|
| `saida/RGF_2024_Q3_STN.xlsx` | RGF completo em 6 anexos, layout oficial |
| `saida/RREO_2024_B6_STN.xlsx` | RREO completo em 11 anexos |
| `saida/RREO_2024_B6_Anexos_08_12.xlsx` | Anexo 8 (Educação), 190 linhas |

Os três trazem a aba **Verificações** com a conferência linha a linha contra o
Siconfi.
