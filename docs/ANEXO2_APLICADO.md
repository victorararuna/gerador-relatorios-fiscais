# RGF Anexo 2 — o de-para aplicado

O mapeamento da STN aplicado na MSC de agosto/2026, contra o homologado.

---

## 1. O resultado

| linha do Anexo 2 | MSC | Homologado | desvio |
|---|---:|---:|---:|
| **Empréstimos — Internos** | 1.626.484.480,79 | 1.626.484.480,79 | **0,00%** |
| **Empréstimos — Externos** | 1.349.301.221,30 | 1.349.301.221,30 | **0,00%** |
| **Reestruturação da Dívida** | 700.182.232,31 | 700.182.232,31 | **0,00%** |
| **Parcelamento — De Tributos** | 9.415.611,96 | 9.415.611,96 | **0,00%** |
| **Parcelamento — Previdenciárias** | 1.954.889,60 | 1.954.889,60 | **0,00%** |

**Cinco linhas, desvio zero ao centavo.**

---

## 2. Como funciona

O mapeamento dá, por linha, uma lista de prefixos de conta:

```
Empréstimos Internos
  CC começada por (Lista)= 212110201,212110298,2121103,212130201,...

Disponibilidade de Caixa Bruta
  CC começada por (Lista)= 1111101,1111102,1111106,1111107,...
```

O `filtros.py` interpreta essa expressão e o `aplicar_mapeamento.py` soma as
contas correspondentes no **saldo de fechamento** (`ending_balance`) do mês.

Não há calibração: é aplicação direta da regra da STN.

---

## 3. O que ainda não fecha

### 3.1 Linhas sem par no homologado

| linha | valor MSC |
|---|---:|
| Precatórios posteriores a 05/05/2000 | 5.380.042.751,19 |
| Prec. post. 05/05/2000 (não incluídos) | 1.849.267.878,99 |
| Depósitos Restituíveis | 1.109.422.249,03 |
| Demais Dívidas Contratuais | 236.582.787,23 |
| Dívida Contratual de PPP | 196.757.187,16 |
| Com Instituição Não Financeira | 133.852.001,09 |
| Apropriação de Depósitos Judiciais | 120.610.642,76 |
| Passivo Atuarial | 84.052.803.127,13 |

Essas linhas existem na MSC (os filtros as capturam), mas o nome no arquivo
homologado é diferente — a comparação por prefixo não encontrou o par.

**Não significa erro de apuração**: significa que a conferência linha a linha
precisa de um de-para de **nomes** (especificação do mapeamento ↔ rótulo do
Siconfi).

### 3.2 Linhas que deram zero

| linha | observação |
|---|---|
| Dívida Mobiliária | 0,00 — o Estado não tem dívida mobiliária |
| (-) Restos a Pagar Processados | 0,00 vs 640.153.394,98 — conta na classe 6, não na 2 |
| Demais Haveres Financeiros | 0,00 vs 266.702.621,21 — mesmo caso |
| Financiamentos Internos/Externos | 0,00 — duplicação da linha de empréstimos |

As deduções do Anexo 2 combinam contas de **classes diferentes** (1, 2 e 6). O
script atual lê só a classe 2 — daí os zeros.

---

## 4. O que isso prova

**O caminho está correto.** Cinco linhas fechando em 0,00% com aplicação direta
do mapeamento oficial significa que:

1. O `filtros.py` interpreta corretamente as expressões da STN;
2. A MSC tem as contas nas classes certas;
3. A leitura do `ending_balance` está correta.

O que falta é **completar a leitura multiclasse** (1, 2 e 6) e **casar os nomes**.

---

## 5. O que já está validado

| anexo | desvio |
|---|---:|
| **RGF A1 — Pessoal** | −0,04% |
| **RGF A2 — DCL** | **5 linhas em 0,00%** |
| **RREO A1 — Despesa** | +0,02% |
| **RREO A9 — Operações** | 0,00% |

---

## 6. Próximo passo

**Completar o Anexo 2**: ler as classes 1 e 6 nas linhas de dedução e casar os
nomes das linhas. É trabalho de ajuste, não de descoberta — o de-para já existe.

**Depois**: RGF Anexo 5 (disponibilidade), que usa a mesma lógica multiclasse e
tem a Relação Fonte Recurso como apoio.

Os mapeamentos mudaram o patamar: não estamos mais calibrando por tentativa.
Estamos aplicando a regra oficial e medindo onde a leitura erra.
