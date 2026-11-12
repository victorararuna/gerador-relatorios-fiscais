# Extração do DOE-RN por coordenada X

Os Anexos 8 (Educação) e 12 (Saúde) do RREO não integram o arquivo consolidado do
Siconfi — são publicados separadamente. A fonte usada foi o **DOE-RN de
30/01/2025**, que traz os dois relatórios impressos (RREO nas páginas 33-51, RGF
nas 52-55).

---

## 1. O método

O PDF do Diário Oficial não tem estrutura de tabela: cada fragmento de texto é
posicionado por coordenadas. A reconstrução usada:

1. **coleta os X** de todos os fragmentos que são números;
2. **agrupa em clusters** — cada cluster é uma coluna de valores;
3. cada fragmento é **atribuído à coluna** de centro mais próximo;
4. o que fica à esquerda da primeira coluna é o **rótulo** da linha;
5. linha sem número, na faixa do rótulo, é **continuação** do rótulo anterior
   (quebra de linha do PDF) e é concatenada.

O passo 5 é o que resolveu o problema anterior: os rótulos vinham concatenados
porque a quebra de linha do PDF criava fragmentos soltos ("Comunicação – ICMS"
era a segunda linha de "1.1- Receita Resultante do Imposto sobre a Circulação
de Mercadorias e Serviços de Transporte Interestadual e Intermunicipal e de
Comunicação – ICMS").

## 2. Resultado por anexo

### Anexo 8 — Educação: extração completa

**190 linhas com valores.** Colunas (a) Previsão Atualizada e (b) Receitas
Realizadas separadas corretamente:

| Linha | (a) | (b) |
|---|---|---|
| 1- RECEITA DE IMPOSTOS | 10.503.584.000,00 | 10.668.910.603,05 |
| 1.1.1- ICMS Principal e Encargos | 8.344.437.000,00 | 8.414.267.290,50 |
| 1.1.2- Adicional de até 2% do ICMS (FCP) | 124.779.000,00 | 45.626.466,86 |
| 1.2- ITCD | 30.000.000,00 | 45.648.113,46 |
| 1.3- IPVA | 611.368.000,00 | 644.100.255,46 |
| 1.4- IRRF | 1.393.000.000,00 | 1.519.268.476,77 |
| 2- Transferências Constitucionais e Legais | 7.993.147.534,52 | 7.486.895.491,51 |
| 3- Deduções de Transferências aos Municípios | 2.375.313.000,00 | 2.404.734.005,55 |
| **4- TOTAL DA RECEITA LÍQUIDA DE IMPOSTOS** | **16.121.418.534,52** | **15.751.072.089,43** |

A tabela do Anexo 8 tem as colunas bem separadas (rótulo em x≈54, valores em
x≈464 e x≈709), o que permite a clusterização funcionar.

### Anexo 12 — Saúde: extração parcial

A tabela da página 49 tem **as colunas comprimidas entre x≈370 e x≈490** — seis
colunas em 120 pontos, o que dá ~20 pontos por coluna. A clusterização (tolerância
de 60) funde todas numa só.

Tentei ancorar nas posições do cabeçalho, mas o cabeçalho tem títulos em várias
sub-linhas (PREVISÃO INICIAL, Até o bimestre, (b), % (b/a)) e a ancoragem gerou
mais âncoras do que colunas reais, piorando o resultado. Revertido.

**O que resolve:** reduzir a tolerância para ~8 pontos e usar apenas a linha de
cabeçalho principal ("PREVISÃO INICIAL", "Até o bimestre", "%"), ignorando as
sub-linhas de rótulo de coluna. É um ajuste de duas linhas no código, mas exige
calibração manual por anexo — cada tabela do DOE tem densidade diferente.

## 3. Limite do método

A extração por X funciona bem quando:
- as colunas estão separadas por mais de ~40 pontos;
- os valores têm o mesmo número de casas decimais (o alinhamento é à direita).

Ela falha quando a tabela é comprimida ou quando há colunas de texto no meio dos
valores. Nesses casos, o caminho seguro é o **arquivo estruturado** (XLS do
Siconfi), que só não existe para os Anexos 8 e 12.

## 4. O que o DOE de 30/01/2025 entregou

| Página | Conteúdo |
|---|---|
| 33-35 | RREO Anexo 1 — Balanço Orçamentário |
| 36-38 | RREO Anexo 2 — Despesas por função |
| 39-40 | RREO Anexo 3 — RCL |
| 41 | RREO Anexo 6 — Resultado Primário |
| 42 | RREO Anexo 7 — Restos a Pagar |
| **43-44** | **RREO Anexo 8 — Educação** ✅ extraído |
| 45-48 | RREO Anexo 10 — Projeção Atuarial (2 quadros) |
| **49** | **RREO Anexo 12 — Saúde** ⚠️ parcial |
| 50 | RREO Anexo 13 — PPP |
| 51 | RREO Anexo 14 — Simplificado |
| 52 | RGF Anexo 1 — Despesa com Pessoal |
| 53 | RGF Anexo 2 — DCL |
| 54 | RGF Anexo 4 — Operações de Crédito |
| 55 | RGF Anexo 6 — Simplificado |

Esse mapa é o que permite completar os anexos que faltavam no arquivo do Siconfi.
