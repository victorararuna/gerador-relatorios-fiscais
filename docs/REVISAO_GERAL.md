# Revisão geral do motor de demonstrativos fiscais do RN

Documento de 13/11/2026. **Ponto de entrada único**: consolida o que foi
descoberto, o que está verificado e o que resta. Substitui a leitura dispersa
dos demais documentos.

---

## 1. As quatro origens de dado

O trabalho só avançou quando ficou claro que existem **quatro** fontes, e que
cada linha de cada anexo bebe de uma delas.

| origem | onde está | o que fornece |
|---|---|---|
| **MSC** (matriz de saldos contábeis) | `dados/acervo` | execução orçamentária e saldos, formato longo |
| **Balancete** (SIGEF) | `dados/fontes/13nov` | saldo por conta, com todos os níveis |
| **Mapeamentos STN** (MDF 15ª ed.) | `dados/mapeamentos` | de-para linha do anexo → conta × natureza |
| **Planilhas de trabalho da equipe** | `RELATÓRIOS CONTAG` | memória de cálculo por anexo |

Regra que se confirmou quatro vezes: **quando o número não fecha, a resposta
está na planilha da equipe, não no CSV do Siconfi.**

---

## 2. Situação por anexo

### Verificado ao centavo (contra o homologado)

| anexo | linhas | desvio |
|---|---|---:|
| RREO Anexo 1 — despesa | 4 grupos + total | **0,00** |
| RREO Anexo 1 — receita | total e itens | **0,00** |
| RREO Anexo 2 — função | 23 funções | **0,00** |
| RREO Anexo 3 — RCL | 5 linhas, 2025 e 2026 | **0,00** |
| RREO Anexo 7 — restos a pagar | 5 linhas | **0,00** |
| RREO Anexo 9 — despesa de capital | 4 linhas | **0,00** |
| RREO Anexo 14 — simplificado | 6 linhas | **0,00** |
| RGF Anexo 3 — garantias | 5 linhas | **0,00** |
| RGF Anexo 4 — limites | 3 limites | **0,00** |
| RGF Anexo 6 — limites | 3 limites | **0,00** |

### Apurado com desvio pequeno e documentado

| anexo | situação |
|---|---|
| **RGF Anexo 1 — pessoal** | bruta a −0,36% (2025 Q3); a líquida desvia pela dedução |
| **RREO Anexo 4 — previdenciário** | 4/4: inatividade e pensões militares **exatas**; civis a +0,02% e +0,15% |
| **RGF Anexo 2 — DCL** | **8 de 14 linhas exatas**; as demais com causa identificada |
| **RGF Anexo 5 — disponibilidade** | (b) +0,11%, (c) +0,74%, (f) exata; (a) explicada; (e) a 0,7% |

### Aberto

| anexo | o que falta |
|---|---|
| RREO Anexo 1 completo | 47 de 105 linhas no aplicador de mapeamento |
| RREO Anexo 9 — receita | separar operação nova de refinanciamento |
| RREO Anexo 13 — PPP | cadastro de contratos |
| RGF Anexo 5 — quebra por vinculação | rodar as 27 linhas do MAPEAMENTO com as contas da classe 8 |

---

## 3. Como cada anexo é apurado

| anexo | fonte | critério |
|---|---|---|
| RREO 1 despesa | MSC classe 6 | conta 62213 por grupo de natureza |
| RREO 1 receita | MSC classe 6 | conta 6212/6213 + natureza (mapeamento) |
| RREO 2 | MSC classe 6 | conta de liquidação + função |
| RREO 3 | RREO Anexo 3 | RCL menos deduções publicadas |
| RREO 7 | MSC classe 6 | contas 6.3.1 / 6.3.2 |
| RREO 9 | MSC classe 6 | 62213 por natureza 44/45/46 |
| RREO 14 | MSC classe 6 | empenhado, liquidado, pago |
| RREO 4 | MSC + mapeamento | ND × FS (função+subfunção) × FR × CO |
| RGF 1 | MSC classes 3/4/6 + class 8 | janela móvel de 12 meses |
| RGF 2 | **balancete** | base de 301 contas da planilha |
| RGF 3/4/6 | RCL | limites da LRF |
| RGF 5 | MSC + classe 8 + balancete | MAPEAMENTO: conta × fonte |

---

## 4. As cinco armadilhas

### 4.1 Sinal do passivo
Contas da classe 2 têm saldo **credor**; no balancete o crédito vem negativo.
Sem inverter, toda linha de dívida sai com o dobro do desvio. Foi o que
derrubou metade do Anexo 2.

### 4.2 Nível da conta
O prefixo `6321` casa com `6.3.2.1.0` **e** `6.3.2.1.1` — soma em dobro. A MSC
já vem agregada em 9 dígitos; o balancete, não. Regra:
**MSC → prefixo de 9 dígitos; balancete → conta exata.**

### 4.3 Fonte errada
A matriz não tem a dívida analítica (classe 2 com 128 contas apenas). O DCL
nasce do **balancete**. Já a receita e a despesa nascem da **matriz**.

### 4.4 Referência errada
Dois valores que usei como "oficial" estavam errados, ambos vindos do CSV do
Siconfi sem conferir o que representavam:

- **pensões militares**: eu usava 119,9 mi; o correto é 250,9 mi — e nossa
  apuração já batia;
- **dívida mobiliária**: eu usava 2.205,1 mi; o correto é **zero**.

### 4.5 Escopo
Linha oficial pode ser subconjunto. "Demais Dívidas Contratuais" é zero no
demonstrativo embora as contas somem 272,3 mi — o ente as classifica em
"Outras Dívidas". Não é erro de soma.

---

## 5. O que está aberto, com o próximo passo

| # | item | próximo passo |
|---|---|---|
| 1 | Anexo 2 — Empréstimos Internos (−32,9 mi) | localizar a conta de encargos negativa |
| 2 | Anexo 2 — RP processados | usar as abas `RP` / `RP_MSC` (execução orçamentária) |
| 3 | Anexo 5 — coluna (e) | rodar 8.2.1.1.3.02/03 por fonte |
| 4 | Anexo 5 — quebra por vinculação | 27 linhas do MAPEAMENTO × contas classe 8 |
| 5 | RREO 1 — 47/105 linhas | blocos duplicados e bloco intra no aplicador |
| 6 | RREO 9 — receita | atributo de refinanciamento |

---

## 6. Como executar

```bash
python verificar_tudo.py                 # 27 conferências de ponta a ponta
python rreo_anexo4_blocos.py             # RREO Anexo 4 (4 linhas)
python rgf_anexo2_dcl.py                 # RGF Anexo 2 (balancete)
python rgf_anexo5_disp.py                # RGF Anexo 5 (mapeamento)
python gerar_rreo.py --ano 2026 --bimestre 4
python gerar_consolidado.py --ano 2025 --quadrimestre 3
```

**Testes**: 41 (leitor 14, Anexo 1 15, Anexo 3 3, limites 9) — todos verdes.

---

## 7. Histórico de conclusões que mudaram

Registro para quem retomar não repetir o caminho:

| eu concluí | na verdade |
|---|---|
| mapeamento do RGF Anexo 2 não é público | está na aba "Anexo 2 - RGF BASE" |
| faltam blocos de receita no material | estão no mapeamento do RREO Anexo 01 |
| Anexo 4 exige atributo civil/militar | é a subfunção 272/274 (FS) |
| classe 8 não serve ao Anexo 5 | é a fonte da coluna (e) |
| Anexo 1 e Anexo 6 são inconsistentes (3,2 mi) | diferença é o RPNP, por regra |
| linha de exercícios anteriores se repete | é a alocação de dezembro, por regra |
| pensões militares 2,05× acima | a referência é que estava errada |
| dívida mobiliária de 2,2 bi | é zero |

**Padrão**: em todas, o dado existia. O que faltava era saber onde olhar.

---

## 8. Item 4 executado — quebra por vinculação do Anexo 5

Implementado em `rgf_anexo5_vinculacao.py`. Cada linha do anexo é um filtro de
**fonte de recursos** (posição 2, lista de valores); as colunas vêm do
MAPEAMENTO.

| coluna | contas |
|---|---|
| (b) RP liquidados | 6321, 6313 |
| (c) RP do exercício | 6327 |
| (d) RP não liquidados | 6311, 6312 |

**Resultado: 46 de 54 células exatas** (19 linhas × 3 colunas), contra o QUADRO
PRINCIPAL.

As oito divergências:

| linha | coluna | diferença |
|---|---|---:|
| Recursos Não Vinculados de Impostos | b | +524.118 |
| Recursos Não Vinculados de Impostos | c | +1.769.977 |
| Recursos Não Vinculados de Impostos | d | +1.548.101 |
| Outros Recursos não Vinculados | c | +15.137 |
| Outros Recursos não Vinculados | d | +751.849 |
| Recursos Vinculados a Fundos | c | +8.624.787 |
| Outras Vinculações Legais | b | +594.952 |
| Outras Vinculações Legais | c | +13.522.393 |

Todas são **para mais** e concentradas em três linhas. O padrão sugere que o
anexo desconta algo que o filtro de fonte sozinho não captura — provavelmente os
RP cancelados, que aparecem em coluna própria do demonstrativo.

### 8.1 A fonte 759 e o salto para 48 de 54

"Recursos Vinculados a Fundos" e "Outras Vinculações Legais" **compartilham a
fonte 759**. O anexo a atribui somente à primeira:

```
FR 759 ... 6321 = 581.150,15 | 6313 = 13.801,55 | 6327 = 13.522.392,88
```

Removendo 759 de "Outras Vinculações Legais":

| célula | nosso | oficial |
|---|---:|---:|
| Outras — (b) | 7.213,51 | 7.213,81 |
| Outras — (c) | 13.318.440,16 | 13.318.440,16 |

**48 de 54 células exatas** (89%).

Restam seis, todas concentradas em duas linhas:

| linha | coluna | diferença |
|---|---|---:|
| Recursos Não Vinculados de Impostos | b | +524.118 |
| Recursos Não Vinculados de Impostos | c | +1.769.977 |
| Recursos Não Vinculados de Impostos | d | +1.548.101 |
| Outros Recursos não Vinculados | c | +15.137 |
| Outros Recursos não Vinculados | d | +751.849 |
| Recursos Vinculados a Fundos | c | +8.624.787 |

A hipótese dos RP cancelados **não se confirmou**: subtrair 6329/6319 produz
valores negativos em várias linhas. O caminho agora é a coluna (H) do arquivo,
que trata dos cancelados separadamente.
