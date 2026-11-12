# RGF Anexo 4 — Operações de Crédito

Apuração a partir da **Matriz de Saldos Contábeis** (exercício 2024), 3º
quadrimestre, confrontada com o RGF homologado no Siconfi.

---

## 1. Estrutura do demonstrativo

Extraída do relatório do Siconfi (MDF 14ª edição, tópico 04.04):

```
OPERAÇÕES DE CRÉDITO                         No Quadrimestre | Até o Quadrimestre
    Mobiliária
        Interna · Externa
    Contratual
        Interna
            Empréstimos
            Aquisição Financiada de Bens e Arrendamento Mercantil
            Antecipação de Receita pela Venda a Termo
            Assunção, Reconhecimento e Confissão de Dívidas (LRF, art. 29, § 1º)
        Externa
    Operações não sujeitas ao limite (I)
    Operações de crédito não sujeitas (II)
    TOTAL (III)

APURAÇÃO DO CUMPRIMENTO DOS LIMITES          VALOR | % SOBRE A RCL AJUSTADA
    RECEITA CORRENTE LÍQUIDA - RCL (IV)
    (-) Emendas individuais (V)
    RECEITA CORRENTE LÍQUIDA AJUSTADA (VI)
    OPERAÇÕES VEDADAS (VII)
    TOTAL CONSIDERADO (VIII) = (IIIa + VII - Ia - IIa)
    LIMITE GERAL (16% da RCL ajustada)
    LIMITE DE ALERTA (90% do limite)
    OPERAÇÕES POR ANTECIPAÇÃO DA RECEITA ORÇAMENTÁRIA (ARO)
    LIMITE PARA ARO (7% da RCL ajustada)
```

## 2. Resultado da apuração

| Linha | Apurado | Homologado | Desvio |
|---|---|---|---|
| Total das Operações de Crédito (III) | 0,00 | 429.228.593,51 | **−100%** |
| RCL (IV) | 17.259.892.416,73 | 17.259.892.416,73 | **0,00%** |
| (–) Emendas individuais (V) | 4.802.839,15 | 4.802.839,15 | **0,00%** |
| **RCL Ajustada (VI)** | **17.255.089.577,58** | **17.255.089.577,58** | **0,00%** |
| Total considerado para o limite (VIII) | 0,00 | 429.228.593,51 | **−100%** |
| **Limite geral (16%)** | **2.760.814.332,41** | **2.760.814.332,41** | **0,00%** |
| **Limite de alerta (14,4%)** | **2.484.732.899,17** | **2.484.732.899,17** | **0,00%** |
| **Limite para ARO (7%)** | **1.207.856.270,43** | **1.207.856.270,43** | **0,00%** |

Os limites fecham no centavo. O que **não** foi apurado é a operação de crédito
realizada — R$ 429.228.593,51 contratados até o 3º quadrimestre.

## 3. Por que a operação de crédito não foi apurada

A operação de crédito é **receita orçamentária**. Procurei na matriz:

| Tentativa | Resultado |
|---|---|
| Contas 4.5.1 / 4.5.2 (receitas) | valores de R$ 588 mi a R$ 18 bi — são outras naturezas |
| Naturezas de receita 1111/2111 (operações de crédito) | nenhuma ocorrência |
| Busca de subconjunto nas contas 4.x | combinação de R$ 429,27 mi, mas com contas incoerentes (4.6.3.9, 4.1.2.2) |

A MSC registra a receita por conta contábil, mas **não traz no arquivo o código
reduzido da natureza de receita** nos mesmos moldes em que traz a ND da despesa.
Sem esse atributo (ou sem o mapeamento oficial), não há como isolar as operações
de crédito das demais receitas.

**Consequência prática:** o Anexo 4 sai com as operações zeradas e os limites
corretos. As verificações marcam as duas linhas de operação como divergentes
(−100%), o que é proposital — melhor sinalizar do que preencher com valor
estimado.

## 4. O que é preciso para fechar

1. **O mapeamento da receita** (qual conta/natureza corresponde a "Operações de
   Crédito — Empréstimos"), ou
2. **A extração da receita por natureza** do SIAFEM (o relatório "Comparativo da
   Receita" ou similar), que traria a natureza 1.1.1.1.1.03 diretamente.

Com um dos dois, o Anexo 4 fecha como os demais.
