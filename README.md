# Gerador de Relatórios Fiscais — RREO e RGF do RN

Ferramenta que apura os demonstrativos fiscais do **Rio Grande do Norte** a
partir das **Matrizes de Saldos Contábeis (MSC)** do Siconfi e dos relatórios do
**SIGEF/RN**, e confere cada célula contra o arquivo homologado.

Estado em **23/11/2026**: **605 de 608 células exatas** (99,5%), em 40 abas de
verificação (27 de anexo e uma de resumo). As **3 divergências** estão em
[`docs/DIVERGENCIAS.md`](docs/DIVERGENCIAS.md) — todas o mesmo erro de R$ 5.241,65
no arquivo publicado de abril/2026, provado no MAPA do auditor. O acerto por
relatório está em [`docs/PLACAR.md`](docs/PLACAR.md).

---

## Como rodar

```bash
python verificar_tudo.py    # 30 conferências de ponta a ponta
python verificacao.py       # livro, divergências e certificado
python rodar_testes.py      # 134 testes: quantos executam, quantos pulam
python placar_relatorios.py # docs/PLACAR.md — acerto por relatório
```

Saídas, todas no mesmo comando:

| arquivo | conteúdo |
|---|---|
| `saida/verificacao_anexos.xlsx` | uma aba por anexo |
| `docs/DIVERGENCIAS.md` | as divergências com causa |
| `docs/CERTIFICADO.md` | data, commit, contagem e ressalvas |

### Ambiente

Os módulos do caminho atual resolvem os caminhos por **`caminhos.py`**
(`msc_antiga()`, `siconfi_publicados()`, `arquivos_etonjones()`,
`relatorios_contag()`), que procura em `Downloads`, no workspace e em
`Antigravity`. A pasta original em `AppData\...\Microsoft VS Code` sumiu; dois
reconstutores a substituem dentro do repo:

```bash
python baixar_msc.py          # MSC da API -> dados/acervo
python reconstruir_msc.py     # dados/acervo -> dados/siconfi_rn_msc (formato antigo)
python reconstruir_siconfi.py # dados/siconfi -> dados/siconfi_rn (publicados)
```

As pastas de dados **não são versionadas** (`.gitignore`): um clone do
repositório traz só código e documentação.

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
| **RGF Anexo 2** — DCL | **15 de 16 linhas** + 3 somas · 6 também em 2026 |
| **RGF Anexo 3** — garantias | **5 de 5 linhas** em 2025 · 2 limites em 2026 |
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
| [`docs/INDEX.md`](docs/INDEX.md) | **o mapa dos documentos** — o que é atual, histórico e referência |
| [`docs/PASSAGEM.md`](docs/PASSAGEM.md) | **comece aqui** — estado, motores, armadilhas e ambiente |
| [`docs/PLACAR.md`](docs/PLACAR.md) | acerto por relatório (gerado) |
| [`docs/REVISAO_GERAL.md`](docs/REVISAO_GERAL.md) | o diário completo, seção 2 e a última 17 |
| [`docs/DIVERGENCIAS.md`](docs/DIVERGENCIAS.md) | as 3 divergências com causa (gerado do livro) |
| [`docs/MANUAL_MAPA_ANEXO1.md`](docs/MANUAL_MAPA_ANEXO1.md) | especificação da MAPA, linha a linha |
| [`docs/METODOLOGIA_RGF_ANEXO1.md`](docs/METODOLOGIA_RGF_ANEXO1.md) | manual metodológico da equipe |
| [`docs/REGRAS_ANEXOS_RESTANTES.md`](docs/REGRAS_ANEXOS_RESTANTES.md) | regras descobertas para os demais anexos |
| [`docs/PROXIMO_PASSO.md`](docs/PROXIMO_PASSO.md) | o que fazer quando chegar o relatório por fonte |
| [`docs/ENTRADAS_NECESSARIAS.md`](docs/ENTRADAS_NECESSARIAS.md) | o que extrair do SIGEF a cada período |

---

## O que falta

| item | depende de |
|---|---|
| **de-para de nomes do Anexo 2** no `gerar_rgf_rn.py` | tabela de correspondência (~20 linhas); o motor exato já fecha em 0,00 |
| **RREO no molde do gerador** | reaproveitar a estrutura do `gerar_rgf_rn.py` |
| **Anexo 1 e 2 só da matriz** | subelemento do ND + classe 2 detalhada na MSC (pedido ao Estado) |

Todo o resto fecha: **605 de 608 células** contra os arquivos publicados; as 3
divergências são o erro de R$ 5.241,65 do publicado em abril/2026.

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
contêm matrizes e relatórios do Estado.

Conferido em 23/11/2026: o repositório tem **173 arquivos `.py` e 71 `.md`**, mais
três `.bat` e dois PDFs de leiaute da STN — **nenhum CSV, planilha ou PDF de
dado fiscal**. Os dados ficam em `dados/` (não versionado).

Os únicos arquivos de dado são os dois leiautes em `docs/_apoio/` (formato da MSC),
que são públicos.
