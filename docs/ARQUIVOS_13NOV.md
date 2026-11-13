# Os arquivos de 13/11 — o que fecharam

Recebi 10 arquivos. Identifiquei cada um e testei o que cobrem.

---

## 1. Inventário

| arquivo | ano | o que é |
|---|---|---|
| `Relatorio_13112026103042.xls` | 2026 | **Relação Plano Contas MSC × SIGEF** — 18.917 linhas, 12.609 contas |
| `Relatorio_13112026101605.xls` | 2026 | Relação Fonte Recurso MSC × SIGEF — 377 linhas |
| `Imprimir Balancete Consolidado (1).xls` | 2026 | balancete de **julho** |
| `(2)` | 2026 | julho |
| `(3)` | 2026 | **agosto** |
| `(4)` | 2026 | agosto |
| `(5)` e o original | 2025 | encerramento 2025 |
| `Comparativo ... (2).xls` | 2026 | receita |
| `Comparativo ... (3).xls` | 2026 | receita |
| `Comparativo ... (1)` e `(1)(1)` | 2025 | receita |
| `Comparativo ... .xls` | 2024 | receita |

---

## 2. A descoberta: o de-para de contas

O `Relatorio_13112026103042.xls` é a **Relação Plano Contas MSC × SIGEF**:

```
Conta Contábil MSC
1.1.1.1.1.01.00 - CAIXA
1.1.1.1.1.01.00.00 - =Caixa
...
```

**12.609 contas mapeadas.** É exatamente o que faltava para os Anexos 2 e 5 do
RGF — o vínculo entre a conta da matriz e a conta do SIGEF.

Ainda não é o de-para de **linhas de anexo** (qual conta vai em qual linha), mas
é a ponte entre os dois planos de contas.

---

## 3. O que fechou com esses arquivos

### RGF Anexo 1 — 2026 Q2

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| **Despesa Bruta (I)** | 16.107.522.522 | 16.113.277.246 | **−0,04%** |
| Vencimentos | 7.053.932.565 | 7.014.607.987 | +0,56% |
| Obrigações Patronais | 2.519.213.024 | 2.492.438.756 | +1,07% |
| **Aposentadorias** | 5.444.994.850 | 5.444.934.753 | **+0,00%** |
| **Terceirização** | 196.334.588 | 196.334.588 | **−0,00%** |
| Inativos Vinculados | 3.664.873.771 | 3.656.295.712 | +0,23% |
| Pensões | 893.047.496 | 964.961.162 | −7,45% |

**Dois quadrimestres validados**: Q1 em −0,31% e Q2 em −0,04%.

---

## 4. O que **não** fechou: a despesa não executada

Os balancetes de 2026 trazem a conta da não executada assim:

```
saldo anterior :   623.792.553,08 C
movimento D    :   628.259.785,05
movimento C    :     4.467.231,97
saldo final    :              0,00 D
```

**O mesmo valor nos quatro balancetes** (julho e agosto), e **zera no mês**.

Isso não bate com o homologado: a diferença entre a minha apuração e o oficial é
de **R$ 5,8 milhões**, não de R$ 623,8 milhões.

**Conclusão**: o balancete está mostrando o **encerramento** da conta, não a
despesa não executada do período. O valor de R$ 623,8 mi é o saldo que foi
baixado — não o que compõe o Anexo 1.

Para o Anexo 1, a não executada de 2026 é **pequena** (a diferença residual de
R$ 5,8 mi), e a apuração sem ela já fecha em −0,04%.

---

## 5. O que isso significa

| item | situação |
|---|---|
| **RGF A1 — despesa com pessoal** | ✅ **−0,04%** |
| Acervo da MSC | ✅ completo (8 classes, até agosto) |
| Conversor do formato antigo | ✅ |
| **De-para de contas MSC × SIGEF** | ✅ **recebido** |
| De-para de linhas de anexo | ❌ falta (a Relação é de contas, não de linhas) |
| Despesa não executada | ⚠️ o balancete não entrega o valor do período |

---

## 6. O que falta para os outros anexos

O de-para de contas resolve **metade** do problema. Falta a outra metade: **qual
conta vai em qual linha** de cada anexo.

Para o Anexo 2 (DCL): quais contas do passivo compõem "Dívida Contratual",
"Reestruturação", "Parcelamento"...

Para o Anexo 5 (Disponibilidade): o de-para das ~96 fontes de recurso para as
categorias (Educação, Saúde, FUNDEB...).

**A Relação Fonte Recurso** (377 linhas) é o começo do Anexo 5 — liga a FR da MSC
à FR do SIGEF.

---

## 7. Resumo

**O que fechou**: o Anexo 1 do RGF, em dois quadrimestres (−0,31% e −0,04%).

**O que os arquivos trouxeram de novo**: o de-para de contas (12.609 contas) e o
de-para de fontes de recurso (377 linhas) — as duas pontes que faltavam entre a
matriz e o SIGEF.

**O que não fechou**: a despesa não executada pelo balancete. O valor que ele
mostra (R$ 623,8 mi) é o encerramento da conta, não a despesa do período.
