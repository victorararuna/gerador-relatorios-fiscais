# Certificado de verificação

Emitido em **13/11/2026 22:41** a partir do código no commit `05c1c3d` (branch `main`).

Último commit: *Certificado: ressalvas geradas do estado, nao escritas a mao*

---

## 1. Resultado

**305 de 310 células exatas** (98.4%), em 26 grupos de verificação.

Cada célula compara um valor **apurado pelo motor** com o valor do **arquivo publicado pelo Siconfi** — não com a planilha de trabalho da equipe.

## 2. Abas do livro

| aba | células | exatas |
|---|---:|---:|
| RGF Anexo 1 - 2026 | 24 | 22 |
| RGF Anexo 2 | 16 | 15 |
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
| RGF Anexo 6 | 1 | 1 |
| RREO Anexo 2 - totais | 1 | 1 |
| RREO Anexo 1 | 3 | 3 |
| RREO Anexo 7 | 5 | 5 |
| RREO Anexo 14 | 6 | 6 |

## 3. Divergências

| grupo | item | apurado | referência | desvio |
|---|---|---:|---:|---:|
| RGF Anexo 1 - 2026 | 2026 — Abril — I — Despesa Bruta | 680,626,929.97 | 680,632,171.62 | -5,241.65 |
| RGF Anexo 1 - 2026 | 2026 — Abril — III — Despesa Líquida | 303,562,294.70 | 303,567,536.35 | -5,241.65 |
| RGF Anexo 2 | (-) Restos a Pagar Processados (Exceto Preca | 788,629,587.54 | 750,866,596.13 | 37,762,991.41 |
| RGF Anexo 1 - totais | RGF Anexo 1: despesa bruta (I) | 15,422,754,491.59 | 15,478,621,265.08 | -55,866,773.49 |
| RGF Anexo 1 - totais | RGF Anexo 1: despesa líquida (III) | 11,086,434,730.47 | 11,001,153,864.38 | 85,280,866.09 |

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

Suíte: **79 testes definidos em 11 arquivos**. Rode `python rodar_testes.py` para ver quantos executam e quantos pulam.

---

## 5. Ressalvas

- **RGF Anexo 1 - 2026 — 2026 — Abril — I — Despesa Bruta**: -5,241.65 de desvio (-0.00%). Par de anulacao (35.094,19) e re-empenho (29.852,54) no ND 31909203 do PO 10112, em abril: a diferenca e 5.241,65. O homologado trata o par de forma diferente do Comparativo.
- **RGF Anexo 1 - 2026 — 2026 — Abril — III — Despesa Líquida**: -5,241.65 de desvio (-0.00%). Par de anulacao (35.094,19) e re-empenho (29.852,54) no ND 31909203 do PO 10112, em abril: a diferenca e 5.241,65. O homologado trata o par de forma diferente do Comparativo.
- **RGF Anexo 2 — (-) Restos a Pagar Processados (Exceto Precatóri**: 37,762,991.41 de desvio (+5.03%). Formula da aba RP: 6.3.1.3 + 6321 + 6.2.2.1.3.07, sem fontes 32/46/800/801/802, menos a conta 8.6.3.2.2. Fecha ao centavo em agosto/2025 com controle zero. Em dezembro sobram 37.762.991,41 porque o controle de 942.052.222,15 e de outro mes (precisaria ser 979.815.213,56).
- **RGF Anexo 1 - totais — RGF Anexo 1: despesa bruta (I)**: -55,866,773.49 de desvio (-0.36%). Total anual de 2025 apurado pela via da MSC (apurar_janela), nao pela MAPA do SIGEF que sustenta o Anexo 1 de 2026. Desvio de -55,9 mi (-0,36%): a MSC nao identifica a parcela intra-orcamentaria, que a equipe conhece pelo SIGEF. A conferencia de origem aceitava 0,5% e marcava OK; aqui se exige o centavo.
- **RGF Anexo 1 - totais — RGF Anexo 1: despesa líquida (III)**: 85,280,866.09 de desvio (+0.78%). Idem: decorre da mesma apuracao anual de 2025 pela MSC (+85,3 mi, +0,78%).
- **RCL**: é lida do Anexo 3, não apurada — o bloco de deduções do RPPS não existe na matriz.

---

*Este certificado é gerado por `certificado.py`. O número que vale é o do livro `saida/verificacao_anexos.xlsx`; se este texto divergir dele, o livro está certo.*
