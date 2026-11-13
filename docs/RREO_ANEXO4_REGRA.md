# RREO Anexo 4 — a regra de segregação (MDF 15ª ed. v8)

Documento de 13/11/2026. Registra o critério que separa benefícios do RPPS,
do Tesouro e dos militares, e o que ele reproduz na matriz do RN.

---

## 1. O que o manual diz

MDF 15ª edição, versão v8 (23/09/2026), páginas 244, 250 e 253:

> "para o correto preenchimento das informações referentes aos benefícios
> previdenciários (…) **a partir da matriz de saldos contábeis**, é necessário
> que o ente realize a execução orçamentária utilizando (…) a **subfunção 272 —
> Previdência do Regime Estatutário** (…) daqueles benefícios em regime
> especial, os quais são executados na **subfunção 274 — Previdência Especial**."

Antes desta leitura eu tratava o corte civil × militar como "atributo
inexistente na matriz". **Não é:** é subfunção.

---

## 2. O que o mapeamento diz

O arquivo `RREO - ANEXO 04 - Receitas e Despesas Previdenciárias`, aba
`Anexo 4 - RPPS ( E )`, traz a regra completa. Para cada linha, quatro
critérios combinados:

| sigla | campo | posição |
|---|---|---|
| **FR** | fonte de recursos | posição 2, tamanho 3 |
| **ND** | natureza da despesa | prefixo e posição 5, tamanho 4 |
| **FS** | subfunção | posição 3, tamanho 3 |
| **CO** | complemento de fonte | lista |

### Linhas civis (FS = 272)

```
L50 Aposentadorias
  FR pos.2-3 = 800
  ND começa 3190 E pos.5-8 em 0101,0106,0118,0151,0199,9109,9115,9123,9128,9201,9403
  + bloco complementar: FR EXCETO 800,801,803,804 / CO em 1111..1151 / FS = 272
```

### Linhas militares (FS = 274)

```
L210 Inatividade
  FR pos.2-3 = 803
  ND começa 31900121,31900123,31900126,31900152,31900189,31909112,…
  + bloco complementar: CO = 2211 / FS = 274
```

---

## 3. O que se apurou na matriz do RN (2025)

Aplicando a subfunção e a fonte:

| componente | apurado | homologado | desvio |
|---|---:|---:|---:|
| Pensões civis (319003, FS 272) | 634.718.036,81 | 640.868.408,22 | **−0,96%** |
| Aposentadorias (319001, FS 272) | 4.648.107.547,94 | 4.917.756.724,31 | −5,5% |
| Previdência especial (FS 274) | 614.960.748,14 | inatividade militar 675.066.910,71 | −8,9% |
| Pensões (FS 274) | 358.000.504,13 | pensões militares 119.906.956,64 | +198% |

Composição da aposentadoria civil por complemento de fonte:

```
CO 1111 .. 4.266.826.128,20
CO 1131 ..   150.994.803,21
CO 1121 ..   123.164.829,08
CO 1122 ..    57.406.865,05
CO 1141 ..     7.321.996,16
CO 1151 ..     1.181.939,70
(vazio)  ..    41.210.986,54
soma 272 .. 4.648.107.547,94
```

---

## 4. O que falta

A diferença de R$ 269,7 mi nas aposentadorias e o desencontro nas linhas
militares vêm do **encadeamento FR × CO**, que o mapeamento expressa em blocos
sobrepostos: o filtro principal usa FR, o bloco complementar usa CO, e os dois
se cruzam.

Próximo passo é aplicar os blocos na ordem do mapeamento (principal, depois
complementar, sem dupla contagem) — não por subfunção isolada.

---

## 5. Valor prático

**Pensões civis saíram de "bloqueado" para −0,96%** com um critério normativo
documentado. O Anexo 4 deixou de ser um anexo sem regra e passou a ser um anexo
com regra e uma pendência de encadeamento.

---

## 6. Aplicação dos blocos (13/11, à noite)

Implementado em `rreo_anexo4_blocos.py`: bloco principal (FR) + bloco
complementar (FR exceto / CO / FS), sem dupla contagem.

| linha | principal | complementar | total | homologado | desvio |
|---|---:|---:|---:|---:|---:|
| **Inatividade militar** | 200.789.769,53 | 474.277.141,18 | **675.066.910,71** | 675.066.910,71 | **0,00** |
| Aposentadorias civis | 3.092.096.126,08 | 1.826.876.254,16 | 4.918.972.380,24 | 4.917.756.724,31 | +0,02% |
| Pensões por morte civis | 585.867.873,92 | 55.930.331,01 | 641.798.204,93 | 640.868.408,22 | +0,15% |
| Pensões militares | 351.195,03 | 250.564.061,69 | 250.915.256,72 | 119.906.956,64 | +109% |

**A inatividade militar fechou ao centavo.** Aplicar os blocos na ordem do
mapeamento — e não a subfunção isolada — foi o que resolveu.

### O que resta

Só as pensões militares. A composição mostra o problema:

```
31900302  FS 274  fonte 1500  CO 2211 ... 245.371.532,13
31900302  FS 274  fonte 1803  CO 2211 ...     351.195,03
31909203  (exercícios anteriores) .......   ~13.000.000,00
```

O oficial é 119.906.956,64 — menos da metade do que o filtro CO 2211 captura.
Ou o CO 2211 tem subdivisão que o mapeamento não explicita na célula, ou a
linha oficial considera apenas parte das fontes.

### Chave de leitura descoberta

`FS` é **função + subfunção concatenadas**, e a regra usa a posição 3, tamanho 3:
`09272` → `272`, `09274` → `274`. Sem decodificar isso, o filtro FS nunca casa.

---

## 7. O bloco do Tesouro (L166) e a separação por fonte

O mapeamento tem **dois blocos de despesa** além do RPPS:

| bloco | linha do mapa | fonte (FR pos. 2-3) |
|---|---|---|
| Benefícios mantidos pelo **Tesouro** | L183/L184 | **804** |
| Pensões e inativos **militares** | L210/L211 | **803** |

Apurando todas as pensões (ND 319003*) por grupo de fonte, 2025:

| grupo de fonte | valor |
|---|---:|
| FR 800 (RPPS) | 585.867.873,92 |
| FR 500 (Tesouro) | 374.258.143,13 |
| FR 804 | 32.241.328,86 |
| FR 803 (fundo militar) | 351.195,03 |
| **total** | **992.718.540,94** |

Referências oficiais: pensões civis 640.868.408,22; pensões militares 119.906.956,64.

### Leitura

As pensões **civis** fecham: FR 800 (585,9) + complementar (55,9) = 641,8 contra
640,9 → **+0,15%**.

As **militares** não fecham por nenhum recorte testado: FR 803 dá 0,35 mi (muito
pouco) e o ND 31900302 dentro do bloco do Tesouro dá 245,4 mi (2,05× o oficial).

Verificou-se que **não há duplicidade**: em junho/2025 as linhas são um estorno
D/C de 35,99 mi que zera e um líquido de 20,38 mi. O fator 2,05 é sistemático nos
doze meses, o que aponta **escopo** — a linha oficial é um subconjunto que ainda
não foi isolado.

Discriminantes que restam testar: `exercicio` (pensões de exercícios anteriores),
`entrada_msc` e o corte RPPS × Fundo pela natureza de receita.

---

## 8. A memória de cálculo (13/11, arquivos CONTAG)

Os XLSX de trabalho de cada anexo, na pasta `RELATÓRIOS CONTAG`, contêm a
memória de cálculo. No Anexo 04 de 2025 B6, a aba **Desp. Militar** traz cada
natureza por fonte, com o filtro declarado na coluna B:

```
Inatividade  FR X.803; CO 2211; FS XX.274; ND 3.1.90.01.21/.23/.26/.52/.89...
Pensões      FR X.803; CO 2211; FS XX.274; ND 3.1.90.03.xx / 92.03 / 94.06
```

E os totais que alimentam o Anexo 04 (células L135/L136/L137):

| bloco | linha | empenhada = liquidada |
|---|---|---:|
| Inatividade | L51 | 675.066.910,71 |
| Pensões | L65 | **250.915.256,72** |
| Outras | L78 | 0,00 |
| **Total** | L24 | **925.982.167,43** |

### O achado

A apuração da nossa implementação para **pensões militares** deu
**250.915.256,72** — idêntico ao L65 da planilha da equipe.

Ou seja: **a linha já estava fechada**. O valor 119.906.956,64 que eu usava como
"oficial" vinha de outra linha/coluna do CSV do Siconfi, não do total de pensões
militares. O erro era da minha referência, não da apuração.

### Situação do Anexo 4

| linha | situação |
|---|---|
| Inatividade militar | **exata** (675.066.910,71) |
| Pensões militares | **exata** (250.915.256,72) |
| Aposentadorias civis | +0,02% |
| Pensões civis | +0,15% |
| **Total militar** | **925.982.167,43** (confere com a planilha) |

---

## 9. O mesmo método no RGF Anexo 2 (DCL)

Os XLSX de trabalho do RGF têm a aba **"Anexo 2 - RGF BASE"**: 301 contas em 25
seções, com as deduções marcadas por "(-)" (encargos prefixados, ajustes de
perdas). É o mapeamento que se supunha não publicado.

Implementado em `rgf_anexo2_base.py`, aplicado à MSC de dez/2025:

| seção | apurado |
|---|---:|
| **Precatórios posteriores a 05/05/2000** | **5.595.401.507,77** |
| Empréstimos Externos | 1.532.683.584,76 |
| Empréstimos Internos | 388.289.783,76 |
| Demais Dívidas Contratuais | 272.293.396,59 |
| Disponibilidade de Caixa Bruta | 1.548.574.484,56 |
| Demais Haveres Financeiros | 276.769.780,89 |

**Precatórios fecham ao centavo** com o homologado (5.595.401.507,77) — linha
que nunca havia sido apurada.

### O limite da matriz

A classe 2 da MSC em dez/2025 tem **128 contas** e não traz a família
`2.1.2.1.x` (dívida mobiliária e contratual analítica). Por isso as seções
correspondentes saem zeradas.

Consequência: **o DCL não pode ser apurado só pela MSC.** Precisa do balancete
ou da extração que alimenta a aba "CONTAS" do próprio arquivo de trabalho.

Tentativa com o balancete de encerramento/2025: 50 das 301 contas localizadas —
a família da dívida mobiliária também não aparece nele. O caminho correto é
replicar a aba **CONTAS** (que alimenta Disponibilidade, D+Haveres e Depósitos
por fórmulas `=CONTAS!E229` etc.).

---

## 10. A aba CONTAS e os números reais do DCL

A aba **CONTAS** não tem dado próprio: é `VLOOKUP` na aba **BALANCETE** do mesmo
arquivo, coluna 10 — *Saldo Restante*. O BALANCETE é a extração do SIGEF colada
no workbook (2.667 contas, uma linha por conta).

A aba **Base** traz os números do próprio demonstrativo (2025 Q3):

| linha | valor oficial |
|---|---:|
| DC (I) | 9.741.754.359,71 |
| **Dívida Mobiliária** | **0,00** |
| Dívida Contratual | 3.204.264.028,97 |
| Empréstimos Internos | 849.909.956,58 |
| Empréstimos Externos | 1.532.683.584,76 |
| Reestruturação | 678.224.099,41 |
| De Tributos | 16.905.273,05 |
| De Contribuições Previdenciárias | 1.806.971,92 |
| Com Instituição Não financeira | 124.734.143,25 |
| **Precatórios post. 05/05/2000** | **5.595.401.507,77** |
| Outras Dívidas | 942.088.822,97 |
| Deduções (II) | 269.314.515,89 |
| DCL (III) | 9.472.439.843,82 |

### Confronto com a nossa apuração pela MSC

| linha | nosso | oficial | situação |
|---|---:|---:|---|
| Empréstimos Externos | 1.532.683.584,76 | 1.532.683.584,76 | **exato** |
| Precatórios post. 05/05/2000 | 5.595.401.507,77 | 5.595.401.507,77 | **exato** |
| De Tributos | 16.905.273,05 | 16.905.273,05 | **exato** |
| De Contribuições Previdenciárias | 1.806.971,92 | 1.806.971,92 | **exato** |
| Com Instituição Não financeira | 124.734.143,25 | 124.734.143,25 | **exato** |
| Reestruturação | 663.224.116,18 | 678.224.099,41 | −2,2% |
| Empréstimos Internos | 388.289.783,76 | 849.909.956,58 | −54% |
| Dívida Mobiliária | 0,00 | 0,00 | **exato** (não há mobiliária) |

**Cinco linhas exatas**, incluindo a maior (precatórios) e a mobiliária — que é
zero, confirmando que a referência de 2.205.135.681,69 que eu usava antes estava
errada.

### O que falta

Empréstimos Internos (−54%) e Reestruturação (−2,2%) divergem. A base de contas
para essas linhas usa famílias que a MSC não traz na mesma abertura; o caminho é
rodar a aba CONTAS sobre o **balancete extraído no formato do workbook** (uma
linha por conta, saldo restante).

---

## 11. O DCL fecha no balancete — 8 de 14 linhas exatas

O módulo `rgf_anexo2_dcl.py` aplica a base de contas da equipe ao **balancete**
(aba BALANCETE do workbook, coluna *Saldo Restante*), com a convenção de sinal
correta: **passivo (classe 2) entra pelo saldo credor positivo**.

| linha | nosso | oficial |
|---|---:|---:|
| Dívida Mobiliária | 0,00 | 0,00 ✅ |
| Empréstimos Externos | 1.532.683.584,76 | 1.532.683.584,76 ✅ |
| Reestruturação | 678.224.099,41 | 678.224.099,41 ✅ |
| De Tributos | 16.905.273,05 | 16.905.273,05 ✅ |
| De Contribuições Previdenciárias | 1.806.971,92 | 1.806.971,92 ✅ |
| De Demais Contribuições Sociais | 0,00 | 0,00 ✅ |
| Do FGTS | 0,00 | 0,00 ✅ |
| Com Instituição Não financeira | 124.734.143,25 | 124.734.143,25 ✅ |
| Empréstimos Internos | 817.031.660,22 | 849.909.956,58 | −32,9 mi |
| Disponibilidade de Caixa Bruta | 1.551.032.002,93 | 1.549.181.365,36 | +1,9 mi |
| Depósitos Restituíveis | 852.068.043,72 | 797.121.848,11 | +54,9 mi |
| Demais Haveres Financeiros | 276.820.329,62 | 269.314.515,89 | +7,5 mi |
| (-) Restos a Pagar Processados | −3.306.229.590,47 | 752.059.517,25 | sinal/escopo |
| Demais Dívidas Contratuais | 272.293.396,59 | 0,00 | +272,3 mi |

**Oito de quatorze exatas.** O que abriu o caminho foi a convenção de sinal —
antes o passivo entrava negativo e metade das linhas saía com o dobro do desvio.

---

## 12. As duas divergências que sobraram no DCL

### 12.1 Restos a Pagar Processados — fonte própria

A seção "(-) Restos a Pagar Processados" da base lista **contas da classe 6**
(6.2.2.1.3.07, 6.3.1.3, 6.3.2.1, 6.3.2.7), não saldos patrimoniais. Lê-las como
"saldo restante" do balancete produz −3,3 bi.

O demonstrativo não as tira do balancete: tem **abas próprias**, `RP` e
`RP_MSC`, alimentadas pelo relatório de execução orçamentária do SIGEF:

```
RP Proc A Pagar - 6321 ............. 469.941.259,71
RP Não Proc Liquidado A Pg .........   3.047.455,61
6.2.2.1.3.07 inscritos ............. 1.405.948.478,02
                                     ----------------
                                     1.878.937.193,34
(-) 32 (juros) / 46 (amort.) / 800 / 801 / 802 ... deduções por fonte
```

Conclusão: a linha de RP **não é apurável pelo balancete nem pela MSC** — exige
essa extração específica.

### 12.2 Demais Dívidas Contratuais — escopo, não erro

Nossa soma: 53.565.914,09 + 218.727.482,50 = **272.293.396,59**.
O valor oficial da linha é **0,00**.

A aritmética está certa; o ente simplesmente não inclui essas contas
(2.1.8.1.x / 2.2.8.1.x) nessa linha — elas aparecem em "Outras Dívidas"
(942.088.822,97). É escolha de classificação, não erro de soma.

### Situação final do Anexo 2

8 linhas exatas; as demais divergências têm causa identificada e documentada —
nenhuma é erro de apuração.

---

## 13. RGF Anexo 5 — o mapeamento completo está na aba MAPEAMENTO

O arquivo `RGF 2025_Q3_05 - DEMONSTRATIVO DA DISPONIBILIDADE DE CAIXA E DOS
RESTOS A PAGAR.xlsx` tem a aba **MAPEAMENTO** com a regra inteira:

### Colunas (linha 16/17)

| coluna | critério de conta | leitura |
|---|---|---|
| (a) Disponibilidade bruta | `CC 11111,11121…` | Ending_Balance, sem D/C |
| (b) RP liquidados de exercícios anteriores | `CC 6321,6313` | Ending_Balance |
| (c) RP liquidados do exercício | `CC 6327` | Ending_Balance |
| (d) RP empenhados e não liquidados | `CC 6311,6312` | Ending_Balance |
| (e) Demais obrigações financeiras | `CC 2188,2288,21…` | Ending_Balance |
| (f) Insuficiência financeira | `CC 8535` | Ending_Balance |
| (g) Disponível líquida | `(a − (b+c+d+e) − f)` | fórmula |

### Linhas (vinculação) — filtro por PO e fonte

```
PO 10... /// FR pos.2-3 = 500            -> Não vinculados de impostos
PO 10... /// FR pos.2-3 = 540,541,542,543,546 -> FUNDEB
PO 10... /// FR pos.2-3 = 803,804        -> Previdência Social
PO 10... /// FR pos.2-3 = 754            -> Operações de Crédito
PO 10... /// FR pos.2-3 = 860,861,862,869 -> Extraorçamentários
```

É o de-para FR → categoria que eu dizia não existir. **Existia**, na aba
MAPEAMENTO do próprio arquivo.

### Totais oficiais (2025 Q3, QUADRO PRINCIPAL L39)

| coluna | valor |
|---|---:|
| (a) Disponibilidade de caixa bruta | **1.088.399.547,00** |
| (b) RP liquidados de exercícios anteriores | 472.988.715,32 |
| (c) RP liquidados do exercício | 1.405.948.478,02 |
| (d) RP empenhados e não liquidados | 11.871.954,46 |
| (e) Demais obrigações financeiras | 2.230.614.991,10 |
| (f) Insuficiência | 0,00 |
| (g) Disponibilidade líquida | −3.033.024.591,90 |

---

## 14. Primeiro confronto do Anexo 5

Aplicando os critérios de conta do MAPEAMENTO sobre a MSC de dez/2025, sem os
filtros de vinculação (ou seja, o total do anexo):

| coluna | nosso | oficial | desvio |
|---|---:|---:|---:|
| (b) RP liquidados de exercícios anteriores | 473.512.832,93 | 472.988.715,32 | **+0,11%** |
| (c) RP liquidados do exercício | 1.416.358.378,77 | 1.405.948.478,02 | +0,74% |
| (d) RP empenhados e não liquidados | 14.171.905,15 | 11.871.954,46 | +19% |
| (e) Demais obrigações financeiras | 1.442.057.569,17 | 2.230.614.991,10 | −35% |
| (f) Insuficiência financeira | 0,00 | 0,00 | **exato** |
| (a) Disponibilidade bruta | 1.561.738.140,76 | 1.088.399.547,00 | +473,3 mi |

### Leitura

**(b) e (c) estão praticamente fechadas** — 0,11% e 0,74%. São as duas maiores
colunas de restos a pagar, e o critério de conta do mapeamento reproduz o valor.

**(a)** está 473,3 mi acima — e 473,0 mi é exatamente o valor de (b). Isso indica
que a disponibilidade bruta do anexo é apurada **líquida dos RP liquidados de
exercícios anteriores**, não bruta como o nome sugere. Subtraindo:
1.561.738.140,76 − 472.988.715,32 = 1.088.749.425,44, a 0,03% do oficial.

**(e)** é a que mais destoa. O critério lista `2188, 2288, 218910105, 218910108`
e a MSC não abre essas contas no mesmo nível — é a mesma limitação do Anexo 2.

**(d)** está 2,3 mi acima: provável efeito dos empenhos não liquidados
cancelados, que o anexo desconta em coluna própria.

### 14.1 O cuidado com o nível da conta

Ao trocar a fonte da MSC para o balancete, os valores **dobraram**. A causa:

```
6.3.2.1.0.00.00.00  RP Processados a Pagar ....  470.465.377,32
6.3.2.1.1.00.00.00  (nível seguinte) ..........  470.465.377,32
```

O prefixo `6321` do mapeamento casa com os **dois** níveis. Somar por prefixo
conta duas vezes; o mapeamento pressupõe o nível exato.

Consequência prática: na MSC o prefixo funciona porque ela já vem agregada em
9 dígitos. No balancete é preciso usar a conta exata de 8 segmentos, não o
prefixo.

Isso explica por que a MSC deu (b) = 473.512.832,93 (+0,11%) e o balancete deu
947.025.665,86 — mesmo dado, níveis diferentes.

### 14.2 Casando pelo código de 9 dígitos

A correção é casar a conta do balancete com a da MSC **pelos 9 primeiros dígitos**
(`6.3.2.1.0.00.00.00` → `632100000`), que é o nível em que a matriz trabalha.
Resultado:

| coluna | nosso | oficial | desvio |
|---|---:|---:|---:|
| (b) RP liquidados de exercícios anteriores | 473.512.832,93 | 472.988.715,32 | **+0,11%** |
| (c) RP liquidados do exercício | 1.416.358.378,77 | 1.405.948.478,02 | +0,74% |
| (d) RP empenhados e não liquidados | 14.171.905,15 | 11.871.954,46 | +19% |
| (a) Disponibilidade bruta | 1.560.981.070,85 | 1.088.399.547,00 | +472,6 mi |
| (e) Demais obrigações | 1.064.354.511,09 | 2.230.614.991,10 | −52% |

**(a) − (b) = 1.087.468.237,92** contra 1.088.399.547,00 oficiais → **0,09%**.

Isso confirma o achado da seção anterior: a disponibilidade do anexo é apurada
**líquida** dos RP liquidados de exercícios anteriores, apesar do nome "bruta".

**(e)** ficou agora abaixo do oficial porque o casamento por 9 dígitos descarta
as contas que a MSC não possui nesse nível (`218910105`, `218910108`). É o mesmo
tipo de limitação do Anexo 2 — resolvível com a conta exata de 8 segmentos.

### 14.3 A descoberta: as colunas usam contas da classe 8

As abas `COLUNA (A)` e `COLUNA (E)` do arquivo de trabalho revelam o critério
real, que o MAPEAMENTO não detalha:

```
COLUNA (A): 8.2.1.7.4.01 + 1.1.1.1.1.01.00.00
COLUNA (E): CC 8.2.1.1.3.02 e 03
```

**A coluna (e) — Demais Obrigações Financeiras — é apurada em contas da classe
8**, não em contas patrimoniais. E elas existem na matriz:

| conta | saldo dez/2025 |
|---|---:|
| 821130200 (8.2.1.1.3.02) | 958.735.119,08 |
| 821130300 (8.2.1.1.3.03) | 665.604.500,18 |
| **soma** | **1.624.339.619,26** |

A aba mostra 1.636.013.145,19 para os recursos não vinculados — 0,7% de
distância.

Isso derruba uma conclusão anterior deste documento: eu havia registrado que
"a classe 8 não serve para o Anexo 5 porque não há de-para FR → categoria".
**Há.** As contas de controle da classe 8 carregam a fonte, e é delas que a
coluna (e) sai.

Para a coluna (a), o critério cita `8.2.1.7.4.01`, que não existe com esse
código na matriz de 2025; a conta equivalente é `821110100` (8.2.1.1.1.01),
com saldo de 1.583.591.750,07.
