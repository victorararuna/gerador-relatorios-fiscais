# RREO — o que a MSC já reproduz

> **Documento histórico.** Escrito quando o trabalho era sobre o **RGF 2024**.
> Os números e as pendências abaixo **não valem mais**: o Anexo 1 passou a fechar
> em 10 de 10 meses, o Anexo 5 chegou a 90 de 90 células e o Anexo 4 fechou.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2** —
> ou, melhor, abra `saida/verificacao_anexos.xlsx`, que é gerado do código.

---


Teste feito com 2025 (acervo completo) contra os anexos homologados de 2025 B6.

---

## 1. A descoberta que vale

A conta **`622920103`** — "Despesa liquidada" — totalizou em 2025:

```
23.361.499.529,63
```

E o **RREO Anexo 1 de 2025 B6** declara o total liquidado:

```
23.361.499.529,63
```

**Idêntico ao centavo.**

Isso valida a cadeia de despesa do RREO Anexo 1: a MSC reproduz o total
liquidado sem nenhum ajuste.

---

## 2. O que testei anexo por anexo

| Anexo | Conta testada | MSC | Homologado | Desvio |
|---|---|---:|---:|---:|
| **A1 — despesa liquidada** | `622920103` | 23.361.499.529,63 | 23.361.499.529,63 | **0,00%** ✅ |
| A2 — empenhada por função | `622130400` | 21.945.141.150,86 | 21.209.089.460,89 | **+3,47%** |
| A2 — empenhada por função | `622110000` | 1.696.605.668,71 | 21.209.089.460,89 | −92,00% |
| A7 — restos a pagar | `622920101` | 510.563.239,08 | 487.684.738,08 | +4,69% |
| A9 — operações de crédito | comparativo 4.2.1 | 2.491.012,67 | 2.491.012,67 | **0,00%** ✅ |

### O que cada resultado significa

**A1 — liquidada: fecha.** É o anexo mais importante do RREO, e o total bate.

**A2 — por função: +3,47%.** A conta `622130400` (liquidado a pagar) é a mais
próxima da empenhada, mas não é a mesma coisa. A diferença de R$ 736 mi é a
despesa empenhada e **não liquidada**. Para fechar, é preciso somar
`622130400 + 622920101` e filtrar o que é do exercício — o que exige o
`ano_inscricao`, que a MSC tem mas o acervo não traz preenchido para 2025.

**A7 — restos a pagar: +4,69%.** A conta `622920101` (empenhos a liquidar) chega
perto do saldo a pagar, mas o RREO A7 separa por **ano de inscrição** (exercícios
anteriores × 31/12 do ano). Sem esse atributo, não fecha.

**A9 — operações: fecha.** Já validado.

---

## 3. O que dá para entregar do RREO

| Anexo | Situação | Depende de |
|---|---|---|
| **A1 — Balanço Orçamentário (despesa)** | ✅ total liquidado | classe 6 |
| A1 — receita | ❌ | **classe 5** (ausente no acervo) |
| A2 — Despesa por Função | ⚠️ +3,47% | `ano_inscricao` preenchido |
| A3 — RCL | ❌ | **classe 5** |
| A4 — Previdenciário | ⚠️ | classe 5 + separar civil/militar |
| A6 — Resultado Primário | ⚠️ | classe 5 (receita) |
| A7 — Restos a Pagar | ⚠️ +4,69% | `ano_inscricao` |
| **A9 — Operações de Crédito** | ✅ | comparativo |
| A11 — Alienação | ⚠️ | classe 5 |
| A13 — PPP | ⚠️ | cadastro de contratos |
| A14 — Simplificado | ⚠️ | herda os demais |

**Com o acervo atual (classes 3, 4, 6)**: 2 anexos com certeza (A1-despesa e A9).

**Com a classe 5**: mais quatro (A1-receita, A3, A6, A11).

---

## 4. A pergunta que você fez

> "vários relatórios do RREO a gente consegue entregar batendo, o que acha?"

**Acho que sim, mas com uma condição**: a **classe 5**.

Hoje o acervo tem a despesa (classe 6) e as variações patrimoniais (3 e 4), mas
**não tem os controles orçamentários da receita** (classe 5). Sem ela:

- o RREO A1 fica pela metade (só a despesa);
- o A3 (RCL) não existe;
- o A6 (resultado primário) não fecha.

**Com a classe 5**, a ferramenta entrega o RREO A1 completo, A3, A6 e A11 — além
do A9 que já funciona.

### Como pedir

Na consulta da MSC do Siconfi: marcar **todas as classes** (1 a 8) e os **três
tipos de valor**. O acervo atual é um recorte de três classes.

---

## 5. O que eu faria nos três dias

| Dia | Entrega |
|---|---|
| **13-14/11** | gerador do RREO A1 (despesa) + A9 validado |
| **15/11** | gerador do RREO A14 (soma dos que fecham) |
| **16/11** | rodar com set-out, comparar com os auditores |

Se você conseguir a **classe 5** de 2026 antes do dia 16, acrescento o A1-receita
e o A3 (RCL) — que é a base dos limites do RGF.

---

## 6. Resumo honesto

| Pergunta | Resposta |
|---|---|
| Quantos anexos do RREO a MSC reproduz hoje? | **2 com certeza** (A1-despesa, A9) |
| Quantos com a classe 5? | **6** |
| Quantos com `ano_inscricao`? | **8** |
| O total liquidado bate? | **Sim, ao centavo** |
