# Especificação da MAPA — RGF Anexo 1 (Despesa com Pessoal)

Documento de 13/11/2026. Transcreve a especificação operacional da planilha da
equipe: as fontes, a construção linha a linha e as travas de conferência.

---

## 1. Arquitetura

A planilha tem duas abas integradas:

- **MAPA** — dados brutos e deduções, colunas D a O (janeiro a dezembro),
  totalização em P; a linha 5 controla o GND 31 e a linha 4 é a verificação
  (`=L5-L6`).
- **QUADRO** — espelho oficial do Anexo 1; colunas B a M recebem os totais da
  MAPA somando os últimos 12 meses (coluna N) e os RPNP (coluna O).

## 2. As quatro fontes do SIGEF/RN

| # | relatório | filtro | coluna usada |
|---|---|---|---|
| 1 | Comparativo da Despesa Autorizada/Empenhada/Liquidada/Paga | Executivo consolidado (inclui RPPS 162233/162011), por ND (4 níveis) e fonte | **Liquidada → No Mês** |
| 2 | IEO UG 162233 (FUNFIRN) | Gestão 16233, por Subação/Fonte/Elemento, "No mês" | **Liquidado** |
| 3 | IEO UG 162011 (IPERN) | Gestão 00001, idem | **Liquidado** |
| 4 | Razão das contas 8.6.3.3.1.01 e 8.6.3.3.1.02 | Módulo de Contabilidade | **Mov. Credor − Mov. Devedor** |

## 3. Convenções de leitura da MAPA

- **Códigos com `XX`** (ex.: `31.XX.11.00`): somam-se todas as modalidades
  (31.90.11.00, 31.91.11.00…) na linha sintética `.00` do elemento — sem somar
  os subelementos para não duplicar.
- **Códigos de 8 dígitos** (ex.: `31.90.91.01`): busca-se exatamente aquele
  subelemento, sem filtro de fonte.

## 4. Construção da Despesa Bruta (MAPA L6 → QUADRO L17)

`L6 = L7 + L181 + L245 + L250`

| passo | linhas | fórmula |
|---|---|---|
| 2.1 Vencimentos | 8-101 | `=SUM(D11:D101)+D9-D10` |
| 2.2 Patronal | 102-180 | `=SUM(D103:D163)-SUM(D164:D180)` |
| 2.3 Aposentadorias | 182-208 | `=SUM(D183:D202)-SUM(D203:D208)` |
| 2.4 Pensões | 209-244 | `=SUM(D210:D227)-SUM(D228:D244)` |
| 2.5 Terceirização | 245-249 | `=SUM(D246:D249)` |
| 2.6 Não executada | 250-251 | `=SUM(D251)` |

### 2.2 Expurgo da patronal — por natureza, no Comparativo

| Poder | naturezas deduzidas (31.91.13.xx) | linhas |
|---|---|---|
| ALRN | 22, 43, 49, 71 | 164, 165, 166, 177 |
| DPRN | 46 | 167 |
| MPRN | 25, 48, 53, 75 | 168, 169, 170, 180 |
| TCE/RN | 23, 44, 50, 72 | 171, 172, 173, 178 |
| TJRN | 24, 45, 51, 73 | 174, 175, 176, 179 |

### 2.3 Expurgo dos inativos — IEO, **as duas fontes**

**Regra de ouro:** somar o Liquidado **na fonte 0.5.00 (Tesouro) e na 0.8.00
(RPPS)** — ambas compõem a linha 183 e não pertencem ao Executivo.

| linha | Poder | subação | elemento |
|---|---|---|---|
| 203 | ALRN | 222201 | 31.90.01 |
| 204 | DPRN | 218401 | 31.90.01 |
| 205 | MPRN | 222401 | 31.90.01 |
| 206 | TCE/RN | 222501 | 31.90.01 |
| 207 | TCE/RN (DEA) | 222501 | 31.90.92 |
| 208 | TJRN | 221201 | 31.90.01 |

### 2.4 Expurgo das pensões — IEO, fontes 0.8.00 e 0.8.04

| linha | Poder | subação (UG) | elemento |
|---|---|---|---|
| 228 | ALRN | 409101 (162233) | 31.90.03 |
| 229 | ALRN especial | 412301 (162011) | 31.90.03 |
| 230 | ALRN DEA | 409101 + 412301 | 31.90.92 |
| 232 | MPRN | 408701 (162233) | 31.90.03 |
| 233 | MPRN especial | 412401 (162011) | 31.90.03 |
| 234 | MPRN DEA | 408701 + 412401 | 31.90.92 |
| 237 | TCE | 408901 (162233) | 31.90.03 |
| 238 | TCE especial | 412501 (162011) | 31.90.03 |
| 239 | TCE DEA | 408901 + 412501 | 31.90.92 |
| 240 | TJRN | 408801 (162233) | 31.90.03 |
| 241 | TJRN especial | 412601 + 412701 (162011) | 31.90.03 |
| 244 | TJRN DEA | 408801 + 412601 + 412701 | 31.90.92 |

## 5. Despesas Não Computadas (MAPA L252 → QUADRO L26)

| passo | linhas | regra |
|---|---|---|
| 3.1 Indenizações | 253-261 | 31.XX.94.00 bruto menos fontes 800/801/803/804/604/605 |
| 3.2 Decisão judicial | 262-273 | 31.XX.91.00 bruto menos fontes vinculadas |
| 3.3 Exercícios anteriores | 274-285 | **deduzido só em dezembro** (Nota Explicativa nº 4) |
| 3.4 Inativos vinculados | 286-328 | 31.XX.01.00 e 03.00 nas fontes 800-804, menos os demais Poderes |
| 3.5 ACS e enfermagem | 329-338 | FR 604 a 100%; FR 605 a **72% em 2026** |

## 6. Travas de conferência

1. **MAPA L5 (GND 31 SIGEF)** deve bater com o total do grupo 31.00.00.00 no
   Comparativo do mês (exceto execução direta em 31.90.04.15).
2. **MAPA L4 = L5 − L6** é a verificação: evidencia a soma líquida das deduções
   dos demais Poderes, compensada por terceirização e não executadas.
3. **RPNP (QUADRO coluna O)** só é apurado em 31/12; permanece fixo no 1º e 2º
   quadrimestres seguintes, salvo cancelamento formal com nota explicativa.
4. **DTP (QUADRO L43)** = Despesa Líquida 12M (N34) + RPNP (O34), dividida pela
   RCL Ajustada e comparada a 49,00% / 46,55% / 44,10% (e 51,78% da LC 178/2021).
