# Certificado de verificação

Emitido em **13/11/2026 22:28** a partir do código no commit `fa85a57` (branch `main`).

Último commit: *Certificado de verificacao gerado do codigo*

---

## 1. Resultado

**307 de 310 células exatas** (99.0%), em 26 grupos de verificação.

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
| RGF Anexo 1 - totais | 2 | 2 |
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

Suíte completa: **78 testes em 11 arquivos**.

---

## 5. Ressalvas

1. **RGF Anexo 2 — RP Processados**: 5,0% de desvio. O método está provado (fecha ao centavo em agosto/2025); falta o saldo da conta 8.6.3.2.2 em 31/12/2025, que não existe em nenhuma fonte disponível.
2. **RGF Anexo 1 — abril/2026**: 5.241,65 em 680 milhões (0,0008%), causado por um par de anulação e re-empenho no ND 31909203.
3. **RCL**: é lida do Anexo 3, não apurada — o bloco de deduções do RPPS não existe na matriz.

---

*Este certificado é gerado por `certificado.py`. O número que vale é o do livro `saida/verificacao_anexos.xlsx`; se este texto divergir dele, o livro está certo.*
