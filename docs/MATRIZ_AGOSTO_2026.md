# Os arquivos do SIAFIC — o que entregaram e o que falta

Arquivos recebidos:

- `24EX-2026-08-006.csv` — Matriz de Saldos Contábeis de **agosto/2026**, formato
  antigo (16 colunas), **todas as classes**
- `Relatorio_13112026101605.xls` — Relação Fonte Recurso (MSC × SIGEF)

---

## 1. O que a matriz de agosto trouxe

**62.975 lançamentos**, com **todas as classes**:

| classe | linhas |
|---|---:|
| 1 — Ativo | 1.961 |
| 2 — Passivo | 2.583 |
| 3 — Variações diminutivas | 1.741 |
| 4 — Variações aumentativas | 446 |
| **5 — Controles da receita** | **17.324** |
| 6 — Controles da despesa | 35.454 |
| 7 — Controles devedores | 1.109 |
| **8 — Controles credores** | **2.357** |

**É o acervo completo** — inclusive a classe 5 (receita) e a 8 (controles), que
faltavam. E os três tipos de saldo (`beginning_balance`, `period_change`,
`ending_balance`).

Atributos presentes: `PO`, `FR`, `CO`, `ND`, `NR`, `AI`, `FS`, `FP`, `DC`.

---

## 2. Dois bugs que isso revelou

### 2.1 O delimitador do CSV

O `Acervo.ler` usava `csv.DictReader(fh)` sem delimitador — o padrão é `,`.

Os arquivos normalizados usam `,`. O convertido do formato antigo usa `;`.
Resultado: **todas as contas vinham vazias** para agosto.

Corrigido com detecção pelo cabeçalho:

```python
cabecalho = fh.readline()
delim = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
fh.seek(0)
rd = csv.DictReader(fh, delimiter=delim)
```

### 2.2 O conversor do formato antigo

Criei o `converter_msc.py`, que traduz as 16 colunas do formato antigo
(`CONTA;IC1;TIPO1;...`) para as 21 do formato longo. Os atributos vêm em pares
(valor, tipo) e a posição varia — o conversor mapeia por tipo (PO, FR, CO, ND,
NR, AI).

Resultado: **62.975 linhas convertidas, 0 descartadas**, em 24 arquivos (8
classes × 3 tipos de saldo).

---

## 3. O que deu para apurar

### 2026 Q1 — janela completa (12 meses)

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| **Despesa Bruta** | 15.875.707.077 | 15.925.794.076 | **−0,31%** |
| Vencimentos | 6.939.371.638 | 6.926.091.326 | +0,19% |
| Aposentadorias | 5.389.511.531 | 5.391.390.194 | −0,03% |
| Terceirização | 206.992.307 | 206.992.307 | **0,00%** |
| Vinculados | 3.644.048.430 | 3.637.723.790 | +0,17% |

### 2026 Q2 — 11 de 12 meses

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| Despesa Bruta | 14.843.285.976 | 16.113.277.246 | **−7,88%** |
| Vencimentos | 6.530.880.724 | 7.014.607.987 | −6,90% |
| Aposentadorias | 5.002.640.569 | 5.444.934.753 | −8,12% |

**Os −7,88% são exatamente 1 mês de 12** (8,3%). O motor está correto; falta
**julho/2026**.

---

## 4. O que falta

| item | para quê |
|---|---|
| **MSC de julho/2026** | fechar a janela do Q2 (11 → 12 meses) |
| **MSC de setembro e outubro** | o fechamento do dia 16 |
| **Balancete de 2026** | despesa não executada (classe 8) |

Com julho, o Q2 deve fechar na mesma faixa do Q1 (−0,3%).

---

## 5. O que a matriz completa destrava

Com as classes 1, 2, 5, 8 que agora existem:

| Anexo | Antes | Agora |
|---|---|---|
| RGF A2 — DCL | ❌ classe 2 | ⚠️ falta o de-para |
| RGF A3 — Garantias | ❌ classe 2 | ⚠️ falta o de-para |
| RGF A5 — Disponibilidade | ❌ classe 8 | ⚠️ falta o de-para FR |
| RREO A1 — receita | ❌ classe 5 | ⚠️ falta o de-para |
| RREO A3 — RCL | ❌ classe 5 | ⚠️ falta o de-para |

**A matéria-prima chegou.** O que falta agora é o **de-para de contas** — qual
conta vai em qual linha de cada anexo.

---

## 6. A Relação Fonte Recurso

O `Relatorio_13112026101605.xls` traz 377 linhas mapeando **Fonte Recurso MSC ×
Fonte Recurso SIGEF**. É uma peça do de-para do **Anexo 5** (disponibilidade por
fonte) — liga a FR da matriz à classificação do SIGEF.

Vou analisá-la quando atacar o Anexo 5.

---

## 7. Resumo

| Pergunta | Resposta |
|---|---|
| A matriz de agosto serve? | **Sim** — todas as classes, 62.975 lançamentos |
| O que ela revelou? | Dois bugs (delimitador e conversor) — corrigidos |
| O Q1 fecha? | **−0,31%** |
| O Q2 fecha? | **Falta julho** (11 de 12 meses, −7,88% = 1 mês) |
| O que falta para o dia 16? | Julho, setembro, outubro |
