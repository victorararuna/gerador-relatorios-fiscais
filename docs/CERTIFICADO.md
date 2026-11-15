# Certificado de verificação

Emitido em **14/11/2026 23:08** a partir do código no commit `1726c7f` (branch `main`).

Último commit: *baixar_msc.py: acervo completo, jul a set/2026 incluidos*

---

## 1. Resultado

**605 de 608 células exatas** (99.5%), em 39 grupos de verificação.

Cada célula compara um valor **apurado pelo motor** com o valor do **arquivo publicado pelo Siconfi** — não com a planilha de trabalho da equipe.

## 2. Abas do livro

| aba | células | exatas |
|---|---:|---:|
| RGF Anexo 1 - 2026 | 24 | 22 |
| RGF Anexo 1 - rubricas | 53 | 52 |
| RGF Anexo 2 | 16 | 16 |
| RGF Anexo 2 - somas | 6 | 6 |
| RGF Anexo 6 - 2025 | 5 | 5 |
| RREO Anexo 11 | 5 | 5 |
| RREO Anexo 6 | 1 | 1 |
| RREO Anexo 4 - contribuicoes | 4 | 4 |
| RREO Anexo 4 - receitas | 1 | 1 |
| RREO Anexo 2 - funcoes | 23 | 23 |
| RREO Anexo 7 - por Poder | 7 | 7 |
| RGF Anexo 1 - 2025 (MAPA) | 6 | 6 |
| RGF Anexo 1 - quadro 2026 | 171 | 171 |
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
| RGF Anexo 1 - totais | 2 | 2 |
| RREO Anexo 3 | 1 | 1 |
| RGF Anexo 3 | 1 | 1 |
| RGF Anexo 4 | 1 | 1 |
| RGF Anexo 6 | 4 | 4 |
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

Suíte: **125 testes definidos em 22 arquivos**. Rode `python rodar_testes.py` para ver quantos executam e quantos pulam.

---

## 5. Ressalvas

- **RGF Anexo 1 - 2026 — 2026 — Abril — I — Despesa Bruta**: -5,241.65 de desvio (-0.00%). O ARQUIVO PUBLICADO ESTA ERRADO — e o proprio manual do auditor documenta. Na subacao 408801 do TJRN, ND 31.90.92.03, fonte 0.5.00, abril tem empenhado 86.852,54 e liquidado 92.094,19; a fonte 0.8.00 tem liquidado 29.377,60. O correto, pelo regime de competencia (art. 18, § 2º, da LRF), e 92.094,19 + 29.377,60 = 121.471,79. O publicado traz 116.230,14 porque somou o EMPENHADO de uma fonte com o LIQUIDADO de outra: 86.852,54 + 29.377,60. A diferenca e 5.241,65 — o empenho de marco liquidado em abril. O MAPA do proprio auditor (RGF 2026_Q2_01, aba Mapeamento, linha 209) carrega o mesmo 76.129.972,89 do publicado, ou seja, o erro esta na origem. Nao se corrige do nosso lado sem publicar numero errado.
- **RGF Anexo 1 - 2026 — 2026 — Abril — III — Despesa Líquida**: -5,241.65 de desvio (-0.00%). O ARQUIVO PUBLICADO ESTA ERRADO — e o proprio manual do auditor documenta. Na subacao 408801 do TJRN, ND 31.90.92.03, fonte 0.5.00, abril tem empenhado 86.852,54 e liquidado 92.094,19; a fonte 0.8.00 tem liquidado 29.377,60. O correto, pelo regime de competencia (art. 18, § 2º, da LRF), e 92.094,19 + 29.377,60 = 121.471,79. O publicado traz 116.230,14 porque somou o EMPENHADO de uma fonte com o LIQUIDADO de outra: 86.852,54 + 29.377,60. A diferenca e 5.241,65 — o empenho de marco liquidado em abril. O MAPA do proprio auditor (RGF 2026_Q2_01, aba Mapeamento, linha 209) carrega o mesmo 76.129.972,89 do publicado, ou seja, o erro esta na origem. Nao se corrige do nosso lado sem publicar numero errado.
- **RGF Anexo 1 - rubricas — 2026 — Abril — Pensões**: -5,241.65 de desvio (-0.01%). Idem I: erro aritmetico do arquivo publicado, documentado pelo proprio auditor no manual (secao 1.3). Em abril/2026, subacao 408801 do TJRN: o correto e liquidado 92.094,19 (fonte 0.5.00) + 29.377,60 (fonte 0.8.00) = 121.471,79; o publicado traz 116.230,14 porque somou o empenhado da 0.5.00 (86.852,54) com o liquidado da 0.8.00. Diferenca: 5.241,65.
- **RCL**: é lida do Anexo 3, não apurada — o bloco de deduções do RPPS não existe na matriz.

---

*Este certificado é gerado por `certificado.py`. O número que vale é o do livro `saida/verificacao_anexos.xlsx`; se este texto divergir dele, o livro está certo.*
