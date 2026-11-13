# Entradas necessárias para gerar todos os relatórios

Lista do que precisa ser extraído do SIGEF/RN (e de onde mais) para o motor gerar
RREO e RGF completos. Organizada por anexo e por rotina de período.

---

## 1. O que já temos (não precisa reenviar)

| item | onde está |
|---|---|
| Matrizes MSC do Siconfi (classes 1, 2, 4, 5, 6, 8) | `dados/acervo` |
| Comparativo da Despesa — jan a out/2026 | `Arquivos etonjones` |
| IEO UG 162233 e UG 162011 — jan a out/2026 | `Arquivos etonjones` |
| Balancetes 8.6.3.3.1.01 e .02 — abertura e jan a mai/2026 | `Arquivos etonjones` |
| Planilha Quadro_e_Mapa 2026 | `Arquivos etonjones` |
| RGF 2º quadrimestre/2026 homologado | `Arquivos etonjones` |
| RREO homologados (CSVs do Siconfi) | `dados/siconfi` |
| Mapeamentos STN (RGF 1-5, RREO 01-13) | `dados/mapeamentos` |
| MDF 15ª edição v8 | `MDF_STN` |

---

## 2. O que falta para fechar os anexos em obra

### 2.1 RGF Anexo 2 — DCL  ⟵ **prioridade de segunda**

**Relatório:** "Imprimir Execução Orçamentária **por Fonte**" — bloco de
**Restos a Pagar**.

| item | exigência |
|---|---|
| Dimensão **Poder** | todos os sete: Executivo, TJ, AL, MP, TCE, DP e FDM |
| Dimensão **fonte de recursos** | obrigatória — é o que o balancete não tem |
| Bloco de RP | inscritos em exercícios anteriores, inscritos no exercício, liquidados de RPNP, pagos de RPP, pagos de RPNP, cancelados de RPP |
| Mês | o de fechamento do quadrimestre (ago/2026 para o 2º Q) |

Sem a dimensão Poder, fecham 8 das 14 linhas. Com os sete Poderes, as 14.

### 2.2 RREO Anexo 13 — PPP

| item | por quê |
|---|---|
| **MSC de dezembro do exercício anterior** | preenche a coluna "31/12 do exercício anterior" (ativos, passivos, garantias) |
| **Valor presente das contraprestações** (âncora de 2027) | hoje R$ 60.190.422,53 — cláusula 25.6 do contrato 001/2011 (Arena das Dunas); recalculado em abril |

A âncora é **um número por ano**; o resto das 24 células sai dela com IPCA e Selic
publicados na nota do anexo.

### 2.3 RGF Anexo 5 — Disponibilidades

Nada a pedir: as três correções (filtro de Poder, classe 8 e espelho da classe 1)
saem das matrizes que já temos.

### 2.4 RREO Anexo 9 — Receita

Nada a pedir: a natureza de receita está na MSC (classe 6). O refinanciamento é
zero no RN.

### 2.5 RCL e limites do RGF Anexo 1

Nada a pedir: o Anexo 3 do RREO já é apurado pelo motor e confere com o homologado.

---

## 3. Rotina por período

### A cada bimestre (RREO)

1. **Comparativo da Despesa** — Poder Executivo, "Apresentar UG Administrativa:
   Não", por Natureza de Despesa e Fonte, **no mês**.
2. **IEO UG 162233** (FUNFIRN) — Gestão 16233, por Subação/Fonte/Elemento,
   "No mês", Fonte Detalhada: Não.
3. **IEO UG 162011** (IPERN) — Gestão 00001, mesmos filtros.
4. **MSC do mês** (download do Siconfi).

### A cada quadrimestre (RGF), além dos itens acima

5. **Execução Orçamentária por Fonte com bloco de RP**, por Poder.
6. **Balancete de encerramento** (conta de 8 segmentos, coluna "Saldo Restante").

### Anualmente, no fechamento

7. **RPNP** — só se apura em 31/12 (Empenhado − Liquidado do ano).
8. **Balancetes 8.6.3.3.1.01 e .02** — abertura e todos os meses até zerar
   (normalmente maio).
9. **MSC de dezembro** do exercício que se encerra.

---

## 4. Cuidados na extração

**Cabeçalho obrigatório.** Todo PDF do SIGEF precisa sair com as linhas
`Ano Base: <ano>` e `Mês Referência: <mês>`. O validador lê essas duas linhas e
**recusa o arquivo** se não conferirem com o período esperado
(`app/fonte_sigef.py`). É a trava que impede uma extração de 2025 entrar na
apuração de 2026.

**Nome do arquivo.** Manter o padrão que já usamos: o mês no nome
(`..._Setembro.pdf`) — é o que o leitor usa para casar arquivo e período.

**Formato.** PDF para os relatórios do SIGEF; as matrizes do Siconfi em CSV
(formato longo). Planilhas em XLSX/XLS.

**Um arquivo por UG e por mês.** Não juntar meses no mesmo PDF.

---

## 5. O que **não** é necessário

- **A planilha da equipe.** O motor já reproduz o Anexo 1 do RGF ao centavo em
  dez meses sem ela. Continua útil como conferência, não como fonte.
- **Os relatórios do SIGEF de 2025** para as janelas móveis: a MSC cobre.
- **Extração manual de valores publicados**: a regra é sempre partir do dado
  bruto.

---

## 6. Para a verificação

Para cada período, o **homologado do Siconfi** (RREO e RGF) do mesmo período. É
contra ele que o motor confere — sem ele, geramos o relatório mas não provamos
que está certo.

---

## Resumo em uma tabela

| anexo | o que falta | esforço |
|---|---|---|
| RGF Anexo 2 | Execução por Fonte + RP, por Poder | extração |
| RREO Anexo 13 | MSC de dez do ano anterior + âncora do contrato | extração + 1 número |
| RGF Anexo 5 | — | só código |
| RREO Anexo 9 | — | só código |
| RCL e limites | — | só código |
| Demais anexos | — | já exatos |
