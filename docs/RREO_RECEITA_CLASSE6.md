# RREO — a receita está na classe 6, não na 5

> **Documento histórico.** Escrito quando o trabalho era sobre o **RGF 2024**.
> Os números e as pendências abaixo **não valem mais**: o Anexo 1 passou a fechar
> em 10 de 10 meses, o Anexo 5 chegou a 90 de 90 células e o Anexo 4 fechou.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2** —
> ou, melhor, abra `saida/verificacao_anexos.xlsx`, que é gerado do código.

---


Aplicação do mapeamento do Anexo 1 na MSC. Um erro meu de premissa e o que ele
revelou.

---

## 1. O erro

Eu vinha lendo a **receita na classe 5** (controles orçamentários da receita).
Por isso ela nunca fechava — dava −109%.

**O mapeamento do Anexo 1 diz outra coisa:**

```
RECEITAS REALIZADAS (b)
  CC começada por LISTA: 6212,6213
  SEM MÊS
  PERIOD_CHANGE MOVIMENTAÇÃO
  SEM D/C
  6.2.1.2.0.00.00 RECEITA REALIZADA
  + 6.2.1.3.0.00.00 (-) DEDUÇÕES DA RECEITA ORÇAMENTÁRIA
```

**A receita realizada está nas contas `6.2.1.2` e `6.2.1.3` — classe 6.**

A classe 5 serve a **outra coisa**: previsão inicial (`5.2.1.1`) e alteração da
previsão (`5.2.1.2`).

---

## 2. Os números

Aplicando os critérios na classe 6:

| critério | jul+ago | desvio | jan-ago | desvio |
|---|---:|---:|---:|---:|
| `6212` | 5.499.745.777 | +40,13% | 22.122.531.294 | +38,15% |
| `6212` + `6213` | 4.414.322.015 | +12,48% | 17.875.134.904 | +11,63% |
| `6212` − `6213` | 6.585.169.540 | +67,79% | 26.369.927.684 | +64,68% |
| **homologado** | **3.924.645.278** | — | **16.012.885.982** | — |

**O `6212 + 6213` é o mais próximo (+12,5%)** — e é a leitura literal da fórmula
(`+ (-)`).

---

## 3. O que sobra

A diferença de R$ 1,58 bi no bimestre.

As maiores naturezas dentro do `6212` (jul+ago):

| NR | valor |
|---|---:|
| 11145011 — ICMS | 1.796.564.548 |
| 17115001 | 1.266.983.139 |
| 11130311 | 562.463.305 |
| 72150211 | 296.070.744 |
| 17515001 | 264.464.101 |
| 19999921 | 207.929.515 |
| 72155011 | 170.940.498 |

**Os prefixos `7xxx`** (72150211, 72155011) são intra-orçamentários pela
natureza. E o mapeamento exclui NRs específicas — mas não todas as `7xxx`.

**Hipótese**: o filtro `NR começada por 1,2` da linha "Receitas (exceto intra)"
(I) deveria ser aplicado **também** ao cálculo da receita realizada. Se sim, as
`7xxx` saem.

Teste rápido:

```
72150211: 296.070.744
72155011: 170.940.498
soma:      467.011.242
```

Retirando: 4.414.322.015 − 467.011.242 = **3.947.310.773** — contra 3.924.645.278
do homologado. **+0,58%**.

**É a explicação.** A receita realizada é `6212 + 6213` **filtrando as NRs da
linha** (começadas por 1 ou 2).

---

## 4. O que já está validado no RREO

| anexo | situação |
|---|---|
| **RREO A1 — Despesa** | ✅ **+0,02%** |
| **RREO A9 — Operações** | ✅ **0,00%** |
| RREO A1 — Receita | ⚠️ +0,58% com o filtro composto (falta aplicar) |

---

## 5. O que falta aplicar

O `aplicar_mapeamento` do RREO precisa combinar **dois critérios**:

1. O **filtro de contas** da coluna `RECEITAS REALIZADAS (b)` — `6212,6213`;
2. O **filtro de NR** da linha — `começada por 1,2 EXCETO ...`.

O `filtros2.py` já interpreta os dois separadamente. Falta o gerador que os
combina: **conta começa com X E natureza começa com Y**.

---

## 6. Resumo da rodada

**O que descobri**: a receita do RREO não está na classe 5 — está na classe 6,
nas contas `6.2.1.2` (realizada) e `6.2.1.3` (deduções).

**O que testei**: três combinações, com os desvios acima.

**O que falta**: combinar o filtro de conta com o filtro de natureza. Com os dois,
a receita vai a +0,58%.

**O que já fecha**: RGF A1 (−0,04%), RGF A2 (12 linhas em 0,00%), RREO A1 despesa
(+0,02%) e RREO A9 (0,00%).
