# Gerador de Relatórios Fiscais — RREO e RGF do RN

Ferramenta que apura os demonstrativos fiscais do **Rio Grande do Norte** a
partir das **Matrizes de Saldos Contábeis (MSC)** do Siconfi e dos relatórios do
**SIGEF/RN**, e confere cada célula contra o arquivo homologado.

Estado em **13/11/2026**: **294 de 299 células exatas** (98,3%), em 24 abas de
verificação (23 de anexo e uma de resumo). As 5 divergências estão em
[`docs/DIVERGENCIAS.md`](docs/DIVERGENCIAS.md), cada uma com valor, referência e
causa.

---

## Como rodar

```bash
python verificar_tudo.py    # 27 conferências de ponta a ponta
python verificacao.py       # gera o livro de verificação e o relatório de divergências
```

Saídas: `saida/verificacao_anexos.xlsx` (uma aba por anexo) e
`docs/DIVERGENCIAS.md`.

### Por anexo

```bash
python mapa_anexo1.py Setembro      # RGF Anexo 1 completo (MAPA)
python rgf_anexo2_dcl.py            # RGF Anexo 2 — DCL
python rgf_anexo5_vinculacao.py     # RGF Anexo 5 — disponibilidades
python rreo_anexo9.py               # RREO Anexo 9 — operações de crédito
python rreo_anexo13.py              # RREO Anexo 13 — PPP
python rreo_anexo4_blocos.py        # RREO Anexo 4 — previdenciário
python verificar_anos.py            # barra extração de outro exercício
```

---

## O que fecha hoje

| anexo | situação |
|---|---|
| **RGF Anexo 1** — despesa com pessoal | **exato em 10 de 10 meses** (I, II e III); por Poder, 100 de 100 |
| **RGF Anexo 2** — DCL | **11 de 14 linhas** |
| **RGF Anexo 3** — garantias | exato |
| **RGF Anexo 4** — limites | exato |
| **RGF Anexo 5** — disponibilidades | **90 de 90 células** e os 5 totais contra o Siconfi |
| **RGF Anexo 6** — limites | exato |
| **RREO Anexos 1, 2, 3, 7, 9, 14** | exatos (2, 7 e 14 também em 2026) |
| **RREO Anexo 4** — previdenciário | 2 de 4 (as outras a 0,02% e 0,15%) |
| **RREO Anexo 13** — PPP | **7 de 7 valores**, projeções exatas |

---

## Como o Anexo 1 é apurado

Não sai da MSC: sai dos relatórios do SIGEF, na ordem do manual da equipe. As
seis seções da MAPA:

| seção | linhas | fonte |
|---|---|---|
| Vencimentos | 8-101 | Comparativo da Despesa |
| Patronal | 102-180 | Comparativo + expurgo por natureza |
| Aposentadorias | 182-208 | Comparativo + IEO 162233 (fontes 0.8.00 e 0.5.00) |
| Pensões | 209-244 | Comparativo + IEO 162233 e 162011 |
| Terceirização | 245-249 | Comparativo |
| Não executada | 250-251 | Balancetes 8.6.3.3.1 |

A trava de conferência: a soma das naturezas do grupo 31 no Comparativo tem de
bater com o GND 31 — e bate.

---

## Documentos que importam

| documento | o que tem |
|---|---|
| [`docs/REVISAO_GERAL.md`](docs/REVISAO_GERAL.md) | **comece aqui** — estado completo, seções 9 a 17 |
| [`docs/DIVERGENCIAS.md`](docs/DIVERGENCIAS.md) | as 9 divergências com causa (gerado do livro) |
| [`docs/MANUAL_MAPA_ANEXO1.md`](docs/MANUAL_MAPA_ANEXO1.md) | especificação da MAPA, linha a linha |
| [`docs/METODOLOGIA_RGF_ANEXO1.md`](docs/METODOLOGIA_RGF_ANEXO1.md) | manual metodológico da equipe |
| [`docs/REGRAS_ANEXOS_RESTANTES.md`](docs/REGRAS_ANEXOS_RESTANTES.md) | regras descobertas para os demais anexos |
| [`docs/PROXIMO_PASSO.md`](docs/PROXIMO_PASSO.md) | o que fazer quando chegar o relatório por fonte |
| [`docs/ENTRADAS_NECESSARIAS.md`](docs/ENTRADAS_NECESSARIAS.md) | o que extrair do SIGEF a cada período |

---

## O que falta

| item | depende de |
|---|---|
| RGF Anexo 2 — RP processados | relatório "Execução Orçamentária por Fonte" (bloco de RP), por Poder |
| RGF Anexo 2 — Disponibilidade e Haveres | **fechadas**; resta a abertura de 8 segmentos dos Depósitos |
| RCL | é **lida** do Anexo 3: o bloco RPPS de deduções não existe na matriz |
| RREO Anexo 4 — 2 linhas | classificação fina de naturezas (0,02% e 0,15%) |

---

## Aviso sobre o restante do repositório

Os **~80 scripts na raiz** além dos listados acima são histórico de
investigação: diagnósticos, tentativas e comparações de sessões anteriores.
Continuam funcionando em parte, mas **não são o caminho atual** e vários apontam
para pastas que não existem mais.

O caminho atual é: `verificar_tudo.py` → `verificacao.py` → os seis módulos por
anexo listados acima.

---

## Dados

As pastas `dados/`, `saida/` e `MDF_STN/` **não são versionadas** (`.gitignore`):
contêm matrizes e relatórios do Estado. O repositório tem só código e
documentação — nenhum dado fiscal.
