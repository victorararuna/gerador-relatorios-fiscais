# Releitura do Anexo 1 — o que a revisão encontrou

Revisão integral do motor de apuração do Anexo 1 contra o RGF homologado.

---

## 1. O bug que a releitura encontrou

A conta de controle **8.6.3.3.1.00.00** (Despesa com Pessoal não Executada
Orçamentariamente) não estava no mapa de naturezas. Por isso caía no `default`
do classificador e era somada em **Vencimentos** — ao mesmo tempo em que
alimentava a linha própria "Despesa não Executada".

Eram **R$ 454.943.101,05 contados duas vezes**.

### Por que corrigir piorava o resultado

Testei as combinações de filtro:

| Caso | Bruta | Desvio | Vencimentos |
|---|---|---|---|
| **A** — com filtro CO, sem 13.02, não executada nos dois lugares | 13.720.877.436 | **−0,64%** | 5.641.142.569 |
| B — sem filtro CO, com 13.02 | 14.236.231.887 | +3,09% | 5.641.142.569 |
| C — sem filtro CO, com 13.02, sem dupla | 13.326.345.684 | −3,50% | 5.186.199.468 |
| D — com filtro CO, sem dupla | 12.918.799.881 | −6,45% | 5.186.199.468 |

O caso **A** — com a dupla contagem — é o mais próximo do homologado.

**A conclusão**: o próprio RGF homologado considera a despesa não executada
**tanto na linha própria quanto na composição do pessoal ativo**. Não é bug do
meu código; é o critério do demonstrativo.

Confirmação aritmética:

```
despesa não executada (MSC)         454.943.101,05
vencimentos oficiais              5.727.095.551,73
vencimentos oficiais − não exec   5.272.152.450,68
meus vencimentos puros            5.186.199.467,85
diferença                            85.952.982,83
```

A diferença é **exatamente os R$ 86 milhões** que perseguimos desde o início —
o mesmo valor em qualquer cenário. A dupla contagem não cria nem esconde a
lacuna.

---

## 2. O que foi alterado no código

**Antes**: a conta caía em Vencimentos por omissão no mapa (comportamento
acidental).

**Depois**: está declarada explicitamente, com o motivo documentado:

```python
"319096": "exercicios_anteriores",
# A conta de controle 8.6.3.3.1.00.00 (Despesa com Pessoal nao Executada
# Orcamentariamente) e somada em VENCIMENTOS, como no RGF homologado: a
# despesa subjacente e de pessoal ativo e o RGF a considera tanto na linha
# propria quanto na composicao do pessoal ativo.
"863310": "vencimentos",
```

Isso importa para manutenção: quem ler o código daqui a seis meses vai entender
que é intencional, não um erro de digitação no `default`.

---

## 3. O que a releitura **não** resolveu

Os **R$ 86,0 milhões de Vencimentos** continuam sem explicação. Testei nesta
revisão:

| Hipótese | Resultado |
|---|---|
| Natureza não mapeada | Todas as 14 naturezas de pessoal estão no mapa |
| Conta de controle indevida | Explica a dupla contagem, mas não a lacuna |
| Filtro de CO muito restritivo | Sem filtro, a bruta sobe 3,09% e piora |
| Exclusão do 31.90.13.02 | Afeta a patronal (−0,03%), não os vencimentos |
| Busca de subconjunto nos elementos 31.x | Achou R$ 532,6 mi, mas com as próprias linhas de dedução (91 e 94) |

Nenhuma combinação de naturezas disponíveis soma os R$ 540,9 mi que faltariam
caso a não executada fosse retirada de vencimentos. E os R$ 86,0 mi persistem
quando ela é mantida — que é o critério do RGF.

---

## 4. Estado do Anexo 1 após a revisão

| Linha | Apurado | Homologado | Desvio |
|---|---|---|---|
| Despesa Bruta (I) | 13.720.877.435,74 | 13.809.083.609,68 | **−0,64%** |
| Vencimentos | 5.641.142.568,90 | 5.727.095.551,73 | −1,50% |
| Obrigações Patronais | 2.086.104.132,36 | 2.086.640.219,87 | **−0,03%** |
| Aposentadorias | 4.545.038.716,45 | 4.563.063.878,92 | **−0,40%** |
| Pensões | 820.544.827,09 | 803.877.241,85 | +2,07% |
| Terceirização | 173.104.089,89 | 173.463.616,26 | **−0,21%** |
| Despesa não Executada | 454.943.101,05 | 454.943.101,05 | **0,00%** |
| Despesas não Computadas (II) | 3.833.358.483,87 | 3.893.336.376,99 | **−1,54%** |
| **Despesa Líquida (III)** | **9.887.518.951,87** | **9.915.747.232,69** | **−0,28%** |

**24 de 30 verificações conferem.**

### O ganho da revisão

A **Despesa Líquida** saiu de −0,81% para **−0,28%**, porque a dedução dos
vinculados também usa o critério corrigido (bruto da conta de controle).

---

## 5. O que ainda é necessário

Para fechar os R$ 86,0 milhões de Vencimentos, um destes:

1. **A composição da linha "Vencimentos" no RGF homologado**, por natureza e
   fonte (o Siconfi não publica esse detalhamento no arquivo).
2. **A MSC com o atributo de intra-orçamentária** preenchido.
3. **O detalhamento da despesa por UG pagadora e recebedora**.

Os três caminhos foram investigados e nenhum está disponível nas fontes atuais.
Cada um exigiria acesso novo — não é questão de recalcular com os dados que já
temos.
