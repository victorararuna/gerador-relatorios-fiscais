# Lista exata do que preciso — e o estado de cada anexo

Documento de handoff. Abaixo o que já fecha, o que falta e o que só você pode
fornecer.

---

## 1. O QUE JÁ FECHA

| anexo | desvio | como |
|---|---:|---|
| **RGF Anexo 1 — Pessoal** | **−0,04%** | MSC classes 3/4/6 + balancete + de-para de naturezas |
| **RGF Anexo 2 — DCL** | **12 linhas em 0,00%** | MSC classes 1/2/6 + mapeamento STN |
| **RREO Anexo 1 — Receita** | **41 linhas em 0,00%** | MSC classe 6 + mapeamento STN (conta + natureza) |
| **RREO Anexo 1 — Despesa** | **+0,02%** | MSC classe 6 (conta 622130400) |
| **RREO Anexo 9 — Operações** | **0,00%** | Comparativo da Receita (rubrica 4.2.1) |

**Cinco anexos validados contra o homologado.**

---

## 2. O QUE FALTA — E O QUE VOCÊ PRECISA ENTREGAR

### 2.1 Para o fechamento do dia 16 (setembro e outubro)

| # | item | formato | para quê |
|---|---|---|---|
| **1** | **MSC de setembro/2026** | `24EX-2026-09-XXX.csv` | Anexo 1 do RGF Q3 |
| **2** | **MSC de outubro/2026** | `24EX-2026-10-XXX.csv` | idem |

**Formato**: o antigo, de 16 colunas (`CONTA;IC1;TIPO1;...;Valor;Tipo_valor;Natureza_valor`).
O conversor está pronto.

**Periodicidade**: um arquivo por mês.

---

### 2.2 Para destravar o RREO Anexo 3 (RCL)

| # | item | por quê |
|---|---|---|
| **3** | **MSC de janeiro a junho/2026 com todas as classes** | só tenho jul/ago da classe 5. O A3 precisa da janela de 12 meses |
| **4** | **Confirmação do critério de exclusão das naturezas `7xxx`** | o A3 fica +14% porque as intra entram; o Anexo 1 as exclui com `NR começada por 1,2` |

**Se o item 3 não vier**: o A3 pode ser feito só para jul/ago (2 meses), mas não
fecha a janela.

---

### 2.3 Para o RGF Anexo 2 terminar de fechar

| # | item | por quê |
|---|---|---|
| **5** | **De-para de nomes** — especificação do mapeamento ↔ rótulo do Siconfi | as linhas "Precatórios", "Depósitos Restituíveis" e "Demais Dívidas" existem na MSC mas o nome no homologado é diferente |
| **6** | **Confirmação da linha de Precatórios** | dá +8,86% (R$ 456 mi); o filtro inclui a conta `1135108` que pode ser de outra linha |

---

### 2.4 Para o RREO Anexo 2 (Despesa por Função)

| # | item | por quê |
|---|---|---|
| **7** | **MSC com o atributo `funcao` preenchido** | a matriz de 16 colunas não traz; o formato longo traz |

**Como pedir**: na consulta da MSC, marcar a coluna de função, ou exportar no
formato longo (`MSC_24_2026_m..._msc_orcamentaria_classe6_...`).

---

### 2.5 Para o RREO Anexo 4 (Previdenciário)

| # | item | por quê |
|---|---|---|
| **8** | **Separação civil × militar da despesa previdenciária** | a MSC não tem esse atributo |

**Alternativa**: o relatório "Despesa com Pessoal por Poder e Tipo de Servidor"
do SIAFIC.

---

### 2.6 Para o RGF Anexo 5 (Disponibilidade)

| # | item | por quê |
|---|---|---|
| **9** | **Nada** — os dados existem | o mapeamento tem 6 colunas com filtros próprios; é implementação minha |

---

## 3. RESUMO — O QUE SÓ VOCÊ PODE ENTREGAR

| prioridade | item | destrava |
|---|---|---|
| **1** | MSC de **setembro** | fechamento dia 16 |
| **2** | MSC de **outubro** | fechamento dia 16 |
| **3** | MSC de **jan–jun/2026 completa** | RREO A3 (RCL) |
| **4** | De-para de **nomes** do Anexo 2 | RGF A2 completo |
| **5** | MSC com **`funcao`** | RREO A2 |
| **6** | **Civil × militar** | RREO A4 |

---

## 4. O QUE É TRABALHO MEU (não precisa entregar)

| item | anexo | esforço |
|---|---|---|
| Cálculo mensal (12 colunas) | RREO A3 | 1 dia |
| Exclusão das `7xxx` na receita | RREO A3 | meio dia |
| Interpretador de sinal (`+`/`-`) | RREO A6 | 1 dia |
| Ler as 6 colunas do mapeamento | RGF A5 | 1 dia |
| Casar nomes (normalização) | RGF A2 | meio dia |

---

## 5. ESTADO POR ANEXO

| anexo | situação | falta |
|---|---|---|
| **RGF A1** | ✅ −0,04% | — |
| **RGF A2** | ✅ 12 linhas em 0,00% | de-para de nomes (item 5) |
| RGF A3 | ⚠️ não testado | — |
| RGF A4 | ⚠️ não testado | — |
| RGF A5 | ⚠️ interpretador pronto | ler as 6 colunas |
| RGF A6 | ⚠️ herda | — |
| **RREO A1 — receita** | ✅ 41 linhas em 0,00% | — |
| **RREO A1 — despesa** | ✅ +0,02% | — |
| RREO A2 | ❌ | `funcao` (item 7) |
| RREO A3 | ⚠️ +14,28% | MSC jan–jun + exclusão 7xxx |
| RREO A4 | ❌ | civil/militar (item 8) |
| RREO A5 | **não existe** | — |
| RREO A6 | ⚠️ estrutura lida | sinal |
| RREO A7 | ⚠️ estrutura lida | `ano_inscricao` |
| **RREO A9** | ✅ 0,00% | — |
| RREO A11 | ⚠️ sem critério de conta | mapeamento usa fórmula |
| RREO A12 | ⚠️ mapeamento existe | igual ao A4 (civil/militar) |
| RREO A13 | ⚠️ | cadastro de PPP |

---

## 6. O QUE ISSO SIGNIFICA PARA O PRAZO

**Para o dia 16**, com setembro e outubro:

| entrega | depende de |
|---|---|
| **RGF A1 do Q3** | MSC set/out (itens 1 e 2) |
| RREO A1 despesa | MSC set/out |

**Cinco anexos**: dois do RGF, três do RREO. É o que dá para levar ao teste com
os auditores.

**Para depois do dia 16**, com os itens 3 a 8: mais seis anexos.

---

## 7. O QUE EU RECOMENDO PARA O TESTE

Levar **só o que fecha**:

1. RGF Anexo 1 — 18 linhas, −0,04%
2. RREO Anexo 1 — receita (41 linhas) e despesa
3. RREO Anexo 9

**Não levar** os que estão em construção. Um relatório que não fecha desgasta a
confiança no que fecha.
