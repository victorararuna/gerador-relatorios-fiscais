# Regras descobertas para os anexos restantes (13/11/2026)

Varredura feita por seis agentes sobre os materiais do projeto. Cada regra abaixo
foi provada com números contra o homologado. **Nenhuma delas está implementada
ainda** — este documento é a especificação para a implementação.

---

## 1. RGF Anexo 2 — DCL

### Empréstimos Internos: usar a conta-PAI

O critério da STN enumera os filhos (`2.1.2.1.1.02.01`, `...02.98` etc.), mas o
plano de contas do RN **não tem o `.02.98`** — tem `.02.01`, `.02.02` e `.02.03`.

```
pai   2.1.2.1.1.02.00.00 ...... 380.969.268,90
filho 2.1.2.1.1.02.01 ......... 348.090.972,54
diferença (= .02.02) ..........  32.878.296,36   <- a lacuna
```

Com o pai, fecha em **849.909.956,58** (publicado, 31/12/2025). Em 31/08/2026:
**1.626.484.480,79**, também exato.

Fonte: balancete do SIGEF, conta de 8 segmentos, coluna **"Saldo Restante"** —
com o sinal de natureza já embutido. **Não inverter sinal de classe 2 aqui.**

### RP Processados: depende de extração

```
bruto_p = Inscritos_ex_ant + Inscritos_exer_ant + Liquidados_RPNP
        - Pagos_RPP - Pagos_RPNP - Cancelados_RPP + (Liquidado - Pago)
excl_p  = RP_p(FR 32) + RP_p(FR 46) + RP_p(FR 800) + RP_p(FR 801) + RP_p(FR 802)
RPP     = Σ liquido_p (7 Poderes) - saldo de 8.6.3.2.2.00.00
```

Conferido: **640.153.394,98** (31/08/2026), exato.

**Bloqueio:** exige o relatório do SIGEF com a dimensão **fonte de recursos** por
Poder — que o balancete consolidado não tem.

Atenção: usar `6.3.1.3.0` + `6.3.2.1.0` (leitura ingênua) inclui "Retenções a
Pagar" e estoura em +13.280.918,23. O correto é `6.3.1.3.1` + `6.3.2.1.1`.

### Armadilha de escopo

"Demais Dívidas Contratuais" soma 236,6 mi nas contas `2.1.8.1.x`/`2.2.8.1.x`,
mas o RN publica **zero** nessa linha e aloca em "Outras Dívidas". Linha oficial
pode ser subconjunto da soma das contas.

---

## 2. RGF Anexo 5 — Disponibilidades

Três correções, todas provadas (114/114 células exatas em 2025 Q3):

**a) Filtro de Poder** — `poder_orgao` começando por **"10"** (só o Executivo).
É a causa das 6 células que faltavam; sem ele, os demais Poderes entram na soma.

**b) Coluna (e)** — exige a **classe 8**, hoje nunca aberta:

```
821130200 + 821130300  (8.2.1.1.3.02 + 8.2.1.1.3.03)
+ 863310000 (8.6.3.3.1) — SÓ na linha "Recursos Não Vinculados de Impostos"
= 2.230.614.991,10   (total oficial)
```

O acréscimo de 8.6.3.3.1 vale **623.792.553,08** e está documentado na Nota 4 do
próprio demonstrativo.

**c) Coluna (a)** — classe 1 com sinal D−C, **excluindo a conta-espelho
`111120000`**, que repete `111110200` em todas as 95 fontes.

**d) FR 759** pertence só a "Recursos Vinculados a Fundos" (já implementado).

Regra de ouro: a **fonte de verdade é o texto do critério (coluna C)**, não a
lista de códigos (coluna B) — a 759 aparece em B38 e não em C38.

---

## 3. RREO Anexo 9 — Receita

**O módulo usa a natureza errada.** Hoje filtra `17115001` — que é FPE
(transferência corrente, R$ 6,70 bi) — e por isso o anexo parecia parcial.

```
(I) = Σ 6.2.1.2 + 6.2.1.3  com natureza de receita prefixo "21" (+ "81")
      em ending_balance
refinanciamento = NR 211102, 211255, 212102, 212255 (+ 811102, 811255, 812102, 812255)
operacao_nova   = (I) - refinanciamento
```

No RN o refinanciamento é **zero** (nenhuma dessas naturezas existe no acervo).

Conferido: 2025 B6 = **2.491.012,67**; 2026 B4 = **833.803.782,54** — ambos exatos.

Cuidados: não usar `6.2.1.1` como previsão (é o resíduo a−b); a previsão vem da
classe 5 (`5.2.1.1` + `5.2.1.2`) com sinal invertido. E o Anexo 9 só existe no
último bimestre.

---

## 4. RREO Anexo 13 — PPP

**Não depende de cadastro de contratos** — é conta contábil. 11/11 células exatas.

| linha | conta | valor (2026 B4) |
|---|---|---:|
| Ativos da SPE | `89122*` | 400.000.000,00 |
| Obrigações com a SPE | `2186101*` + `2286101*` | 196.757.187,16 |
| Garantias concedidas | `812110122` | 413.225.632,16 |
| Despesa do contrato | `62211*` + `6221202*` + `62213*` com ND 33/44/45.67 | 102.811.000,00 |

Dívida de PPP: RCL do Anexo 3, previsão atualizada = **21.653.811.631,30**;
V = **0,47%**.

Projeções: `60.190.422,53 × (1,035 / 1,1068)^n` — uma âncora (valor presente das
contraprestações da Arena das Dunas) e dois índices publicados na nota do anexo.

**Pendência única:** a âncora de 60.190.422,53 é dado contratual. A coluna
"31/12 do exercício anterior" **já é apurável**: a MSC de dezembro/2025 está no
acervo e reproduz os três valores ao centavo (400.000.000,00 / 215.455.288,93 /
38.506.744,29), assim como a coluna do período em ago/2026
(400.000.000,00 / 196.757.187,16 / 413.225.632,16).

---

## 5. RCL e limites — e a correção do percentual

A RCL ajustada o motor **já apura**: `app/anexo3_msc.py::ler_rcl()`.

```
RCL ............................ 20.966.424.987,22
(-) emendas individuais ........      4.541.042,12
(-) emendas de bancada .........      3.707.946,35
= RCL ajustada p/ pessoal ...... 20.958.175.998,75
```

Limites em reais: máximo **10.269.506.239,39**; prudencial **9.756.030.927,42**;
alerta **9.242.555.615,45**.

### O percentual correto é 55,17%, não 44,32%

O painel gerencial divide uma DTP de **10 meses** por uma RCL de **12 meses**:

```
9.288.694.215,97 ÷ 20.958.175.998,75 = 44,32%   <- janela mista
```

O número oficial é 12 sobre 12:

```
11.563.398.205,71 ÷ 20.958.175.998,75 = 55,17%   <- publicado
```

Conferência da janela (set/2025 a ago/2026): soma das 12 despesas líquidas =
11.560.220.164,47; + RPNP 3.178.041,24 = **11.563.398.205,71**, exato.

Série histórica publicada: 2021 = 54,57%; 2022 = 53,37%; 2023 = 56,94%;
2025 = 56,41%; 2026 Q2 = 55,17%. Teto da LC 178/2021 para 2026 = **52,34%**.

**Regra a gravar no código: nunca dividir janelas diferentes.**

---

## 6. O que falta implementar

| anexo | o que fazer |
|---|---|
| RGF Anexo 2 | trocar o filho pelo pai em `rgf_anexo2_dcl.py` (uma linha) |
| RGF Anexo 5 | filtro de PO "10", classe 8 na coluna (e), classe 1 em (a) |
| RREO Anexo 9 | trocar a natureza `17115001` por prefixo "21" sobre 6.2.1.2+6.2.1.3 |
| RREO Anexo 13 | montar as contas de saldo e dotação; parametrizar a âncora |
| RCL/limites | ligar o Anexo 3 ao bloco de limites do Anexo 1 |


---

## 7. Achados da varredura de materiais (agente 6)

### 7.1 De-paras confirmados

| anexo | arquivo | aba / linha |
|---|---|---|
| RGF 2 | `RGF - ANEXO 2 ... MSC 2026.xlsx` | "Anexo 2 - Dívida (E, DF e M)": L17 empréstimos, L53 RP, L59-61 RCL |
| RGF 2 (uso do pai) | `RGF 2026_Q2_02 - DCL.xlsx` | aba **oculta** "Contas MSC", L25: `2.1.2.1.1.02.00.00` |
| RGF 2 (RP por Poder) | idem | aba **oculta** "RP", L12-20, com as exclusões -32/-46/-800/-801/-802 |
| RGF 5 | `RGF - ANEXO 5 ... MSC 2026.xlsx` | L16 (colunas) e L18 (conta da coluna e) |
| RREO 9 | `RREO - ANEXO 09 ... MSC 2026.xlsx` | E12 e E13 (6212/6213 + NR) |
| RREO 13 | `RREO - ANEXO 13 ... MSC 2026.xlsx` | B15-B24 (saldos) e linha 30 (dotação) |
| RCL | `RREO - ANEXO 03 - RCL ... MSC 2026.xlsx` | L46-52 (a cadeia completa) |

### 7.2 A regra da RCL, agora escrita

```
L46  RCL (III) = I - II
L47  (-) emendas individuais ...... NR 171; CO = 3110, 3111
L48  RCL ajustada p/ endividamento = V
L49  (-) emendas de bancada ....... NR 171; CO = 3120, 3121; TODAS as FR exceto 604
L50  (-) ACS/ACE .................. NR 171; FR = 604
L51  (-) outras deduções .......... "NÃO HÁ MAPEAMENTO"
L52  RCL ajustada p/ pessoal ...... V - VI - VII - VIII
```

### 7.3 RISCO: a RCL está com valores fixos no código

`app/layout_stn.py` linhas 166-167 trazem a cadeia **digitada**:

```python
"rcl": 17259989216.73, "emendas_individuais": 4802839.15,
"emendas_bancada": 22049553.00, "rcl_ajustada": 17233040024.58,
```

E `app/anexo3_msc.py` lê **apenas** as emendas individuais — a bancada e o ACS não
são calculados. Se esse caminho for usado para gerar 2026, publica a RCL de outro
período. **Corrigir antes de qualquer geração.**

### 7.4 O Anexo 13 muda de regra no 6º bimestre

| coluna | 1º ao 5º bimestre | 6º bimestre |
|---|---|---|
| despesa do contrato | `6.2.2.1.1` + `6.2.2.1.2.02` + `6.2.2.1.3` | **só** `6.2.2.1.3` |
| RCL (IV) | Anexo 3, "Previsão Atualizada" | Anexo 3, "Total últimos 12 meses" |

Como o fechamento do ano é no 3º quadrimestre / 6º bimestre, a regra de dezembro é
a segunda coluna — não a que foi validada em agosto.

### 7.5 O Anexo 5 não tem homologado de 2026

Só existem Anexo 5 de **2024 Q3** e **2025 Q3** (e os consolidados). Não há 2026
Q1/Q2 para conferir — a validação de 2026 terá de ser feita contra o RREO Anexo 7
e a coerência interna, não contra o homologado.

### 7.6 Divergência STN × prática do ente (Anexo 5, coluna e)

O template da STN manda ler `2.1.8.9.1.01.05/.08`. O RN usa a **classe 8**
(`8211302`/`8211303` + `8.6.3.3.1`), e isso está documentado nas **notas 3 e 4** do
próprio demonstrativo publicado. **Seguir a prática, não o template** — e registrar
essa escolha no código.

### 7.7 O que a varredura não achou

- a redação escrita da regra "conta-pai" — só o uso (aba oculta "Contas MSC");
- de-para para "Outras Deduções Constitucionais" — a STN declara "não há mapeamento";
- teto de 5% da RCL para PPP em nenhum arquivo.
