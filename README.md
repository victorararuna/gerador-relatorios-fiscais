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

## Motor novo — matrizes MSC de 2025 em diante

A partir de 2025 o Siconfi abandonou o `instancia.csv` e passou a publicar a
matriz em **um arquivo por classe, mês e tipo de saldo**, com os atributos em
colunas próprias (`poder_orgao`, `natureza_despesa`, `natureza_receita`,
`funcao`, `ano_inscricao`). O motor antigo não lê esse formato.

### Módulos

| módulo | função |
|---|---|
| `app/leitor_msc.py` | índice e leitura do formato longo; conferência fluxo × estoque |
| `app/anexo1_msc.py` | RGF Anexo 1 — janela móvel de 12 meses, de-para e deduções |
| `app/relatorio_anexo1.py` | planilha do Anexo 1 com aba de verificações |
| `app/anexo3_msc.py` | RCL do RREO Anexo 3 + RGF Anexo 3 (garantias) |
| `app/anexo4_msc.py` | limites do RGF Anexo 4 (operações de crédito) |
| `app/anexo6_msc.py` | limites do RGF Anexo 6 (despesa com pessoal) |
| `app/regras_anexo1.py` | regras de validação do próprio Siconfi |
| `rreo_anexo1_grupos.py` | RREO Anexo 1 — despesa por grupo, com intra derivada |
| `rreo_anexo1_receita.py` | RREO Anexo 1 — receita nas três bases |
| `rreo_anexo2.py` | RREO Anexo 2 — despesa por função |
| `rreo_anexo7.py` | RREO Anexo 7 — restos a pagar (contas 6.3.1/6.3.2) |
| `rreo_anexo14.py` | RREO Anexo 14 — simplificado (despesa e RCL) |
| `rreo_anexo9.py` | RREO Anexo 9 — despesa de capital empenhada |
| `app/rreo_gerador.py` | apura o bimestre inteiro a partir da MSC |
| `app/rreo_layout.py` | renderiza os anexos no layout oficial (molde = arquivo do Siconfi) |
| `gerar_painel.py` | painel consolidado de verificação em XLSX |

### Como rodar

```bash
python verificar_tudo.py          # 27 conferências de ponta a ponta (sai != 0 se falhar)
python gerar_rreo.py --ano 2026 --bimestre 4   # RREO do bimestre a partir da MSC
python gerar_anexo1.py            # Anexo 1 (2025 Q3, 2026 Q1 e Q2) -> saida/
python gerar_anexo1_poderes.py    # Anexo 1 por Poder (7 POs + consolidado)
python gerar_painel.py            # painel de verificação consolidado
python app/anexo3_msc.py --rreo ... --rgf ...
python app/regras_anexo1.py --raiz <acervo> --ano 2025 --quadrimestre 3
python tests/test_leitor_msc.py   # 41 testes, sem dependência externa
```

### Documentação

| documento | conteúdo |
|---|---|
| [`docs/RELATORIO_FINAL.md`](docs/RELATORIO_FINAL.md) | **consolidação da fase: o que fecha, o que não fecha e por quê** |
| [`docs/LEITOR_MSC.md`](docs/LEITOR_MSC.md) | o formato novo e as duas regras de leitura |
| [`docs/ANEXO1_CALIBRACAO.md`](docs/ANEXO1_CALIBRACAO.md) | calibração do Anexo 1 nas três janelas |
| [`docs/ANEXO2_CALIBRACAO.md`](docs/ANEXO2_CALIBRACAO.md) | por que o Anexo 2 não fecha |
| [`docs/RREO_ANEXO1.md`](docs/RREO_ANEXO1.md) | despesa e receita do Balanço |
| [`docs/RREO_ANEXO2.md`](docs/RREO_ANEXO2.md) | despesa por função e intra derivada |
| [`docs/REGRAS_VALIDACAO_ANEXO1_2026.md`](docs/REGRAS_VALIDACAO_ANEXO1_2026.md) | as 125 regras do Siconfi para o Anexo 1 |
| [`docs/PAINEL_ANEXOS.md`](docs/PAINEL_ANEXOS.md) | situação de cada demonstrativo |

### Resultado em 2025 Q3 / B6

| demonstrativo | desvio |
|---|---:|
| RGF Anexo 1 — Despesa Bruta | −0,36% |
| RGF Anexo 3 — Garantias | 0,00% (5/5 linhas) |
| RGF Anexos 4 e 6 — limites | 0,00% (6/6 linhas) |
| RREO Anexo 1 — despesa | 4 de 6 grupos exatos |
| RREO Anexo 2 — total por função | 0,00% |
| RREO Anexo 3 — RCL | 0,00% (2025 e 2026) |
| RREO Anexo 7 — Restos a Pagar | 0,00% (5/5 linhas) |
| RREO Anexo 14 — Simplificado | 0,00% (6/6 linhas) |
| RREO Anexo 9 — despesa de capital | 0,00% (4/4 linhas) |

---

## Licença

MIT — ver [LICENSE](LICENSE).



