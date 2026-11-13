# RREO Anexos 4, 5 e 6 — o que avançou

Persistência pedida. Abaixo o estado de cada um, sem maquiar o que não fechou.

---

## 1. O Anexo 5 não existe

O RREO vai do **4 para o 6**. O mapeamento da STN tem: 01, 02, 03, 04, 06, 07,
08, 09, 11, 12 e 13.

**Não há Anexo 5.** A numeração salta porque o antigo Anexo 5 ("Resultado
Nominal") foi incorporado ao 6, que hoje se chama "Demonstrativo dos Resultados
Primário e Nominal".

Mesma situação do RGF, onde o Anexo 5 existe mas o RREO não tem.

---

## 2. O que construí nesta rodada

### 2.1 Parser de conta pontuada

Os mapeamentos do RREO escrevem a conta no formato do plano:

```
6.2.1.2.0.00.00 RECEITA REALIZADA
```

A MSC guarda no formato compacto: `621200000`. O conversor:

```python
def conta_para_prefixo(conta):
    return conta.replace(".", "")   # 6.2.1.2.0.00.00 -> 621200000
```

**Isso destrava os anexos que usam fórmula de contas** — o 3, o 4 e o 6.

### 2.2 Separador `//` (duas barras)

O Anexo 6 usa `//` como separador de critérios, não `///`:

```
CC começada por (Lista): 5211,5212 // MÊS: 02
```

O `filtros2.py` agora aceita de duas a três barras.

### 2.3 Relação OU entre contas

A fórmula `6.2.1.2.0.00.00 + (-) 6.2.1.3.0.00.00` cita **duas contas**. Elas são
**somadas**, não interseccionadas:

```python
if not any(c.casar(r) for c in fc.condicoes):
    continue   # entra se casar com QUALQUER conta
```

Antes eu usava `all()`, e o resultado era zero para toda linha com mais de uma
conta.

---

## 3. O Anexo 3 (RCL) — avançou, não fechou

### O que funciona

As linhas com filtro de natureza fecham valores plausíveis:

| linha | valor |
|---|---:|
| ICMS | 6.748.757.920,80 |
| IPVA | 533.431.401,91 |
| ITCD | 29.139.635,82 |
| IRRF | 1.466.178.284,41 |
| Cota-Parte do FPE | 5.930.444.454,26 |

### O que não funciona

As linhas com "Resultado de fórmula" ficam **invalidas** e o filtro de conta
(que é o mesmo para todas) pega **tudo**:

| linha | valor | deveria |
|---|---:|---|
| RECEITAS CORRENTES (I) | 22.098.375.496,21 | soma das linhas abaixo |
| Receita Patrimonial | 22.098.375.496,21 | ~168 milhões |

**O problema**: quando o filtro da linha é inválido, o `apurar` não filtra por
natureza e soma todo o critério de conta.

**A correção**: as linhas de total devem ser **calculadas** (somar as linhas
filhas), não apuradas por filtro. O mapeamento diz "Resultado de fórmula" — é
instrução para somar, não para buscar.

---

## 4. O Anexo 6 (Resultado Primário)

### A estrutura

```
LINHA 17:  c4 = 'CC começada por (Lista): 5211,5212 // MÊS: 02'
           c5 = 'CC começada por (Lista): 6212,6213 // MÊS: ...'
LINHA 19:  c5 = '6.2.1.2.0.00.00 RECEITA REALIZADA (+)'
```

**A mesma fórmula do Anexo 1** — receita realizada em `6212 + 6213`.

### O que falta

O Anexo 6 tem **4 abas** (acima da linha, abaixo da linha, resultado nominal,
resultado primário). Cada uma com sua estrutura.

E o cálculo do resultado primário exige **subtrair** despesas de receitas — o
gerador atual só soma. Precisa de um interpretador de fórmula com sinal.

---

## 5. O Anexo 4 (Previdenciário)

### A estrutura

```
LINHA 11:  RECEITAS | No Bimestre | %
LINHA 14:  SUBTOTAL DAS RECEITAS (III) = (I + II)
LINHA 15:  OPERAÇÕES DE CRÉDITO / REFINANCIAMENTO
LINHA 16:  Operações de Crédito - Mercado Interno
```

**Não tem a linha 15 com "Critérios (Contas Contábeis)"** — a estrutura é
diferente dos outros.

E o Anexo 4 exige separar **civil de militar**, atributo que a MSC não tem
(documentado desde a primeira análise).

---

## 6. Placar atualizado

| anexo | situação |
|---|---|
| RGF A1 — Pessoal | ✅ −0,04% |
| RGF A2 — DCL | ✅ 12 linhas em 0,00% |
| **RREO A1 — Receita** | ✅ **41 linhas em 0,00%** |
| RREO A1 — Despesa | ✅ +0,02% |
| RREO A9 — Operações | ✅ 0,00% |
| RREO A3 — RCL | ⚠️ linhas com filtro OK; totais precisam de fórmula |
| RREO A4 — Previdenciário | ❌ estrutura própria + civil/militar |
| RREO A5 | **não existe** |
| RREO A6 — Resultado | ⚠️ mesma fórmula do A1; falta o sinal |

---

## 7. O que a rodada ensinou

**Cada anexo tem uma estrutura de mapeamento diferente.** Já identifiquei quatro:

| tipo | exemplo | como ler |
|---|---|---|
| critério por coluna | A1 receitas | linha 15, coluna a coluna |
| critério por bloco | A1 despesas | linha 104, bloco separado |
| critério único | A3 | linha 18, uma conta para tudo |
| estrutura própria | A4 | sem linha de critérios — layout diferente |

**E há dois tipos de linha**: as que se apuram por filtro e as que se calculam
por fórmula ("Resultado de fórmula"). O gerador atual só trata o primeiro.

---

## 8. O que falta para fechar A3, A4 e A6

**Uma peça**: interpretar "Resultado de fórmula" como instrução de **somar as
linhas filhas** (pela indentação), em vez de buscar na matriz.

Com ela:
- **A3** fecha (as linhas filhas já estão corretas)
- **A6** avança (mesma fórmula do A1)
- **A4** continua travado no civil/militar

É a próxima implementação — e é menor do que parece: a indentação da coluna 1 já
diz quem é filho de quem.
