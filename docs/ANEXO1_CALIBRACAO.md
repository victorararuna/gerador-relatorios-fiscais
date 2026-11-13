# Anexo 1 do RGF — calibração contra o homologado

Reproduzir com `python confere_periodos.py` (três janelas) e
`python mensal_janelas.py` (mês a mês).

---

## 1. Base de cálculo

| item | definição |
|---|---|
| Fonte | MSC (`MSCC`), classe 6, `period_change` |
| Contas | 6.2.2.1.3.03, .04 e .07 |
| Medida | movimento **líquido** (crédito − débito) |
| Recorte | POs 10111 + 10112 + 60611 (Executivo) |
| Janela | **12 meses móveis** terminados no mês do quadrimestre (Q1→abr, Q2→ago, Q3→dez) |

O Anexo 1 não é acumulado do ano: os totais homologados vão de 14,05 bi
(2025 Q1) a 16,11 bi (2026 Q2) — só compatível com janela móvel.

**Teste que valida o motor**: a mesma extração, sem filtro de pessoal e com os
7 POs, reproduz o total liquidado do **RREO 2025 B6 Anexo 1** — R$ 23.361.499.529,63,
diferença **0,00**.

---

## 2. Resultado nas três janelas

| linha | 2025 Q3 | 2026 Q1 | 2026 Q2 |
|---|---:|---:|---:|
| Vencimentos | −0,10% | −5,03% | −3,96% |
| Obrigações Patronais | +0,25% | +0,44% | +1,07% |
| Pessoal Ativo | −0,01% | −3,60% | −2,64% |
| Aposentadorias | −1,12% | +5,92% | +5,85% |
| Pensões | +0,41% | +0,40% | +0,48% |
| Inativo e Pensionistas | −0,90% | +5,09% | +5,04% |
| **DESPESA BRUTA (I)** | **−0,36%** | **−0,09%** | **+0,45%** |

As janelas de 2025 Q1 e Q2 não podem ser fechadas: começam em 2024, e a MSC de
2024 não está no acervo.

---

## 3. Duas descobertas que fizeram o relatório fechar

### 3.1 Pensões: o desdobramento `3.1.90.03.05` não pertence à linha

Pensões desviava +12,3% a +13,0% **nas três janelas** — estável, portanto regra.
Testei os sete desdobramentos de pensão, um a um:

| cenário | 2025 Q3 | 2026 Q1 | 2026 Q2 |
|---|---:|---:|---:|
| integral | +12,95% | +12,40% | +12,26% |
| sem `31900301` | −58,29% | −56,83% | −56,93% |
| sem `31900302` | −14,63% | −14,93% | −15,44% |
| sem `31900304` | +12,94% | +10,23% | +10,14% |
| **sem `31900305`** | **+0,41%** | **+0,40%** | **+0,48%** |

R$ 111,7 mi/ano que o homologado **não** considera pensão do Anexo 1. Excluído,
a linha fecha nas três janelas com menos de meio ponto.

### 3.2 Patronais: a regra da STN estava certa

O mapeamento manda **excluir** `3.1.90.13.02` e **incluir** `3.1.91.92`
(patronal de inativo). Eu havia feito o contrário — excluía o `.02` e jogava o
`319192` em exercícios anteriores. Corrigido:

| | 2025 Q3 | 2026 Q1 | 2026 Q2 |
|---|---:|---:|---:|
| antes | +1,42% | +5,81% | +5,84% |
| **depois** | **+0,25%** | **+0,44%** | **+1,07%** |

E derrubou junto o Pessoal Ativo de +0,30% para **−0,01%** em 2025.

### 3.3 O filtro de CO foi testado e descartado

Aplicar o filtro de CO (1111/1151/2111/2151/2211) em aposentadorias e pensões
piora tudo: −3,03%, −2,72% e −2,15%. Não é o critério que o homologado usa.
A opção `--filtrar-co` fica no código apenas para auditoria.

---

## 4. Demais decisões de de-para

| regra | efeito |
|---|---|
| Só `31.xx` entra nas linhas de pessoal | o de-para anterior jogava 32/44/46 em "vencimentos" pelo `default` — R$ 1,12 bi de despesa não-pessoal dentro do Anexo 1 |
| `31.90.92.01` → Vencimentos; `.03` → Pensões; demais → Exercícios anteriores | tirou vencimentos de −6,18% para −0,10% |
| `31.90.04` em linha própria | R$ 368,7 mi que a linha oficial de Vencimentos não absorve |
| Terceirização = qualquer `3.3.xx.34` | −0,15% |
| Não executada = conta `8.6.3.3.1.00.00` em **fluxo anual** | 168,8 mi contra 167,5 (+0,80%) |

**Conta de controle 8.6.3.3.1.00.00**: o movimento mensal é errático — jan −252,0 mi,
fev −4,7, mar −58,2, abr −140,0, mai a nov 0,00, **dez +623,8 mi**. Só a soma
anual se aproxima do homologado. É **estoque**, não fluxo: entra no total anual e
nunca na comparação mensal.

---

## 5. O que ainda não fecha

**Vencimentos × Aposentadorias em 2026** erram −R$ 278 mi e +R$ 319 mi — somam
quase zero. É reclassificação entre as duas linhas, não falta de valor. A origem
está visível na comparação 2025 × 2026 por natureza (média mensal):

| natureza | 2025/mês | 2026/mês | Δ |
|---|---:|---:|---:|
| `31900101` aposentadorias RPPS | 383,9 mi | 433,8 mi | **+49,9 mi** |
| `31909201` exerc. anteriores | 33,2 mi | 1,1 mi | **−32,0 mi** |
| `31911310` patronal (novo em 2026) | 0,00 | 203,2 mi | +203,2 mi |
| `31911311` + `31911312` | 160,1 mi | 5,0 mi | −155,1 mi |

Ou seja: em 2026 o RPPS passou a registrar mais em `31.90.01` e quase nada em
`31.90.92.01`, e a patronal migrou de desdobramento. São mudanças reais na fonte,
que o RGF homologado de 2026 não acompanha na mesma proporção.

**Aposentadorias 2025 (−R$ 59,2 mi)** é o único desvio de 2025 acima de 1%.

### 5.1 A linha de exercícios anteriores não é soma de nada

Teste de subconjunto exato sobre os componentes de `31.90.92`, `31.91.92` e
`31.90.96` da matriz (`busca_exerc_ant.py`):

| conjunto | componentes | resultado |
|---|---:|---|
| todos os Poderes | 40 | "acha" R$ 248.732.357,39 com 12 componentes |
| **só Executivo** | 26 | **nenhum subconjunto** |

O primeiro resultado é **artefato combinatório**, não descoberta: com 40
componentes em precisão de centavos existem 2⁴⁰ combinações para ~10¹⁰ valores
possíveis — qualquer alvo é atingível por acaso. A prova está na própria
composição encontrada: ela usa contas dos POs `20211`, `30390` e `50511`, que não
pertencem ao Executivo, e o arquivo homologado é `co_poder=E`.

Restringindo ao Executivo, **nada fecha**. Conclusão: a linha de R$ 248,7 mi do
homologado não é soma de componentes da matriz — é valor lançado à mão e repetido
entre exercícios.

---

## 5-A. Grupo II (despesas não computadas)

| linha | 2025 Q3 | 2026 Q1 | 2026 Q2 |
|---|---:|---:|---:|
| Indenizações (3.1.90.94 inteiro) | **0,00%** | +0,004% | +0,003% |
| Decisão judicial (3.1.90.91) | −0,04% | **0,00%** | +0,000% |
| Inativos/pensionistas vinculados | **+0,03%** | −0,13% | −0,13% |
| Piso do enfermeiro | −1,23% | −11,34% | −8,63% |
| Exercícios anteriores | −56,87% | −77,34% | −86,66% |

**Vinculados** fecha com FR `18xx` **e** CO de benefício do RPPS
(1111/1151/2111/2151/2211). Só o grupo 18xx, sem o CO, excede em R$ 332 mi.

**Indenizações** e **judiciais** fecham quando não se desdobra o elemento: o
homologado usa `3.1.90.94` inteiro e `3.1.90.91` inteiro.

**Enfermagem**: o percentual do ADCT depende do exercício (100% em 2022-23, 90%
em 2024, 80% em 2025, 70% em 2026). Com 80% em 2025 a linha erra −1,23%; em 2026
o percentual de 70% erra −8,6% a −11,3%, o que indica que a base do homologado
não é a mesma (provável empenho, não liquidação).

**Exercícios anteriores não é reproduzível.** O homologado traz
R$ 181.744.273,43 em 2025 Q1 e Q2 e **R$ 248.732.357,39 idênticos em 2025 Q3,
2026 Q1 e 2026 Q2** — três janelas móveis diferentes com o mesmo valor, o que só
se explica por repetição manual no preenchimento. A matriz apura R$ 107,3 mi em
2025 e R$ 33-56 mi em 2026. Enquanto o dado oficial não for refeito, essa linha
não serve de benchmark — e ela é a maior responsável pelo desvio da Despesa
Líquida (III).

---

## 6. Situação e próximos passos

O **total** do Anexo 1 fecha nas três janelas (−0,36%, −0,09%, +0,45%), mas nem
todas as linhas estão dentro de 0,5% — aposentadorias (2026) e vencimentos (2026)
ainda não estão. Critério de aceite: todas as linhas dentro de 0,5%.

1. Resolver a reclassificação 2026 vencimentos × aposentadorias (R$ 300 mi).
2. Fechar aposentadorias de 2025 (−R$ 59,2 mi, −1,12%).
3. Repetir em 2026 Q3 quando a matriz de dezembro/2026 existir.
4. Só então montar as 18 linhas completas (grupo II, RCL e limites).
