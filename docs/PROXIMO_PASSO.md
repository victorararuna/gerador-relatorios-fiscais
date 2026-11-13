# Próximo passo — o que fazer quando o relatório chegar

Documento de operação. Escrito em 13/11/2026, para a retomada de segunda.

---

## 1. O que pedir (e conferir na entrega)

**Relatório:** "Imprimir Execução Orçamentária **por Fonte**" — bloco de
**Restos a Pagar**.

| item | exigência | como conferir |
|---|---|---|
| Poder | os sete: Executivo, TJ, AL, MP, TCE, DP e FDM | cada um deve ter seu bloco |
| Fonte de recursos | coluna presente | sem ela não se aplicam as exclusões |
| Bloco de RP | inscritos, liquidados, pagos, cancelados, separados | |
| Mês | o de fechamento do quadrimestre | ago/2026 para o 2º Q |
| Cabeçalho | `Ano Base:` e `Mês Referência:` legíveis | o validador recusa sem isso |

Se vier só o Executivo, fecham 8 das 14 linhas do Anexo 2. Com os sete, as 14.

---

## 2. O que fazer com o arquivo

### 2.1 Guardar
Salvar em `Arquivos etonjones` com o nome do mês, como os demais.

### 2.2 Implementar a linha dos RP processados

Em `rgf_anexo2_dcl.py`, a função `apurar_secao` hoje só lê o balancete. A linha
`(-) Restos a Pagar Processados` passa a ser calculada assim:

```
para cada Poder p:
    bruto_p = inscritos_ex_anteriores + inscritos_exercicio_anterior
            + liquidados_RPNP - pagos_RPP - pagos_RPNP
            - cancelados_RPP + (liquidado - pago)
    excl_p  = RP(p, FR 32) + RP(p, FR 46) + RP(p, FR 800)
            + RP(p, FR 801) + RP(p, FR 802)
    liquido_p = bruto_p - excl_p

RPP = soma(liquido_p) - saldo de 8.6.3.2.2.00.00
```

Referência de conferência: em 31/08/2026 o publicado é **640.153.394,98**.

### 2.3 Conferir
```
python rgf_anexo2_dcl.py
```
Esperado: **14 de 14 linhas exatas** (hoje 9 de 14).

### 2.4 Atualizar o livro
```
python verificacao.py
```
O livro e o `docs/DIVERGENCIAS.md` se atualizam sozinhos. Esperado: de **267
para 272 células exatas** (as 5 do Anexo 2 fecham).

---

## 3. As três linhas que continuam abertas depois disso

| linha | valor | causa | decisão |
|---|---:|---|---|
| Disponibilidade de Caixa Bruta | +1.850.637,57 | blocos por Poder | precisam das abas "Disponibilidade" |
| (−) Depósitos Restituíveis | +54.946.195,61 | blocos por Poder | aba "Depósitos" |
| Demais Haveres Financeiros | +7.505.813,73 | blocos por Poder | aba "D+ Haveres" |

Essas três não saem do balancete consolidado: ele é do Executivo, e o anexo é
consolidado dos sete Poderes.

**Achado de 13/11 (caminho novo):** a **MSC do Siconfi é consolidada do Estado**
e separa os Poderes por `poder_orgao`. Testando a lista de contas da aba
"Disponibilidade" sobre a MSC de dez/2025:

| PO | Poder | disponibilidade | confere com a aba |
|---|---|---:|---|
| 20212 | TCE | 64.555.550,90 | **exato** |
| 50511 | MP | 13.829.962,38 | **exato** |
| 60611 | DP | 14.858.839,33 | **exato** |
| 30390 | TJ | 330.047.905,00 | a conferir |
| 20211 | AL + FDM | 50.046.336,15 | AL 46.519.232,58 + FDM 3.527.103,57 |
| 10111+10112 | Executivo | 1.085.946.796,13 | resíduo de 10.104.024,53 |

O total dá 1.559.285.389,89 contra 1.549.181.365,36 publicados — **a diferença
está toda no Executivo**, não nos demais Poderes.

**Mas o ajuste fino não fecha.** Testei conta por conta contra a coluna
"Executivo" da aba e as diferenças são compensatórias:

| conta | nosso (MSC) | equipe | diferença |
|---|---:|---:|---:|
| 1.1.1.1.1.02 | 45.608.012,65 | 23.572.282,07 | +22.035.730,58 |
| 1.1.1.1.1.19 | 423.874.247,22 | 383.713.738,02 | +40.160.509,20 |
| 1.1.1.1.1.50 | 605.744.640,93 | 669.641.329,17 | −63.896.688,24 |
| 1.1.1.3.1 | 0,00 | 757.069,91 | −757.069,91 |

A equipe usa uma abertura **diferente** entre as contas (1119 e 1150 trocam de
lugar), e o total só se aproxima por compensação.

Testando exclusões de PO no total consolidado:

| escopo | total | contra o oficial |
|---|---:|---:|
| todos os POs | 1.559.285.389,89 | +10.104.024,53 |
| sem 10112 (RPPS) | 1.548.574.484,56 | −606.880,80 |
| sem 60611 (DP) | 1.544.426.550,56 | −4.754.814,80 |

**Conclusão:** a MSC tem os Poderes, mas a consolidação traz duplicações
intra-estado e a abertura por conta não é a do anexo. O balancete (só Executivo)
chega mais perto — +1.850.637,57 — do que a MSC inteira.

Para fechar essas três linhas é preciso a **abertura por Poder que a equipe usa**
(abas "Disponibilidade", "Depósitos" e "D+ Haveres"), não uma dedução nossa a
partir da matriz.

**Demais Dívidas Contratuais** (272,3 mi contra zero publicado) não é erro: é o
RN alocando o valor em "Outras Dívidas". Decisão de classificação — se quiser
espelhar o publicado, a linha entra como zero com nota.

---

## 4. As duas do Anexo 4 (RREO)

Desvios de **0,02%** (aposentadorias civis) e **0,15%** (pensões civis).

A memória de cálculo da equipe (`RREO 2025_B6_04`, aba "Desp. Previdenciária")
mostra a estrutura em dois blocos:

| bloco | natureza | FR | valor |
|---|---|---|---:|
| RPPS | 31.90.01 | 800 | 3.092.096.126,08 |
| RPPS | 31.90.03 | 800 | 585.867.873,92 |
| Tesouro | 31.90.01 | 500 | 1.556.121.159,85 |
| Tesouro | 31.90.03 | 500 | 48.850.166,20 |
| | 31.90.92 (a−b) | | 275.833.684,57 |

O caminho para fechar: comparar, natureza por natureza, os conjuntos
`APOS_CIVIL`, `PENS_CIVIL`, `PENS_MIL` e `INAT_MIL` de `rreo_anexo4_blocos.py`
com essa memória — lembrando que o sufixo **9203 aparece nos dois conjuntos de
pensões** e que o desvio **não** corresponde a uma natureza isolada (o sufixo
9403 vale 926.078,43; o desvio das pensões é 929.796,71).

---

## 5. O que **não** precisa ser feito

- A planilha da equipe não é mais fonte: o Anexo 1 fecha do dado bruto.
- O Anexo 13 não precisa de cadastro de contratos: só da âncora
  `ANCORA_ARENA` (R$ 60.190.422,53), que é um número por ano.
- A RCL não precisa ser digitada: `limites_do_rreo()` lê o Anexo 3.

---

## 6. Comandos do dia a dia

```bash
python verificar_tudo.py     # 27 conferências de ponta a ponta
python verificacao.py        # gera o livro e o relatório de divergências
python mapa_anexo1.py        # Anexo 1 do mês (MAPA completa)
python rgf_anexo2_dcl.py     # Anexo 2
python rgf_anexo5_vinculacao.py
python rreo_anexo9.py
python rreo_anexo13.py
python rreo_anexo4_blocos.py
python verificar_anos.py     # barra extração de outro exercício
```
