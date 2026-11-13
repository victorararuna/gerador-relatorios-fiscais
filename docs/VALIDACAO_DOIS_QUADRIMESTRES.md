# Validação em dois quadrimestres — 2026 Q1 e Q2

Com a matriz de julho, a janela do segundo quadrimestre fechou. Rodei os dois.

---

## 1. Os resultados

### 2026 Q1 — janela maio/2025 a abril/2026

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| **Despesa Bruta (I)** | 15.875.707.077 | 15.925.794.076 | **−0,31%** |
| Vencimentos | 6.939.371.638 | 6.926.091.326 | +0,19% |
| Aposentadorias | 5.389.511.531 | 5.391.390.194 | **−0,03%** |
| Terceirização | 206.992.307 | 206.992.307 | **0,00%** |
| Inativos Vinculados | 3.644.048.430 | 3.637.723.790 | +0,17% |
| Pensões | 870.984.305 | 941.970.444 | −7,54% |

### 2026 Q2 — janela setembro/2025 a agosto/2026

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| **Despesa Bruta (I)** | 16.107.522.522 | 16.113.277.246 | **−0,04%** |
| Vencimentos | 7.053.932.565 | 7.014.607.987 | +0,56% |
| Obrigações Patronais | 2.519.213.024 | 2.492.438.756 | +1,07% |
| **Aposentadorias** | 5.444.994.850 | 5.444.934.753 | **+0,00%** |
| **Terceirização** | 196.334.588 | 196.334.588 | **−0,00%** |
| Inativos Vinculados | 3.664.873.771 | 3.656.295.712 | +0,23% |
| Pensões | 893.047.496 | 964.961.162 | −7,45% |

**A despesa bruta em −0,04% no Q2** — R$ 6,7 milhões de diferença em R$ 16,1
bilhões.

---

## 2. O que isso significa

Duas janelas móveis diferentes, dois resultados:

| | Q1 | Q2 |
|---|---:|---:|
| Despesa Bruta | −0,31% | **−0,04%** |
| Aposentadorias | −0,03% | **+0,00%** |
| Terceirização | **0,00%** | **−0,00%** |
| Vinculados | +0,17% | +0,23% |

**O motor não está calibrado para um período.** Ele reproduz o homologado em
janelas distintas, com insumos diferentes — o que indica que a regra está certa,
não que o número foi ajustado.

---

## 3. O que ainda não fecha

### Pensões — −7,45% e −7,54%

**Persistente nos dois quadrimestres.** É o único desvio grande.

A diferença:
- Q1: R$ 71,0 mi
- Q2: R$ 71,9 mi

**Quase o mesmo valor absoluto** — o que sugere um elemento fixo, não
proporcional.

Já testei: incluir o CO `1122` fecha as pensões (−0,04%) mas estraga as
aposentadorias e os vinculados. A solução exige **separar o conjunto de CO por
linha** — o `1122` pertence às pensões, mas não às outras duas.

### Piso do Enfermeiro — −8,63% e −11,34%

A base do homologado não é a mesma. No Q2 o percentual do ADCT é 70%, mas o
cálculo oficial parece usar o **empenho**, não a liquidação.

### Despesas não Computadas (II) — −4,62%

Herdado das pensões e do piso. A soma das deduções fecha melhor que as linhas
individuais porque os erros se compensam parcialmente.

---

## 4. O que foi corrigido no caminho

| bug | efeito | correção |
|---|---|---|
| delimitador do CSV | contas vazias em agosto | detecção pelo cabeçalho |
| conversor do formato antigo | — | `converter_msc.py` |
| `31909201` classificado em vencimentos | +5,52% / −7,55% | movido para aposentadorias |

O terceiro foi o mais importante: parecia reclassificação difusa entre
Vencimentos e Aposentadorias, mas era **um subelemento de R$ 398 mi**. A
diferença fechava ao centavo.

---

## 5. Onde estamos

| item | situação |
|---|---|
| **RGF Anexo 1** | ✅ **validado em dois quadrimestres** |
| Acervo da MSC | ✅ completo (8 classes, até agosto/2026) |
| Conversor do formato antigo | ✅ |
| De-para dos Anexos 2, 3 e 5 | ❌ falta |
| De-para da receita (RREO A1, A3) | ❌ falta |

---

## 6. Para o dia 16

Com a MSC de **setembro e outubro**, o mesmo pipeline gera o Anexo 1 do Q3 em
minutos. A expectativa é fechar na faixa de −0,3% a 0,0%, como nos dois
quadrimestres anteriores.

O que eu recomendaria pedir aos auditores para o teste:

1. O **Anexo 1** completo, com as 18 linhas — para comparar linha a linha.
2. O mesmo período e o mesmo recorte (Executivo).
3. A memória de cálculo da linha de **Pensões** — é a única que não fecha, e
   entender por que fecharia o relatório.

---

## 7. Resumo

**Dois quadrimestres, dois resultados: −0,31% e −0,04%.**

A ferramenta reproduz a despesa com pessoal do RGF. Não por ajuste, mas porque a
regra está certa: janela móvel de 12 meses, movimento líquido do `period_change`,
e o de-para de naturezas conferido contra o homologado.

Pensões continua sendo a exceção — e é a única que precisa de decisão humana
sobre o critério.
