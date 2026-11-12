# Caça aos R$ 86 milhões de Vencimentos

Investigação da diferença entre a apuração pela MSC e o RGF homologado na linha
"Vencimentos, Vantagens e Outras Despesas Variáveis".

---

## 1. O tamanho do problema

| | Valor |
|---|---|
| Apurado (MSC) | 5.641.142.568,90 |
| Homologado | 5.727.095.551,73 |
| **Diferença** | **−85.952.982,83 (−1,50%)** |

Essa linha responde por **97,4%** da diferença total da despesa bruta
(−R$ 88,2 milhões). As outras três linhas com desvio somam R$ 22 milhões e, com
sinais opostos, se anulam quase por completo.

## 2. O que já foi descartado

### 2.1 Natureza não mapeada — descartado

Listei **todas** as naturezas de pessoal do Executivo na matriz:

| Elemento | Valor |
|---|---|
| 31.90.01 | 4.846.477.565,01 |
| 31.90.03 | 871.549.974,27 |
| 31.90.04 | 248.151.804,58 |
| 31.90.07 | 36.995,52 |
| 31.90.11 | 3.554.513.059,85 |
| 31.90.12 | 951.934.060,07 |
| 31.90.13 | 106.925.096,49 |
| 31.90.16 | 191.286.442,41 |
| 31.90.17 | 367.683,25 |
| 31.90.91 | 384.656.887,50 |
| 31.90.92 | 63.318.177,10 |
| 31.90.94 | 3.173.891,05 |
| 31.90.96 | 3.831.817,98 |
| 31.91.13 | 1.965.711.788,56 |
| 31.91.92 | 1.177.332,73 |

Todas estão classificadas. Não há natureza de pessoal fora do mapa.

### 2.2 PO faltante — descartado

Os POs do arquivo são 7: **10111** (Governo), **10112** (RPPS) e **60611**
(Defensoria) — o Executivo —, mais 30390, 50511, 20211 e 20212, que são os demais
Poderes. O recorte do Anexo 1 é exatamente 10111 + 10112 + 60611, conforme o
mapeamento da STN.

### 2.3 Restos a pagar de 2023 — descartado

A matriz de 2023 foi comparada e a hipótese não se confirmou. Além disso, os RP
de 2023 pagos em 2024 **não passam** pela despesa de 2024: são baixados da conta
de RP (5.3.1.1), não da conta de variação patrimonial.

## 3. O que a comparação com o RREO revelou

| Base | Valor |
|---|---|
| **MSC** — pessoal do Executivo (créditos brutos, todos os elementos) | 13.853.528.963,03 |
| **RGF** — despesa bruta menos não executada | 13.354.140.508,63 |
| **RREO** — pessoal e encargos, exceto intra-orçamentárias | 13.077.836.673,15 |
| **RREO** — pessoal e encargos, intra-orçamentárias | 2.270.546.730,00 |

Relações:

```
RGF  − RREO(exceto intra)  =  +276.303.835,48
MSC  − RREO(exceto intra)  =  +775.692.289,88
MSC  − RGF                 =  +499.388.454,40
```

A MSC traz **R$ 499,4 milhões a mais** que o RGF. Parte disso é a despesa
**intra-orçamentária** — transferências entre unidades do mesmo orçamento (a
contribuição do Tesouro ao RPPS é o caso típico). O RGF do Poder elimina a
duplicidade; a matriz de saldos registra as duas pontas.

## 4. Conclusão da investigação

**Não foi possível isolar os R$ 86 milhões de vencimentos.** As três causas
plausíveis foram testadas e descartadas, e o resíduo aponta para a **parcela
intra-orçamentária**, que a matriz não identifica por atributo.

O que a investigação acrescentou de concreto:

1. O erro **não** está no mapeamento de naturezas — todas estão classificadas.
2. O erro **não** está no recorte de PO — os três POs do Executivo são os certos.
3. O erro **não** está na competência dos restos a pagar.
4. A MSC e o RGF divergem em R$ 499,4 milhões no total de pessoal, e essa
   diferença tem o perfil de despesa intra-orçamentária.

## 5. O que resolveria

Para fechar a linha é necessário **o atributo de intra-orçamentária** — presente
na contabilidade mas não no arquivo `instancia.csv`. Na prática, um destes:

1. A MSC com a informação complementar de intra-orçamentária preenchida;
2. O detalhamento da despesa por UG pagadora e recebedora;
3. A composição da linha "Vencimentos" no RGF homologado, por natureza e fonte.

Com qualquer um deles, a diferença deixa de ser um resíduo e passa a ser uma
conta identificada.
