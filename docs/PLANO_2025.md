# Plano de trabalho — exercício 2025

Decisão: trabalhar com **2025**, o primeiro exercício com a estrutura completa
no SIAFIC (em 2024 os Poderes ainda não estavam integrados).

---

## 1. Inventário do que temos

| insumo | situação | cobre |
|---|---|---|
| **MSC 2025** | ✅ completo — 12 meses, classes 3, 4 e 6, `period_change` | despesa liquidada, receita, RCL |
| **Comparativo da Receita 2025** | ✅ consolidado, encerramento | operações de crédito, receita por rubrica |
| **Balancete Consolidado** | ⚠️ **é de 2024** | classe 8 de 2024 |
| RGF homologado 2025 Q3 | ❌ | conferência |
| RREO homologado 2025 B6 | ❌ | conferência |
| `ending_balance` | ❌ | conferir fluxo × saldo |

---

## 2. O que já está apurado

### RGF Anexo 1 — Despesa com Pessoal (2025 Q3)

Janela 2025-01 a 2025-12, movimento líquido do `period_change`, POs
10111 + 10112 + 60611.

| linha | valor |
|---|---:|
| **DESPESA BRUTA (I)** | **15.209.208.030,01** |
| Vencimentos | 6.914.271.022,13 |
| Obrigações Patronais | 2.411.358.188,07 |
| Aposentadorias | 4.882.968.816,04 |
| Pensões | 820.116.992,13 |
| Terceirização | 180.493.011,64 |
| Despesa não Executada | 0,00 ← **falta o balancete de 2025** |
| **DESPESAS NÃO COMPUTADAS (II)** | **3.699.058.569,43** |
| Indenizações | 3.685.106,37 |
| Inativos e Pensionistas Vinculados | 3.539.334.657,80 |
| Piso do Enfermeiro | 48.755.181,18 |
| **DESPESA LÍQUIDA (III)** | **11.510.149.460,58** |

**12 colunas mensais preenchidas**, somando exatamente o TOTAL.

### Conferência contra a referência calibrada

| linha | apurado | oficial implícito | desvio |
|---|---:|---:|---:|
| Despesa Bruta | 15.209.208.030 | 15.264.169.000 | **−0,36%** |
| Vencimentos | 6.914.271.022 | 6.921.190.000 | **−0,10%** |

### Operações de crédito — 2025

| rubrica | valor |
|---|---:|
| 4.2.1 — Operações de Crédito | **2.491.012,67** |
| Receitas correntes | 26.659.603.708,77 |
| Receitas de capital | 318.362.312,73 |

R$ 2.491.012,67 é **exatamente** o valor que o RREO Anexo 9 de 2025 declara.

---

## 3. O que falta para fechar 2025

### 3.1 Balancete de encerramento de 2025

**O insumo mais importante.** Sem ele:

- a linha "Despesa não Executada" fica zerada (≈ R$ 168,8 mi em 2025);
- a Despesa Bruta fica subavaliada em igual valor;
- a Despesa Líquida herda o erro.

Com ele, a linha fecha em **0,00%** — como fechou em 2024.

### 3.2 RGF e RREO homologados de 2025

Para conferência linha a linha. Sem eles, a verificação é contra os desvios de
referência do `ANEXO1_CALIBRACAO.md` (−0,36% na bruta), não contra os valores.

### 3.3 `ending_balance`

Permite conferir a identidade fluxo × saldo: a soma dos 12 `period_change` deve
ser idêntica ao saldo de dezembro. É um teste de integridade, não um dado novo.

---

## 4. O que dá para fechar com o que temos

| demonstrativo | situação |
|---|---|
| **RGF Anexo 1 — Despesa com Pessoal** | ✅ 15,2 bi, 12 colunas, −0,36% |
| RGF Anexo 4 — Operações de Crédito | ⚠️ operações apuradas (R$ 2,49 mi); falta a RCL de 2025 |
| RGF Anexo 3 — Garantias | ⚠️ precisa do balancete (contas 2.2.8) |
| RGF Anexo 2 — DCL | ⚠️ precisa do balancete (contas 2.2.1 a 2.2.3) |
| RREO | ❌ precisa do arquivo homologado |

**A RCL de 2025** — necessária para os Anexos 3, 4 e 6 — está no RREO Anexo 3,
que não temos. O comparativo traz as receitas correntes brutas
(R$ 26.659,6 mi), mas a RCL exige as deduções (transferências constitucionais,
FUNDEB).

---

## 5. Ordem de prioridade

1. **Balancete de encerramento de 2025** → fecha o Anexo 1 em todas as linhas
2. **RREO 2025 B6 homologado** → traz a RCL e permite os Anexos 3, 4 e 6
3. **RGF 2025 Q3 homologado** → conferência linha a linha
4. `ending_balance` → integridade fluxo × saldo

Com os dois primeiros, 2025 fecha completo.
