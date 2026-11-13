# O que a ferramenta entrega hoje — e o que o teste vai revelar

Resposta direta à pergunta: **damos conta do Anexo 1 com certeza. Dos outros, só
com o acervo completo e o de-para de contas.**

---

## 1. O inventário honesto

### O que é gerado (não baixado)

| Anexo | Situação | Desvio |
|---|---|---|
| **RGF Anexo 1 — Despesa com Pessoal** | ✅ **gerado da MSC** | **−0,31%** (2026 Q1) |

É o único anexo que a ferramenta **produz** hoje. Os demais são **baixados** do
Siconfi — o que não serve para o propósito, porque o Siconfi já tem o que o
Estado declarou.

### O que é baixado (não serve como teste)

RGF A2 a A6, RREO A1 a A14. São os arquivos homologados, usados como
**referência** para conferência — não como saída.

### O que o acervo atual permite gerar

O acervo tem **classes 3, 4 e 6**. Falta a **classe 5** (controles orçamentários
da receita) e a **classe 8** (controles credores).

| Anexo | Precisa de | Temos? |
|---|---|---|
| RGF A1 | classe 6 + balancete (classe 8) | ✅ |
| RGF A2 — DCL | classes 1.1, 1.2, 2.2 + de-para | ⚠️ classe 2 ausente |
| RGF A3 — Garantias | classe 2.2.8 + de-para | ⚠️ classe 2 ausente |
| RGF A4 — Operações | comparativo + RCL | ✅ receita; RCL na classe 5 |
| RGF A5 — Disponibilidade | classe 8 + FR + de-para | ⚠️ |
| RREO A1 — Balanço | **classe 5** (receita) e 6 (despesa) | ⚠️ classe 5 ausente |
| RREO A3 — RCL | classe 5 | ⚠️ classe 5 ausente |

**Conclusão**: com o acervo de três classes, só o Anexo 1 fecha. Para os demais,
o acervo precisa ser **completo** (classes 1 a 8).

---

## 2. O teste que você propôs

A ideia é boa e é o caminho certo. Vou detalhar como fazê-lo de forma que o
resultado seja útil.

### 2.1 O desenho

```
ferramenta gera  ──┐
                   ├──▶  compara  ──▶  o que fecha / o que não fecha
auditor faz à mão ─┘
```

O ponto crítico: **a ferramenta não pode ver o resultado do auditor antes**. Se
virmos o gabarito, o teste perde valor — passamos a calibrar contra ele, que é o
que fizemos até agora.

### 2.2 O que precisa ser combinado antes

| Item | Por quê |
|---|---|
| **Mesmo período** | ex.: 2026 Q1, ou set-out/2026 |
| **Mesmo escopo** | Executivo ou consolidado |
| **Mesmos insumos** | a ferramenta e o auditor partem dos mesmos arquivos |
| **Saída em planilha** | para comparar linha a linha, não só o total |
| **Sem comunicação entre as equipes** | para não haver contaminação |

### 2.3 O que o teste vai medir

| Métrica | O que revela |
|---|---|
| Linhas que fecham (< 0,5%) | cobertura real da ferramenta |
| Linhas que divergem | onde o de-para está errado |
| Linhas que a ferramenta não produz | lacuna de escopo |
| Tempo de execução | ganho operacional |

---

## 3. O que eu preciso para o teste dar certo

### 3.1 Acervo completo da MSC

As classes que faltam:

| Classe | Conteúdo | Para quê |
|---|---|---|
| **1** | Ativo | deduções da DCL (Anexo 2) |
| **2** | Passivo | DCL, garantias (Anexos 2 e 3) |
| **5** | Controles orçamentários — receita | RREO A1 e A3 (RCL) |
| **7** | Controles devedores | complemento |
| **8** | Controles credores | disponibilidade, não executada |

**Como pedir**: na consulta da MSC no Siconfi, marcar **todas as classes** e os
**três tipos de valor** (`beginning_balance`, `period_change`, `ending_balance`).

### 3.2 O de-para de contas da STN

Para os Anexos 2, 3 e 5 do RGF. Está na aba de anexos do sisweb (que retornou
503 nas tentativas). É referência pública, não depende do ente.

### 3.3 O balancete do mês de referência

Com `Ano Base` do exercício, `Consolidado Geral`, `Encerramento`.

---

## 4. Sobre a data

Você falou **16 de fevereiro de 2026** — mas estamos em **novembro de 2026**.
Imagino que seja **16/02/2027**, com os dados de set-out/2026 (que o Siconfi
ainda não publicou: hoje tem só até o B4/agosto).

Se for essa a data, há **três meses** de margem. É suficiente para:

| Prazo | Entrega |
|---|---|
| dezembro/2026 | acervo completo + de-para dos Anexos 2, 3 e 5 |
| janeiro/2027 | gerador dos seis anexos do RGF e dos onze do RREO |
| fevereiro/2027 | teste cego com os auditores |

---

## 5. O que eu recomendo como primeiro passo

**Não comece pelo teste completo.** Comece por um **piloto com um anexo só** — o
Anexo 1 — no período que vocês já fecharam (2026 Q1).

O piloto responde três perguntas em uma semana:

1. A ferramenta acerta o que o auditor faz à mão?
2. O tempo de execução justifica a mudança?
3. O formato de saída serve para publicar?

Se o piloto passar, escala para os demais. Se não passar, o custo foi baixo.

---

## 6. A resposta curta

**Damos conta?** Do Anexo 1, sim — está em −0,31%.

Dos outros, **depende de dois insumos** que não são código:

1. O acervo completo (classes 1, 2, 5, 8 — hoje temos 3, 4, 6)
2. O de-para de contas da STN (Anexos 2, 3 e 5)

Com esses dois, a ferramenta gera os seis anexos do RGF e os onze do RREO. Sem
eles, gera um.

E há uma coisa que o teste vai mostrar e que é importante aceitar: **alguns
anexos podem não valer a pena automatizar**. Se um anexo tem 20 linhas e leva 10
minutos para preencher à mão, o esforço de mapear as contas pode não se pagar.
O teste serve para descobrir isso também.
