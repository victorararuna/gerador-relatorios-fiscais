# Estrutura oficial do RREO no Siconfi

Fonte: **Guia de Preenchimento das Declarações do Siconfi — RREO** (Regras Gerais
e Instruções de Preenchimento, edição 2026), página 7.

Arquivo: `MDF_STN/_apoio/2026_Regras_Gerais_Instrucoes_RREO.pdf`

---

## 1. Os anexos que compõem o RREO no Siconfi

O guia lista **onze** anexos:

| Anexo | Demonstrativo |
|---|---|
| 1 | Balanço Orçamentário |
| 2 | Execução das Despesas por Função / Subfunção |
| 3 | Receita Corrente Líquida |
| 4 | Receitas e Despesas Previdenciárias |
| 6 | Resultados Primário e Nominal |
| 7 | Restos a Pagar por Poder e Órgão |
| 9 | Receitas de Operações de Crédito e Despesas de Capital |
| 10 | Projeção Atuarial do Regime de Previdência |
| 11 | Receita de Alienação de Ativos e Aplicação dos Recursos |
| 13 | Parcerias Público-Privadas |
| 14 | Demonstrativo Simplificado do RREO |

**Não há Anexo 5, 8 nem 12 nessa lista.**

## 2. Onde ficam os Anexos 8 e 12

A STN é explícita:

> "As informações e os dados relacionados ao **Anexo 8** — Demonstrativo das
> Receitas e Despesas com Manutenção e Desenvolvimento do Ensino — e ao
> **Anexo 12** — Demonstrativo das Receitas e Despesas com Ações e Serviços
> Públicos de Saúde — do Relatório Resumido da Execução Orçamentária deverão ser
> enviados, respectivamente, ao **Sistema de Informações sobre Orçamentos
> Públicos em Educação (SIOPE)** e ao **Sistema de Informação sobre Orçamento
> Público em Saúde (SIOPS)**.
>
> Ressalta-se que as informações prestadas no Siconfi devem refletir aquelas
> declaradas para fins de publicação e cumprimento da LRF."

**Consequência prática:** o arquivo consolidado do RREO no Siconfi **nunca**
conterá os Anexos 8 e 12. A ausência deles não é falha de extração nem de
declaração — é a arquitetura do sistema.

A fonte para esses dois anexos é:
- **Educação (Anexo 8)**: SIOPE — `siope.inep.gov.br`
- **Saúde (Anexo 12)**: SIOPS — `sops.datasus.gov.br`

Alternativamente, os valores publicados no **DOE-RN** (edição de 30/01/2025,
páginas 43-44 e 49) reproduzem os dois anexos.

## 3. O que isso significa para o projeto

O arquivo `SICONFI_RREO_171_BIMESTRAL_6.xls` tem **exatamente as 11 abas** da
lista oficial:

```
RREO-Anexo 01 · 02 · 03 · 04 · 06 · 07 · 09 · 10 · 11 · 13 · 14
```

Ou seja: **o RREO está completo em anexos**. O que falta não são anexos — são os
**rótulos** das linhas, que o arquivo do Siconfi não traz para a maioria deles.

| Anexo | Rótulos |
|---|---|
| 01 | ✅ no XLS (100%) |
| 02 | parcial no XLS (39%) |
| 03 | ✅ catálogo minerado |
| 04 | ✅ catálogo minerado |
| 06 | ✅ catálogo minerado |
| 07 | ✅ catálogo minerado |
| 09 | ❌ sem rótulo |
| 10 | ❌ sem rótulo |
| 11 | ❌ sem rótulo |
| 13 | ❌ sem rótulo |
| 14 | ❌ sem rótulo |

## 4. O Anexo 5

O guia não o menciona. Na 14ª edição do MDF o Anexo 5 do RREO
("Demonstrativo das Receitas e Despesas Previdenciárias do RPPS") foi
incorporado ao Anexo 4, que passou a tratar das receitas e despesas
previdenciárias em quadros próprios. Por isso a numeração salta do 4 para o 6.

## 5. Próximo passo para os rótulos que faltam

O DOE-RN de 30/01/2025 tem os anexos publicados com rótulo. O mapa de páginas é:

| Página | Anexo |
|---|---|
| 33-35 | 1 |
| 36-38 | 2 |
| 39-40 | 3 |
| 41 | 6 |
| 42 | 7 |
| 43-44 | **8 (SIOPE)** |
| 45-48 | 10 |
| 49 | **12 (SIOPS)** |
| 50 | 13 |
| 51 | 14 |
| 52 | RGF 1 |
| 53 | RGF 2 |
| 54 | RGF 4 |
| 55 | RGF 6 |

Com a extração por coordenada X calibrada por anexo (a tolerância varia com a
densidade da tabela), os rótulos de 10, 13 e 14 saem do DOE. O Anexo 9 não
apareceu no intervalo mapeado e precisa ser localizado.
