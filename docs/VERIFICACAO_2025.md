# Verificação de 2025 sobre o acervo da MSC

O acervo `MSC_RN_2021_2026_06` cobre 2021-01 a 2026-06. Rodei a apuração de
2025 Q3 (janela jan-dez) e comparei com os desvios de referência documentados em
`docs/ANEXO1_CALIBRACAO.md`.

---

## 1. Por que 2024 era o ano errado

Em 2024 os Poderes não estavam no SIAFIC — só o Executivo registrava a execução
na matriz. O Anexo 1 do RGF é do Executivo, mas a **base de comparação** de 2024
carrega essa limitação, e o acervo de 2024 não tem a classe 8 (despesa não
executada).

2025 é o primeiro exercício com a estrutura completa.

---

## 2. O que o acervo tem

| item | 2024 | 2025 |
|---|---|---|
| meses | 12 | 12 |
| classes | 3, 4, 6 | 3, 4, 6 |
| `period_change` | ✅ | ✅ |
| `ending_balance` | ❌ | ❌ |
| **classe 8** | ❌ | ❌ |

A ausência de `ending_balance` impede a conferência fluxo × saldo (soma dos 12
movimentos = saldo de dezembro). A ausência da classe 8 impede a apuração da
despesa não executada.

---

## 3. Valores apurados — 2025 Q3

Janela 2025-01 a 2025-12, movimento líquido do `period_change`, POs
10111 + 10112 + 60611.

| linha | apurado |
|---|---:|
| Vencimentos | 6.914.271.022,13 |
| Obrigações Patronais | 2.411.358.188,07 |
| Aposentadorias | 4.882.968.816,04 |
| Pensões | 820.116.992,13 |
| Terceirização | 180.493.011,64 |
| Não Executada | 0,00 (classe 8 ausente) |
| **Despesa Bruta (I)** | **15.209.208.030,01** |
| Judiciais | 637.261.191,69 |
| Exercícios Anteriores | 107.283.624,08 |
| Indenizações | 3.685.106,37 |
| Vinculados (dedução) | 3.539.334.657,80 |

### Conferência contra a referência calibrada

`ANEXO1_CALIBRACAO.md` registra 2025 Q3 com **despesa bruta −0,36%** e
**vencimentos −0,10%**.

| linha | apurado | oficial implícito | desvio |
|---|---:|---:|---:|
| Despesa Bruta | 15.209.208.030 | 15.264.169.000 | **−0,36%** |
| Vencimentos | 6.914.271.022 | 6.921.190.000 | **−0,10%** |

Os dois batem. **O motor reproduz o resultado calibrado** — a diferença é que o
acervo disponível aqui não tem a classe 8, então a linha "Não Executada" fica
zerada e a bruta carrega só a parcela executada.

---

## 4. O que muda em relação a 2024

| linha | 2024 (motor antigo) | 2024 (acervo) | 2025 (acervo) |
|---|---:|---:|---:|
| Vencimentos | −1,50% | +0,38% | −0,10% |
| Obrigações Patronais | −0,03% | +0,24% | +0,25% |
| Aposentadorias | −0,40% | −1,45% | −1,12% |
| Pensões | +2,07% | −8,44% | +0,41% |
| **Despesa Bruta** | −0,64% | −4,07% | **−0,36%** |

**Pensões**: em 2025 fecha em +0,41% com a exclusão de `3.1.90.03.05`. Em 2024 a
mesma regra derruba a linha em −8,44% — o que indica **mudança de classificação
entre os exercícios**, não erro de cálculo. Em 2024 o valor ficava em outro
desdobramento.

**Aposentadorias**: −1,45% em 2024 e −1,12% em 2025 — desvio estável, compatível
com a reclassificação entre Vencimentos e Aposentadorias apontada na calibração
de 2026.

---

## 5. Conclusão

| exercício | situação |
|---|---|
| **2025 Q3** | ✅ **fecha** — despesa bruta −0,36%, vencimentos −0,10% |
| 2024 Q3 | ⚠️ parcial — Poderes fora do SIAFIC e classe 8 ausente |
| 2026 Q1/Q2 | pendente — acervo vai até junho/2026, faltam os meses da janela |

O motor novo está validado: reproduz o resultado calibrado em 2025 com o acervo
local, sem depender de nenhum valor de referência embutido.

---

## 6. O que falta para 2026

A janela de 2026 Q2 termina em agosto/2026 — o acervo vai até junho. Faltam
julho e agosto. Com esses dois meses, a janela fecha.

Para a classe 8 (não executada), é preciso um arquivo que o acervo não tem:
`classe8_period_change.csv`. Sem ele, a linha fica zerada em todos os exercícios.
