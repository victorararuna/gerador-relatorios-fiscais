# Painel de verificação — RGF 2025/2026 a partir da MSC

Situação de cada anexo com o número que o sustenta. Atualizado na rodada 9.

| anexo | situação | número |
|---|---|---|
| 1 — Despesa com Pessoal | **apurado**, ressalvas documentadas | I a −0,36% (2025 Q3) |
| 2 — Dívida Consolidada Líquida | **bloqueado** | DC −3,78% sem mapa de contas |
| 3 — Garantias e Contragarantias | ✅ **fechado** | 5/5 linhas a 0,00% |
| 4 — Operações de Crédito | limites fechados, operações pendentes | 3/3 limites a 0,00% |
| 5 — Disponibilidade e Restos a Pagar | não iniciado | depende da conta 8.2.1.7.4.01 |
| 6 — Demonstrativo Simplificado | depende dos anexos 4 e 5 | — |

---

## Anexo 1

Janela móvel de 12 meses, contas 6.2.2.1.3.03/04/07, POs do Executivo.

| linha | 2025 Q3 | 2026 Q1 | 2026 Q2 |
|---|---:|---:|---:|
| Vencimentos | −0,10% | −5,03% | −3,96% |
| Patronais | +0,25% | +0,44% | +1,07% |
| Aposentadorias | −1,12% | +5,92% | +5,85% |
| Pensões | +0,41% | +0,40% | +0,48% |
| **Despesa Bruta (I)** | **−0,36%** | **−0,09%** | **+0,45%** |
| **Despesa Líquida (III)** | **+0,78%** | +1,66% | +2,56% |

Passa nas cinco regras estruturais do Siconfi (ES1005, ES1016, ES1017, ES1018,
ED1002). A III é puxada pela linha de Exercícios Anteriores do homologado, que
repete R$ 248.732.357,39 em três janelas diferentes.

**Por Poder**: `gerar_anexo1_poderes.py` produz as sete apurações + consolidado
em um XLSX (`saida/RGF_<ano>_Q<q>_Anexo01_Poderes.xlsx`).

| janela | Executivo | demais Poderes | consolidado (I) | líquida (III) |
|---|---:|---:|---:|---:|
| 2025 Q3 | 15.422.754.491,59 | 1.668.885.665,54 | **17.091.640.157,13** | 12.641.025.255,09 |
| 2026 Q2 | 16.185.150.619,87 | 1.847.801.645,76 | **18.032.952.265,63** | 13.615.243.150,19 |

O consolidado é exatamente a soma dos sete.

Ressalva: só o Executivo tem homologado para comparar — os 216 downloads do
acervo usaram `co_poder=E`. Para os demais Poderes os números são **apurados**,
não conferidos.

## Anexo 2

O mapa de contas do MDF não é público. O mapa de 2024 reproduz abril (+1,01%) e
agosto (+1,60%) de 2025, mas quebra em dezembro (−11,39%) — o salto está em
precatórios (+R$ 2,65 bi) e numa "Outras Dívidas" de R$ 941,9 mi que não existia
em agosto. Detalhes em `ANEXO2_CALIBRACAO.md`.

## Anexo 3

| linha | desvio |
|---|---:|
| RCL | 0,00% |
| (-) emendas individuais | 0,00% |
| RCL ajustada | 0,00% |
| Limite do Senado (22%) | 0,00% |
| Limite de alerta (90%) | 1 centavo |

RCL vem do RREO Anexo 3 (não da MSC) e confere ao centavo. O mesmo motor foi
validado em **2026 Q2**: RCL 20.966.424.987,22, RCL ajustada 20.961.883.945,10,
limites 4.611.614.467,92 e 4.150.453.021,13 — 5 de 5 linhas a 0,00%.

## Anexo 4

Limites calculados sobre a RCL ajustada de endividamento:

| limite | desvio |
|---|---:|
| ARO (7%) | 0,00% |
| Geral (16%) | 0,00% |
| Alerta (90% do geral) | 0,00% |

Bloco de operações pendente: a matriz traz **R$ 6,70 bi** na natureza de receita
`17115001` (m01–m08) contra **R$ 2,49 mi** declarados como operações realizadas.
A diferença é refinanciamento/rolagem, que o Anexo 4 não computa — precisa de
recorte que a MSC ainda não oferece.

## Anexo 6

Bloco da despesa com pessoal calculado a partir da RCL ajustada de pessoal:

| linha | desvio |
|---|---:|
| Limite máximo (49%) | 0,00% |
| Limite prudencial (46,55%) | 0,00% |
| Limite de alerta (44,10%) | 1 centavo |

**% DTP**: apurado 56,83% contra 56,41% homologados — +0,42 p.p., herdados do
desvio de 0,78% da Despesa Líquida do Anexo 1.

Achado: os próprios documentos oficiais divergem entre si. A Despesa Líquida do
Anexo 1 (R$ 11.001.153.864,38) e a DTP do Anexo 6 (R$ 11.004.331.905,62)
diferem em **R$ 3.178.041,24** para o mesmo conceito.

## Anexo 5

Investigado. A conta que o MDF cita (8.2.1.7.4.01 — Disponibilidade por Fonte a
Utilizar) **não existe no plano de contas novo**: a classe 8 de dez/2025 tem 36
contas e nenhuma começa por `8217`.

A boa notícia é que as contas de controle `8.2.1.1.x` **carregam a fonte de
recursos**: `821110100` tem 143 linhas e 96 fontes, `821130100` tem 48 fontes,
`821140100` tem 80. Em 2024 essa informação não existia — é um dado novo.

A má notícia é que os totais ainda não conversam com o homologado:

| base | valor |
|---|---:|
| Anexo 5 oficial — disponibilidade de caixa bruta (IV) | 1.088.399.547,00 |
| Classe 8, conta `821110100` | 1.583.591.750,07 |
| Classe 1, caixa (`111`) | 1.607.346.153,41 |
| Classe 1, aplicações (`1135`) | 3.381.578.777,08 |

Falta o de-para FR → categoria do Anexo 5 (educação, FUNDEB, saúde, SUS, RPPS…)
e a definição de quais contas compõem "disponibilidade bruta". É trabalho de
mapeamento, não de dado ausente — diferente de 2024.

## Anexo 6

Depende dos anexos 4 (operações) e 5. Sem eles, não fecha.

---

## RREO

| anexo | situação | número |
|---|---|---|
| 1 — Balanço Orçamentário (despesa) | ✅ | 4 de 6 grupos exatos; intra derivada soma 2.664.925.314,43 |
| 1 — Balanço Orçamentário (receita) | ⚠️ | matriz fica entre líquido e bruto; recorte de deduções a replicar |
| 2 — Despesa por função | ✅ | 23 funções somam 23.361.499.529,63 (0,00) |
| 3 — RCL | ✅ | 2025 e 2026, 5/5 linhas a 0,00% |
| 9 — Operações de crédito (despesa de capital) | ✅ | 4/4 linhas a 0,00% |
| 7 — Restos a Pagar | ✅ | 5/5 linhas a 0,00% |
| 14 — Simplificado (despesa e RCL) | ✅ | 6/6 linhas a 0,00% |

A receita tem três bases distintas: Anexo 3 bruto (26.656.696.864,94), Anexo 1
líquido (23.329.936.436,26) e classe 5 da matriz (24.872.967.329,22). A matriz
não coincide com nenhuma — abate cerca de 82% das deduções de impostos, mas não
todas. Não é erro de leitura: é critério de apuração.

## Próximos passos, em ordem de retorno

1. **Receita do Balanço** — reproduzir o recorte de deduções (FUNDEB,
   transferências constitucionais, contribuição do servidor). Depende de tabela,
   não de código.
2. **RGF Anexo 4 — operações realizadas**: separar operação nova de
   refinanciamento na receita `17115001` (R$ 6,70 bi contra R$ 2,49 mi
   declarados).
3. **RGF Anexo 5** — de-para FR → categoria das 25 linhas (as contas 8.2.1.1.x
   já trazem a fonte).
4. **RGF Anexo 2** — bloqueado até obter o mapeamento de contas da STN.

## Motor

| módulo | função |
|---|---|
| `app/leitor_msc.py` | índice e leitura do formato longo |
| `app/anexo1_msc.py` | Anexo 1 (janela móvel, de-para, deduções) |
| `app/relatorio_anexo1.py` | planilha do Anexo 1 + aba de verificações |
| `app/anexo3_msc.py` | RCL do RREO Anexo 3 e Anexo 3 |
| `app/anexo4_msc.py` | limites do Anexo 4 |
| `app/anexo6_msc.py` | limites do Anexo 6 (pessoal) |
| `app/regras_anexo1.py` | regras de validação do Siconfi |
| `rreo_anexo1_grupos.py` | RREO Anexo 1 — despesa por grupo |
| `rreo_anexo2.py` / `rreo_anexo2_intra.py` | RREO Anexo 2 — despesa por função |
| `gerar_painel.py` | painel consolidado em XLSX |

41 testes verdes (leitor 14, Anexo 1 15, Anexo 3 3, limites 9).



