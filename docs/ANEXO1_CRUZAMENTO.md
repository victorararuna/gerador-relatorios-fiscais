# Anexo 1 do RGF — o cruzamento das três fontes

| fonte | o que é | onde está |
|---|---|---|
| **MDF 15ª ed. / mapeamento STN** | a regra oficial: contas, filtros, listas | `dados/mapeamentos/rgf/.../RGF - ANEXO 1 ... MSC 2026.xlsx` |
| **Metodologia etonjones** | como o auditor extraiu e por quê | `prompt_e_metodologia_rgf_anexo1_despesa_pessoal_rn.md` |
| **Nosso código** | o que a `mapa_anexo1` faz hoje | `mapa_anexo1.py` |

---

## 1. Onde a despesa é buscada

| item | MDF / STN | etonjones | nosso código |
|---|---|---|---|
| **contas** | `6.2.2.1.3.03` + `.04` + `.07` | Comparativo da Despesa + IEO | Comparativo (PDF) |
| **filtro de Poder** | `PO começada por 10,60` (Executivo) | `Poder: Executivo`, UG Administrativa: Não | **não aplica** |
| **natureza** | posicional: modalidade + elemento | subelemento (8 dígitos) cruzado com fonte | listas montadas à mão |
| **granularidade** | MSC (conta + PO + ND) | Comparativo + IEO por subação/fonte | Comparativo por ND |

**Consequência medida:** sem o filtro de Poder, o erro de janeiro é **+84%**; com as três contas, **+9%**; com PO 10,60, **+0,49%**.

---

## 2. O expurgo dos inativos e pensionistas dos outros Poderes

Esta é a parte que explica o desvio de 16 células.

| item | MDF / STN | etonjones |
|---|---|---|
| **por que existe** | art. 20, § 7º, da LRF: cada Poder apura seus próprios inativos | idem |
| **quem executa** | — | **UG 162233 (FUNFIRN)** e **UG 162011 (IPERN)** pagam a folha de **todos** os Poderes |
| **como separar** | — | pela **subação orçamentária**: ALRN `408501/408502`, DPRN `408601/408602`, MPRN `408701/408702`, TJRN `408801/408802`, TCE `408901/408902` |
| **quais fontes** | — | **Fonte 500 + 800 + 804** |
| **valor jan–out/2026** | — | aposentadorias **276.411.282,40** · pensões **93.223.848,61** |

### E o expurgo patronal — a resposta que eu procurava

O manual diz, em 1.4:

> dentro da UG 162233 havia exatamente **R$ 1.337.759,24** de encargos patronais sobre o 13º salário de outros Poderes
> (`31.91.13.71` TJ = 869.035,06 · `.72` AL = 192.345,57 · `.73` TCE = 44.331,85 · `.75` MP = 232.046,76)

**Os subelementos `.71` a `.75` de `31.91.13` são as obrigações patronais dos outros Poderes.**

É exatamente a lista que a `mapa_anexo1` já usa em `EXPURGO_PATRONAL` — mas aplicada pelo **Comparativo**, sem a dimensão de fonte.

**Conferido na matriz:** os `.71` a `.75` de janeiro/2026 no Comparativo somam
**exatamente 1.337.759,24** — o mesmo número do manual.

| subelemento | Poder | valor |
|---|---|---:|
| `31.91.13.71` | TJ | 196.658,26 |
| `31.91.13.72` | AL | 122.204,94 |
| `31.91.13.73` | TCE | 864.423,52 |
| `31.91.13.74` | DPE | 0,00 |
| `31.91.13.75` | MP | 154.472,52 |
| **soma** | | **1.337.759,24** |

**Hipótese do desvio de 138.865,10:** o nosso `EXPURGO_PATRONAL` inclui, além
dos `.71` a `.75`, os subelementos `.22` a `.25` e `.43` a `.53` (FGTS e INSS).
O total nosso é 11.641.413,58 e o do SIGEF 11.502.548,48 — a diferença pode ser
a parcela de Fonte 500 dentro desses outros subelementos, que o Comparativo não
separa.

---

## 3. A dedução dos inativos vinculados — duas camadas

| camada | regra | fonte |
|---|---|---|
| **Quadro I** (despesa bruta) | subtrai **tudo** que FUNFIRN/IPERN pagou aos outros Poderes: Fonte **500 + 800 + 804** | etonjones 1.2 |
| **Quadro II** (não computadas) | deduz **só** o custeado por recursos próprios do RPPS: Fontes **800, 801, 802, 803, 804** | art. 19, §1º, VI e §3º, LRF |
| **vedação** | **nunca** deduzir a Fonte **500** (aporte do Tesouro) | etonjones 1.2 |

Sem essa distinção, a despesa líquida sai distorcida — o mesmo valor seria expurgado duas vezes.

---

## 4. A despesa não executada orçamentariamente

| item | MDF / STN | etonjones |
|---|---|---|
| **contas** | `8.6.3.3.1.00.00` | `8.6.3.3.1.01.00.00` (salários) e `8.6.3.3.1.02.00.00` (13º) |
| **cálculo** | movimento do mês, somente crédito | **movimento credor − movimento devedor** |
| **expurgo** | — | **1.337.759,24** na UG 162233 (patronal do 13º dos outros Poderes) |

O crédito é a despesa reconhecida por competência; o débito é a baixa quando ela é executada. Sem o sinal negativo, a folha de dezembro conta duas vezes na janela de 12 meses.

---

## 5. As quatro travas de dupla dedução

O MDF proíbe deduzir a mesma parcela duas vezes no Quadro II. O etonjones implementa quatro interseções:

| interseção | valor jan–out/2026 |
|---|---:|
| Sentenças judiciais (`31.XX.91`) × recursos vinculados (FR 800) | 2.975,86 |
| DEA (`31.XX.92`) × recursos vinculados (FR 800/804) | 4.191,42 |
| DEA (`31.XX.92`) × piso da enfermagem (FR 605) | 1.123.833,39 |
| Indenizações (`31.90.94`) × ACS/ACE (FR 604) | — |

**Nosso código não implementa nenhuma das quatro.**

---

## 6. O piso da enfermagem

| exercício | parcela computada | parcela deduzida |
|---|---:|---:|
| 2023 | 100% | 0% |
| 2024 | 90% | 10% |
| 2025 | 80% | 20% |
| **2026** | **28%** | **72%** |

Base: `31.90.11`, `31.90.13`, `31.90.92` e `31.91.13` na Fonte `X.6.05`.

---

## 7. A diferença de 5.241,65 em abril — explicada

| item | valor |
|---|---:|
| empenhado em abril (subação 408801, TJRN, ND 31.90.92.03, FR 500) | 86.852,54 |
| **liquidado** em abril | **92.094,19** |
| diferença | **5.241,65** |

A liquidação de abril inclui empenho de março (5.241,65 empenhado, 0,00 liquidado).

**A planilha oficial somou o empenhado de uma fonte com o liquidado de outra** (`86.852,54 + 29.377,60 = 116.230,14`). O correto, pelo regime de competência: `92.094,19 + 29.377,60 = 121.471,79`.

Não é erro nosso — é erro de digitação no arquivo publicado, de 5.241,65.

---

## 8. O quadro do que falta implementar

| regra | fonte | no nosso código? |
|---|---|---|
| filtro de Poder (PO 10,60) | MDF/STN | **não** |
| três contas `6.2.2.1.3.03/.04/.07` | MDF/STN | parcial |
| expurgo por subação × fonte (500/800/804) | etonjones | **não** — usa subelemento |
| dupla camada do Quadro II | etonjones + LRF | **não** |
| não executada = crédito − débito | etonjones | **não** — usa só crédito |
| quatro travas de dupla dedução | etonjones | **não** |
| piso da enfermagem 72% em 2026 | etonjones | parcial |

---

## 9. Por que ainda não fecha

Nenhuma das divergências do Anexo 1 vem de número errado na matriz. Todas vêm de **recorte**:

1. **sem o filtro de Poder**, entram despesas dos outros Poderes (erro de 9%);
2. **sem a subação**, o expurgo dos inativos não separa quem é o inativo;
3. **sem a fonte**, o expurgo patronal conta parcela a mais (138.865,10/mês);
4. **sem o sinal do débito**, a não executada conta duas vezes.

O dado está na matriz. O que falta é a **extração por subação e fonte** — que o etonjones fez em 20 relatórios do SIGEF.

---

*Cruzamento das três fontes, rodada 132.*


---

## 10. O MAPA do auditor — o gabarito completo (rodada 145)

Faltava um documento: a aba **`Mapeamento`** do `RGF 2025_Q3_01 - DEMONSTRATIVO DA
DESPESA COM PESSOAL.xlsx`. Ela nao e um mapeamento de contas — e o **MAPA do
auditor**, a memoria de calculo linha a linha, com o valor de cada mes.

**340 linhas, 324 com valor.** Extraido para `dados/benchmarks/anexo1_2025_mapa.json`.

### O que ele mostra

| linha | rotulo | janeiro | ano |
|---|---|---:|---:|
| 4 | **OBRIGACOES PATRONAIS; INATIVOS E PENSIONISTAS DOS PODERES** | **289.358.696,13** | — |
| 5 | GND 31 SIGEF | 1.100.407.900,09 | — |
| 6 | DESPESA BRUTA COM PESSOAL (I) | 811.049.203,96 | **15.478.621.265,08** |
| 7 | Pessoal Ativo | 594.245.174,31 | — |
| 8 | Vencimentos | 426.026.503,19 | **6.552.405.214,64** |
| 101 | Obrigacoes Patronais | 168.218.671,12 | **2.405.400.638,81** |
| 250 | Decisoes judiciais | 1.245.845,89 | — |
| 262 | DEA | 46.473.885,54 | — |
| 274 | Inativos e Pensionistas com Recursos Vinculados | 237.630.833,96 | **3.538.152.718,10** |

### O que isso revela

A linha 4 — o expurgo — vale **289.358.696,13 em janeiro**, nao 11,6 milhoes.

Ela **nao e so a patronal**: e "obrigacoes patronais **e** inativos e pensionistas
dos Poderes". O expurgo dos inativos (que vem do IEO por subacao) esta na **mesma
linha** do expurgo patronal.

O nosso codigo trata os dois separadamente — a patronal no `EXPURGO_PATRONAL` e os
inativos dentro de aposentadorias/pensoes. Por isso o split diverge: **estamos
comparando partes diferentes de uma linha que o auditor totaliza.**

### O proximo passo

Comparar as 324 linhas com a nossa apuracao, uma a uma. A primeira diferenca que
aparecer aponta a regra que falta — e agora ha um gabarito por linha, nao so por
total.
