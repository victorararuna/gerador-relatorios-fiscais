# O de-para chegou — o que ele muda

Os dois ZIPs trouxeram os **mapeamentos oficiais da STN** para o MDF 15ª edição,
calibrados para a MSC 2026.

---

## 1. O que veio

### RGF — Parte IV

| arquivo | linhas |
|---|---:|
| Anexo 1 — Despesas com Pessoal | 65 |
| Anexo 2 — Dívida Consolidada Líquida | 61 |
| Anexo 3 — Garantias e Contragarantias | 41 |
| Anexo 4 — Operações de Crédito | 46 |
| Anexo 5 — Disponibilidade e Restos a Pagar | 41 |

### RREO — Parte III

| arquivo | linhas |
|---|---:|
| Anexo 01 — Balanço Orçamentário | 192 |
| Anexo 02 — Função/Subfunção | 405 |
| Anexo 03 — RCL | 45 |
| Anexo 04 — Previdenciárias | 109 |
| Anexo 06 — Resultado Primário e Nominal | 102 |
| Anexo 07 — Restos a Pagar | 36 |
| **Anexo 08 — MDE** | — |
| Anexo 09 — Operações e Despesa de Capital | 23 |
| Anexo 11 — Alienação de Ativos | 26 |
| **Anexo 12 — ASPS** | 125 |
| Anexo 13 — PPP | 41 |

**Inclusive os Anexos 8 e 12** — que eu tinha documentado como "fora do Siconfi,
vão para SIOPE e SIOPS". Eles **têm mapeamento oficial** para a MSC.

---

## 2. A estrutura

Cada arquivo tem, por aba (Estados / Municípios / DF):

| coluna | conteúdo |
|---|---|
| 1 | **ESPECIFICAÇÃO** — o rótulo da linha do anexo |
| 2 | **FILTROS SICONFI** — o filtro em linguagem natural |
| 3 | **Critérios** — as contas contábeis |

Exemplo (RREO Anexo 1):

```
RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I) | NR começada por 1,2 EXCETO NR (Lista): 211102,211255
RECEITAS CORRENTES                        | NR começada com (Lista): 1
IMPOSTOS, TAXAS E CONTRIBUIÇÕES           | NR começada com (Lista): 11
Impostos                                  | NR começada por 111
Taxas                                     | NR começada por 112
```

**É exatamente o de-para que faltava** — linha do anexo ↔ filtro sobre a matriz.

---

## 3. O que já foi construído

### `app/mapeamento.py`

Lê os 15 arquivos e devolve, por anexo, a lista de linhas com especificação,
filtro e critério.

### `app/filtros.py`

Interpreta as expressões:

```
"NR começada por 1,2 EXCETO NR (Lista): 211102,211255"
  → prefixos: nr começa com 1 ou 2
  → exceto:   nr 211102, 211255
```

Testado em cinco expressões — todas interpretadas corretamente.

---

## 4. O obstáculo que apareceu

Apliquei o filtro do Anexo 1 na classe 5 (jul+ago):

| item | valor |
|---|---:|
| filtro "receitas exceto intra" aplicado | −356.601.505 |
| RREO A1 no bimestre | 3.924.645.278 |
| desvio | −109% |

**A leitura da receita na MSC não é o líquido dos controles.**

A estrutura da classe 5:

| conta | crédito | débito |
|---|---:|---:|
| `522990000` | 1.115.995.862 | 7.802.036.574 |
| `522920101` | 85.166.749 | 2.595.333.815 |
| `522920102` | 0 | 2.596.453.265 |

A receita realizada **não é** o líquido (crédito − débito), nem o crédito, nem o
débito isolado de uma conta. É uma combinação que o mapeamento ainda precisa
esclarecer — os critérios da coluna 3 do Anexo 3 (RCL) citam:

```
6.2.1.2.0.00.00 RECEITA REALIZADA + (-) 6.2.1.3.2.00.00 RENÚNCIA + ...
```

Ou seja: a receita é apurada por **fórmula sobre contas** (soma e subtração de
contas específicas), não por um filtro simples.

---

## 5. O que isso significa

### O que ficou resolvido

| item | situação |
|---|---|
| De-para de linhas | ✅ **chegou** |
| Interpretador de filtros | ✅ **funciona** |
| RGF A1 | ✅ −0,04% |
| RREO A1 despesa | ✅ +0,02% |
| RREO A9 | ✅ 0,00% |

### O que ficou pendente

**A receita** — o de-para existe, mas a apuração é por fórmula de contas, não por
filtro de NR. E a classe 5 só tem julho e agosto neste acervo.

**Os Anexos 2 e 5 do RGF** — o de-para existe; falta aplicá-lo (é a próxima
etapa natural).

---

## 6. O caminho a partir daqui

Os mapeamentos transformam o projeto de "calibração por tentativa" em
**aplicação de regra oficial**. Cada linha do anexo tem um filtro declarado pela
STN.

A ordem de ataque:

| prioridade | anexo | por quê |
|---|---|---|
| 1 | **RGF A2 — DCL** | de-para existe, dados na classe 2 |
| 2 | **RGF A5 — Disponibilidade** | de-para existe, FR mapeada |
| 3 | **RREO A3 — RCL** | depende da fórmula de receita |
| 4 | RREO A2 — Função | precisa do atributo `funcao` |
| 5 | RREO A7 — Restos a Pagar | precisa de `ano_inscricao` |

---

## 7. Resumo

**Os mapeamentos são a peça que faltava.** Eles dizem, linha a linha, o que cada
anexo espera.

O que trava agora não é mais "não sei o de-para" — é **como a receita é apurada**
(fórmula de contas) e **a cobertura da classe 5** (só julho e agosto).

Para os Anexos 2 e 5 do RGF, o caminho está aberto: o de-para existe e os dados
estão na matriz.
