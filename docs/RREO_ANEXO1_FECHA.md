# RREO — o Anexo 1 fecha

> **Documento histórico.** Escrito quando o trabalho era sobre o **RGF 2024**.
> Os números e as pendências abaixo **não valem mais**: o Anexo 1 passou a fechar
> em 10 de 10 meses, o Anexo 5 chegou a 90 de 90 células e o Anexo 4 fechou.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2** —
> ou, melhor, abra `saida/verificacao_anexos.xlsx`, que é gerado do código.

---


A conta que reproduz a despesa liquidada do RREO Anexo 1 é a **`622130400`** —
crédito empenhado liquidado a pagar.

---

## 1. O resultado

**RREO Anexo 1 — 2026 B4 (julho-agosto):**

| item | MSC | Homologado | desvio |
|---|---:|---:|---:|
| **Despesa liquidada até o bimestre** | 16.016.351.029,35 | 16.013.488.241,73 | **+0,02%** |

**+2,9 milhões em R$ 16 bilhões.**

---

## 2. A conta que não servia

Eu vinha usando a `622920103` — "despesa liquidada total" — que dava **+4,88%**.

A diferença está no que ela inclui:

| conta | valor | o que é |
|---|---:|---|
| `622130400` | 16.016.351.029 | **crédito empenhado liquidado a pagar** |
| `622920103` | 16.795.005.664 | despesa liquidada total |
| diferença | **778.654.635** | |

A `622920103` soma também o que já foi **pago** no mesmo movimento — daí os
R$ 778,7 mi a mais.

A `622130300` (crédito empenhado a liquidar) dá 778,6 mi — é exatamente a
diferença. Ou seja: a `622920103` = `622130400` + `622130300`.

**La liquidada do RREO é só a `622130400`.**

---

## 3. O que isso muda

| relatório | antes | agora |
|---|---|---|
| RGF Anexo 1 | −0,04% | −0,04% |
| **RREO Anexo 1 (despesa)** | **+4,88%** | **+0,02%** |

**Os dois anexos principais agora fecham.**

---

## 4. O que ainda falta no RREO

### 4.1 A receita

O RREO A1 tem duas metades: receita e despesa. A **despesa fecha**; a **receita
não**.

O problema é duplo:

1. **A classe 5 só existe para julho e agosto** neste acervo. O RREO B4 é
   acumulado jan-ago — faltam 6 meses.
2. **As contas de controle da receita têm sinal negativo e não batem** com o
   valor do bimestre. A `522990000` dá −6,69 bi contra 3,92 bi do homologado.

Para a receita, o caminho é o **Comparativo da Receita Orçada com a Arrecadada** —
que já sabemos ler (é de lá que saiu a operação de crédito de R$ 2,49 mi).

### 4.2 O Anexo 2 — despesa por função

A MSC antiga **não traz o atributo `funcao`**. O formato novo traz; o de 16
colunas, não.

Sem ele, o Anexo 2 não é reproduzível da matriz.

### 4.3 Os demais

| anexo | depende de |
|---|---|
| A3 — RCL | classe 5 (receita) |
| A4 — Previdenciário | classe 5 + separar civil/militar |
| A6 — Resultado Primário | classe 5 |
| A7 — Restos a Pagar | `ano_inscricao` preenchido |
| A9 — Operações | ✅ **já fecha** (comparativo) |
| A11 — Alienação | classe 5 |
| A14 — Simplificado | soma dos demais |

---

## 5. O que temos hoje

| anexo | situação |
|---|---|
| **RGF A1 — Pessoal** | ✅ **−0,04%** |
| **RREO A1 — Despesa liquidada** | ✅ **+0,02%** |
| **RREO A9 — Operações** | ✅ **0,00%** |
| RREO A1 — Receita | ❌ classe 5 incompleta |
| RGF A2 a A6 | ❌ de-para de linhas |
| RREO A2, A3, A4, A6, A7, A11, A14 | ❌ |

**Três anexos fecham.** E os dois principais — pessoal e despesa — estão abaixo
de 0,05%.

---

## 6. O caminho para os outros

### Para a receita (A1-receita, A3, A6, A11)

O **Comparativo da Receita** tem a receita realizada por rubrica. É a mesma fonte
que deu a operação de crédito. Falta o de-para das rubricas para as linhas do
RREO.

### Para o Anexo 2

O atributo `funcao`. A matriz de 16 colunas não tem; a de formato longo tem.
Se o SIAFIC exportar a matriz incluindo a função, o Anexo 2 sai.

### Para os Anexos 2 e 5 do RGF

A **Relação Plano Contas MSC × SIGEF** (12.609 contas) que você mandou é o
começo. Falta o de-para de **linhas**.

---

## 7. Resumo

**O RREO Anexo 1 agora fecha em +0,02%.**

A descoberta foi simples: a conta de controle certa é a `622130400`, não a
`622920103`. A diferença entre as duas (R$ 778,7 mi) é o que já foi pago — que o
RREO não inclui na liquidada.

Com isso, os dois relatórios principais da LRF — despesa com pessoal (RGF) e
execução orçamentária (RREO) — reproduzem o homologado com desvio abaixo de
0,05%.
