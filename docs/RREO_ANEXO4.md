# RREO Anexo 4 — Receitas e Despesas Previdenciárias (primeira leitura)

> **Documento histórico.** Escrito quando o trabalho era sobre o **RGF 2024**.
> Os números e as pendências abaixo **não valem mais**: o Anexo 1 passou a fechar
> em 10 de 10 meses, o Anexo 5 chegou a 90 de 90 células e o Anexo 4 fechou.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2** —
> ou, melhor, abra `saida/verificacao_anexos.xlsx`, que é gerado do código.

---


2025 B6. Reproduzir com o script de diagnóstico descrito abaixo.

---

## 1. O anexo tem três blocos

| bloco | receitas | despesas | resultado |
|---|---:|---:|---:|
| Fundo em Capitalização (RPPS) | 3.526.965.581,92 | 5.558.625.132,53 | −2.021.593.847,26 |
| Administração RPPS | 36.426.758,30 | 19.623.492,05 | +16.803.266,25 |
| Benefícios mantidos pelo Tesouro (militares) | 22.237.288,50 | 119.906.956,64 | −97.669.668,14 |

## 2. O achado: a contribuição patronal é uma receita intra-orçamentária

A linha "Receita de Contribuições Patronais" do Fundo (R$ 2.490.846.806,78)
**não** vem da natureza 1.2.x — vem da **7.2.1.5** (receita intra-orçamentária):

| natureza | valor | linha do Anexo 4 |
|---|---:|---|
| `7215` | 2.500.460.000,00 | Contribuições Patronais (2.490.846.806,78 — **+0,39%**) |
| `1215` | 1.125.909.000,00 | Contribuições dos Segurados (908.360.001,62 — +24%) |

Faz sentido: o Tesouro paga a patronal ao RPPS por transferência entre unidades
do mesmo orçamento, e o RPPS registra como receita intra. É a outra ponta da
dupla contagem que aparece no Anexo 1 do RGF e no intra da função Previdência.

## 3. Por que os segurados não fecham direto

`1215` (R$ 1.125,9 mi) engloba também as contribuições dos **militares**, que o
Anexo 4 leva para o bloco "Benefícios mantidos pelo Tesouro":

```
1.125.909.000,00
(-) militares (133.912.023,96 + 40.438.549,63 + 26.779.906,65 = 201.130.480,24)
= 924.778.519,76   contra 908.360.001,62 homologados  (+1,81%)
```

Continua 1,8% acima — resíduo a investigar, mas a ordem de grandeza e a
composição estão identificadas.

## 4. Despesas

| linha | oficial | MSC (PO 10112) | desvio |
|---|---:|---:|---:|
| Aposentadorias | 4.917.756.724,31 | 4.606.896.561,40 | −6,3% |
| Pensões | 640.868.408,22 | 746.412.506,78 | +16,5% |

O PO 10112 agrega civis e militares; o Anexo 4 separa. Sem o atributo que
distingue militar de civil na despesa, a linha não fecha.

## 5. Situação

Receita patronal identificada e a 0,39%. Receita de segurados a 1,8%, com
composição conhecida. Despesas pendentes de separação civil/militar.

Próximo passo: testar se o desdobramento da natureza (subelemento) ou a fonte de
recursos distingue militar de civil nos lançamentos do PO 10112.
