# Anexo 2 (DCL) — calibração 2025 a partir da MSC

Reproduzir com `python diag_dcl.py`.

---

## 1. O que o homologado de 2025 Q3 pede

Referência: 31/12/2025, coluna "Até o 3º Quadrimestre" do
`RGF_24_2025_quad3_anexo02.csv`.

| bloco | valor |
|---|---:|
| Dívida Contratual | 3.204.264.028,97 |
| — Empréstimos | 2.382.593.541,34 |
| — Reestruturação | 678.224.099,41 |
| — Parcelamento e renegociação | 143.446.388,22 |
| Precatórios posteriores a 05/05/2000 | 5.595.401.507,77 |
| Outras Dívidas | 941.926.197,62 |
| **DÍVIDA CONSOLIDADA (I)** | **9.741.591.734,36** |
| **DEDUÇÕES (II)** | **269.314.515,89** |
| **DCL (III)** | **9.472.277.218,47** |
| RCL ajustada (VI) | 19.509.346.803,92 |
| % DC / RCL | 49,93% |

> Nota: 49,93% da DC sobre a RCL — o Estado está no limite de alerta. Em 2024
> eram 41,74%.

## 2. O mapa de contas de 2024 não transporta para 2025

A lista de contas validada em 2024 (docs/ANEXO2_DCL.md, §2) foi aplicada a
dezembro/2025:

| componente | oficial | MSC (contas de 2024) | diferença |
|---|---:|---:|---:|
| Precatórios | 5.595.401.507,77 | 5.300.769.287,13 | **−294.632.220,64** |
| Dívida Contratual | 3.204.264.028,97 | 3.919.563.925,08 | **+715.299.896,11** |
| Outras Dívidas | 941.926.197,62 | 152.829.064,57 | **−789.097.133,05** |
| **Dívida Consolidada** | **9.741.591.734,36** | **9.373.162.276,78** | **−368.429.457,58 (−3,78%)** |

Contas usadas:

| componente | contas |
|---|---|
| Precatórios | `221110302`, `221110303` |
| Dívida contratual / empréstimos | `222210200`, `222110298`, `222130401`, `223110103`, `223110402`, `223110403` |
| Outras dívidas | `218910106`, `218810110`, `218910200`, `218919800` |

## 3. Leitura do desvio

Os erros são **grandes e de sinais opostos**: a dívida contratual está
R$ 715 mi acima e "outras dívidas" R$ 789 mi abaixo. Isso não é erro de soma —
é **reclassificação entre blocos**.

Mas o teste decisivo é aplicar o mesmo mapa em abril e agosto, quando a
estrutura ainda é a de 2024:

| data | MSC (mapa de 2024) | oficial | desvio |
|---|---:|---:|---:|
| 30/04/2025 | 6.406.100.826,49 | 6.342.196.943,49 | **+1,01%** |
| 31/08/2025 | 6.391.845.099,18 | 6.291.113.177,93 | **+1,60%** |
| 31/12/2025 | 8.632.344.765,82 | 9.741.591.734,36 | **−11,39%** |

Ou seja: **o mapa de 2024 continua válido até agosto** (erro de 1 a 1,6%) e
quebra em dezembro. O que acontece em dezembro:

| conta | 31/08 | 31/12 | variação |
|---|---:|---:|---:|
| `221110302` precatórios RPPS | 1.765.856.872,50 | 3.854.095.412,98 | **+2.088.238.540,48** |
| `223110402` parcelamento previdenciário | 846.845.402,52 | 1.171.337.683,37 | +324.492.280,85 |
| `222210200` dívida externa | 1.355.659.880,21 | 1.225.389.883,47 | −130.269.996,74 |
| `222110298` dívida interna | 621.102.021,83 | 461.620.172,82 | −159.481.849,01 |

A Dívida Consolidada oficial salta de R$ 6,29 bi (agosto) para R$ 9,74 bi
(dezembro) — **+R$ 3,45 bi em quatro meses**. O mapa captura +R$ 2,6 bi desse
salto: falta explicar cerca de R$ 850 mi, além das reclassificações entre blocos.

## 4. O evento de dezembro, bloco por bloco

Comparando as colunas de agosto e dezembro do homologado:

| bloco | 31/08/2025 | 31/12/2025 | variação |
|---|---:|---:|---:|
| Precatórios | 2.950.369.186,35 | 5.595.401.507,77 | **+2.645.032.321,42** |
| Empréstimos — externos | 1.562.953.581,50 | 1.532.683.584,76 | −30.269.996,74 |
| Empréstimos — internos | 954.935.633,39 | 849.909.956,58 | −105.025.676,81 |
| Reestruturação | 669.506.458,98 | 678.224.099,41 | +8.717.640,43 |
| Parcelamento e renegociação | 153.348.317,71 | 143.446.388,22 | −9.901.929,49 |
| **Outras Dívidas** | **0,00** | **941.926.197,62** | **+941.926.197,62** |
| **Dívida Consolidada** | **6.291.113.177,93** | **9.741.591.734,36** | **+3.450.478.556,43** |

Todo o salto está em **precatórios (+R$ 2,65 bi)** e em **"outras dívidas", que
não existia em agosto e aparece com R$ 941,9 mi em dezembro**.

Nossas contas de precatório (`221110302` + `221110303`) cresceram +R$ 2,31 bi no
mesmo período — faltam ~R$ 335 mi. É consistente com a inscrição de precatórios
no encerramento do exercício, que a matriz registra em conta diferente.

## 5. Tentativas que não funcionaram

- **Busca de subconjunto exato** (`busca_dcl.py`, meet-in-the-middle, centavos):
  nenhum subconjunto das contas 2.1.x/2.2.x reproduz precatórios, dívida
  contratual ou outras dívidas.
- **Somar as contrapartidas de curto prazo** (`2.1.2.x`): fecha dois componentes
  exatamente — empréstimos externos (`222210200` + `212210200` =
  1.532.683.584,76) e reestruturação (`222130401` + `212130401` =
  678.224.099,41) — mas, aplicada a abril e agosto, joga o total para +12%.
  O pareamento existe, mas não é uniforme no ano.
- **Parcelamento**: as contas `223110402` (R$ 1,17 bi) e `223110403` (R$ 402 mi)
  não cabem na linha de R$ 143 mi. Em agosto já não cabiam. É reclassificação
  de origem, não de encerramento.

## 6. Conclusão e próximo passo

O Anexo 2 não fecha por engenharia reversa: o mapa de contas do MDF **não é
público** (o próprio `ANEXO2_DCL.md` registra que o sisweb da STN estava fora do
ar). Em 2024 o mapa foi obtido por reconciliação; em 2025 a estrutura mudou
(precatórios de encerramento e "outras dívidas" novas) e a reconciliação não
converge mais.

Caminhos, em ordem de custo:

1. Obter a tabela de mapeamento do Anexo 2 (STN/sisweb) ou a memória de cálculo
   da DCL do ente.
2. Reconciliar por bloco **com o saldo de 31/12/2024** (que o homologado traz:
   DC 7.201.713.061,97) para validar o mapa em um ponto conhecido — exige a MSC
   de 2024, que não está no acervo.
3. Adiar o Anexo 2 e atacar o **Anexo 4/6 (operações de crédito)**, que a matriz
   nova destrava via `natureza_receita`.
