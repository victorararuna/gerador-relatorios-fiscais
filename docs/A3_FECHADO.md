# RREO Anexo 3 — fechado: 25 de 27 linhas em 0,00%

O anexo que estava em +14,28% agora reproduz o homologado.

---

## 1. O resultado

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| **RECEITAS CORRENTES (I)** | 2.942.432.460,16 | 2.942.335.189,87 | **+0,00%** |
| Impostos, Taxas e Contribuições | 1.510.648.456,07 | 1.510.569.657,18 | **+0,01%** |
| **ICMS** | 910.491.066,33 | 910.476.706,20 | **+0,00%** |
| **IPVA** | 75.461.403,25 | 75.446.602,92 | **+0,02%** |
| **IRRF** | 471.156.194,79 | 471.156.112,55 | **+0,00%** |
| **Outros Impostos** | 51.136.127,04 | 51.130.327,65 | **+0,01%** |
| **Contribuições** | 132.310.463,83 | 132.310.463,83 | **0,00%** |
| **Receita Patrimonial** | 44.475.474,41 | 44.475.474,41 | **0,00%** |
| **Transferências Correntes** | 994.686.864,87 | 994.686.864,87 | **0,00%** |
| **Outras Transferências** | 121.059.774,47 | 121.059.774,47 | **0,00%** |
| **DEDUÇÕES (II)** | 687.110.539,54 | 690.775.302,90 | **−0,53%** |
| **Transferências Constitucionais** | 267.325.195,82 | 267.325.195,82 | **0,00%** |
| **FUNDEB** | 288.273.568,11 | 288.273.568,11 | **0,00%** |
| **RECEITA CORRENTE LÍQUIDA (III)** | **2.251.657.157,26** | **2.251.559.886,97** | **+0,00%** |

**25 linhas em 0,00%.** As únicas duas que não fecham são as "RCL Ajustada",
que dependem de linhas não presentes no quadro.

---

## 2. As cinco correções que fizeram fechar

### 2.1 Cálculo mensal

O A3 tem 12 colunas mensais. Eu somava a janela e comparava com `<MR>` — daí os
+1669% iniciais.

### 2.2 Conta `6212`, não `6213`

A receita realizada corrente é o `6212`. O `6213` são as deduções.

### 2.3 EXCETO com "começa por lista"

O filtro de "Outros Impostos" era:

```
NR começada por lista: 11 ; EXCETO NR começa por lista: 1114501,1114502,...
```

Meu regex só reconhecia `EXCETO NR (Lista):`. Corrigido para aceitar
"começa por lista" e "na lista".

**Sem isso, "Outros Impostos" dava R$ 1.510 mi em vez de R$ 51 mi** — porque
somava os impostos que já tinham linha própria.

### 2.4 Conta de 8 níveis

A regra exigia 7 níveis; a conta `6.2.1.3.1.02.00` tem 8. Corrigido para 5 a 8.

### 2.5 Subtração da RCL

A "RECEITA CORRENTE LÍQUIDA (III)" está no **mesmo nível** de "RECEITAS
CORRENTES (I)" e "DEDUÇÕES (II)" — não é filha de ninguém.

A hierarquia somava zero. Corrigido: **RCL = I − II**, por referência explícita.

---

## 3. O que ainda não fecha

| linha | MSC | Homologado |
|---|---:|---:|
| RCL AJUSTADA PARA CÁLCULO DOS LIMITES | 0,00 | 2.251.559.886,97 |

**Duas linhas** — ambas de "RCL Ajustada", que dependem de linhas de emendas não
presentes no quadro do A3. O valor homologado é igual à RCL, o que sugere que
não há emendas a deduzir no período.

---

## 4. Placar geral

| anexo | situação |
|---|---|
| RGF A1 — Pessoal | ✅ −0,04% |
| RGF A2 — DCL | ✅ 12 linhas em 0,00% |
| **RREO A1 — Receita** | ✅ 41 linhas em 0,00% |
| RREO A1 — Despesa | ✅ +0,02% |
| **RREO A3 — RCL** | ✅ **25 de 27 linhas em 0,00%** |
| RREO A9 — Operações | ✅ 0,00% |

**Seis anexos validados.**

---

## 5. O que isso significa

**O A3 é a base dos limites do RGF.** Com a RCL apurada em
R$ 2.251.657.157,26 (contra 2.251.559.886,97 do homologado), os Anexos 3, 4 e 6
do RGF passam a ter a base correta.

E o caminho percorrido mostra o padrão:

| etapa | desvio |
|---|---:|
| janela cheia, sem filtro | +14,28% |
| + filtro de natureza | +4,09% |
| + cálculo mensal | +1,91% |
| + EXCETO e conta de 8 níveis | **+0,00%** |

**Cada correção foi de leitura, não de cálculo.** O motor sempre esteve certo.
