# Motor de coleta e verificação — Siconfi

Três peças novas, construídas para trazer os dados de 2024 a 2026 para dentro do
projeto e conferir o Anexo 1 com o motor novo.

---

## 1. O que existe

| arquivo | função |
|---|---|
| `app/siconfi.py` | coleta: cadastro de entes, diagnóstico dos endpoints, normalização de acervo |
| `app/acervo.py` | índice e leitura da MSC em formato longo (2021-2026) |
| `verificar_anexo1.py` | apura o Anexo 1 pela janela móvel e confere com o homologado |

```bash
python app/siconfi.py --diagnostico            # estado dos endpoints
python app/siconfi.py --entes                  # cadastro de entes (funciona)
python app/siconfi.py --acervo "D:\...\MSC_RN_2021_2026_06" --destino dados/acervo
python verificar_anexo1.py --ano 2024 --quadrimestre 3
```

---

## 2. O acervo encontrado

`D:\Downloads\PASEP Estado\MSC_RN_2021_2026_06` — **198 arquivos**, formato
longo, cobrindo:

| ano | meses |
|---|---|
| 2021 a 2025 | 12 |
| 2026 | 6 (jan-jun) |

Colunas: `poder_orgao`, `natureza_despesa`, `natureza_receita`,
`fonte_recursos`, `complemento_fonte`, `funcao`, `ano_inscricao`, `valor`,
`natureza_conta` (C/D), `tipo_valor`.

Normalizado em `dados/acervo/<ano>/RN_<ano>_<mm>_classe<n>_<saldo>.csv`.

**Classe 8 ausente**: o acervo só tem as classes 3, 4 e 6. A conta de controle
`8.6.3.3.1.00.00` (despesa não executada) não está disponível — é a única linha
que fica zerada.

---

## 3. O diagnóstico dos endpoints

| endpoint | resultado |
|---|---|
| `/tt/entes` | **200** com dados |
| `/tt/rgf` | 200, **0 itens** |
| `/tt/rreo` | 200, **0 itens** |
| `/tt/msc` | **404** |
| consulta RGF / RREO / MSC (HTML) | 200 |

Ou seja: a API de dados abertos **não serve** RGF, RREO nem MSC. As declarações
saem pela área pública de consulta (download manual) e a MSC pela consulta
interativa. Por isso o motor normaliza um acervo local em vez de baixar.

---

## 4. O resultado da verificação de 2024

Janela 2024-01 a 2024-12, movimento líquido do `period_change`.

| linha | apurado | homologado | desvio |
|---|---:|---:|---:|
| **Vencimentos** | 5.749.015.716 | 5.727.095.552 | **+0,38%** |
| Obrigações Patronais | 2.091.575.530 | 2.086.640.220 | +0,24% |
| Aposentadorias | 4.497.126.235 | 4.563.063.879 | −1,45% |
| Pensões | 736.055.738 | 803.877.242 | −8,44% |
| Terceirização | 173.104.090 | 173.463.616 | −0,21% |
| Não Executada | 0 | 454.943.101 | −100% |
| **Despesa Bruta (I)** | 13.246.877.309 | 13.809.083.610 | **−4,07%** |
| Judiciais | 497.395.069 | 497.754.595 | −0,07% |
| Exercícios Anteriores | 87.976.675 | 181.744.273 | −51,59% |
| Indenizações | 25.113.430 | 25.011.201 | +0,41% |
| **Vinculados (dedução)** | 3.119.978.565 | 3.121.824.884 | **−0,06%** |

---

## 5. Duas descobertas que valem para a regra

### 5.1 O CO vazio pertence aos benefícios

Em 2024 o RN registrou:

| CO | aposentadorias | pensões |
|---|---:|---:|
| 1111 | 3.967.849.138 | 570.159.076 |
| **(vazio)** | **528.647.110** | **218.416.120** |
| 1131 | 138.623.290 | 67.377.146 |
| 1121 | 106.895.966 | 14.880.556 |

O motor novo exclui o vazio (foi calibrado em 2025/2026, quando o CO vem
preenchido). Em 2024 isso derruba aposentadorias em −13% e pensões em −36%.
**Incluir o vazio** traz aposentadorias para −1,45%.

### 5.2 A contratação temporária entra em Vencimentos

`3.1.90.04` é mapeada em linha própria (`contratacao_temporaria`) no motor novo.
Mas o homologado de 2024 a soma em **Vencimentos**: sem ela, a linha fecha em
−5,21%; com ela, **+0,38%**.

---

## 6. O que ainda não fecha

| linha | desvio | causa |
|---|---:|---|
| Pensões | −8,44% | a exclusão de `3.1.90.03.05` (que fecha 2025/2026) não vale para 2024 |
| Não Executada | −100% | **classe 8 ausente do acervo** |
| Exercícios Anteriores | −51,59% | o homologado repete R$ 248,7 mi entre janelas — dado oficial inconsistente |

Somando a não executada do homologado (454.943.101,05), a **despesa bruta** vai
para **−0,78%** — melhor que os −0,64% do motor antigo? Não: fica próximo, mas
com uma composição de desvios diferente e mais defensável, porque agora
**Vencimentos fecha em +0,38%** (antes −1,50%) e **Vinculados em −0,06%**.

O motor antigo compensava o erro de Vencimentos com a dupla contagem da despesa
não executada. O motor novo acerta Vencimentos e expõe as pensões.

---

## 7. Para fechar de verdade

| pendência | insumo |
|---|---|
| Não executada (R$ 454,9 mi) | arquivo da **classe 8** do acervo |
| Pensões de 2024 | conferir se `3.1.90.03.05` era pensão em 2024 (mudança de regra?) |
| Exercícios Anteriores | o dado homologado precisa ser refeito pelo ente |
