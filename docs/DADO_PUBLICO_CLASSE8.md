# Onde está o dado que falta (classe 8 e ending_balance)

Pergunta: existe dado público com a despesa não executada e o saldo de
fechamento?

**Sim — o Siconfi publica a MSC completa.** O acervo que temos é um recorte.

---

## 1. O que o Siconfi publica

O leiaute oficial (`Matriz_de_Saldos_Contabeis_Informacoes_auxiliares_sobre_o_leiaute.pdf`,
p. 7) define três tipos de valor por conta:

| tipo | significado |
|---|---|
| `beginning_balance` | saldo inicial do período |
| `period_change` | **movimentação** dentro do período, com natureza devedora e credora |
| `ending_balance` | saldo final do período |

E a matriz cobre **todas as classes contábeis**:

| classe | conteúdo |
|---|---|
| 1 | Ativo |
| 2 | Passivo |
| 3 | Variações patrimoniais diminutivas (despesa) |
| 4 | Variações patrimoniais aumentativas (receita) |
| 5 | Controles orçamentários (receita) |
| 6 | Controles orçamentários (despesa) |
| 7 | Controles devedores |
| **8** | **Controles credores — inclui a 8.6.3.3.1.00.00** |
| 9 | Contas compensadas |

## 2. O que o acervo local tem

| item | disponível |
|---|---|
| classes | **3, 4 e 6** apenas |
| tipos de valor | **`period_change` apenas** |
| `ending_balance` | ❌ |
| classe 8 | ❌ |

É um recorte: serve para apurar a despesa liquidada (classe 6, movimento), mas
não para a conta de controle da despesa não executada (classe 8) nem para
conferir fluxo × saldo (`ending_balance`).

## 3. Onde obter o que falta

### Caminho 1 — consulta da MSC no Siconfi

**https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_matriz_filtro.jsf**

Na consulta, é preciso selecionar:

- **Ente**: Rio Grande do Norte (24)
- **Exercício**: 2025
- **Mês**: 12 (ou o mês de referência)
- **Classe contábil**: **todas** (ou ao menos a 8)
- **Tipo de valor**: **todos os três** (`beginning_balance`, `period_change`, `ending_balance`)

O download vem em ZIP, com um CSV por combinação classe × tipo.

### Caminho 2 — SIAFIC do Estado

A MSC é gerada pelo SIAFIC e transmitida ao Siconfi. A Secretaria de Fazenda
(SEFAZ/RN) e a Controladoria têm acesso à matriz completa — inclusive às contas
de controle, que o recorte publicado às vezes omite.

### Caminho 3 — o próprio RGF homologado

O valor da despesa não executada **já está publicado** no RGF:

```
Despesa com Pessoal não Executada Orçamentariamente
RGF 2024 Q3: R$ 454.943.101,05
```

Se o objetivo for apenas completar a linha do relatório, o valor oficial existe.
Mas isso é usar o gabarito — a verificação independente exige a classe 8 da MSC.

## 4. Por que a classe 8 importa

A conta `8.6.3.3.1.00.00` é uma **conta de controle** (natureza credora). Ela não
é movimentada por lançamento orçamentário comum: registra a **despesa empenhada
e não executada** para fins de apuração do limite de pessoal.

Sem ela:

- a linha "Despesa não Executada Orçamentariamente" fica zerada;
- a Despesa Bruta (I) perde R$ 454,9 mi;
- a Despesa Líquida (III) herda o erro.

## 5. O que já dá para afirmar

Com o acervo atual (classes 3, 4 e 6, movimento), a apuração de **2025 Q3**
fecha em **−0,36%** na despesa bruta e **−0,10%** em Vencimentos — mesmo sem a
classe 8.

Isso significa que a ausência da classe 8 **não compromete** as demais linhas: o
motor acerta Vencimentos, Patronais, Aposentadorias, Pensões, Terceirização,
Judiciais e Indenizações sem ela. A classe 8 afeta **uma única linha**.

## 6. Resumo

| pergunta | resposta |
|---|---|
| Existe dado público? | **Sim** — MSC completa no Siconfi |
| O que falta no acervo? | classe 8 e `ending_balance` |
| Onde obter? | consulta MSC do Siconfi (todas as classes, três tipos) |
| Alternativa? | SIAFIC/SEFAZ ou o valor do RGF homologado |
| Compromete o resto? | **não** — só a linha da não executada |
