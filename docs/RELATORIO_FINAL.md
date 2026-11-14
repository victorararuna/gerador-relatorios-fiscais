# Relatório final da fase — motor de demonstrativos fiscais sobre a MSC

> **Documento histórico.** Os números e as pendências abaixo **não valem mais**:
> o Anexo 1 passou a fechar em 10 de 10 meses, o Anexo 5 chegou a 90 de 90
> células, o Anexo 4 fechou e a DCL está em 15 de 16 linhas.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2** —
> ou, melhor, abra `saida/verificacao_anexos.xlsx`, que é gerado do código.

---


Documento de encerramento da fase. Consolida o que foi construído, o que fecha,
o que não fecha e por quê. Dados de referência: RGF 2025 Q3 e RREO 2025 B6,
conferidos contra os arquivos homologados do Siconfi.

---

## 1. O que mudou na fonte

A partir de 2025 o Siconfi abandonou o `instancia.csv` e passou a publicar a
Matriz de Saldos Contábeis em **um arquivo por classe, mês e tipo de saldo**,
com os atributos em colunas próprias — `poder_orgao`, `natureza_despesa`,
`natureza_receita`, `fonte_recursos`, `funcao`, `ano_inscricao`.

Isso resolveu três lacunas históricas do projeto original:

| lacuna antiga | como a matriz nova resolve |
|---|---|
| Poderes ausentes / rótulos minerados do DOE | `poder_orgao` e `funcao` explícitos |
| Anexo 4 impossível ("a MSC só traz natureza da despesa") | `natureza_receita` na classe 5 |
| Restos a pagar sem ano de inscrição | `ano_inscricao` |

E criou duas exigências novas, documentadas em `LEITOR_MSC.md`:

1. `ending_balance` é saldo; `period_change` é movimento. A despesa líquida
   (créditos − débitos) só existe no movimento.
2. O Anexo 1 do RGF é **janela móvel de 12 meses**, não acumulado do ano.

---

## 2. Arquitetura

```
app/leitor_msc.py        índice + leitura + conferência fluxo x estoque
app/anexo1_msc.py        RGF Anexo 1 (janela móvel, de-para, deduções)
app/anexo3_msc.py        RCL do RREO Anexo 3 + RGF Anexo 3
app/anexo4_msc.py        limites do RGF Anexo 4
app/anexo6_msc.py        limites do RGF Anexo 6
app/regras_anexo1.py     regras de validação do Siconfi
app/relatorio_anexo1.py  planilha do Anexo 1 + verificações
rreo_anexo1_grupos.py    RREO Anexo 1 — despesa por grupo
rreo_anexo1_receita.py   RREO Anexo 1 — receita nas três bases
rreo_anexo2.py           RREO Anexo 2 — despesa por função
verificar_tudo.py        27 conferências de ponta a ponta
```

Duas camadas de verificação: **41 testes unitários** e **23 conferências contra
o homologado**.

---

## 3. O que fecha

| demonstrativo | resultado |
|---|---|
| RREO — total de despesas liquidada | 23.361.499.529,63 — **0,00** |
| RREO Anexo 3 — RCL (2025 e 2026) | **0,00** nas cinco linhas |
| RGF Anexo 3 — garantias | **0,00** nas cinco linhas |
| RGF Anexo 4 — limites (7%, 16%, 90%) | **0,00** |
| RGF Anexo 6 — limites (49%, 46,55%, 44,10%) | **0,00** |
| RREO Anexo 2 — total por função | **0,00** (23 funções) |
| RREO Anexo 1 — 4 grupos sem intra | **0,00** (juros, investimentos, inversões, amortização) |
| RREO Anexo 7 — restos a pagar | **0,00** nas cinco linhas |
| RREO Anexo 14 — despesa e RCL | **0,00** nas seis linhas |
| RREO Anexo 9 — despesa de capital | **0,00** nas quatro linhas |
| RGF Anexo 1 — despesa bruta | **−0,36%** |
| RGF Anexo 1 — despesa líquida | +0,78% |

O padrão é claro: **tudo que deriva da RCL fecha ao centavo**; o que deriva da
despesa fecha ou fica abaixo de 1%.

---

## 4. O que não fecha — quatro causas, nenhuma de cálculo

### 4.1 Mapeamento de contas da STN (RGF Anexos 2 e 5)

O MDF descreve o significado das linhas, não o de-para de contas. Os
"mapeamentos" ficam na aba de anexos do sisweb, que estava fora do ar na coleta
do acervo e não respondeu nas tentativas seguintes.

- **Anexo 2**: o mapa de 2024 reproduz abril (+1,01%) e agosto (+1,60%) de 2025,
  mas quebra em dezembro (−11,39%) — salto de precatórios (+R$ 2,65 bi) e nova
  "Outras Dívidas" (R$ 941,9 mi).
- **Anexo 5**: a conta que o MDF cita (8.2.1.7.4.01) não existe no plano novo;
  as contas de controle `8.2.1.1.x` trazem a fonte de recursos (96 fontes), mas
  o de-para FR → categoria não é público.

### 4.2 Atributo de intra-orçamentária (despesa)

A matriz não identifica o que é intra. Consequências:

- **RREO Anexo 1**: 4 de 6 grupos fecham; Pessoal e Outras Correntes carregam
  toda a intra (R$ 2,617 bi + R$ 47,45 mi), derivada por diferença.
- **RREO Anexo 2**: o total fecha; a intra por função foi derivada (Previdência
  concentra 54%).

### 4.3 Critério de apuração da receita (RREO Anexo 1 — receita)

A cadeia do RREO está inteiramente reconciliada:

```
26.656.696.864,94 (bruto)
- 2.733.005.621,51 (transferências constitucionais)
- 3.175.469.290,58 (FUNDEB)
= 20.748.221.952,85 (Anexo 1)
- 1.110.322.676,50 - 115.005.627,07 - 9.046.989,30
= 19.513.846.659,98 (RCL)
```

A matriz abate **86%** dessas deduções; faltam R$ 827,6 mi (15,5%), sem conta
localizada.

### 4.4 Corte civil/militar e operação nova
- **RREO Anexo 4**: a patronal do RPPS é receita intra (`7215` — 2.500,46 mi
  contra 2.490,85 homologados, +0,39%); as despesas exigem separar civil de
  militar, atributo que a matriz não tem.
- **RGF Anexo 4**: a receita `17115001` tem R$ 6,70 bi contra R$ 2,49 mi de
  operações declaradas — falta separar operação nova de refinanciamento.

**Confirmação pelo RREO Anexo 9**: o demonstrativo das operações de crédito
declara exatamente **R$ 2.491.012,67** de receita realizada — o mesmo número do
RGF Anexo 4. Busquei esse valor na matriz, por natureza e por Poder, com
tolerância de R$ 50 mil: **não existe**. A natureza `17115001` registra
R$ 6,70 bi brutos.

Ou seja: os dois demonstrativos contam só a operação **nova**; a matriz registra
a **entrada financeira**, que inclui refinanciamento e rolagem. A distinção não é
atributo do dado — é decisão de apuração que o ente toma fora da matriz.

---

## 5. O que é preciso para terminar

| pendência | insumo necessário | disponível? |
|---|---|---|
| RGF Anexos 2 e 5 | mapeamento de contas da STN | 🔒 não (sisweb 503) |
| RREO Anexo 1 receita | memória de cálculo das deduções | 🔒 não |
| RREO Anexo 4 despesas | atributo civil/militar | 🔒 não na matriz |
| RGF Anexo 4 operações | atributo de refinanciamento | 🔒 não na matriz |
| RGF Anexo 1 linhas | linha de exercícios anteriores do homologado é repetida | ⚠️ dado oficial inconsistente |
| Anexo 1 por Poder (6 Poderes) | RGF de L/J/M/D | 🔒 API vazia |

Nenhuma pendência é de cálculo. Todas são de **dado de entrada indisponível**.

---

## 6. Como verificar

```bash
python verificar_tudo.py         # 27 conferências de ponta a ponta
python tests/test_leitor_msc.py  # e os outros três arquivos de teste
python gerar_painel.py           # saida/Painel_Verificacao_2025Q3.xlsx
```

Os artefatos estão em `saida/`:
`RGF_2025_Q3_Anexo01_MSC.xlsx`, `RGF_2026_Q1_Anexo01_MSC.xlsx`,
`RGF_2026_Q2_Anexo01_MSC.xlsx`, `RGF_2025_Q3_Anexo01_Poderes.xlsx`,
`RGF_2026_Q2_Anexo01_Poderes.xlsx`, `Painel_Verificacao_2025Q3.xlsx`.



