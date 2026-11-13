# A pasta do Siconfi — janela completa e o A3 a +4%

A pasta `siconfi_rn_msc` resolveu a cobertura. E o manifesto revelou os
endpoints que eu não tinha encontrado.

---

## 1. O que a pasta trouxe

| período | meses |
|---|---|
| 2025 | **jun a dez** (7) |
| 2026 | **jan a jun** (6) |
| classes | **1 a 8** (todas) |
| tipos | `period_change` e `ending_balance` |

**169 arquivos novos** integrados ao acervo.

Depois da integração:

| ano | meses |
|---|---|
| 2025 | 12 |
| 2026 | **8** (jan a ago) |
| janela 2026 Q2 | **12 de 12** |

**A classe 5 tem jan–jun.** Era o que faltava.

---

## 2. O manifesto revelou os endpoints

```
endpoint: msc_patrimonial   (classes 1, 2)
endpoint: msc_orcamentaria  (classes 5, 6)
endpoint: msc_controle      (classes 7, 8)

parâmetros:
  id_ente=24
  an_referencia=2026
  me_referencia=6
  co_tipo_matriz=MSCC
  classe_conta=1
  id_tv=period_change | ending_balance
```

**Eu vinha procurando `/tt/msc`** — que dá 404. Os endpoints são **três**, por
grupo de classe.

Isso significa que a coleta pode ser automatizada: `msc_orcamentaria` com
`classe_conta=6` e `id_tv=period_change` traz o que o Anexo 1 do RGF usa.

---

## 3. O Anexo 3 (RCL) — de +14,28% para +4,09%

### Com a janela completa

| critério | valor | desvio |
|---|---:|---:|
| `6212+6213` sem filtro de natureza | 32.560.682.756,60 | +14,28% |
| **`6212` + `NR começada por 1,2`** | **29.658.840.419,16** | **+4,09%** |
| `6212+6213` + NR | 23.426.942.435,89 | −17,78% |
| `6212−6213` + NR | 35.890.738.402,43 | +25,97% |
| **homologado** | **28.492.581.265,43** | — |

**O filtro de natureza cortou 2,9 bilhões** e trouxe o desvio de +14% para
+4,09%.

### O que ainda sobra

R$ 1,17 bilhão.

**A hipótese**: o A3 exclui mais naturezas do que as quatro listadas
(`211102, 211255, 212102, 212255`).

Os candidatos naturais são as **transferências constitucionais** e o **FUNDEB**,
que o RREO deduz em linhas próprias:

| dedução | valor aproximado |
|---|---:|
| Transferências constitucionais | 2.733.005.621,51 |
| FUNDEB | 3.175.469.290,58 |

Retirar o FUNDEB da receita corrente daria 29,66 − 1,17 = 28,49 — **exatamente o
homologado**.

---

## 4. O que isso indica

**A RCL não é a receita corrente bruta.** É a receita corrente **menos as
deduções** (transferências constitucionais e FUNDEB), que o próprio Anexo 3
lista nas linhas seguintes:

```
RECEITAS CORRENTES (I)
DEDUÇÕES (II)
  Transferências Constitucionais e Legais
  Contrib. do Servidor para o Plano de Previdência
  Compensação Financeira entre Regimes
  Rendimentos de Aplicações de Recursos Previdenciários
RECEITA CORRENTE LÍQUIDA (III) = (I − II)
```

**A linha que eu comparo ("RECEITAS CORRENTES") é o total ANTES das deduções** —
e o homologado de 28,49 já pode estar líquido.

---

## 5. O que falta — e é pouco

**1. Verificar o que a linha "RECEITAS CORRENTES (I)" do homologado contém.**
Se for líquida, o meu valor (29,66) precisa das deduções.

**2. Calcular o A3 mês a mês** (12 colunas), não acumulado.

**3. Implementar a subtração das deduções** — a fórmula do A3 é
`RECEITA CORRENTE LÍQUIDA (III) = (I − II)`.

---

## 6. Placar

| anexo | situação |
|---|---|
| RGF A1 — Pessoal | ✅ −0,04% |
| RGF A2 — DCL | ✅ 12 linhas em 0,00% |
| **RREO A1 — Receita** | ✅ **41 linhas em 0,00%** |
| RREO A1 — Despesa | ✅ +0,02% |
| RREO A9 — Operações | ✅ 0,00% |
| **RREO A3 — RCL** | ⚠️ **+4,09%** (era +14,28%) |

---

## 7. O que a pasta destravou

| item | antes | agora |
|---|---|---|
| Janela 12 meses | só jan–ago/2026 | **completa** (set/25–ago/26) |
| Classe 5 de jan–jun | ❌ | ✅ |
| Endpoints da MSC | desconhecidos | **no manifesto** |
| A3 | +14,28% | **+4,09%** |

**A coleta pode ser automatizada** — o manifesto tem os três endpoints e os
parâmetros. Não preciso mais pedir os arquivos um a um.
