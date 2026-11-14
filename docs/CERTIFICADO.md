# Certificado de verificação

Emitido em **14/11/2026 14:47** a partir do código no commit `b670447` (branch `main`).

Último commit: *Split fechado nos oito meses: faltava a natureza 31.XX.07.00*

---

## 1. Resultado

**424 de 435 células exatas** (97.5%), em 38 grupos de verificação.

Cada célula compara um valor **apurado pelo motor** com o valor do **arquivo publicado pelo Siconfi** — não com a planilha de trabalho da equipe.

## 2. Abas do livro

| aba | células | exatas |
|---|---:|---:|
| RGF Anexo 1 - 2026 | 24 | 22 |
| RGF Anexo 1 - rubricas | 53 | 52 |
| RGF Anexo 2 | 16 | 15 |
| RGF Anexo 2 - somas | 6 | 3 |
| RGF Anexo 6 - 2025 | 5 | 5 |
| RREO Anexo 11 | 5 | 5 |
| RREO Anexo 6 | 1 | 1 |
| RREO Anexo 4 - contribuicoes | 4 | 4 |
| RREO Anexo 4 - receitas | 1 | 1 |
| RREO Anexo 2 - funcoes | 23 | 23 |
| RREO Anexo 7 - por Poder | 7 | 6 |
| RGF Anexo 1 - 2025 (MAPA) | 4 | 4 |
| RGF Anexo 3 - 2025 | 5 | 5 |
| RGF Anexo 4 - 2025 | 8 | 8 |
| RGF Anexo 5 | 90 | 90 |
| RREO Anexo 9 | 9 | 9 |
| RREO Anexo 13 | 7 | 7 |
| RGF Anexo 1 - limites | 6 | 6 |
| RGF Anexo 5 - totais | 5 | 5 |
| RGF Anexo 1 - por Poder | 100 | 100 |
| RREO Anexo 2 - 2026 | 1 | 1 |
| RGF Anexo 2 - 2026 | 6 | 6 |
| RGF Anexo 3 - 2026 | 2 | 2 |
| RREO Anexo 7 - 2026 | 5 | 5 |
| RREO Anexo 14 - 2026 | 6 | 6 |
| RREO Anexo 4 | 4 | 4 |
| RREO Anexo 13 - projeções | 6 | 6 |
| motor | 1 | 1 |
| RREO - Balanço Orçamentário | 1 | 1 |
| RGF Anexo 1 - totais | 2 | 0 |
| RREO Anexo 3 | 1 | 1 |
| RGF Anexo 3 | 1 | 1 |
| RGF Anexo 4 | 1 | 1 |
| RGF Anexo 6 | 4 | 3 |
| RREO Anexo 2 - totais | 1 | 1 |
| RREO Anexo 1 | 3 | 3 |
| RREO Anexo 7 | 5 | 5 |
| RREO Anexo 14 | 6 | 6 |

## 3. Divergências

| grupo | item | apurado | referência | desvio |
|---|---|---:|---:|---:|
| RGF Anexo 1 - 2026 | 2026 — Abril — I — Despesa Bruta | 680,626,929.97 | 680,632,171.62 | -5,241.65 |
| RGF Anexo 1 - 2026 | 2026 — Abril — III — Despesa Líquida | 303,562,294.70 | 303,567,536.35 | -5,241.65 |
| RGF Anexo 1 - rubricas | 2026 — Abril — Pensões | 76,124,731.24 | 76,129,972.89 | -5,241.65 |
| RGF Anexo 2 | (-) Restos a Pagar Processados (Exceto Preca | 788,629,587.54 | 750,866,596.13 | 37,762,991.41 |
| RGF Anexo 2 - somas | DÍVIDA CONSOLIDADA (I) (soma) | 8,799,665,536.74 | 9,741,591,734.36 | -941,926,197.62 |
| RGF Anexo 2 - somas | DEDUÇÕES (II) (soma) | 231,551,524.48 | 269,314,515.89 | -37,762,991.41 |
| RGF Anexo 2 - somas | DÍVIDA CONSOLIDADA LÍQUIDA (III) (soma) | 8,568,114,012.26 | 9,472,277,218.47 | -904,163,206.21 |
| RREO Anexo 7 - por Poder | Anexo 7 — Executivo — RP Não Processados | 11,871,954.46 | 14,919,410.07 | -3,047,455.61 |
| RGF Anexo 1 - totais | RGF Anexo 1: despesa bruta (I) | 15,421,416,732.35 | 15,478,621,265.08 | -57,204,532.73 |
| RGF Anexo 1 - totais | RGF Anexo 1: despesa líquida (III) | 11,085,096,971.23 | 11,001,153,864.38 | 83,943,106.85 |
| RGF Anexo 6 | RGF Anexo 6: despesa total com pessoal (DTP) | 11,085,096,971.23 | 11,004,331,905.62 | 80,765,065.61 |

As causas estão em `docs/DIVERGENCIAS.md` e na coluna de observação da própria planilha.

## 4. O que sustenta o número

| trava | o que impede |
|---|---|
| `verificar_anos.py` | somar extração de outro exercício |
| `test_layout_stn.py` | publicar a RCL de 2024 como 2026 |
| `test_baseline.py` | usar um valor esperado diferente do publicado |
| `test_rgf_anexo2.py` | linha fechada voltar a abrir |
| `test_coerencia.py` | README, planilha e .md discordarem |
| `test_verificacao.py` | divergência ficar sem causa escrita |

Suíte: **113 testes definidos em 19 arquivos**. Rode `python rodar_testes.py` para ver quantos executam e quantos pulam.

---

## 5. Ressalvas

- **RGF Anexo 1 - 2026 — 2026 — Abril — I — Despesa Bruta**: -5,241.65 de desvio (-0.00%). O ARQUIVO PUBLICADO ESTA ERRADO — e o proprio manual do auditor documenta. Na subacao 408801 do TJRN, ND 31.90.92.03, fonte 0.5.00, abril tem empenhado 86.852,54 e liquidado 92.094,19; a fonte 0.8.00 tem liquidado 29.377,60. O correto, pelo regime de competencia (art. 18, § 2º, da LRF), e 92.094,19 + 29.377,60 = 121.471,79. O publicado traz 116.230,14 porque somou o EMPENHADO de uma fonte com o LIQUIDADO de outra: 86.852,54 + 29.377,60. A diferenca e 5.241,65 — o empenho de marco liquidado em abril. O MAPA do proprio auditor (RGF 2026_Q2_01, aba Mapeamento, linha 209) carrega o mesmo 76.129.972,89 do publicado, ou seja, o erro esta na origem. Nao se corrige do nosso lado sem publicar numero errado.
- **RGF Anexo 1 - 2026 — 2026 — Abril — III — Despesa Líquida**: -5,241.65 de desvio (-0.00%). O ARQUIVO PUBLICADO ESTA ERRADO — e o proprio manual do auditor documenta. Na subacao 408801 do TJRN, ND 31.90.92.03, fonte 0.5.00, abril tem empenhado 86.852,54 e liquidado 92.094,19; a fonte 0.8.00 tem liquidado 29.377,60. O correto, pelo regime de competencia (art. 18, § 2º, da LRF), e 92.094,19 + 29.377,60 = 121.471,79. O publicado traz 116.230,14 porque somou o EMPENHADO de uma fonte com o LIQUIDADO de outra: 86.852,54 + 29.377,60. A diferenca e 5.241,65 — o empenho de marco liquidado em abril. O MAPA do proprio auditor (RGF 2026_Q2_01, aba Mapeamento, linha 209) carrega o mesmo 76.129.972,89 do publicado, ou seja, o erro esta na origem. Nao se corrige do nosso lado sem publicar numero errado.
- **RGF Anexo 1 - rubricas — 2026 — Abril — Pensões**: -5,241.65 de desvio (-0.01%). Idem I: erro aritmetico do arquivo publicado, documentado pelo proprio auditor no manual (secao 1.3). Em abril/2026, subacao 408801 do TJRN: o correto e liquidado 92.094,19 (fonte 0.5.00) + 29.377,60 (fonte 0.8.00) = 121.471,79; o publicado traz 116.230,14 porque somou o empenhado da 0.5.00 (86.852,54) com o liquidado da 0.8.00. Diferenca: 5.241,65.
- **RGF Anexo 2 — (-) Restos a Pagar Processados (Exceto Precatóri**: 37,762,991.41 de desvio (+5.03%). Formula da aba RP: 6.3.1.3 + 6321 + 6.2.2.1.3.07, sem fontes 32/46/800/801/802, menos a conta 8.6.3.2.2. Fecha ao centavo em agosto/2025 com controle zero. Em dezembro sobram 37.762.991,41 porque o controle de 942.052.222,15 e de outro mes (precisaria ser 979.815.213,56).
- **RGF Anexo 2 - somas — DÍVIDA CONSOLIDADA (I) (soma)**: -941,926,197.62 de desvio (-9.67%). A linha 'Outras Dividas' TEM lista de contas no mapeamento da STN (celula C45): 8.5.3.7 + 8.6.3.2.1 + 8.6.3.2.2 + 2.1.8.9.1.01.05/.08 + 2.1.8.9.3/4/5 + 2.2.8.2.1/.3/.4/.5, exceto PO 10112/10122/10132. Apuradas as doze na MSC de 2025, sai 36.600,82 contra 941.926.197,62 publicados: falta a conta 8.6.3.2.2.00.00, que nao existe na matriz em nenhuma classe nem tipo. E o RP inscrito sem disponibilidade de caixa (Nota 4).
- **RGF Anexo 2 - somas — DEDUÇÕES (II) (soma)**: -37,762,991.41 de desvio (-14.02%). Herda a diferenca do RP Processados (37.762.991,41). As outras tres parcelas — disponibilidade, depositos e haveres — estao exatas.
- **RGF Anexo 2 - somas — DÍVIDA CONSOLIDADA LÍQUIDA (III) (soma)**: -904,163,206.21 de desvio (-9.55%). Herda as duas anteriores: falta 'Outras Dividas' na DC e sobra o RP sem disponibilidade nas deducoes. As duas parcelas sao o mesmo valor visto de dois lados.
- **RREO Anexo 7 - por Poder — Anexo 7 — Executivo — RP Não Processados**: -3,047,455.61 de desvio (-20.43%). Os cinco Poderes fecham em RP processados; em nao processados quatro fecham. O Executivo diverge em 3.047.455,61: o arquivo calcula Saldo k = (f + g) - (i + j), que inclui os liquidados nao pagos, enquanto a conta 6.3.1.1 da matriz traz so o saldo a pagar. A diferenca e a parcela liquidada e nao paga que o arquivo soma no saldo.
- **RGF Anexo 1 - totais — RGF Anexo 1: despesa bruta (I)**: -57,204,532.73 de desvio (-0.37%). 2025 nao fecha pela regra do mapeamento de 2026: aplicada aos doze meses, ela erra entre 0,2% e 26%, sem padrao. Em fevereiro o gabarito e 489,8 mi e a regra da 422,2 mi — e o PO 30390 sozinho tem 110 mi em fevereiro, fora de qualquer filtro documentado. Nao ha mapeamento de 2025 em MDF_STN/2025. O gabarito do auditor (aba CONFERENCIAS do RGF 2025_Q3_01) e a referencia: fecha internamente ao centavo e soma exatamente o publicado.
- **RGF Anexo 1 - totais — RGF Anexo 1: despesa líquida (III)**: 83,943,106.85 de desvio (+0.76%). Idem: decorre da mesma apuracao anual de 2025, cuja regra de Poder nao e a de 2026.
- **RGF Anexo 6 — RGF Anexo 6: despesa total com pessoal (DTP)**: 80,765,065.61 de desvio (+0.73%). Herda a despesa liquida de 2025 do Anexo 1, cuja regra de Poder nao e a de 2026. Ver as duas linhas de 2025 do Anexo 1.
- **RCL**: é lida do Anexo 3, não apurada — o bloco de deduções do RPPS não existe na matriz.

---

*Este certificado é gerado por `certificado.py`. O número que vale é o do livro `saida/verificacao_anexos.xlsx`; se este texto divergir dele, o livro está certo.*
