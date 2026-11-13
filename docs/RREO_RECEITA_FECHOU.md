# RREO — a receita fechou: 41 linhas em 0,00%

O combinador de critérios funcionou. A receita do Balanço Orçamentário reproduz
o homologado linha a linha.

---

## 1. O resultado

| linha | MSC | Homologado | desvio |
|---|---:|---:|---:|
| **RECEITAS (EXCETO INTRA) (I)** | 16.012.885.982,23 | 16.012.885.982,23 | **0,00%** |
| RECEITAS CORRENTES | 15.021.220.158,33 | 15.021.220.158,33 | **0,00%** |
| IMPOSTOS, TAXAS E CONTRIBUIÇÕES | 6.214.117.619,69 | 6.214.117.619,69 | **0,00%** |
| Impostos | 5.779.867.456,50 | 5.779.867.456,50 | **0,00%** |
| Taxas | 434.250.163,19 | 434.250.163,19 | **0,00%** |
| CONTRIBUIÇÕES | 884.518.630,35 | 884.518.630,35 | **0,00%** |
| RECEITA PATRIMONIAL | 168.066.258,34 | 168.066.258,34 | **0,00%** |
| TRANSFERÊNCIAS CORRENTES | 7.150.287.962,42 | 7.150.287.962,42 | **0,00%** |

**41 linhas em 0,00%** — o acumulado até agosto, ao centavo.

---

## 2. Como funciona o combinador

Cada célula do RREO Anexo 1 depende de **dois critérios**:

**1. Conta contábil** — do cabeçalho da coluna:

```
RECEITAS REALIZADAS (b)
  CC começada por LISTA: 6212,6213
  SEM MÊS
  PERIOD_CHANGE MOVIMENTAÇÃO
```

**2. Natureza** — da linha:

```
RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)
  NR começada por 1,2 EXCETO NR (Lista): 211102,211255,212102,212255
```

O valor é a soma dos registros que atendem **aos dois**.

### O bug que travava

O `filtros2.py` só reconhecia `(Lista)` com parênteses. O mapeamento do Anexo 1
escreve `LISTA:` sem parênteses — e o filtro de conta voltava vazio, zerando
todas as linhas.

Corrigido: `\(?Lista\)?`.

---

## 3. O que não fechou: as despesas

As despesas do mesmo anexo deram **zero**.

**Por quê**: o critério de conta das despesas fica na **linha 104**, não na 15:

```
linha 104 (despesas)
  c4 = 'CC começada por 52211; MÊS: 02'          → dotação inicial
  c6 = 'CC começada por LISTA: 62213; SEM MÊS'   → empenhada (acumulada)
  c9 = 'CC começada por LISTA: 6221303,6221304,6221307; SEM MÊS' → liquidada
  c12 = 'CC começada por 6221304; MÊS: 02'
```

**A despesa liquidada** são as contas `6221303, 6221304, 6221307` — que é
exatamente o recorte que eu já vinha usando quando a despesa fechou em +0,02%.

O gerador atual lê o critério de uma única linha (15). Precisa ler por **bloco**
— receitas na 15, despesas na 104.

---

## 4. O Anexo 3 (RCL)

Estrutura diferente:

- **um critério único** de conta na linha 18 (`6.2.1.2.0.00.00 RECEITA REALIZADA + (-) 6.2.1.3...`);
- as colunas são **meses** (`<MR-11>` a `<MR>`), não bimestres.

O `filtros2.py` não interpreta o formato de conta completa com pontos
(`6.2.1.2.0.00.00`). Precisa de um parser que converta `6.2.1.2.0.00.00` em
prefixo `621200000` — que é o formato da MSC.

**É a próxima peça**: normalizar conta pontuada ↔ conta da matriz.

---

## 5. Placar geral

| anexo | situação |
|---|---|
| RGF A1 — Pessoal | ✅ −0,04% |
| RGF A2 — DCL | ✅ 12 linhas em 0,00% |
| RGF A5 — Disponibilidade | ⚠️ interpretador pronto |
| **RREO A1 — Receita** | ✅ **41 linhas em 0,00%** |
| RREO A1 — Despesa | ✅ +0,02% |
| RREO A9 — Operações | ✅ 0,00% |
| RREO A3 — RCL | ⚠️ precisa do parser de conta pontuada |
| RREO A2 — Função | ⚠️ precisa do atributo `funcao` |

---

## 6. O que falta

**Duas peças pequenas:**

1. **Ler o critério por bloco** (receita na linha 15, despesa na 104) — resolve a
   despesa do A1 com o mapeamento, em vez da conta isolada.
2. **Normalizar conta pontuada** (`6.2.1.2.0.00.00` → `621200000`) — destrava o
   Anexo 3 (RCL), que é a base dos limites do RGF.

**Depois disso**: RREO A6 (resultado primário), A11 (alienação) e A14
(simplificado), que usam as mesmas contas.

---

## 7. O que aprendi

O RREO tem **três estruturas de mapeamento**:

| tipo | exemplo | como ler |
|---|---|---|
| critério por coluna | Anexo 1 receitas (linha 15) | linha 15, coluna a coluna |
| critério por bloco | Anexo 1 despesas (linha 104) | blocos separados no mesmo arquivo |
| critério único | Anexo 3 (linha 18) | uma conta para todas as colunas |

Tratar os três como se fossem um foi o que me fez perder tempo. Agora sei
identificar cada um pelo cabeçalho.
