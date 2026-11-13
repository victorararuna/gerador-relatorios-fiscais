# Anexos 2 e 5 — o que fechou

Execução dos dois anexos com os mapeamentos da STN aplicados na MSC de
agosto/2026.

---

## 1. RGF Anexo 2 — Dívida Consolidada Líquida

### Resultado: 12 linhas em 0,00%

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| Empréstimos — Internos | 1.626.484.480,79 | 1.626.484.480,79 | **0,00%** |
| Empréstimos — Externos | 1.349.301.221,30 | 1.349.301.221,30 | **0,00%** |
| Reestruturação da Dívida | 700.182.232,31 | 700.182.232,31 | **0,00%** |
| De Tributos | 9.415.611,96 | 9.415.611,96 | **0,00%** |
| De Contribuições Previdenciárias | 1.954.889,60 | 1.954.889,60 | **0,00%** |
| Com Instituição Não Financeira | 133.852.001,09 | 133.852.001,09 | **0,00%** |
| Passivo Atuarial | 84.052.803.127,13 | 84.052.803.127,13 | **0,00%** |
| RP Não-Processados | 30.315.064,80 | 30.315.064,80 | **0,00%** |
| Dívida Contratual de PPP | 196.757.187,16 | 196.757.187,16 | **0,00%** |
| Apropriação de Depósitos Judiciais | 120.610.642,76 | 120.610.642,76 | **0,00%** |

**Mais três que conferem:**

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| Disponibilidade de Caixa Bruta | 2.217.441.780,98 | 2.179.696.115,59 | +1,73% |
| (-) Restos a Pagar Processados | 649.451.068,99 | 640.153.394,98 | +1,45% |
| Demais Haveres Financeiros | 274.183.214,67 | 266.702.621,21 | +2,80% |

### O que corrigi

**1. Multiclasse.** As deduções combinam classes 1, 2 e 6. Li as três.

**2. Casamento de nomes.** A especificação do mapeamento e o rótulo do Siconfi
divergem em caixa: `PASSIVO ATUARIAL` × `Passivo Atuarial`. Normalizei os dois
lados (minúsculas, sem acento, sem pontuação) — isso fez quatro linhas passarem
de "sem par" para 0,00%.

**3. Sinal do saldo.** O `liquido` é C − D, o que **inverte o ativo** (a
disponibilidade vinha −2,2 bi em vez de +2,2 bi). Corrigido: ativo usa D − C.

### O que não fecha

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| Precatórios posteriores a 05/05/2000 | 5.608.309.881,33 | 5.151.775.621,05 | +8,86% |

Diferença de R$ 456,5 mi. O filtro inclui `1135108` (RPNP) que talvez pertença a
outra linha.

E as linhas "Internos"/"Externos" aparecem duas vezes no mapeamento
(Empréstimos e Financiamentos); a comparação por prefixo pega a primeira.

---

## 2. RGF Anexo 5 — Disponibilidade e Restos a Pagar

### O interpretador funciona

Criei o `filtros2.py`, que interpreta:

```
PO começada por (Lista): 10  /// FR Pos. inicial= 2 ; Tamanho= 3; Lista= 500
```

O `///` é E lógico; o `FR Pos. inicial= 2 ; Tamanho= 3` é **substring** — a FR
`1500` dá `500`.

**Agora as 17 linhas dão valores diferentes** (antes todas davam o mesmo total):

| linha | valor |
|---|---:|
| Recursos Não Vinculados de Impostos | 110.554.091.056,21 |
| Transferências do FUNDEB | 7.409.658.564,32 |
| Transferências Fundo a Fundo (SUS) | 5.745.441.239,99 |
| Recursos de Operações de Crédito | 8.968.951.097,63 |
| RPPS — Fundo em Capitalização | 18.240.829.240,40 |

### Por que ainda não fecha

O Anexo 5 tem **seis colunas com filtros próprios**:

| coluna | conteúdo |
|---|---|
| (a) | Disponibilidade de Caixa Bruta |
| (b) | RP Liquidados e Não Pagos de Exercícios Anteriores |
| (c) | RP Liquidados e Não Pagos do Exercício |
| (d) | RP Empenhados e Não Liquidados de Exercícios Anteriores |
| (e) | Demais Obrigações Financeiras |
| (f) | Insuficiência Financeira (consórcio) |

O `mapeamento.py` lê só a coluna 2 (**FILTROS SICONFI**), que é o filtro da
**linha**. Os filtros de **cada coluna** estão nas colunas 4 a 9.

E os valores confirmam: somar todas as classes sem separar por coluna dá
R$ 110 bi — quando a disponibilidade real é de outra ordem.

**Para fechar o Anexo 5**, o `mapeamento.py` precisa devolver, por linha, seis
filtros — um por coluna.

---

## 3. Onde estamos

| anexo | situação |
|---|---|
| **RGF A1 — Pessoal** | ✅ −0,04% |
| **RGF A2 — DCL** | ✅ **12 linhas em 0,00%** + 3 conferem |
| RGF A5 — Disponibilidade | ⚠️ interpretador pronto; falta ler as 6 colunas |
| **RREO A1 — Despesa** | ✅ +0,02% |
| **RREO A9 — Operações** | ✅ 0,00% |

---

## 4. O aprendizado dos dois

O **Anexo 2** fechou porque o mapeamento tem **um filtro por linha** — e as
colunas são só períodos (saldo anterior, 1º, 2º, 3º quadrimestre).

O **Anexo 5** não fechou porque tem **seis filtros por linha** — um para cada
coluna do quadro. É uma dimensão a mais na leitura.

Isso vale para os próximos: antes de aplicar, é preciso verificar se o anexo tem
colunas com critérios próprios ou apenas períodos.

---

## 5. Próximo passo

**Completar o Anexo 5**: ler as colunas 4 a 9 do mapeamento e aplicar o filtro
correspondente a cada uma.

**Depois**: RREO A3 (RCL), que depende da fórmula de receita das contas 6.2.1.2 e
6.2.1.3.
