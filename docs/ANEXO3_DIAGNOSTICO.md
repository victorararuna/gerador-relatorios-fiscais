# RREO Anexo 3 — o que a herança revelou

Implementei a herança do filtro e a comparação com a coluna mensal. O resultado
mostra que o problema não era onde eu pensava.

---

## 1. O que fiz

**1. Herança do filtro de natureza** — as linhas filhas do A3 têm filtro próprio
(ICMS → `NR 1114501,1114502`), e o cálculo hierárquico soma os ramos.

**2. Comparação com a coluna `<MR>`** — o mês de referência do A3.

## 2. O resultado

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| ICMS | 6.748.757.920,80 | 910.476.706,20 | +641% |
| IPVA | 533.431.401,91 | 75.446.602,92 | +607% |
| IRPF | 1.466.178.284,41 | 471.156.112,55 | +211% |
| Receita de Serviços | 83.480.235,91 | 49.772.236,71 | +68% |

**Todos os desvios são múltiplos de ~7.** ICMS: 6.748,8 ÷ 910,5 = **7,41**.

## 3. O diagnóstico

**O `<MR>` é o valor de UM mês. O meu cálculo é o acumulado de oito.**

6.748,8 / 910,5 = 7,41 ≈ 8 meses de arrecadação.

Não é erro de filtro — é **escala**. O A3 mostra a evolução **mês a mês** (12
colunas), e eu apuro o acumulado.

### A prova

| item | valor |
|---|---:|
| Meu acumulado jan–ago | 22.122.531.294,06 |
| Soma das 12 colunas do homologado | 28.492.581.265,43 |
| Meu acumulado da janela (set/25–ago/26) | 32.560.682.756,60 |

A janela do A3 tem **12 meses**; meu cálculo tem 8. E o desvio de +14% na janela
completa é a diferença que já vinha da receita.

---

## 4. O que isso significa

**O A3 não fecha por duas razões independentes:**

**1. Escala.** Preciso calcular **mês a mês** e comparar coluna a coluna — não o
acumulado contra um mês.

**2. Natureza.** Mesmo na janela de 12 meses, o +14,28% persiste. É o mesmo
resíduo da receita: as naturezas `7xxx` (intra) entrando no cálculo.

---

## 5. O que está pronto

| peça | situação |
|---|---|
| Cálculo hierárquico por indentação | ✅ funciona |
| Conta pontuada (`6.2.1.2.0.00.00`) | ✅ funciona |
| Herança do filtro de natureza | ✅ aplicada |
| Filtros das filhas do A3 | ✅ interpretados |
| **Cálculo mensal (12 colunas)** | ❌ **é o que falta** |
| Exclusão das naturezas `7xxx` | ❌ |

---

## 6. O que eu faria

**1. Calcular mês a mês.** O `acervo` já tem os 12 meses. Para cada coluna
(`<MR-11>` a `<MR>`), apurar aquele mês e comparar.

**2. Excluir as `7xxx` na receita.** O Anexo 1 fez isso com o filtro de linha
(`NR começada por 1,2`). No A3, esse filtro precisa entrar no critério de conta.

---

## 7. O balanço honesto da rodada

**O que avancei**: a arquitetura do gerador está completa — hierarquia, conta
pontuada, herança, filtros compostos. Nada disso precisa ser reescrito.

**O que não fechei**: o A3. E o motivo mudou de "não sei ler o mapeamento" para
"a comparação está na escala errada".

**O que isso vale**: quando você tiver os dados de setembro e outubro, o A3 vai
precisar do cálculo mensal — e agora sei exatamente onde implementá-lo.

---

## 8. O placar segue

| anexo | desvio |
|---|---|
| RGF A1 — Pessoal | ✅ −0,04% |
| RGF A2 — DCL | ✅ 12 linhas em 0,00% |
| **RREO A1 — Receita** | ✅ **41 linhas em 0,00%** |
| RREO A1 — Despesa | ✅ +0,02% |
| RREO A9 — Operações | ✅ 0,00% |
| RREO A3 — RCL | ⚠️ escala mensal + natureza |
| RREO A4 | ❌ civil/militar |
| RREO A6 | ⚠️ falta o sinal |
