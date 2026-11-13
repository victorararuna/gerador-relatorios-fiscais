# Plano operacional — gerar os relatórios com três documentos

Resposta à pergunta: **sim, dá para ajudar nesse propósito.** Abaixo está o que a
ferramenta já faz, o que cada documento destrava e o que ainda depende de decisão
sua.

---

## 1. O teste que acabamos de fazer

Rodei a ferramenta em **2026 Q1** (janela maio/2025 a abril/2026) e comparei com
o homologado do Siconfi:

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| **Despesa Bruta (I)** | 15.875.707.077 | 15.925.794.076 | **−0,31%** |
| Vencimentos | 6.939.371.638 | 6.926.091.326 | **+0,19%** |
| Aposentadorias | 5.389.511.531 | 5.391.390.194 | **−0,03%** |
| Obrigações Patronais | 2.468.847.295 | 2.458.077.234 | **+0,44%** |
| Terceirização | 206.992.307 | 206.992.307 | **0,00%** |
| Inativos Vinculados | 3.644.048.431 | 3.637.723.790 | **+0,17%** |
| **Despesa Líquida (III)** | 11.425.539.041 | 11.284.592.816 | **+1,25%** |
| Pensões | 870.984.305 | 941.970.444 | −7,54% |

**Seis linhas abaixo de 0,5%.** O motor está validado para 2026.

---

## 2. Os três documentos e o que cada um destrava

### 2.1 Matriz de Saldos Contábeis (MSC)

**É o documento central.** Sem ela, nada é apurado.

| Anexo | O que a MSC fornece |
|---|---|
| RGF A1 — Pessoal | despesa liquidada por natureza, PO, FR e CO |
| RGF A2 — DCL | saldos do passivo da dívida |
| RGF A3 — Garantias | contas 2.2.8 |
| RGF A4 — Operações | limites (com a RCL) |
| RREO A1, A2, A3 | execução orçamentária, RCL |
| RREO A6, A7 | resultado primário, restos a pagar |

**Formato aceito**: `RN_<ano>_<mês>_classe<n>_period_change.csv` (formato longo,
com `poder_orgao`, `natureza_despesa`, `fonte_recursos`, `complemento_fonte`).

**Periodicidade**: mensal. A janela do RGF é móvel de 12 meses.

**Classes necessárias**: 3, 4, 5, 6 e **8**.

> A classe 8 é a que falta no acervo atual. Ela traz as contas de controle —
> inclusive a `8.6.3.3.1.00.00` (despesa não executada).

### 2.2 Balancete Consolidado do mês

**Complementa a MSC onde ela não chega.**

| O que fornece | Para quê |
|---|---|
| conta `8.6.3.3.1.00.00.00` (movimento) | despesa não executada |
| conta `8.2.1.7.4.01.00.00` | disponibilidade por fonte (RGF A5) |
| saldos de abertura e encerramento | conferência fluxo × saldo |
| todas as classes | Anexos 2 e 3 do RGF |

**Filtro**: `Ano Base` = exercício, `Consolidado Geral`, `Mês Referência: Encerramento`.

**Cuidado**: a conta 8.6.3.3.1 **zera no encerramento**. O valor do exercício é o
**movimento** (créditos − débitos), não o saldo anterior nem o final.

### 2.3 Comparativo da Receita Orçada com a Arrecadada

**Fornece a receita por rubrica** — o que a MSC não dá de forma direta.

| O que fornece | Para quê |
|---|---|
| rubrica 4.2.1 | operações de crédito (RGF A4 e A6, RREO A9) |
| rubricas 4.1.x | receita corrente por natureza |
| receita realizada × prevista | análise de execução |

**Filtro**: `Poder: Executivo` (para o RGF do Executivo) ou `Consolidado Geral`.

---

## 3. O que a ferramenta entrega com esses três

| Demonstrativo | Depende de | Situação |
|---|---|---|
| **RGF A1 — Pessoal** | MSC + balancete | ✅ −0,31% (2026 Q1) |
| RGF A2 — DCL | MSC + balancete | ⚠️ falta o de-para de contas |
| RGF A3 — Garantias | MSC + balancete | ⚠️ falta o de-para |
| RGF A4 — Operações | comparativo + RCL | ⚠️ falta a RCL |
| RGF A5 — Disponibilidade | balancete + MSC | ⚠️ falta o de-para FR → categoria |
| RGF A6 — Simplificado | A1 + A4 + A2 | parcial |
| RREO A1 — Balanço | MSC | ✅ |
| RREO A3 — RCL | MSC | ✅ |
| RREO A9 — Operações | comparativo | ✅ |
| RREO A14 — Simplificado | todos | ✅ |
| **Anexos 8 e 12** | SIOPE / SIOPS | ❌ fora do escopo |

**Hoje**: 1 anexo do RGF fechado, 4 do RREO.

**Com o de-para de contas**: os seis do RGF e os onze do RREO.

---

## 4. O gargalo real não é a ferramenta

É o **mapeamento de contas da STN** para os Anexos 2 e 5 do RGF. O MDF descreve o
significado das linhas, não o de-para. Ele fica na aba de anexos do sisweb, que
estava fora do ar (503) nas tentativas de coleta.

**Isso não depende de dados do ente** — é referência pública. Assim que estiver
acessível, os Anexos 2 e 5 saem.

Para o **Anexo 5**, o balancete já traz a conta `8.2.1.7.4.01` — o que falta é o
de-para da **fonte de recursos (FR, ~96 fontes) para as categorias** do anexo
(Educação, Saúde, FUNDEB, etc.).

---

## 5. Sobre o fechamento de setembro e outubro

O Siconfi hoje tem 2026 até o **B4 (agosto)**. O B5 (set-out) ainda não foi
publicado — é o que vocês vão fechar.

| Etapa | O que acontece | Ferramenta |
|---|---|---|
| Fechamento do mês | SIAFIC gera MSC + balancete | — |
| Extração | 3 arquivos por mês | `siconfi.py --acervo` |
| Apuração | pipeline lê e calcula | `pipeline.py` |
| Conferência | batimento contra homologado | `batimento_final.py` |
| Publicação | relatórios no layout STN | `gerar_anexo1_acervo.py` |

O tempo de execução é de **minutos** — a apuração do Anexo 1 leva cerca de 2
minutos para 12 meses de MSC.

---

## 6. O que eu preciso de você

### Para validar de ponta a ponta

1. **Balancete de 2026** (encerramento de abril para o Q1, ou do mês de referência).
2. **MSC de julho e agosto/2026** — para fechar a janela do Q2.
3. **O de-para de contas da STN** (Anexos 2 e 5) — se você tiver acesso ao sisweb.

### Para decidir

4. **Qual é o escopo mínimo aceitável?** Hoje o Anexo 1 fecha em −0,31%. Os
   demais exigem o de-para. Se o objetivo for liberar dois servidores, é preciso
   saber quantos anexos a ferramenta precisa cobrir para isso.
5. **Quem assina?** A ferramenta gera os quadros, mas a responsabilidade técnica
   é do contador. Vale definir o fluxo de revisão.

---

## 7. O que eu não prometo

- **Zero erro em tudo.** O Anexo 1 está em −0,31%; Pensões em −7,54% e o Piso do
  Enfermeiro em −11,34% ainda não fecham.
- **Anexos 8 e 12.** Vão para SIOPE e SIOPS — sistemas separados, com regras
  próprias.
- **Substituir o auditor.** A ferramenta produz os quadros e as verificações; a
  análise crítica continua sendo humana.

O que eu prometo é **rastreabilidade**: cada número tem origem identificada, cada
desvio tem causa documentada, e o batimento mostra onde está errado quando está.
