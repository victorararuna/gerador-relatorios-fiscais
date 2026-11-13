# Os dois arquivos do SIAFEM — o que cobrem

Arquivos recebidos:

- `Imprimir Balancete Consolidado.xls`
- `Comparativo da Receita Orçada com a Arrecadada (1).xls`

Resposta curta: **cobrem, sim** — e o balancete resolve a classe 8.

---

## 1. Balancete Consolidado — resolve a classe 8

O arquivo tem **2.641 contas**, das quais **330 da classe 8**. É o balancete de
**encerramento** (`Mês Referência: Encerramento`, `Tipo Consolidação:
Consolidado Geral`).

### A conta que faltava

| conta | descrição | saldo anterior |
|---|---|---:|
| `8.6.3.3.1.00.00.00` | Controles da Despesa Não Executada Orçamentariamente | **454.943.101,05 C** |
| `8.6.3.3.1.01.00.00` | Não Executada — Salários | 0,00 |
| `8.6.3.3.1.02.00.00` | Não Executada — Décimo Terceiro (13) | 454.943.101,05 C |

**R$ 454.943.101,05** — exatamente o valor do RGF homologado de 2024 Q3.

### A conta do Anexo 5

| conta | descrição | saldo anterior |
|---|---|---:|
| `8.2.1.7.4.01.00.00` | Disponibilidade por Fonte a Utilizar | **1.669.041.113,22 C** |
| `8.2.1.7.4.02.00.00` | Disponibilidade por Fonte — OB Emitida | — |

Era a conta que eu declarei "sem saldo na MSC". **Ela existe** — só não vem no
recorte da matriz que temos.

### Por que o saldo final é zero

Na linha 8281:

```
Saldo anterior : 454.943.101,05 C
Movimento D    : 1.090.914.976,21
Movimento C    : 1.259.764.428,24
Saldo final    : 0,00
```

A conta **zera no encerramento** — o valor relevante é o **saldo do exercício
anterior**, que é a despesa não executada acumulada. Foi por isso que a busca na
MSC não achou nada: eu procurava o saldo final.

---

## 2. Comparativo da Receita — os dois não são do mesmo exercício

| arquivo | consolidação | operações de crédito | receitas correntes |
|---|---|---:|---:|
| `...Arrecadada.xls` | Poder Executivo, Dezembro | **429.228.593,51** | 23.456.344.890,71 |
| `...Arrecadada (1).xls` | **Consolidado Geral**, Encerramento | **2.491.012,67** | 26.659.603.708,77 |

**R$ 2.491.012,67** é exatamente o valor que o `RELATORIO_FINAL.md` da outra
fase identificou no RREO Anexo 9 de **2025**:

> "o demonstrativo das operações de crédito declara exatamente R$ 2.491.012,67
> de receita realizada — o mesmo número do RGF Anexo 4"

Ou seja:

- o **primeiro** comparativo é de **2024** (Executivo) → R$ 429,2 mi;
- o **segundo** é de **2025** (Consolidado) → R$ 2,49 mi.

São exercícios diferentes, não versões do mesmo arquivo.

---

## 3. O que isso muda

### Anexo 1 de 2024 — completo

Com o balancete, a linha da despesa não executada deixa de ser zero:

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| Vencimentos | 5.749.015.716 | 5.727.095.552 | **+0,38%** |
| Obrigações Patronais | 2.091.575.530 | 2.086.640.220 | +0,24% |
| Aposentadorias | 4.497.126.235 | 4.563.063.879 | −1,45% |
| Pensões | 736.055.738 | 803.877.242 | −8,44% |
| Terceirização | 173.104.090 | 173.463.616 | −0,21% |
| **Não Executada** | **454.943.101** | **454.943.101** | **0,00%** ✅ |
| **Despesa Bruta (I)** | **13.701.820.410** | **13.809.083.610** | **−0,78%** |
| Vinculados | 3.119.978.565 | 3.121.824.884 | −0,06% |

A bruta saiu de −4,07% (sem classe 8) para **−0,78%** (com o balancete).

### Anexo 4 de 2025 — agora com o valor certo

O comparativo consolidado de 2025 dá **R$ 2.491.012,67** de operações de
crédito, que é o valor que o RREO Anexo 9 declara. O arquivo de 2024 dava
R$ 429,2 mi — que é a operação daquele exercício.

---

## 4. O que ainda falta

| item | situação |
|---|---|
| **Balancete de 2025** | o recebido é de 2024 (não executada 454,9). Para 2025 o valor é outro (≈168,8 mi) |
| **Comparativo de 2026** | para fechar 2026 Q1/Q2 |
| **`ending_balance`** | o balancete supre em parte (saldo anterior e final por conta) |

O balancete é a peça que faltava: ele traz **todas as classes**, inclusive a 8,
e os saldos de abertura e encerramento. Para 2025, basta o balancete daquele
exercício.

---

## 5. Conclusão

| arquivo | cobre | não cobre |
|---|---|---|
| Balancete Consolidado | classe 8 ✅, disponibilidade por fonte ✅, saldos ✅ | exercício 2025 |
| Comparativo (1) | operações de crédito de 2025 ✅, receita consolidada ✅ | exercício 2026 |
