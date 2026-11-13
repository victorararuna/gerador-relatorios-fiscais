# RREO — continuação: A3, A4, A6

O que construí e o que cada anexo ainda precisa.

---

## 1. O que ficou pronto

### 1.1 Cálculo hierárquico

O `aplicar_rreo2.py` implementa os dois tipos de linha:

- **apurada por filtro** — conta + natureza, valor sai da MSC;
- **calculada** — "Resultado de fórmula", valor é a soma das linhas **filhas**,
  identificadas pela indentação da coluna 1.

### 1.2 Conta pontuada

`6.2.1.2.0.00.00` → `621200000`. Destrava qualquer anexo que use a fórmula de
contas em vez de prefixo.

### 1.3 Separação `//` e `///`

O Anexo 6 usa duas barras; o Anexo 5 usa três. Aceita as duas.

---

## 2. Anexo 3 (RCL) — a estrutura é mensal

### O que descobri

O A3 **não é acumulado**: tem **12 colunas mensais** (`<MR-11>` a `<MR>`).

| coluna | significado |
|---|---|
| `<MR>` | mês de referência (agosto/2026) |
| `<MR-1>` | julho/2026 |
| … | … |
| `<MR-11>` | setembro/2025 |

**É a janela móvel de 12 meses**, mês a mês.

### O teste

| item | apurado | homologado | desvio |
|---|---:|---:|---:|
| Janela set/25–ago/26 (6212+6213) | 32.560.682.756,60 | 28.492.581.265,43 | **+14,28%** |
| Agosto/2026 | 3.256.150.303,39 | 2.942.335.189,87 | **+10,67%** |

### O que falta

**O mesmo filtro de natureza** que fez a receita do A1 fechar: `NR começada por
1,2 EXCETO ...`.

Aplicando só o critério de conta (6212+6213), entram as naturezas `7xxx`
(intra-orçamentárias). No A1, o filtro de linha as excluiu e o resultado foi
0,00%.

**No A3 esse filtro está na coluna 2 da linha** — mas a linha "RECEITAS
CORRENTES (I)" tem "Resultado de fórmula", então o filtro se perde.

**A correção**: quando a linha é fórmula, herdar o filtro de natureza da linha
pai ou do primeiro filho com filtro válido.

---

## 3. Anexo 6 (Resultado Primário) — estrutura de 4 abas

### A estrutura

| aba | conteúdo |
|---|---|
| Acima da linha | receitas e despesas primárias |
| Abaixo da linha | operações que não afetam o resultado |
| Resultado nominal | variação da dívida |
| Resultado primário | receitas − despesas |

### O que já sei

```
LINHA 17:  CC começada por (Lista): 5211,5212 // MÊS: 02
LINHA 19:  6.2.1.2.0.00.00 RECEITA REALIZADA (+)
```

**A mesma fórmula do A1.** Se a receita do A6 for apurada como no A1 (conta +
natureza), ela fecha.

### O que falta

**Interpretar o sinal.** O resultado primário é `receitas − despesas`. O gerador
atual só soma — precisa de um interpretador que respeite o `(+)` e `(-)` das
fórmulas.

---

## 4. Anexo 4 (Previdenciário) — duas barreiras

### 4.1 Estrutura própria

```
LINHA 11:  RECEITAS | No Bimestre | %
LINHA 14:  SUBTOTAL DAS RECEITAS (III) = (I + II)
```

**Não tem a linha 15 com "Critérios (Contas Contábeis)"** — o layout é diferente
dos outros. O `criterio_conta` não encontra nada.

### 4.2 Civil × militar

O Anexo 4 separa:

- servidores civis × militares;
- RPPS capitalização × repartição.

**A MSC não tem esse atributo.** Está documentado desde a primeira análise e
continua sendo a barreira real.

---

## 5. Placar

| anexo | situação | desvio |
|---|---|---|
| RGF A1 — Pessoal | ✅ | −0,04% |
| RGF A2 — DCL | ✅ | 12 linhas em 0,00% |
| **RREO A1 — Receita** | ✅ | **41 linhas em 0,00%** |
| RREO A1 — Despesa | ✅ | +0,02% |
| RREO A9 — Operações | ✅ | 0,00% |
| RREO A3 — RCL | ⚠️ | +14,28% (falta herdar o filtro de NR) |
| RREO A4 — Previdenciário | ❌ | estrutura + civil/militar |
| RREO A6 — Resultado | ⚠️ | falta interpretar o sinal |
| RREO A5 | **não existe** | — |

---

## 6. A próxima peça

**Herdar o filtro de natureza nas linhas de fórmula.**

Quando uma linha diz "Resultado de fórmula", ela soma os filhos — mas os filhos
também precisam do filtro de natureza da linha pai. Hoje o filtro se perde e as
`7xxx` entram.

Com isso:
- **A3 fecha** (o filtro de NR entra na fórmula da receita)
- **A6 avança** (mesma fórmula do A1)

E depois o **interpretador de sinal** para o resultado primário.

---

## 7. O que a persistência rendeu

Nesta rodada, três peças novas:

1. **Cálculo hierárquico** por indentação — resolve as linhas de total;
2. **Conta pontuada** — destrava A3, A4 e A6;
3. **Separador flexível** (`//` e `///`) — destrava o A6.

E um diagnóstico preciso de por que o A3 ainda não fecha: **o filtro de natureza
se perde nas linhas de fórmula**.

Não é mais "não sei como ler" — é "sei o que falta e onde".
