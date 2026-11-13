# Aplicador de mapeamentos da STN — o que se consertou

Documento de 13/11/2026. Registra o defeito que zerava a apuração do RREO
Anexo 01, o conserto, o resultado verificado e o que ficou pendente.

---

## 1. O defeito

O aplicador (`aplicar_rreo2.py`) apurava **zero** em todas as linhas. Duas causas:

**1.1 Coluna de critério errada.** O mapeamento é uma grade: cada coluna do
anexo tem o **seu** critério de conta, na linha 15. O código pegava o primeiro
que encontrava:

    CC começada por LISTA: 5211     <- coluna 4, PREVISÃO INICIAL

e aplicava a todas as linhas. Mas a receita realizada está em `6212,6213`
(colunas 8 e 11). Aplicado `5211` a tudo, nada casava.

**1.2 Linhas legítimas descartadas.** A constante `IGNORAR` continha
`"RECEITAS"` e `"DESPESAS"`, o que apagava da hierarquia justamente
`RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)` e `DESPESAS CORRENTES`.

---

## 2. O conserto

| mudança | efeito |
|---|---|
| `criterio_conta(ws, coluna)` escolhe a coluna acumulada `(c)` | apura o realizado, não a previsão |
| `criterio_da_linha` associa a cada linha a **seção** a que pertence | o mapeamento muda de critério no bloco de despesa (linha 104), intra-receita (141) e intra-despesa (212) |
| `IGNORAR` sem `RECEITAS`/`DESPESAS` | as linhas sintéticas voltam à hierarquia |
| `ler_linhas` grava o **bloco** de cada linha | hierarquia não cruza seções |
| `linha_de_criterio` só aceita linhas com coluna acumulada | linhas 96/97 (só saldo) não abrem bloco falso |
| ramo cai para a soma dos filhos quando o filtro zera | pai com filtro insatisfazível deixa de zerar o bloco |

Commits: `308ffa1` (coluna e seção) e `c91a36f` (hierarquia por bloco).

---

## 3. O resultado

**Antes:** 0 linhas exatas. **Depois:** 47 de 105.

A **receita do Balanço fechou por inteiro** contra o homologado de 2026 B4:

| linha | apurado | homologado |
|---|---:|---:|
| RECEITAS (EXCETO INTRA) (I) | 16.012.885.982,23 | 16.012.885.982,23 |
| RECEITAS CORRENTES | 15.021.220.158,33 | 15.021.220.158,33 |
| Impostos | 5.779.867.456,50 | 5.779.867.456,50 |
| Taxas | 434.250.163,19 | 434.250.163,19 |
| Contribuições Sociais | 884.518.630,35 | 884.518.630,35 |
| Receita Patrimonial | 168.066.258,34 | 168.066.258,34 |
| Receita de Serviços | 83.480.235,91 | 83.480.235,91 |
| Transferências Correntes | 7.150.287.962,42 | 7.150.287.962,42 |

O bloco de capital também fechou: `DESPESAS DE CAPITAL = 1.015.934.400,34`,
pela soma dos três filhos (796.524.885,45 + 45.772.388,08 + 173.637.126,81).

---

## 4. O que continua aberto

**4.1 Blocos duplicados.** O mapeamento repete a estrutura de despesa nas
linhas 107–128 e 208–221, com os mesmos rótulos. A comparação casa por rótulo,
então cada linha aparece duas vezes — uma com valor, outra zerada.

**4.2 O bloco intra.** A linha usa
`ND começada por (Lista): 3,4 + Pos. inicial= 3; Tamanho= 2; Lista=...`.
O `+` não é adição nem E: é união de dois critérios sobre campos diferentes.
Tratado como prefixo puro, soma R$ 16,79 bi contra R$ 1,81 bi oficiais.

Caminho recomendado: **tabela de blocos por anexo** (onde cada seção começa e
termina, qual coluna é a acumulada), em vez de parser genérico.

---

## 5. O balancete contra a matriz — teste de independência

Confronto do balancete consolidado de agosto/2026 (SIGEF) com o `period_change`
de agosto da MSC, ligados pelo plano de contas (`6.317` pares MSC → SIGEF).

| resultado | contas |
|---|---:|
| comparáveis | 30 |
| batem ao centavo | **22** |
| divergem | 8 |

As oito divergências são a **família da liquidação** (6221301, 02, 03, 04), a
622920103, a agregadora 622990000 e as contas de RP (6314, 6322).

Duas hipóteses testadas e descartadas/confirmadas:

- **nível hierárquico:** descartada — a conta do balancete é folha, sem filhos;
- **escopo:** provável — no 622130300 a matriz tem R$ 630,9 mi a mais no débito
  e R$ 627,6 mi a mais no crédito. Débito e crédito sobem juntos, o que indica
  volume que existe numa visão e não na outra (compensação intra), não conta
  trocada.

Conclusão: o balancete serve como conferência **secundária**. Onde diverge, o
árbitro é o homologado do Siconfi — e nele os números de liquidação batem ao
centavo.

---

## 6. Cuidado com o método

O casamento por valor (procurar no balancete a conta com o mesmo par D/C)
produziu falsos positivos: `622120200` e `622910100` apontaram para a mesma
conta do SIGEF. Serve para investigar, **não** para corrigir de-para.

---

## 7. Inventário dos arquivos de 13/11

Doze recebidos, **dez distintos** (dois pares duplicados por hash):

| arquivo | referência |
|---|---|
| Balancete Consolidado | Encerramento 2025 (já existia na base) |
| Balancete (1) e (2) | Julho/2026 |
| Balancete (3) e (4) | Agosto/2026 |
| Relação Plano Contas MSC × SIGEF | 6.317 pares |
| Comparativos da Receita (3 arquivos) | 2026 |
| Balancete Unidade Gestora (PDF) | por UG |

Os mapeamentos da STN enviados em 13/11 são **idênticos** aos que já estavam em
`dados/mapeamentos` (16 de 16 arquivos, mesmo MD5). O MDF 15ª edição **v8**
(23/09/2026) é novo — a base tinha a v6 (set/2025).
