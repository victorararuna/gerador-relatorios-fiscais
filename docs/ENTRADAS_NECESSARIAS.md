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

**Situação:** 15 das 16 linhas do DCL já fecham ao centavo contra o arquivo
publicado. Falta **uma**: `(-) Restos a Pagar Processados`.

**Relatório:** "Imprimir Execução Orçamentária **por Fonte**" — bloco de
**Restos a Pagar**.

| item | exigência |
|---|---|
| Conta | **6.3.2.1.1** (RP processados inscritos) — não a conta-pai 6.3.2.1.0 |
| Dimensão **Poder** | todos os sete: Executivo, TJ, AL, MP, TCE, DP e FDM |
| Dimensão **fonte de recursos** | obrigatória — é o que o balancete não tem |
| Data | **31/12/2025** (fechamento do 3º quadrimestre) |
| Escopo | incluir a **inscrição do exercício** e excluir o que já foi pago |

### Por que a data importa

Em agosto/2025 a nossa conta quase fecha (3,4% de diferença). Em dezembro a
diferença salta para 37%, porque é o momento em que os empenhos não pagos viram
RP. Pedir o saldo em outra data devolve um número que não serve.

### O que já sabemos e não precisa ser reenviado

| item | valor |
|---|---:|
| estoque de RP de exercícios anteriores (2017–2024) | 470.465.377,32 |
| inscrição de 2025 (vista em 01/2026) | 1.005.773.328,13 |
| o que o DCL publica em 31/12/2025 | 750.866.596,13 |

O publicado fica **entre** os dois — é um recorte que combina estoque e
inscrição. A abertura por Poder e fonte é o que permite reproduzi-lo.

### 2.1b RGF Anexo 1 de 2025 — **opcional** (2 células)

O Anexo 1 de **2026** fecha porque é apurado pela MAPA do SIGEF. O de **2025**
está sendo apurado pela via da MSC (`apurar_janela`), e por isso desvia:

| linha | apurado pela MSC | publicado (2025) | desvio |
|---|---:|---:|---:|
| Despesa bruta (I) | 15.422.754.491,59 | 15.478.621.265,08 | −55.866.773,49 |
| Despesa líquida (III) | 11.086.434.730,47 | 11.001.153.864,38 | +85.280.866,09 |

**O que resolveria:** os mesmos três relatórios do SIGEF, mas de **2025** —
Comparativo da Despesa, IEO 162233 e IEO 162011, mês a mês.

Não é urgente: o Anexo 1 de **2026**, que é o do exercício corrente, já fecha em
10 de 10 meses. Mas com a MAPA de 2025 as duas linhas acima fechariam também.

### 2.2 RREO Anexo 13 — PPP

**Nada a pedir.** Fechado.

| item | situação |
|---|---|
| MSC de dezembro do exercício anterior | já temos — reproduz os três saldos ao centavo |
| Âncora das contraprestações (R$ 60.190.422,53) | **parametrizada** em `rreo_anexo13.ANCORA_ARENA`, com IPCA e Selic publicados na nota |

Conferido: **7 valores e 6 projeções**, todos exatos contra o homologado.

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



---

## 7. Anexo 2 — o que já foi resolvido e o que falta (13/11/2026)

| linha | situação | o que falta |
|---|---|---|
| Empréstimos Internos | **exata** (conta-pai 2.1.2.1.1.02) | — |
| Empréstimos Externos, Reestruturação, Tributos, Contribuições, FGTS, Instituição Não Financeira | **exatas** | — |
| **Demais Haveres Financeiros** | **exata** (PO 10111 + conta 121310199) | — |
| Demais Dívidas Contratuais | 272,3 mi contra zero publicado | decisão de classificação do ente |
| Disponibilidade de Caixa Bruta | 1,85 mi | escopo de conta no Executivo |
| (−) Depósitos Restituíveis | 54,9 mi | **abertura de 8 segmentos por fonte** (bloco IPERN) |
| (−) Restos a Pagar Processados | 4,06 bi | relatório por fonte (bloco de RP) |

Duas das cinco linhas que faltavam fecharam em 13/11. Das três restantes, uma
espera o relatório e duas esperam a abertura de conta da equipe.
