# Gerador de Relatórios Fiscais — RREO e RGF (MDF/Siconfi)

Ferramenta que **lê as Matrizes de Saldos Contábeis (MSC)** do Siconfi e gera os
demonstrativos do **Relatório de Gestão Fiscal (RGF)** no layout oficial, com aba
de conferência linha a linha.

Nascida do trabalho real de apuração do RGF 2024 do Estado do Rio Grande do
Norte — cada regra de negócio aqui foi validada contra o relatório homologado no
Siconfi.

---

## O problema que ela resolve

O arquivo consolidado do RGF no Siconfi **não traz rótulos de linha** e o
relatório "Comparativo da Despesa" do SIAFEM tem **R$ 2,1 bilhões de despesa sem
classificação de natureza**. Apurar o Anexo 1 por esses caminhos produz erro.

A Matriz de Saldos Contábeis, por outro lado, tem tudo: **PO** (Poder/Órgão),
**ND** (natureza da despesa), **FR** (fonte de recurso) e **CO** (classificação
orçamentária) em cada lançamento. É dela que a ferramenta parte.

---

## Como usar

### Janela

Duplo clique em **`gerar_relatorios.bat`** → escolher a pasta das matrizes →
**Gerar relatórios**.

### Linha de comando

```bash
python gerar_relatorios.py --entrada "C:\caminho\das\matrizes"
python gerar_relatorios.py --entrada "..." --saida "..." --exercicio 2024 --quadrimestre 3
```

A pasta é varrida recursivamente. O programa lê a primeira linha de cada arquivo
(`24EX;2024-12`) e identifica exercício e mês sozinho — **não depende do nome dos
arquivos**.

### O que a pasta precisa ter

| Matriz | Situação |
|---|---|
| **Dezembro do exercício** | **obrigatória** — base do RGF |
| Dezembro do ano anterior | opcional — saldo do exercício anterior |
| Abril e agosto | opcional — colunas dos quadrimestres |
| As 12 mensais | opcional — colunas mensais do Anexo 1 |

---

## O que é gerado

`RGF_<ano>_Q<quadrimestre>_STN.xlsx`, com sete abas:

| Aba | Conteúdo |
|---|---|
| `RGF-Anexo 01` | Despesa com Pessoal — 18 linhas, 12 colunas mensais e apuração do limite |
| `RGF-Anexo 02` | Dívida Consolidada Líquida — 42 linhas, 4 colunas de quadrimestre |
| `RGF-Anexo 03` | Garantias e Contragarantias |
| `RGF-Anexo 04` | Operações de Crédito |
| `RGF-Anexo 05` | Disponibilidade de Caixa e Restos a Pagar |
| `RGF-Anexo 06` | Demonstrativo Simplificado |
| `Verificações` | Conferência com semáforo: verde até 2%, amarelo até 10%, vermelho acima |

---

## A regra que faz a diferença

As contas de liquidação do Anexo 1 são de **variação patrimonial diminutiva**:

```
6.2.2.1.3.03.00   crédito empenhado liquidado a pagar
6.2.2.1.3.04.00   crédito empenhado liquidado pago
6.2.2.1.3.07.00   empenhos liquidados inscritos em RP processados
```

A despesa é o **movimento credor líquido**:

```
despesa = créditos − débitos
```

Os débitos são estornos e baixas por pagamento. **Somar o valor absoluto de cada
lançamento duplica a despesa** — foi o erro que manteve a apuração R$ 1,4 bilhão
acima do homologado na linha de obrigações patronais.

Outras regras validadas (ver [`docs/MAPEAMENTO_STN_ANEXO1.md`](docs/MAPEAMENTO_STN_ANEXO1.md)):

- recorte do Executivo: POs `10111` + `10112` + `60611`;
- aposentadorias e pensões com filtro de **CO** (1111, 1151, 2111, 2151 ou vazio);
- dedução dos vinculados pela **FR 18xx** com filtro de CO;
- piso da enfermagem a **90%** da fonte 0.605 em 2024 (ADCT art. 38, § 2º — tabela
  progressiva: 100% em 2022-23, 90% em 2024, 80% em 2025…);
- limite do Executivo: **49%** da RCL ajustada (Resolução do Senado 40/2001), não 60%.

---

## O que a ferramenta **não** faz

Escopo declarado para não gerar expectativa errada:

| Item | Motivo |
|---|---|
| **RREO** | não vem da MSC — os anexos estão no arquivo do Siconfi |
| Anexos 8 e 12 do RREO | vão para o **SIOPE** (Educação) e o **SIOPS** (Saúde), não para o Siconfi |
| RGF Anexo 4 e 6 — operações de crédito | a MSC traz a natureza da **despesa**, não a da **receita** |
| RGF Anexo 5 — disponibilidade por fonte | a conta 8.2.1.7.4.01 vem sem saldo na matriz |

---

## Estrutura

```
gerar_relatorios.py          entrada — CLI e janela Tkinter
gerar_relatorios.bat         atalho Windows
main.py                      entrada legada (leitura dos rascunhos Siconfi)

app/
  pipeline.py                lê as matrizes, monta o conjunto e orquestra
  leitor_xls.py              leitor .xls em Python puro (CFB/OLE2 + BIFF8)
  leitor_pdf.py              extrator de texto de PDF com posição (x, y)
  msc_pessoal.py             apuração do Anexo 1 (despesa com pessoal)
  msc_dcl.py                 apuração do Anexo 2 (dívida consolidada)
  colunas_mensais.py         colunas mensais do Anexo 1
  colunas_quadrimestre.py    colunas dos quadrimestres
  colunas_garantias.py       colunas do Anexo 3
  layout_stn.py              estrutura dos seis anexos e valores de referência
  gerar_oficial.py           monta o XLSX e a aba de verificações
  gerar_stn.py               apuração e geração
  gerar_rreo.py              geração do RREO a partir do arquivo do Siconfi
  gerar_rreo_doe.py          extração dos anexos do DOE por coordenada X
  modelo.py                  domínio: Documento, Anexo, Bloco, Linha, Coluna
  rascunho.py                parser dos rascunhos Siconfi
  catalogo.py                rótulos minerados por anexo
  validacao.py               motor de conferência
  ui.py                      interface legada

ferramentas/
  descobrir_rotulos.py       minera rótulos oficiais das planilhas de trabalho

docs/
  MAPEAMENTO_STN_ANEXO1.md   mapeamento completo do Anexo 1 (STN + prática do RN)
  STATUS_FINAL.md            o que fecha, o que falta e o dado que cada lacuna exige
  ESTRUTURA_RREO.md          os 11 anexos do RREO segundo o guia do Siconfi
  ANEXO2_DCL.md              Dívida Consolidada Líquida
  ANEXO3_GARANTIAS.md        Garantias e contragarantias
  ANEXO4_OPERACOES.md        Operações de crédito
  EXTRACAO_DOE.md            extração de tabelas impressas por coordenada X
  INVESTIGACAO_VENCIMENTOS.md a caça aos R$ 86 milhões
  PLANO.md                   plano por fases
```

---

## Requisitos

- Python 3.10+
- `openpyxl`
- Tkinter (já vem com o Python no Windows)

```bash
pip install -r requirements.txt
```

Sem `pandas`, sem `xlrd`, sem `PyPDF2`: o leitor de `.xls` e o extrator de PDF são
**implementados no projeto, em Python puro**.

---

## Resultado da validação

Contra o RGF 2024 Q3 homologado no Siconfi:

| Anexo | Desvio |
|---|---|
| Anexo 2 — DCL | **+0,01%** |
| Anexo 3 — Garantias | **0,00%** |
| Anexo 1 — Despesa Bruta | −0,64% |
| Anexo 1 — Deduções | −0,19% |
| Anexo 1 — Despesa Líquida | −0,81% |

**24 de 30 verificações conferem** (desvio até 2%). As seis restantes estão
documentadas em [`docs/STATUS_FINAL.md`](docs/STATUS_FINAL.md), com a causa e o
dado específico que cada uma exige.

---

## Licença

MIT — ver [LICENSE](LICENSE).
