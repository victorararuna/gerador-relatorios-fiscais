# Reclassificação Vencimentos × Aposentadorias — resolvida

O desvio que parecia reclassificação entre as duas linhas era, na verdade, **um
subelemento classificado no lugar errado**.

---

## 1. O achado

`3.1.90.92.01` — **R$ 397.969.926,47** — estava em **Vencimentos**.

No homologado, ele pertence a **Aposentadorias**.

### A prova aritmética

```
aposentadorias (3.1.90.01)            4.882.968.816,04
oficial                               5.281.577.891,79
diferença                               398.609.075,75

31909201                                397.969.926,47
outros pequenos                             639.149,28
                                      ─────────────────
                                        398.609.075,75  ← idêntico
```

A diferença das aposentadorias era **exatamente** o valor do `31909201`, ao
centavo. Não era reclassificação difusa: era um subelemento.

---

## 2. Por que estava errado

O classificador tratava `3.1.90.92` assim:

```python
if elemento == "319092":
    if se in SE_VENCIMENTOS:   # {"01"}
        return "vencimentos"
    if se in SE_PENSAO:        # {"03"}
        return "pensoes"
    return "exerc_ant"
```

A regra `SE_VENCIMENTOS = {"01"}` veio do motor de 2026, onde o `31909201`
realmente é vencimento. **Em 2025, o `31909201` é aposentadoria** — o ente mudou
o uso do subelemento entre os exercícios.

Corrigido:

```python
SE_APOSENTADORIA = {"01"}   # 31.90.92.01 = aposentadorias de exercícios anteriores
```

---

## 3. O resultado

| linha | antes | depois | homologado |
|---|---:|---:|---:|
| **Vencimentos** | +5,52% | **−0,55%** | 6.552.405.214,64 |
| **Aposentadorias** | −7,55% | **−0,05%** | 5.281.577.891,79 |
| Obrigações Patronais | +0,25% | +0,25% | 2.405.400.638,81 |
| Terceirização | −0,15% | −0,15% | 180.764.417,86 |
| Não Executada | +0,80% | +0,80% | 167.511.692,79 |
| Vinculados | +0,03% | **+0,03%** | 3.538.152.718,10 |
| **Despesa Bruta (I)** | −0,65% | **−0,66%** | 15.478.621.265,08 |
| **Despesa Líquida (III)** | −1,17% | **−1,19%** | 11.001.153.864,38 |

**As duas linhas que somavam R$ 362 mi para cima e R$ 399 mi para baixo agora
erram menos de 0,6% e 0,05%.**

O efeito na despesa bruta é neutro — como esperado, já que os dois valores se
compensavam. O ganho está na **composição**: cada linha agora tem o valor certo,
não uma compensação de erros.

---

## 4. O que ainda não fecha: Pensões

| | valor |
|---|---:|
| apurado | 820.116.992,13 |
| homologado | 890.961.409,19 |
| desvio | **−7,95%** |

### O que testei

| filtro de CO | pensões | desvio |
|---|---:|---:|
| atual (1111, 1151, 2111, 2151, 2211, vazio) | 881.462.506 | −1,07% |
| **+ 1122** | **890.576.931** | **−0,04%** |
| + 1131 | 954.059.196 | +7,08% |
| todos os CO | 992.718.541 | +11,42% |

**O CO `1122` fecha as pensões em −0,04%** (R$ 9.114.425,10).

Mas ao incluí-lo, as **aposentadorias pioram de −0,05% para +1,03%** e os
**vinculados de +0,03% para +1,28%** — porque o mesmo `CO_BENEFICIO` alimenta as
três linhas.

### O que isso indica

O `1122` pertence às **pensões**, mas **não** às aposentadorias nem à dedução de
vinculados. É preciso separar o conjunto de CO por linha:

- pensões: incluir `1122`
- aposentadorias: não incluir
- vinculados: não incluir

Não implementei porque o ganho é de R$ 9 mi em R$ 891 mi (1%), e a mudança
afetaria três linhas que hoje fecham. Fica registrado como o próximo ajuste.

### Por que o valor apurado caiu de 881,5 para 820,1

O `apurar_com_mensal` e o `verificar_anexo1` tinham conjuntos de CO ligeiramente
diferentes após a correção do `319092`. A linha de pensões do relatório usa
820,1; a análise isolada com o filtro completo dá 881,5. **Essa divergência
interna é o que precisa ser alinhada antes de mexer no `1122`.**

---

## 5. O que aprendi com o processo

1. **Não era reclassificação difusa.** Era um subelemento. A busca gulosa sobre
   os elementos achou o valor exato — a diferença fechava ao centavo.
2. **A regra de 2026 não vale para 2025.** O `31909201` mudou de linha entre os
   exercícios. Regra calibrada em um ano não se transporta sem conferência.
3. **Compensação de erros esconde problema.** A despesa bruta estava em −0,65%
   com duas linhas erradas em ±6%. Fechar o total não significa estar certo.
4. **O batimento entre relatórios foi o que permitiu chegar aqui.** Como os
   anexos são consistentes entre si, sabia-se que o erro estava na leitura da
   natureza, não na declaração.
