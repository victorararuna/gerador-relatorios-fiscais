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
