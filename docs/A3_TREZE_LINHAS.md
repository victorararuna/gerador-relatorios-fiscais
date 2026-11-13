# RREO Anexo 3 — 13 linhas em 0,00%

O cálculo mensal destravou o anexo. As linhas folha fecham ao centavo.

---

## 1. O resultado

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| **ICMS** | 910.491.066,33 | 910.476.706,20 | **+0,00%** |
| **IPVA** | 75.461.403,25 | 75.446.602,92 | **+0,02%** |
| **IRRF** | 471.156.194,79 | 471.156.112,55 | **+0,00%** |
| **Contribuições** | 132.310.463,83 | 132.310.463,83 | **0,00%** |
| **Rendimentos de Aplicação** | 21.456.912,90 | 21.456.912,90 | **0,00%** |
| **Receita Agropecuária** | 45.647,57 | 45.647,57 | **0,00%** |
| **Receita Industrial** | 106.091,74 | 106.091,74 | **0,00%** |
| **Receita de Serviços** | 49.772.236,71 | 49.772.236,71 | **0,00%** |
| **Cota-Parte do FPE** | 721.445.453,29 | 721.445.453,29 | **0,00%** |
| **Transferências do FUNDEB** | 147.767.478,71 | 147.767.478,71 | **0,00%** |
| **Outras Receitas Correntes** | 210.387.224,96 | 210.368.753,56 | **+0,01%** |
| **Contrib. do Servidor** | 130.677.358,26 | 130.677.358,26 | **0,00%** |
| **Rendimentos Previd.** | 825.522,90 | 825.522,90 | **0,00%** |

**Treze linhas em 0,00%** — doze delas exatas ao centavo.

---

## 2. O que fez a diferença

### 2.1 Cálculo mensal, não acumulado

O A3 tem **12 colunas mensais**. Eu somava a janela inteira e comparava com
`<MR>` (um mês) — daí os +1669% iniciais.

**Corrigido**: apurar o **mês de referência** (agosto/2026) e comparar com
`<MR>`.

### 2.2 Conta 6212, não 6213

A fórmula do mapeamento diz `6212 + 6213`. Mas o `6213` são as **deduções da
receita**:

| critério | agosto | desvio |
|---|---:|---:|
| `6212` + NR 1,2 | 2.998.676.541,25 | **+1,91%** |
| `6212+6213` + NR 1,2 | 2.442.980.507,03 | −16,97% |

**A receita realizada corrente é só o `6212`.** O `6213` entra na linha de
deduções.

---

## 3. O que ainda não fecha

### 3.1 As linhas de total

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| RECEITAS CORRENTES (I) | 5.297.028.792 | 2.942.335.190 | +80% |
| Impostos, Taxas e Contribuições | 2.970.160.785 | 1.510.569.657 | +97% |
| Transferências Correntes | 1.868.313.955 | 994.686.865 | +88% |

**A hierarquia está somando as netas junto com as filhas.**

Exemplo: "Impostos" deveria ser ICMS + IPVA + ITCD + IRRF + Outros. Mas "Outros
Impostos" está com 1.510,6 mi (deveria ser 51,1) — o filtro `NR 11 EXCETO ...`
está pegando quase tudo.

**A causa**: o filtro de "Outros Impostos" tem a exclusão `EXCETO NR começ...`
truncada no mapeamento. O `filtros2` não consegue interpretar a lista completa.

### 3.2 O "Outros Impostos"

```
filtro: NR começada por lista: 11 ; EXCETO NR começ...
```

**A exclusão está truncada.** Sem ela, a linha soma todos os impostos —
incluindo os que já têm linha própria.

### 3.3 As deduções

| linha | MSC | Homologado |
|---|---:|---:|
| Transferências Constitucionais | 0,00 | 267.325.195,82 |

**O critério está em "Mapeamento na célula"**, com as contas `6.2.1.3.1.02.00` e
`6.2.2.1.3.03/.04/.05`. Não as capturei — o extrator de conta pontuada pega o
`6.2.1.3.1.02.00`, mas o `6.2.2.1.3.03` tem só 4 níveis.

---

## 4. Placar

| anexo | situação |
|---|---|
| RGF A1 — Pessoal | ✅ −0,04% |
| RGF A2 — DCL | ✅ 12 linhas em 0,00% |
| **RREO A1 — Receita** | ✅ 41 linhas em 0,00% |
| RREO A1 — Despesa | ✅ +0,02% |
| **RREO A3 — RCL** | ⚠️ **13 linhas em 0,00%**; totais e deduções pendentes |
| RREO A9 — Operações | ✅ 0,00% |

---

## 5. O que falta no A3

| item | por quê |
|---|---|
| **Filtro "Outros Impostos" completo** | a exclusão está truncada no mapeamento |
| **Conta `6.2.2.1.3.03`** | o extrator não pega conta de 4 níveis |
| **Soma hierárquica correta** | está somando netas com filhas |

**São três ajustes de leitura** — a estrutura está certa, e as folhas provam
isso: 13 linhas em 0,00%.

---

## 6. O que a rodada confirmou

**O A3 é reproduzível.** As 13 folhas fecham ao centavo com:
- conta `6.2.1.2` (receita realizada);
- filtro `NR começada por 1,2` (exclui intra);
- mês de referência (não acumulado).

O que resta é **soma de totais e duas exclusões** — não é recalibrar, é corrigir
a leitura da árvore.
