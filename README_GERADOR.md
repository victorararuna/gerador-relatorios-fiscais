# Gerador de Relatórios Fiscais

Ferramenta que recebe as **Matrizes de Saldos Contábeis (MSC)** e gera os
demonstrativos do **RGF** no layout oficial do Siconfi, com aba de verificações.

---

## Como usar

### Opção 1 — janela (mais simples)

Dê duplo clique em **`gerar_relatorios.bat`**.

1. Clique em **Procurar…** e escolha a pasta onde estão as matrizes.
2. Confira a pasta de saída (padrão: `saida/`).
3. Clique em **Gerar relatórios**.

O programa lê a primeira linha de cada arquivo (`24EX;2024-12`), identifica o
exercício e o mês, e monta o relatório sozinho.

### Opção 2 — linha de comando

```bat
python gerar_relatorios.py --entrada "C:\caminho\das\matrizes"
python gerar_relatorios.py --entrada "..." --saida "..." --exercicio 2024
```

Também aceita `--quadrimestre 1|2|3` (padrão: 3).

---

## O que a pasta de entrada precisa ter

A ferramenta varre a pasta **recursivamente** e reconhece cada `instancia.csv`
pela sua primeira linha. A organização não importa — pode estar em subpastas,
com qualquer nome de arquivo.

| Arquivo | Para que serve |
|---|---|
| Matriz de **dezembro** do exercício | **obrigatória** — base do RGF |
| Matriz de **dezembro** do ano anterior | opcional — coluna "Saldo do Exercício Anterior" |
| Matriz de **abril** | opcional — coluna "Até o 1º quadrimestre" |
| Matriz de **agosto** | opcional — coluna "Até o 2º quadrimestre" |
| Matrizes **mensais** (12) | opcional — colunas mensais do Anexo 1 |

Sem as opcionais, o relatório sai com as colunas que existirem preenchidas. Com
todas, sai completo.

---

## O que é gerado

Um arquivo `RGF_<ano>_Q<quadrimestre>_STN.xlsx` com sete abas:

| Aba | Conteúdo |
|---|---|
| `RGF-Anexo 01` | Despesa com Pessoal — 18 linhas, 12 colunas mensais, TOTAL e apuração do limite |
| `RGF-Anexo 02` | Dívida Consolidada Líquida — 42 linhas, 4 colunas de quadrimestre |
| `RGF-Anexo 03` | Garantias e Contragarantias — 31 linhas |
| `RGF-Anexo 04` | Operações de Crédito |
| `RGF-Anexo 05` | Disponibilidade de Caixa e Restos a Pagar |
| `RGF-Anexo 06` | Demonstrativo Simplificado |
| `Verificações` | Conferência linha a linha com semáforo (verde até 2%, amarelo até 10%, vermelho acima) |

---

## Como o cálculo funciona

### Anexo 1 — Despesa com Pessoal

A despesa é apurada nas contas de liquidação:

```
6.2.2.1.3.03.00  crédito empenhado liquidado a pagar
6.2.2.1.3.04.00  crédito empenhado liquidado pago
6.2.2.1.3.07.00  empenhos liquidados inscritos em RP processados
```

O recorte é o **Poder Executivo**: POs `10111` (Governo), `10112` (RPPS) e
`60611` (Defensoria).

**Ponto crítico:** essas contas são de **variação patrimonial diminutiva** — a
despesa é o **movimento credor líquido** (`créditos − débitos`). Somar o valor
absoluto de cada lançamento duplica a despesa, porque os débitos são estornos e
baixas por pagamento.

Cada natureza é classificada na linha do Anexo 1 conforme o mapeamento do
Módulo 16 da STN (ver `docs/MAPEAMENTO_STN_ANEXO1.md`).

### Anexo 2 — DCL

A dívida consolidada é a soma das contas de passivo da dívida fundada (2.2.1,
2.2.2, 2.2.3 e demais obrigações), e as deduções vêm das contas de haveres.
O Anexo 2 **abrange todos os Poderes** — não se aplica o recorte por PO.

### Colunas mensais

O movimento de cada mês é a **diferença entre saldos acumulados consecutivos**.
Usar o `period_change` diretamente duplica, porque as contas 6.2.2.1.3.03 e .04
se sobrepõem no mesmo lançamento.

A soma das 12 colunas é escalada para fechar exatamente com o TOTAL apurado, o
que preserva o perfil mensal dos dados e garante a consistência interna.

---

## O que a ferramenta **não** faz

| Item | Motivo |
|---|---|
| **RREO** | não vem da MSC: os anexos estão no arquivo do Siconfi (`SICONFI_RREO_*.xls`) |
| **Anexos 8 e 12 do RREO** | vão para o SIOPE (Educação) e o SIOPS (Saúde), não para o Siconfi |
| **Operações de crédito (RGF 4 e 6)** | a MSC traz a natureza da despesa, não a da receita |
| **Disponibilidade por fonte (RGF 5)** | a conta 8.2.1.7.4.01 vem sem saldo na matriz |

---

## Estrutura do código

```
gerar_relatorios.py         entrada (CLI e janela)
gerar_relatorios.bat        atalho Windows
app/pipeline.py             lê as matrizes, monta o conjunto e orquestra
app/msc_pessoal.py          apuração do Anexo 1
app/msc_dcl.py              apuração do Anexo 2
app/colunas_mensais.py      colunas mensais do Anexo 1
app/colunas_quadrimestre.py colunas dos quadrimestres (Anexos 2 e 3)
app/colunas_garantias.py    colunas do Anexo 3
app/layout_stn.py           estrutura dos seis anexos
app/gerar_oficial.py        monta o XLSX e a aba de verificações
app/gerar_stn.py            apuração e geração
```

---

## Requisitos

- Python 3.10 ou superior
- `openpyxl` (para gerar o XLSX)
- Tkinter (para a janela; já vem com o Python no Windows)

Não usa `pandas`, `xlrd` nem qualquer biblioteca de leitura de Excel: o leitor
de `.xls` e de PDF é próprio, em Python puro.
