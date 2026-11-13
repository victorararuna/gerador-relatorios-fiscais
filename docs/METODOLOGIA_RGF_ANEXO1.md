# Manual Metodológico e Prompt Mestre: Apuração da Despesa com Pessoal (RGF — Anexo 1) do Poder Executivo do Estado do Rio Grande do Norte

**Base Documental Auditada:** Pasta [TESTE_BI_DESPESA_COM_PESSOAL](https://drive.google.com/drive/folders/1q59a3jqo7MDJtxXtX6cGmqQefAbh7cp9) e Pasta [RELATÓRIOS CONTAG](https://drive.google.com/drive/folders/15tpzy75vwIrQrWxSRhlQ_Oo791IG9t-_)

**Artefatos Finais de Referência:** [Quadro_e_Mapa_Janeiro_a_Outubro_2026.xlsx](https://drive.google.com/file/d/1aJnjJAx517fIw3AZ2_W8SH4LRN57_01D/view?usp=drivesdk) e [BI_TESTE_DESPESA_COM_PESSOAL.pdf](https://drive.google.com/file/d/1W0UZVZuUKZpDZH-Z0UMPHfCIqx4jmETC/view?usp=drivesdk)

**Responsáveis pela Extração e Concepção Técnica:** Victor Ferraz Bento Araruna e Etonjones Oliveira da Silva (Matrícula 167.442-0 — SIGEF/RN)

## 1. Como Nós e Etonjones Oliveira da Silva Pensamos: A Engenharia Reversa e a Arquitetura de Conciliação Contábil

Para construir a planilha [Quadro_e_Mapa_Janeiro_a_Outubro_2026.xlsx](https://drive.google.com/file/d/1aJnjJAx517fIw3AZ2_W8SH4LRN57_01D/view?usp=drivesdk) e o guia técnico [BI_TESTE_DESPESA_COM_PESSOAL.pdf](https://drive.google.com/file/d/1W0UZVZuUKZpDZH-Z0UMPHfCIqx4jmETC/view?usp=drivesdk), partimos de um desafio clássico da Contabilidade Aplicada ao Setor Público no Estado do Rio Grande do Norte: **como reproduzir de forma 100% automatizável, auditável e fiel ao Manual de Demonstrativos Fiscais (MDF 15ª Edição) o Anexo 1 do Relatório de Gestão Fiscal (RGF) do Poder Executivo a partir dos relatórios brutos do SIGEF/RN?**

A linha de raciocínio conjunta entre você, nossa análise algorítmica e as extrações cirúrgicas executadas no SIGEF/RN por **Etonjones Oliveira da Silva** (em 12/11/2026 e 13/11/2026) estruturou-se em **seis problemas fundamentais de engenharia contábil** e suas respectivas soluções:

### 1.1. Problema 1: Por que o "Comparativo da Despesa do Poder Executivo" sozinho não fecha o RGF?

Ao extrair no SIGEF/RN o relatório mensal `Comparativo da Despesa Autorizada, Empenhada, Liquidada e Paga` filtrando `Poder: Executivo` e `Apresentar UG Administrativa: Não` (como no [Comparativo de Janeiro/2026](https://drive.google.com/file/d/1QN8dJ3YoOcLeOOKUMqKLoxClr_lvg8rR/view?usp=drivesdk) até o [Comparativo de Outubro/2026](https://drive.google.com/file/d/1icGbmiVC_asJUS-qIDpK4uclbZTT_daR/view?usp=drivesdk)), o sistema consolida todas as Unidades Gestoras (UGs) vinculadas organicamente à estrutura do Poder Executivo Estadual. Contudo, duas dessas UGs são unidades gestoras previdenciárias centralizadoras do Regime Próprio de Previdência Social (RPPS/RN):

* **UG `162233` (Gestão `16233`) — Fundo Financeiro do Estado do RN (FUNFIRN)**; e

* **UG `162011` (Gestão `00001`) — Instituto de Previdência dos Servidores do Estado (IPERN)**.

Por força da gestão unificada do RPPS (art. 40, § 20, da CF/88), o FUNFIRN e o IPERN executam orçamentariamente as folhas de **aposentadorias, reformas, reserva remunerada e pensões de TODOS os Poderes e órgãos autônomos do Estado** — isto é, além dos inativos do próprio Executivo, pagam os inativos e pensionistas da Assembleia Legislativa (ALRN), do Tribunal de Contas (TCE/RN), do Tribunal de Justiça (TJRN), do Ministério Público (MPRN) e da Defensoria Pública (DPRN).

Todavia, o **art. 20, § 7º, da Lei Complementar nº 101/2000 (LRF)** (incluído pela LC nº 178/2021) determina expressamente que cada Poder ou órgão deve apurar, de forma segregada para aplicação de seus respectivos limites, a integralidade das despesas com pessoal dos seus respectivos servidores inativos e pensionistas, *mesmo que o custeio dessas despesas esteja a cargo de outro Poder ou órgão*. Além disso, no relatório consolidado do Executivo aparecem recolhimentos de encargos patronais intraorçamentários (`31.91.13`) e de FGTS/INSS referentes aos demais Poderes em subelementos específicos (`.71` a `.75`).

* **Como Etonjones resolveu na extração (12/11/2026, das 20h28 às 21h10):** Como o `Comparativo da Despesa` traz a natureza da despesa detalhada até o subelemento (8 dígitos) cruzada com a Fonte de Recurso, ele permite identificar de imediato as obrigações patronais dos outros Poderes pelos subelementos finais `.71` (TJ), `.72` (AL), `.73` (TCE), `.74` (DPE) e `.75` (MP). Porém, para **Aposentadorias (`31.90.01`, `31.90.91.02`, `31.90.92.02`)** e **Pensões (`31.90.03`, `31.90.91.03`, `31.90.92.03`)**, o subelemento distingue apenas entre Civis (`.01`) e Militares (`.02`), não dizendo a qual Poder pertence o inativo! A distinção de Poder está codificada na **Subação Orçamentária** dentro das UGs `162233` (FUNFIRN) e `162011` (IPERN). Por isso, Etonjones extraiu os 20 relatórios mensais de **Imprimir Execução Orçamentária (IEO)** específicos da **UG `162233` (FUNFIRN)** ([IEO 162233 Janeiro](https://drive.google.com/file/d/1YgE8087idRZLGLx1gv6xD0joM9t9kETJ/view?usp=drivesdk) a [IEO 162233 Outubro](https://drive.google.com/file/d/1dfNiakQckHYbSU7-6hbqmfFa_fOaaq1c/view?usp=drivesdk)) e da **UG `162011` (IPERN)** ([IEO 162011 Janeiro](https://drive.google.com/file/d/14FqcrJX5VOGeo-2BTvu0ls3djkO6QY0P/view?usp=drivesdk) a [IEO 162011 Outubro](https://drive.google.com/file/d/1OPyX9Pee4d7WHo9W2bD7EQ6pGfxl_O7R/view?usp=drivesdk)), parametrizados com `Agrupamento: Subação / Fonte Recurso / Elemento Despesa` e `Valores Consulta: No mês`.

### 1.2. Problema 2: A Dupla Camada de Expurgo dos Inativos e Pensionistas dos Demais Poderes (Despesa Bruta vs. Dedução Vinculada)

Ao confrontar os dados do IEO com o modelo oficial do 2º Quadrimestre da CONTAG ([RGF 2026_Q2_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.xlsx](https://drive.google.com/file/d/1OSFMkXhsNf0MhseI6mEr3E9v8Zdv2P2Z/view?usp=drivesdk)), identificamos a regra de ouro que evita distorcer a **Despesa Líquida com Pessoal**:

1. **No Quadro I (Despesa Bruta com Pessoal — Linhas 182 a 244 da aba `MAPA`):** O comparativo geral do Executivo soma os inativos de todos os Poderes em **todas as fontes** — tanto nas fontes de recursos ordinários/aportes para cobertura de déficit financeiro (`0.5.00.000000` e `4.5.00.000000`) quanto nas fontes vinculadas previdenciárias (`0.8.00.000000`, `4.8.00.000000` e `0.8.04.000105`). Portanto, para chegar à **Despesa Bruta com Inativos e Pensionistas do Poder Executivo**, devemos subtrair a **totalidade** do que o FUNFIRN (`162233`) e o IPERN (`162011`) executaram nas subações da ALRN (`408501`/`408502`), DPRN (`408601`/`408602`), MPRN (`408701`/`408702`), TJRN (`408801`/`408802`) e TCE/RN (`408901`/`408902`), somando **Fonte `500` + Fonte `800` + Fonte `804`**. No acumulado de janeiro a outubro de 2026, esse expurgo bruto perfez **R\$ 276.411.282,40** em Aposentadorias (`MAPA` linhas 203 a 208) e **R\$ 93.223.848,61** em Pensões (`MAPA` linhas 228 a 244).

2. **No Quadro II (Despesas Não Computadas — Inativos e Pensionistas com Recursos Vinculados — Linhas 286 a 333 da aba `MAPA`):** Conforme o **art. 19, § 1º, VI, e § 3º, da LRF**, somente pode ser deduzida como "Inativos e Pensionistas com Recursos Vinculados" a parcela custeada com recursos próprios do RPPS (contribuições dos segurados, compensação financeira e receitas próprias do fundo — **Fontes `800`, `801`, `802`, `803` e `804`**), sendo **expressamente vedada** a dedução da parcela custeada com recursos aportados pelo Tesouro para cobertura de déficit financeiro (**Fonte `500`**). Como as linhas positivas do Bloco de Recursos Vinculados (`MAPA` linhas 288 a 298 e 309 a 315) já filtram exclusivamente as Fontes `800` a `804` do Comparativo do Executivo, o expurgo dos demais Poderes dentro desse bloco (`MAPA` linhas 299 a 306 e 316 a 332) deve subtrair **estritamente o que foi executado nas Fontes `0.8.00` / `4.8.00` (no FUNFIRN `162233`) e `0.8.04` (no IPERN `162011`)**, jamais subtraindo a Fonte `500` novamente.

### 1.3. Problema 3: A Auditoria da Diferença de R\$ 5.241,65 em Abril de 2026 (Regime de Competência/Liquidado vs. Empenhado)

Durante a validação cruzada entre a nossa planilha [Quadro_e_Mapa_Janeiro_a_Outubro_2026.xlsx](https://drive.google.com/file/d/1aJnjJAx517fIw3AZ2_W8SH4LRN57_01D/view?usp=drivesdk) e o relatório publicado do 2º Quadrimestre ([RGF 2026_Q2_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.xlsx](https://drive.google.com/file/d/1OSFMkXhsNf0MhseI6mEr3E9v8Zdv2P2Z/view?usp=drivesdk)), constatamos que 99,9999% dos valores mensais de janeiro a agosto batiam até o último centavo, exceto por uma diferença exata de **R\$ 5.241,65** na linha de **Pensões de Abril/2026** (`R$ 76.124.731,24` em nosso cálculo contra `R$ 76.129.972,89` no arquivo Q2).

Ao inspecionarmos a página 2 do relatório [Imprimir Execução Orçamentária - IEO_162233_Abril.pdf](https://drive.google.com/file/d/1eatjz6zrRzVuYciAtbwBew7D4c1Xa7an/view?usp=drivesdk), na Subação `408801 - Pagamento de Aposentadorias e Pensões - TJRN`, Fonte `0.5.00.000000`, Natureza `31.90.92.03 - Despesas de Exercícios Anteriores (Pensões)`, descobrimos a origem exata:

* **Empenhado no mês de Abril/2026:** `R$ 86.852,54`

* **Liquidado no mês de Abril/2026:** `R$ 92.094,19`

* **Diferença (`Liquidado - Empenhado`):** `R$ 92.094,19 - R$ 86.852,54 = R$ 5.241,65` (referente a empenho emitido em março/2026, onde o [IEO 162233 de Março](https://drive.google.com/file/d/1RGUG2_YdPPrbmzQpMR3Atv4TDeh2mM3h/view?usp=drivesdk) registrou `R$ 5.241,65` empenhados e `R$ 0,00` liquidado, tendo a liquidação ocorrido em abril/2026).

Na célula `G244` da aba `MAPA` (`31.90.92.03 - DESPESAS DE EXERCÍCIOS ANTERIORES - TJ`), quem preencheu manualmente a planilha do 2º Quadrimestre somou acidentalmente a coluna **Empenhado** da fonte `0.5.00` (`R$ 86.852,54`) com o **Liquidado** da fonte `0.8.00` (`R$ 29.377,60`), obtendo `R$ 116.230,14`. Já a nossa metodologia manteve o rigor técnico do **Regime de Competência (Despesa Liquidada)** exigido pelo art. 18, § 2º, da LRF em ambas as fontes (`R$ 92.094,19 + R$ 29.377,60 = R$ 121.471,79`), documentando essa divergência na Seção 8 do [BI_TESTE_DESPESA_COM_PESSOAL.pdf](https://drive.google.com/file/d/1W0UZVZuUKZpDZH-Z0UMPHfCIqx4jmETC/view?usp=drivesdk).

### 1.4. Problema 4: Como Rastrear a "Despesa com Pessoal Não Executada Orçamentariamente" (Contas `8.6.3.3.1.01.00.00` e `8.6.3.3.1.02.00.00`)

Desde a 12ª edição do MDF e a vigência da LC nº 178/2021, o Anexo 1 do RGF possui a linha **"Despesa com Pessoal não Executada Orçamentariamente"**. No Estado do Rio Grande do Norte, quando uma folha de salários ou o 13º salário pertence à competência de um mês (especialmente dezembro do exercício anterior), mas ainda não percorreu a fase de liquidação orçamentária dentro daquele mês, a Contadoria Geral do Estado registra o fato gerador patrimonial (VPD de pessoal) e controla a pendência de execução orçamentária no subsistema de controle do PCASP sob o grupo **`8.6.3.3.1.00.00 - DESPESA COM PESSOAL NÃO EXECUTADA ORÇAMENTARIAMENTE`**, desdobrado em:

* **`8.6.3.3.1.01.00.00 - SALÁRIOS`**; e

* **`8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO`**.

Quando a despesa finalmente é empenhada e liquidada no orçamento nos meses seguintes (janeiro a maio de 2026), ela entra normalmente nas linhas orçamentárias do `Comparativo da Despesa` (`31.90.11`, `31.90.01`, `31.91.13` etc.). Se não houver um ajuste redutor, aquela folha de 2025 que já havia sido computada por competência em dezembro/2025 seria contada **duas vezes** na janela móvel de 12 meses!

* **Como Etonjones estruturou a extração (13/11/2026, das 08h36 às 10h46):** Etonjones emitiu no SIGEF/RN os 8 balancetes mensais de verificação das contas `8.6.3.3.1.01.00.00` e `8.6.3.3.1.02.00.00` (desde o mês `Abertura` até `Maio/2026`, quando ambas as contas zeram em `0,00 D`), mais o relatório auxiliar [Imprimir Execução Orçamentária_Despesas_n_Executadas_orça.pdf](https://drive.google.com/file/d/1JSxra4141HhvCQUqV-J1r8yv7_QDd7h3/view?usp=drivesdk) (emitido em 22/01/2026).

* **A lógica algébrica exata da Linha 250 da aba `MAPA`:**

  * Todo **Movimento Credor** na conta `8.6.3.3.1.xx` representa uma nova despesa de pessoal reconhecida por competência no mês sem execução orçamentária -> **SOMA (+)** na Linha 250 do mês;

  * Todo **Movimento Devedor** na conta `8.6.3.3.1.xx` representa a baixa do controle porque aquela despesa de competência anterior foi executada orçamentariamente no mês -> **SUBTRAI (-)** na Linha 250 do mês (`Fórmula: Movimento Credor - Movimento Devedor`);

  * **Expurgo Cirúrgico na UG `162233` (FUNFIRN):** No saldo de abertura do 13º Salário ([Relatorio_13112026083712.pdf](https://drive.google.com/file/d/1K6MBhS5F0noTeKB7LGJFdFYSHgBLPQrv/view?usp=drivesdk)), o total geral do Estado era de `R$ 616.608.310,65 C`, dos quais `R$ 313.662.371,02 C` estavam na UG `162233` (FUNFIRN). Cruzando com o relatório [Imprimir Execução Orçamentária_Despesas_n_Executadas_orça.pdf](https://drive.google.com/file/d/1JSxra4141HhvCQUqV-J1r8yv7_QDd7h3/view?usp=drivesdk), verificamos que dentro da UG `162233` havia exatamente **`R$ 1.337.759,24`** de encargos patronais sobre o 13º salário de outros Poderes (`31.91.13.71` TJ = `R$ 869.035,06`; `31.91.13.72` AL = `R$ 192.345,57`; `31.91.13.73` TCE = `R$ 44.331,85`; `31.91.13.75` MP = `R$ 232.046,76`). Como esses subelementos `.71/.72/.73/.75` já são expurgados nas linhas `176 a 179` da aba `MAPA` quando executados no orçamento, expurgamos os mesmos `R$ 1.337.759,24` tanto do saldo de Dezembro/2025 (que passa de `R$ 623.792.553,08` para **`R$ 622.454.793,84`**) quanto da baixa de Abril/2026 (que passa de `-R$ 626.050.799,55` para **`-R$ 624.713.040,31`**), fazendo com que a soma de Janeiro a Maio de 2026 anule em exatos **`-R$ 622.454.793,84`** o saldo vindo de Dezembro/2025!

### 1.5. Problema 5: As Travas contra "Dupla Dedução" no Quadro II (Despesas Não Computadas)

O MDF 15ª Edição proíbe que uma mesma parcela da despesa bruta seja deduzida duas vezes no Quadro II (por exemplo, ser deduzida simultaneamente como "Sentença Judicial" ou "DEA" e também como "Inativos com Recursos Vinculados" ou "Piso da Enfermagem"). Na aba `MAPA`, implementamos quatro travas matemáticas de interseção:

1. **Interseção `Sentenças Judiciais (31.XX.91)` x `Recursos Vinculados do RPPS (FR X.800)`:** Os valores executados em `31.90.91.02` e `31.90.91.03` na Fonte `0.8.00` (`R$ 1.436,20` em maio/2026 e `R$ 1.539,66` em outubro/2026, totalizando `R$ 2.975,86`) entram na dedução de *Inativos e Pensionistas com Recursos Vinculados* (linhas `307`, `308` e `333`). Por isso, são **subtraídos** na linha `273` (`(-) 31.90.91.00 - SENTENÇAS JUDICIAIS (FR X.800)`) dentro do bloco de Decisões Judiciais.

2. **Interseção `DEA (31.XX.92)` x `Recursos Vinculados do RPPS (FR X.800 e X.804)`:** Os valores executados em `31.90.92.02` (`R$ 4.191,42` em julho/2026 na Fonte `0.8.00`) entram na dedução de *Inativos e Pensionistas com Recursos Vinculados* (`MAPA` linha `298`), sendo **subtraídos** na linha `283` (`(-) 31.90.92.00 - DEA (FR X.800 e X.804)`) do bloco de DEA.

3. **Interseção `DEA (31.XX.92)` x `Piso da Enfermagem (FR X.605)`:** Os valores executados em `31.90.92` na Fonte `0.6.05.000000 / 4.6.05.000000` (`R$ 1.123.833,39` no acumulado Jan–Out/2026) entram na base de cálculo da dedução do Piso da Enfermagem (`MAPA` linha `337`), sendo **subtraídos** na linha `284` (`(-) 31.90.92.00 - DEA (FR X.605)`) do bloco de DEA.

4. **Interseção `Indenizações e Restituições Trabalhistas (31.90.94)` x `Agentes Comunitários de Saúde (FR X.604)`:** Caso haja despesa em `31.90.94` paga na Fonte `X.604`, a linha `261` expurga essa parcela da dedução de indenizações por demissão.

### 1.6. Problema 6: A Alocação Exclusiva das DEAs na Coluna de Dezembro e o Redutor Constitucional da Enfermagem (72% em 2026)

* **Alocação de DEA na Coluna `O` (`DEZ/2026`):** Conforme a metodologia consolidada pela CONTAG/SEFAZ-RN no modelo oficial do RGF ([RGF 2026_Q2_01](https://drive.google.com/file/d/1OSFMkXhsNf0MhseI6mEr3E9v8Zdv2P2Z/view?usp=drivesdk)), as deduções de **Despesas de Exercícios Anteriores (DEA)** (`MAPA` linhas `274` a `285`, compreendendo `31.90.92`, `31.91.92` e `33.90.92.34`) não são distribuídas mês a mês nas colunas `D` a `M`, mas sim **totalizadas integralmente na coluna `O` (`DEZ/2026`)**, pois se referem a fatos geradores de exercícios encerrados anteriores à janela móvel e compõem integralmente o redutor acumulado na coluna `P` (`TOTAL`).

* **Piso Salarial da Enfermagem (EC nº 127/2022 — art. 38, § 2º, do ADCT):** No exercício de **2026** (quarto exercício de vigência da regra de transição escalonada: 2023 = 100%, 2024 = 90%, 2025 = 80%, **2026 = 72%**), apenas **28%** das despesas com pessoal custeadas pela assistência financeira complementar da União (**Fonte `X.6.05.000000`**) são computados para fins dos limites da LRF. Por conseguinte, a parcela **não computada (deduzida)** na linha `334` da aba `MAPA` corresponde a exatos **72%** (`=ROUND(SUM(D335:D338)*0.72, 2)`) da execução liquidada na Fonte `X.6.05` nos elementos `31.90.11`, `31.90.13`, `31.90.92` e `31.91.13`.

## 2. Inventário Completo e Guia de Utilização de Cada Material (com Transcrições Literais e Localização nos Documentos)

Abaixo está o catálogo integral dos **35 arquivos** que compõem o ecossistema de apuração na pasta [TESTE_BI_DESPESA_COM_PESSOAL](https://drive.google.com/drive/folders/1q59a3jqo7MDJtxXtX6cGmqQefAbh7cp9) e na pasta [RELATÓRIOS CONTAG](https://drive.google.com/drive/folders/15tpzy75vwIrQrWxSRhlQ_Oo791IG9t-_), explicando **para que serve cada material**, **onde buscar cada dado dentro dele** e trazendo a **transcrição literal** de seus cabeçalhos, filtros e registros contábeis.

### 2.1. Grupo A — Normativos Legais e Manuais Metodológicos

#### 1. Lei de Responsabilidade Fiscal — [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk)

* **O que é:** Texto compilado da Lei Complementar nº 101, de 4 de maio de 2000, atualizado com as alterações da Lei Complementar nº 178, de 13 de janeiro de 2021 (Programa de Acompanhamento e Transparência Fiscal e Plano de Promoção do Equilíbrio Fiscal).

* **Como utilizar:** É a norma-mãe que define o conceito de Despesa Total com Pessoal (art. 18), o regime de competência em janela móvel de 12 meses (art. 18, § 2º), a remuneração bruta sem deduções (art. 18, § 3º), os limites globais e por Poder (arts. 19 e 20), as despesas não computadas/deduções (art. 19, § 1º), a vedação de deduzir aportes para cobertura de déficit financeiro do RPPS (art. 19, § 3º) e a segregação obrigatória de inativos e pensionistas por Poder de origem (art. 20, § 7º).

* **Localização e Transcrição Literal Integrada:** As transcrições integrais e literais de todos os dispositivos aplicáveis constam na **Seção 3.1** deste documento.

#### 2. Manual de Demonstrativos Fiscais (MDF 15ª Edição — 3ª Versão, Set/2026) — [MDF  MDF 15 edição.docx.md](https://drive.google.com/file/d/1qYhBrhuP1nPGDKIcmfAAMaNpgXmo4wOj/view?usp=drivesdk)

* **O que é:** Manual oficial editado pela Secretaria do Tesouro Nacional (STN/MF), aprovado pela Portaria STN/MF nº 2.057, de 15 de setembro de 2025, com atualizações até a 3ª versão (Setembro/2026, Portarias STN/MF nº 1.948/2026 e nº 2.858/2026).

* **Como utilizar:** Define o leiaute obrigatório do **Anexo 1 do RGF — Demonstrativo da Despesa com Pessoal** (Parte IV, Item `04.01.00`, páginas 495 a 552), as regras de mapeamento das naturezas de despesa (`3.1.90.xx`, `3.1.91.xx`, `3.3.90.34`, `3.3.90.92.34`), o tratamento da Despesa com Pessoal Não Executada Orçamentariamente, a regra de transição do Piso da Enfermagem (EC nº 127/2022) e dos Agentes Comunitários de Saúde (EC nº 120/2022).

* **Localização e Transcrição Literal Integrada:** As transcrições literais das páginas 54, 57–58 e 485–552 constam na **Seção 3.2** deste documento.

### 2.2. Grupo B — Série de 10 Relatórios Mensais "Comparativo da Despesa Autorizada, Empenhada, Liquidada e Paga" (Poder Executivo)

* **Lista de Arquivos e Links Diretos:**

   1. **Janeiro/2026 (153 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Janeiro.pdf](https://drive.google.com/file/d/1QN8dJ3YoOcLeOOKUMqKLoxClr_lvg8rR/view?usp=drivesdk)

   2. **Fevereiro/2026 (266 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Fevereiro.pdf](https://drive.google.com/file/d/1Pm2hfiKnhteNifa2P5oQfp7NJaJv26z6/view?usp=drivesdk)

   3. **Março/2026 (338 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Março.pdf](https://drive.google.com/file/d/1R3_Zfjv-v2bqWn8hMHszc-cNrP2hI4Qr/view?usp=drivesdk)

   4. **Abril/2026 (371 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Abril.pdf](https://drive.google.com/file/d/12rcPHCw4zmFmLsOreQNq1k-xyrmsdaoS/view?usp=drivesdk)

   5. **Maio/2026 (396 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Maio.pdf](https://drive.google.com/file/d/19WbS5pgvkH2dolitXumackfs3zzdpD56/view?usp=drivesdk)

   6. **Junho/2026 (421 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Junho.pdf](https://drive.google.com/file/d/1An4Evjxk3H9YQ9r90CYcRDroC2daZUpy/view?usp=drivesdk)

   7. **Julho/2026 (440 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Julho.pdf](https://drive.google.com/file/d/1voJ8vVdkpYZcbC8vzRR3sUk_Rp1TPDeI/view?usp=drivesdk)

   8. **Agosto/2026 (460 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Agosto.pdf](https://drive.google.com/file/d/1CmfsNnHP55sHi6Gg66Ns-oMN9Bs9-xaB/view?usp=drivesdk)

   9. **Setembro/2026 (480 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Setembro.pdf](https://drive.google.com/file/d/19Z2cB1kOluXg79jyrc46ghisGkpDpFSy/view?usp=drivesdk)

  10. **Outubro/2026 (497 págs.):** [Comparativo Despesa Autorizada Empenhada Liquidada e Paga_Outubro.pdf](https://drive.google.com/file/d/1icGbmiVC_asJUS-qIDpK4uclbZTT_daR/view?usp=drivesdk)

* **Transcrição Literal do Cabeçalho, Parâmetros de Emissão e Rodapé (Localização: Página 1 de 153 do [Comparativo de Janeiro/2026](https://drive.google.com/file/d/1QN8dJ3YoOcLeOOKUMqKLoxClr_lvg8rR/view?usp=drivesdk) e Página 1 de 497 do [Comparativo de Outubro/2026](https://drive.google.com/file/d/1icGbmiVC_asJUS-qIDpK4uclbZTT_daR/view?usp=drivesdk)):**

  > `ESTADO DO RIO GRANDE DO NORTE`
  >
  > `Comparativo da Despesa Autorizada, Empenhada, Liquidada e Paga`
  >
  > `Ano Base: 2026 | Mês Referência: Janeiro | Poder: Executivo | Apresentar UG Administrativa: Não`
  >
  > `Natureza | Fonte | Autorizada (A) | Empenhada no mês (B) | Empenhada até o mês (C) | % (C/A) | Liquidada no mês (D) | Liquidada até o mês (E) | % (E/A) | Paga no mês (F) | Paga até o mês (G) | % (G/A)`
  >
  > `3 - Despesas Correntes | | 21.224.219.000,00 | 3.743.920.892,16 | 3.743.920.892,16 | 17,64% | 1.487.583.077,42 | 1.487.583.077,42 | 7,01% | 753.972.811,76 | 753.972.811,76 | 3,55%`
  >
  > `3.1 - Pessoal e Encargos Sociais | | 14.324.477.000,00 | 1.883.485.948,09 | 1.883.485.948,09 | 13,15% | 1.242.735.505,05 | 1.242.735.505,05 | 8,68% | 557.959.442,60 | 557.959.442,60 | 3,89%`
  >
  > `SIGEF - Sistema Integrado de Planejamento e Gestão Fiscal | Emitido por: ETONJONES OLIVEIRA DA SILVA em 12/11/2026 às 17:19 | Página 1 de 153`

  E no [Comparativo de Outubro/2026](https://drive.google.com/file/d/1icGbmiVC_asJUS-qIDpK4uclbZTT_daR/view?usp=drivesdk) (Página 1 de 497):

  > `3.1 - Pessoal e Encargos Sociais | | 15.696.989.940,86 | 1.404.063.368,24 | 14.432.893.627,20 | 91,95% | 1.351.239.020,25 | 13.801.322.485,53 | 87,92% | 1.320.720.233,73 | 13.063.696.265,67 | 83,22%`
  >
  > `SIGEF - Sistema Integrado de Planejamento e Gestão Fiscal | Emitido por: ETONJONES OLIVEIRA DA SILVA em 12/11/2026 às 19:39 | Página 1 de 497`

* **Como utilizar cada coluna e linha deste relatório:**

  1. **Coluna de Extração Obrigatória:** Utilizar **sempre e exclusivamente a Coluna `Liquidada no mês (D)`** para alimentar as colunas mensais `D` (`JAN/2026`) a `M` (`OUT/2026`) da aba `MAPA`. A coluna `Liquidada até o mês (E)` do relatório de Outubro (`R$ 13.801.322.485,53` para o grupo `3.1`) serve como **trava de verificação cruzada** da soma horizontal acumulada de janeiro a outubro (`Coluna P` da Linha 5 `GND 31 SIGEF`).

  2. **Alocação por Natureza de Despesa (8 dígitos = Subelemento):**

     * **Linha 5 (`GND 31 SIGEF`):** Extrair o valor da linha sintética `3.1 - Pessoal e Encargos Sociais` (coluna `Liquidada no mês (D)`).

     * **Linhas 11 a 101 (`Vencimentos, Vantagens e Outras Despesas Variáveis — Bruto`):** Extrair a soma de todas as fontes de recursos da coluna `Liquidada no mês (D)` para cada subelemento de `3.1.90.04.xx` (Contratação por Tempo Determinado), `3.1.90.05.xx` (Outros Benefícios Previdenciários do Ativo, como auxílio-doença e salário-maternidade), `3.1.90.07.03` (Contribuição a Entidades Fechadas de Previdência), `3.1.90.08.xx` (Outros Benefícios Assistenciais do servidor e do militar), `3.1.90.11.xx` (Vencimentos e Vantagens Fixas — Pessoal Civil), `3.1.90.12.xx` (Vencimentos e Vantagens Fixas — Pessoal Militar), `3.1.90.13.08` (Plano de Saúde), `3.1.90.16.xx` (Outras Despesas Variáveis — Pessoal Civil), `3.1.90.17.xx` (Outras Despesas Variáveis — Pessoal Militar), `3.1.90.91.01` e `3.1.90.91.04` a `3.1.90.91.99` (Sentenças Judiciais de Ativos — **excluindo `.02` Aposentadorias e `.03` Pensões**), `3.1.90.92.01` e `3.1.90.92.04` a `3.1.90.92.99` (DEA de Ativos — **excluindo `.02` Aposentadorias e `.03` Pensões**), `3.1.90.94.xx` (Indenizações e Restituições Trabalhistas) e `3.1.90.96.xx` (Ressarcimento de Despesas de Pessoal Requisitado).

     * **Linhas 9 e 10 (`Reclassificação do Subelemento 31.90.92.97 — Obrigações Patronais`):** O subelemento `3.1.90.92.97 (Obrigações Patronais)` é capturado na linha `93` dentro do bloco de Vencimentos (para manter a integridade da lista de subelementos do elemento `31.90.92`), mas como sua natureza é de **Obrigação Patronal**, ele é **subtraído na Linha 10** (`(-) 31.90.92.97 - OBRIGAÇÕES PATRONAIS`) do bloco de Vencimentos e **somado na Linha 134** do bloco de Obrigações Patronais (`R$ 612.885,35` em Jan–Out/2026).

     * **Linhas 103 a 163 (`Obrigações Patronais Brutas`):** Extrair a soma de todas as fontes para `3.1.90.13.xx` (**exceto `3.1.90.13.08`**, que já entrou na linha `54` em Vencimentos), somar a linha `134` (`3.1.90.92.97`), e extrair `3.1.91.13.xx` (Obrigações Patronais Intraorçamentárias), `3.1.91.91.xx` (Sentenças Judiciais Intraorçamentárias) e `3.1.91.92.xx` (DEA Intraorçamentária).

     * **Linhas 164 a 180 (`Deduções de Obrigações Patronais dos Demais Poderes`):** Extrair do próprio `Comparativo da Despesa` os subelementos finais `.71` (TJ), `.72` (AL), `.73` (TCE), `.74` (DPE) e `.75` (MP) dentro dos elementos `3.1.90.13`, `3.1.90.92`, `3.1.91.13`, `3.1.91.91` e `3.1.91.92`. Como já estão discriminados por Poder no código de 8 dígitos do subelemento, não dependem do IEO!

     * **Linhas 183 a 202 (`Aposentadorias, Reserva e Reformas — Bruto`):** Extrair do `Comparativo da Despesa` todos os subelementos de `3.1.90.01.xx` (Aposentadorias, Reserva Remunerada e Reformas), mais `3.1.90.07.01` e `3.1.90.07.02`, mais `3.1.90.91.02` (Sentenças Judiciais — Aposentadorias) e `3.1.90.92.02` (DEA — Aposentadorias).

     * **Linhas 210 a 227 (`Pensões — Bruto`):** Extrair do `Comparativo da Despesa` todos os subelementos de `3.1.90.03.xx` (Pensões do RPPS e do Militar), mais `3.1.90.05.03` (Pensão Especial), mais `3.1.90.91.03` (Sentenças Judiciais — Pensões) e `3.1.90.92.03` (DEA — Pensões).

     * **Linhas 246 a 249 (`Outras Despesas de Pessoal — Terceirização`):** Navegar até o Grupo de Natureza de Despesa `3.3 - Outras Despesas Correntes` do `Comparativo da Despesa` e extrair a coluna `Liquidada no mês (D)` de `3.3.90.34.xx` (`R$ 132.807.642,96` acumulados em Jan–Out/2026) e do subelemento `3.3.90.92.34` (`R$ 26.763.284,02` acumulados em Jan–Out/2026).

     * **Cruzamento Natureza x Fonte para o Quadro II (Despesas Não Computadas):** No mesmo `Comparativo da Despesa`, observar as linhas de Fonte de Recurso logo abaixo de cada subelemento para alimentar:

       * Fontes `0.8.00 / 4.8.00 / 0.8.01 / 0.8.02 / 0.8.03 / 0.8.04 / 4.8.04` nos elementos `31.90.01`, `31.90.03`, `31.90.91.02`, `31.90.91.03` e `31.90.92.02` -> alimentam as linhas de **Inativos e Pensionistas com Recursos Vinculados** (`MAPA` linhas `288 a 298` e `307 a 315`) e as linhas de trava de dupla dedução (`MAPA` linhas `273` e `283`).

       * Fonte `0.6.05.000000` e `4.6.05.000000` (Assistência Financeira da União para Complementação ao Pagamento do Piso Salarial dos Profissionais da Enfermagem) nos elementos `31.90.11`, `31.90.13`, `31.90.92` e `31.91.13` -> alimentam as linhas `335 a 338` da aba `MAPA` (e a linha `284` de trava de DEA).

       * Fonte `0.6.04.000000` e `4.6.04.000000` (Transferências do Governo Federal para Agentes Comunitários de Saúde e de Combate às Endemias) nos elementos `31.90.11`, `31.90.13`, `31.90.92`, `31.90.94` e `31.91.13` -> alimentam as linhas `340 a 344` da aba `MAPA` (em 2026, todos os valores de GND 31 na Fonte `604` foram `R$ 0,00`).

### 2.3. Grupo C — Série de 10 Relatórios Mensais "IEO — Imprimir Execução Orçamentária" da UG `162233` (FUNFIRN)

* **Lista de Arquivos e Links Diretos:**

   1. **Janeiro/2026:** [Imprimir Execução Orçamentária - IEO_162233_Janeiro.pdf](https://drive.google.com/file/d/1YgE8087idRZLGLx1gv6xD0joM9t9kETJ/view?usp=drivesdk)

   2. **Fevereiro/2026:** [Imprimir Execução Orçamentária - IEO_162233_Fevereiro.pdf](https://drive.google.com/file/d/1nYcpK3YSTaXphAsMpvTsecKnmytnDoah/view?usp=drivesdk)

   3. **Março/2026:** [Imprimir Execução Orçamentária - IEO_162233_Março.pdf](https://drive.google.com/file/d/1RGUG2_YdPPrbmzQpMR3Atv4TDeh2mM3h/view?usp=drivesdk)

   4. **Abril/2026:** [Imprimir Execução Orçamentária - IEO_162233_Abril.pdf](https://drive.google.com/file/d/1eatjz6zrRzVuYciAtbwBew7D4c1Xa7an/view?usp=drivesdk)

   5. **Maio/2026:** [Imprimir Execução Orçamentária - IEO_162233_Maio.pdf](https://drive.google.com/file/d/1hnKk1LfDDADcIepanheVYrto5Ry8MI6n/view?usp=drivesdk)

   6. **Junho/2026:** [Imprimir Execução Orçamentária - IEO_162233_Junho.pdf](https://drive.google.com/file/d/1bMMFNF8vHkKzieLcMo3mzFxjsW06n6s-/view?usp=drivesdk)

   7. **Julho/2026:** [Imprimir Execução Orçamentária - IEO_162233_Julho.pdf](https://drive.google.com/file/d/1t_P2ykzfAyXnyiVObj5oFHlsO9xBRMU2/view?usp=drivesdk)

   8. **Agosto/2026:** [Imprimir Execução Orçamentária - IEO_162233_Agosto.pdf](https://drive.google.com/file/d/1feCqTH104EDZl3ay3A79us5LKodmKQHc/view?usp=drivesdk)

   9. **Setembro/2026:** [Imprimir Execução Orçamentária - IEO_162233_Setembro.pdf](https://drive.google.com/file/d/1VcAhyroczxW97dU4NP6tjYr0sjuktnok/view?usp=drivesdk)

  10. **Outubro/2026:** [Imprimir Execução Orçamentária - IEO_162233_Outubro.pdf](https://drive.google.com/file/d/1dfNiakQckHYbSU7-6hbqmfFa_fOaaq1c/view?usp=drivesdk)

* **Transcrição Literal do Cabeçalho, Parâmetros de Emissão e Subações dos Demais Poderes (Localização: Páginas 1 e 2 de 2 do [IEO_162233_Janeiro.pdf](https://drive.google.com/file/d/1YgE8087idRZLGLx1gv6xD0joM9t9kETJ/view?usp=drivesdk) e Página 2 de 2 do [IEO_162233_Abril.pdf](https://drive.google.com/file/d/1eatjz6zrRzVuYciAtbwBew7D4c1Xa7an/view?usp=drivesdk)):**

  > `ESTADO DO RIO GRANDE DO NORTE`
  >
  > `Imprimir Execução Orçamentária - IEO`
  >
  > `Ano Base: 2026 | Mês Referência: Janeiro | Tipo Demonstração: Execução | Valores Consulta: No mês`
  >
  > `Agrupamento: Subação / Fonte Recurso / Elemento Despesa | Unidade Gestora: 162233 - FUNDO FINANCEIRO DO ESTADO DO RN | Gestão: 16233 - FUNFIRN`
  >
  > `Subação: 408501 - Pagamento de Aposentadorias e Pensões - ALRN`
  >
  > `Fonte Recurso: 0.5.00.000000 - Recursos não Vinculados de Impostos | 31.90.01.00 - Aposentadorias, Reserva Remunerada e Reformas | Liquidado: 2.382.228,89`
  >
  > `Fonte Recurso: 0.5.00.000000 - Recursos não Vinculados de Impostos | 31.90.03.00 - Pensões do RPPS e do Militar | Liquidado: 635.291,68`
  >
  > `Fonte Recurso: 0.8.00.000000 - Recursos Próprios do RPPS (Fundo em Repartição - Plano Financeiro) | 31.90.01.00 | Liquidado: 3.160.295,62`
  >
  > `Fonte Recurso: 0.8.00.000000 - Recursos Próprios do RPPS (Fundo em Repartição - Plano Financeiro) | 31.90.03.00 | Liquidado: 842.785,68`
  >
  > `Subação: 408601 - Pagamento de Aposentadorias e Pensões - DPRN`
  >
  > `Subação: 408701 - Pagamento de Aposentadorias e Pensões - MPRN`
  >
  > `Subação: 408801 - Pagamento de Aposentadorias e Pensões - TJRN`
  >
  > `Subação: 408901 - Pagamento de Aposentadorias e Pensões - TCE/RN`
  >
  > `SIGEF - Sistema Integrado de Planejamento e Gestão Fiscal | Emitido por: ETONJONES OLIVEIRA DA SILVA em 12/11/2026 às 20:28 | Página 1 de 2`

  E na Página 2 de 2 do [IEO_162233_Abril.pdf](https://drive.google.com/file/d/1eatjz6zrRzVuYciAtbwBew7D4c1Xa7an/view?usp=drivesdk) (onde reside a divergência auditada de `R$ 5.241,65`):

  > `Subação: 408801 - Pagamento de Aposentadorias e Pensões - TJRN`
  >
  > `Fonte Recurso: 0.5.00.000000 - Recursos não Vinculados de Impostos`
  >
  > `31.90.92.03 - Despesas de Exercícios Anteriores | Empenhado: 86.852,54 | Liquidado: 92.094,19`
  >
  > `Fonte Recurso: 0.8.00.000000 - Recursos Próprios do RPPS (Fundo em Repartição - Plano Financeiro)`
  >
  > `31.90.92.03 - Despesas de Exercícios Anteriores | Empenhado: 29.377,60 | Liquidado: 29.377,60`

* **Como utilizar este relatório:**

  1. Ignorar a Subação `408401 - Pagamento de Aposentadorias e Pensões - Poder Executivo` (pois esta pertence ao próprio Executivo).

  2. Nas **5 Subações dos demais Poderes** (`408501` ALRN, `408601` DPRN, `408701` MPRN, `408801` TJRN e `408901` TCE/RN), extrair a coluna **`Liquidado`**:

     * **Para o Expurgo da Despesa Bruta (Quadro I — Linhas 203 a 208 para Aposentadorias e Linhas 228 a 232 / 240 a 244 para Pensões):** Somar os valores liquidados na **Fonte `0.5.00.000000` (`4.5.00.000000`) + Fonte `0.8.00.000000` (`4.8.00.000000`)** de cada Poder para `31.90.01`, `31.90.91.02`, `31.90.92.02` (Aposentadorias) e para `31.90.03`, `31.90.91.03`, `31.90.92.03` (Pensões).

     * **Para o Expurgo dos Recursos Vinculados (Quadro II — Linhas 299 a 306 para Aposentadorias e Linhas 316 a 320 / 328 a 333 para Pensões):** Extrair **exclusivamente** os valores liquidados na **Fonte `0.8.00.000000` (`4.8.00.000000`)** de cada Poder.

### 2.4. Grupo D — Série de 10 Relatórios Mensais "IEO — Imprimir Execução Orçamentária" da UG `162011` (IPERN)

* **Lista de Arquivos e Links Diretos:**

   1. **Janeiro/2026:** [Imprimir Execução Orçamentária - IEO_162011_Janeiro.pdf](https://drive.google.com/file/d/14FqcrJX5VOGeo-2BTvu0ls3djkO6QY0P/view?usp=drivesdk)

   2. **Fevereiro/2026:** [Imprimir Execução Orçamentária - IEO_162011_Fevereiro.pdf](https://drive.google.com/file/d/1nNM45BYelqegEseCrBTGCeHicbrdho2D/view?usp=drivesdk)

   3. **Março/2026:** [Imprimir Execução Orçamentária - IEO_162011_Março.pdf](https://drive.google.com/file/d/1-9zriv8_06_zGq_d8j4AezA1wEUWD_NM/view?usp=drivesdk)

   4. **Abril/2026:** [Imprimir Execução Orçamentária - IEO_162011_Abril.pdf](https://drive.google.com/file/d/18SHU_yPfe7GZOFn2SRUfjaK5RIOwwFW0/view?usp=drivesdk)

   5. **Maio/2026:** [Imprimir Execução Orçamentária - IEO_162011_Maio.pdf](https://drive.google.com/file/d/1h2XDrmz29_0lWt_rzJf_qHPXLj29Ru1Q/view?usp=drivesdk)

   6. **Junho/2026:** [Imprimir Execução Orçamentária - IEO_162011_Junho.pdf](https://drive.google.com/file/d/1_mRkKlE1FD35A4aigiT8h02Sk4fVS4cU/view?usp=drivesdk)

   7. **Julho/2026:** [Imprimir Execução Orçamentária - IEO_162011_Julho.pdf](https://drive.google.com/file/d/18zHiseu11Wx_MrGRxPXhQhs6Cy7QtGbE/view?usp=drivesdk)

   8. **Agosto/2026:** [Imprimir Execução Orçamentária - IEO_162011_Agosto.pdf](https://drive.google.com/file/d/1fG_8RQVgQq6VFfik4Qz0HjBO2exMXE9n/view?usp=drivesdk)

   9. **Setembro/2026:** [Imprimir Execução Orçamentária - IEO_162011_Setembro.pdf](https://drive.google.com/file/d/1feXwTe2jMcSoZvwblQUSwYD-N4k-RYft/view?usp=drivesdk)

  10. **Outubro/2026:** [Imprimir Execução Orçamentária - IEO_162011_Outubro.pdf](https://drive.google.com/file/d/1OPyX9Pee4d7WHo9W2bD7EQ6pGfxl_O7R/view?usp=drivesdk)

* **Transcrição Literal do Cabeçalho e Subações (Localização: Página 1 de 2 do [IEO_162011_Janeiro.pdf](https://drive.google.com/file/d/14FqcrJX5VOGeo-2BTvu0ls3djkO6QY0P/view?usp=drivesdk)):**

  > `ESTADO DO RIO GRANDE DO NORTE | Imprimir Execução Orçamentária - IEO`
  >
  > `Ano Base: 2026 | Mês Referência: Janeiro | Tipo Demonstração: Execução | Valores Consulta: No mês`
  >
  > `Agrupamento: Subação / Fonte Recurso / Elemento Despesa | Unidade Gestora: 162011 - INSTITUTO DE PREV. DOS SERV. DO ESTADO | Gestão: 00001 - GESTAO TESOURO`
  >
  > `Subação: 408502 - Pagamento de Pensões do IPERN - ALRN | Fonte Recurso: 0.8.04.000105 - Recursos Próprios da Unidade Gestora - IPERN | 31.90.03.00 - Pensões do RPPS e do Militar | Liquidado: 6.727,50`
  >
  > `Subação: 408702 - Pagamento de Pensões do IPERN - MPRN | Fonte Recurso: 0.8.04.000105 | 31.90.03.00 | Liquidado: 4.550,00`
  >
  > `Subação: 408802 - Pagamento de Pensões do IPERN - TJRN | Fonte Recurso: 0.8.04.000105 | 31.90.03.00 | Liquidado: 15.654,48`
  >
  > `Subação: 408902 - Pagamento de Pensões do IPERN - TCE/RN | Fonte Recurso: 0.8.04.000105 | 31.90.03.00 | Liquidado: 2.345,00`
  >
  > `SIGEF - Sistema Integrado de Planejamento e Gestão Fiscal | Emitido por: ETONJONES OLIVEIRA DA SILVA em 12/11/2026 às 20:28 | Página 1 de 2`

* **Como utilizar este relatório:**

  * A UG `162011` (IPERN) executa diretamente pensões na **Fonte Vinculada `0.8.04.000105` (`4.8.04.000105`)** sob as subações terminadas em `02`: `408502` (ALRN), `408602` (DPRN), `408702` (MPRN), `408802` (TJRN) e `408902` (TCE/RN).

  * Como 100% dessa execução nas subações `408502` a `408902` ocorre na Fonte Vinculada `0.8.04.000105` (e eventualmente `31.90.92.03` na fonte `0.5.00` em meses específicos), os valores liquidados alimentam **tanto** o expurgo bruto de Pensões no Quadro I (`MAPA` linhas `233 a 239`, somando R\$ 310.753,90 no acumulado Jan–Out/2026) **quanto** o expurgo de Pensões com Recursos Vinculados no Quadro II (`MAPA` linhas `321 a 327`, pelos mesmos R\$ 310.753,90 na fonte `804`).

### 2.5. Grupo E — Série de 9 Relatórios da "Despesa com Pessoal Não Executada Orçamentariamente" (Contas `8.6.3.3.1.01.00.00` e `8.6.3.3.1.02.00.00`)

Estes 9 arquivos fundamentam integralmente a **Linha 250 da aba `MAPA` (`DESPESA COM PESSOAL NÃO EXECUTADA ORÇAMENTARIAMENTE`)** e a **Coluna `C` (`DEZ/2025`)**:

#### 1. Relatório Orçamentário de Conferência do 13º Salário na UG `162233` — [Imprimir Execução Orçamentária_Despesas_n_Executadas_orça.pdf](https://drive.google.com/file/d/1JSxra4141HhvCQUqV-J1r8yv7_QDd7h3/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 22/01/2026 às 16:16 por Etonjones Oliveira da Silva):**

  > `ESTADO DO RIO GRANDE DO NORTE | Imprimir Execução Orçamentária - IEO`
  >
  > `Ano Base: 2026 | Mês Referência: Janeiro | Tipo Demonstração: Execução | Valores Consulta: Até o mês`
  >
  > `Agrupamento: Unidade Gestora / Gestão / Subação / Elemento Despesa | Unidade Gestora: 162233 - FUNDO FINANCEIRO DO ESTADO DO RN`
  >
  > `Subação: 408401 - Pagamento de Aposentadorias e Pensões - Poder Executivo`
  >
  > `31.90.01.01 - Aposentadorias de Servidores Civis | Empenhado: 251.170.720,03`
  >
  > `31.90.01.02 - Reformas e Reserva Remunerada de Militares | Empenhado: 61.153.891,75`
  >
  > `31.91.13.71 - Contribuições Patronais - Plano Financeiro - TJ | Empenhado: 869.035,06`
  >
  > `31.91.13.72 - Contribuições Patronais - Plano Financeiro - AL | Empenhado: 192.345,57`
  >
  > `31.91.13.73 - Contribuições Patronais - Plano Financeiro - TCE | Empenhado: 44.331,85`
  >
  > `31.91.13.75 - Contribuições Patronais - Plano Financeiro - MP | Empenhado: 232.046,76`
  >
  > `Total Unidade Gestora: 313.662.371,02`

* **Como utilizar:** Comprova matematicamente a decomposição do saldo de abertura de `R$ 313.662.371,02` da UG `162233` na conta `8.6.3.3.1.02.00.00` ([Relatorio_13112026083712.pdf](https://drive.google.com/file/d/1K6MBhS5F0noTeKB7LGJFdFYSHgBLPQrv/view?usp=drivesdk)): somando os encargos patronais dos outros Poderes (`869.035,06 + 192.345,57 + 44.331,85 + 232.046,76`), obtém-se exatamente **`R$ 1.337.759,24`**, que devem ser expurgados do saldo de Dezembro/2025 e da baixa de Abril/2026 para não duplicar o expurgo já feito nas linhas `176 a 179` da aba `MAPA`.

#### 2. Balancete de Abertura da Conta `8.6.3.3.1.01.00.00 - SALÁRIOS` — [Relatorio_13112026083631.pdf](https://drive.google.com/file/d/1M2QZBrxP6B9GO7oMPbmIBHz22i2Xt8wN/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 08:36:31 por Etonjones Oliveira da Silva):**

  > `ESTADO DO RIO GRANDE DO NORTE | Relatório Contábil | Exercício: 2026 | Mês Referência: Abertura`
  >
  > `Conta Contábil: 8.6.3.3.1.01.00.00 - SALÁRIOS`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Exercício Anterior: 7.146.460,76 C | Saldo Atual: 7.146.460,76 C`
  >
  > `320001-00001 - CORPO DE BOMBEIROS MILITAR | Saldo Exercício Anterior: 37.781,67 C | Saldo Atual: 37.781,67 C`
  >
  > `Total Geral | Saldo Exercício Anterior: 7.184.242,43 C | Movimento Devedor: 0,00 | Movimento Credor: 0,00 | Saldo Atual: 7.184.242,43 C`

#### 3. Balancete de Abertura da Conta `8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO` — [Relatorio_13112026083712.pdf](https://drive.google.com/file/d/1K6MBhS5F0noTeKB7LGJFdFYSHgBLPQrv/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 08:37:12 por Etonjones Oliveira da Silva):**

  > `ESTADO DO RIO GRANDE DO NORTE | Relatório Contábil | Exercício: 2026 | Mês Referência: Abertura`
  >
  > `Conta Contábil: 8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO`
  >
  > `110001-00001 - GABINETE CIVIL DO GOVERNADOR DO ESTADO | Saldo Exercício Anterior: 2.340.703,80 C`
  >
  > `160001-00001 - SECRETARIA DE ESTADO DA ADMINISTRACAO | Saldo Exercício Anterior: 26.647.828,15 C`
  >
  > `162233-16233 - FUNDO FINANCEIRO DO ESTADO DO RN | Saldo Exercício Anterior: 313.662.371,02 C`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Exercício Anterior: 81.918.211,75 C`
  >
  > `190001-00001 - SECRETARIA DE ESTADO DA Tributação | Saldo Exercício Anterior: 11.404.737,24 C`
  >
  > `210001-00001 - SECRETARIA DE EST DA SEGURANCA PUB E DEF SOC | Saldo Exercício Anterior: 3.162.728,53 C`
  >
  > `210002-00001 - POLICIA MILITAR | Saldo Exercício Anterior: 59.893.758,84 C`
  >
  > `210004-00001 - POLICIA CIVIL | Saldo Exercício Anterior: 15.839.211,64 C`
  >
  > `240131-24131 - FUNDO DE SAUDE DO RN | Saldo Exercício Anterior: 94.384.619,53 C`
  >
  > `320001-00001 - CORPO DE BOMBEIROS MILITAR | Saldo Exercício Anterior: 7.354.140,15 C`
  >
  > `Total Geral | Saldo Exercício Anterior: 616.608.310,65 C | Movimento Devedor: 0,00 | Movimento Credor: 0,00 | Saldo Atual: 616.608.310,65 C`

* **Como utilizar os relatórios 2 e 3 para formar a Coluna `C` (`DEZ/2025` — Linha 250 da aba `MAPA`):** 

  $$
  \text{DEZ/2025} = \underbrace{7.184.242,43}_{\text{Salários}} + \underbrace{(616.608.310,65 - 1.337.759,24)}_{\text{13º Líquido do Executivo } (615.270.551,41)} = \mathbf{R\$\ 622.454.793,84}
  $$

#### 4. Balancete de Janeiro/2026 da Conta `8.6.3.3.1.01.00.00 - SALÁRIOS` — [Relatorio_13112026104512.pdf](https://drive.google.com/file/d/1GmfI2Yl1vsZxWz0LZmyCdiOKVUkyJHxS/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 10:45:12):**

  > `Exercício: 2026 | Mês Referência: Janeiro | Conta Contábil: 8.6.3.3.1.01.00.00 - SALÁRIOS`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Exercício Anterior: 7.146.460,76 C | Movimento Devedor: 0,00 | Movimento Credor: 3.438.269,71 | Saldo Atual: 10.584.730,47 C`
  >
  > `210002-00001 - POLICIA MILITAR | Saldo Exercício Anterior: 0,00 | Movimento Devedor: 0,00 | Movimento Credor: 89.546,82 | Saldo Atual: 89.546,82 C`
  >
  > `320001-00001 - CORPO DE BOMBEIROS MILITAR | Saldo Exercício Anterior: 37.781,67 C | Movimento Devedor: 0,00 | Movimento Credor: 0,00 | Saldo Atual: 37.781,67 C`
  >
  > `Total Geral | Saldo Exercício Anterior: 7.184.242,43 C | Movimento Devedor: 0,00 | Movimento Credor: 3.527.816,53 | Saldo Atual: 10.712.058,96 C`

* **Valor na Célula `MAPA!D250` (`JAN/2026`):** `3.527.816,53 - 0,00 =` **`+R$ 3.527.816,53`**.

#### 5. Balancete de Fevereiro/2026 da Conta `8.6.3.3.1.01.00.00 - SALÁRIOS` — [Relatorio_13112026104531.pdf](https://drive.google.com/file/d/1f494_wJ1kx1L08PphY-EwXGC3ItbpWEX/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 10:45:31):**

  > `Exercício: 2026 | Mês Referência: Fevereiro | Conta Contábil: 8.6.3.3.1.01.00.00 - SALÁRIOS`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Anterior: 10.584.730,47 C | Movimento Devedor: 576.699,90 | Movimento Credor: 707.028,79 | Saldo Atual: 10.715.059,36 C`
  >
  > `210002-00001 - POLICIA MILITAR | Saldo Anterior: 89.546,82 C | Movimento Devedor: 0,00 | Movimento Credor: 0,00 | Saldo Atual: 89.546,82 C`
  >
  > `320001-00001 - CORPO DE BOMBEIROS MILITAR | Saldo Anterior: 37.781,67 C | Movimento Devedor: 37.781,67 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`
  >
  > `Total Geral | Saldo Anterior: 10.712.058,96 C | Movimento Devedor: 614.481,57 | Movimento Credor: 707.028,79 | Saldo Atual: 10.804.606,18 C`

* **Valor na Célula `MAPA!E250` (`FEV/2026`):** `707.028,79 - 614.481,57 =` **`+R$ 92.547,22`**.

#### 6. Balancete de Março/2026 da Conta `8.6.3.3.1.01.00.00 - SALÁRIOS` — [Relatorio_13112026104546.pdf](https://drive.google.com/file/d/1iF_Us87e5rDzJsNR4-PV5UEuAOG1HtwC/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 10:45:46):**

  > `Exercício: 2026 | Mês Referência: Março | Conta Contábil: 8.6.3.3.1.01.00.00 - SALÁRIOS`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Anterior: 10.715.059,36 C | Movimento Devedor: 0,00 | Movimento Credor: 0,00 | Saldo Atual: 10.715.059,36 C`
  >
  > `210002-00001 - POLICIA MILITAR | Saldo Anterior: 89.546,82 C | Movimento Devedor: 89.546,82 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`
  >
  > `Total Geral | Saldo Anterior: 10.804.606,18 C | Movimento Devedor: 89.546,82 | Movimento Credor: 0,00 | Saldo Atual: 10.715.059,36 C`

* **Valor na Célula `MAPA!F250` (`MAR/2026`):** `0,00 - 89.546,82 =` **`-R$ 89.546,82`**.

#### 7. Balancete de Abril/2026 da Conta `8.6.3.3.1.01.00.00 - SALÁRIOS` — [Relatorio_13112026104604.pdf](https://drive.google.com/file/d/11fWw3HhopPN6coXMKGeymg7D9wBi0FAS/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 10:46:04):**

  > `Exercício: 2026 | Mês Referência: Abril | Conta Contábil: 8.6.3.3.1.01.00.00 - SALÁRIOS`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Anterior: 10.715.059,36 C | Movimento Devedor: 10.715.059,36 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`
  >
  > `Total Geral | Saldo Anterior: 10.715.059,36 C | Movimento Devedor: 10.715.059,36 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`

#### 8. Balancete de Abril/2026 da Conta `8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO` — [Relatorio_13112026104406.pdf](https://drive.google.com/file/d/1Zv7D9awRLiRxOqIoO20rS2iagK5kHFGv/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 10:44:06):**

  > `Exercício: 2026 | Mês Referência: Abril | Conta Contábil: 8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO`
  >
  > `162233-16233 - FUNDO FINANCEIRO DO ESTADO DO RN | Saldo Anterior: 313.662.371,02 C | Movimento Devedor: 313.662.371,02 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Anterior: 81.918.211,75 C | Movimento Devedor: 80.645.641,29 | Movimento Credor: 0,00 | Saldo Atual: 1.272.570,46 C`
  >
  > `240131-24131 - FUNDO DE SAUDE DO RN | Saldo Anterior: 94.384.619,53 C | Movimento Devedor: 94.617.006,18 | Movimento Credor: 232.386,65 | Saldo Atual: 0,00 D`
  >
  > `Total Geral | Saldo Anterior: 616.608.310,65 C | Movimento Devedor: 615.568.126,84 | Movimento Credor: 232.386,65 | Saldo Atual: 1.272.570,46 C`

* **Como utilizar os relatórios 7 e 8 para formar a Célula `MAPA!G250` (`ABR/2026`):**

  * Variação líquida de Salários em Abril/2026: `0,00 - 10.715.059,36 = -R$ 10.715.059,36`

  * Variação líquida de 13º Salário do Executivo em Abril/2026 (expurgando da baixa da UG `162233` os `R$ 1.337.759,24` pertencentes aos outros Poderes): `232.386,65 - (615.568.126,84 - 1.337.759,24) = 232.386,65 - 614.230.367,60 = -R$ 613.997.980,95`

  * **Soma em Abril/2026 (`MAPA!G250`):** `-10.715.059,36 + (-613.997.980,95) =` **`-R$ 624.713.040,31`**.

#### 9. Balancete de Maio/2026 da Conta `8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO` — [Relatorio_13112026104452.pdf](https://drive.google.com/file/d/1LBQEhll3t3-90WLUoOH0qn5WyjTkTlk8/view?usp=drivesdk)

* **Localização e Transcrição Literal (Página 1 de 1, emitido em 13/11/2026 às 10:44:52):**

  > `Exercício: 2026 | Mês Referência: Maio | Conta Contábil: 8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO`
  >
  > `180001-00001 - SECRETARIA DE EST DA EDUCACAO E DA CULTURA | Saldo Anterior: 1.272.570,46 C | Movimento Devedor: 1.272.570,46 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`
  >
  > `Total Geral | Saldo Anterior: 1.272.570,46 C | Movimento Devedor: 1.272.570,46 | Movimento Credor: 0,00 | Saldo Atual: 0,00 D`

* **Valor na Célula `MAPA!H250` (`MAI/2026`):** `0,00 - 1.272.570,46 =` **`-R$ 1.272.570,46`**. (De Junho a Outubro de 2026 o saldo permanece `0,00`).

### 2.6. Grupo F — Arquivos de Referência Oficial e Artefatos Consolidados

1. **Planilha Oficial do 2º Quadrimestre de 2026 (CONTAG/SEFAZ-RN):** [RGF 2026_Q2_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.xlsx](https://drive.google.com/file/d/1OSFMkXhsNf0MhseI6mEr3E9v8Zdv2P2Z/view?usp=drivesdk) e [RGF 2026_Q2_01 - DEMONSTRATIVO DA DESPESA COM PESSOAL.pdf](https://drive.google.com/file/d/17Er-a8kyPR6VDqNiBpwwKVJYMFdur574/view?usp=drivesdk) (localizados na pasta [RELATÓRIOS CONTAG > Demonstrativos Fiscais 2026 > RGF 2026 > 2° QUADRIMESTRE](https://drive.google.com/drive/folders/156_GGrPq9_LrJMXSJZG_DkpDifdULJon)). Serviram como gabarito estrutural das 344 linhas da aba `MAPA` e das 43 linhas da aba `QUADRO`, além de fornecerem os valores fechados de Setembro a Dezembro de 2025 para comparação quadrimestral.

2. **Extrato SICONFI de Validação:** [SICONFI_RGF_171_QUADRIMESTRAL_2.xls](https://drive.google.com/file/d/1dDM9t8V-aSPw9m4v_tOiaskGSsXou1Sg/view?usp=drivesdk) (arquivo de conferência da homologação no SICONFI/STN).

3. **Planilha Final Consolidada (Janeiro a Outubro de 2026):** [Quadro_e_Mapa_Janeiro_a_Outubro_2026.xlsx](https://drive.google.com/file/d/1aJnjJAx517fIw3AZ2_W8SH4LRN57_01D/view?usp=drivesdk).

4. **Manual Técnico de Conciliação (PDF):** [BI_TESTE_DESPESA_COM_PESSOAL.pdf](https://drive.google.com/file/d/1W0UZVZuUKZpDZH-Z0UMPHfCIqx4jmETC/view?usp=drivesdk).

### 2.7. Quadro-Síntese dos Resultados Auditados (Janeiro a Outubro de 2026 — Aba `QUADRO` e Aba `MAPA`)

| Rubrica do Demonstrativo (Anexo 1 — RGF / MDF 15ª Ed.) | Linha `MAPA` | Linha `QUADRO` | Acumulado Jan–Out/2026 (R\$) | 
| ----- | ----- | ----- | ----- | 
| **GND 31 Total Liquidado no SIGEF/RN (Poder Executivo)** | Linha 5 | — | **13.801.322.485,53** | 
| **Diferença de Conciliação (`GND 31 SIGEF - Despesa Bruta RGF`)** | Linha 4 | — | **939.212.769,71** | 
| **DESPESA BRUTA COM PESSOAL (I)** | **Linha 6** | **Linha 17** | **12.862.109.715,82** | 
| 1\. Pessoal Ativo | Linha 7 | Linha 18 | 7.859.903.624,68 | 
| 1.1. Vencimentos, Vantagens e Outras Despesas Variáveis | Linha 8 | Linha 19 | 5.762.045.639,22 | 
| 1.2. Obrigações Patronais (Líquidas dos Demais Poderes) | Linha 102 | Linha 20 | 2.097.857.985,46 | 
| 2\. Pessoal Inativo e Pensionistas | Linha 181 | Linha 21 | 5.465.089.958,00 | 
| 2.1. Aposentadorias, Reserva e Reformas (Líquidas dos Demais Poderes) | Linha 182 | Linha 22 | 4.682.113.817,65 | 
| 2.2. Pensões (Líquidas dos Demais Poderes) | Linha 209 | Linha 23 | 782.976.140,35 | 
| 3\. Outras Despesas de Pessoal decorrentes de Contratos de Terceirização (§ 1º art. 18 LRF) | Linha 245 | Linha 24 | 159.570.926,98 | 
| 4\. Despesa com Pessoal Não Executada Orçamentariamente (Contas `8.6.3.3.1.01` e `02`) | Linha 250 | Linha 25 | \-622.454.793,84 | 
| **DESPESAS NÃO COMPUTADAS (II) (§ 1º do art. 19 da LRF)** | **Linha 252** | **Linha 26** | **3.576.593.541,09** | 
| 1\. Indenizações por Demissão e Incentivos à Demissão Voluntária | Linha 253 | Linha 27 | 3.104.351,03 | 
| 2\. Decorrentes de Decisão Judicial de Período Anterior ao da Apuração | Linha 262 | Linha 28 | 471.957.509,55 | 
| 3\. Despesas de Exercícios Anteriores de Período Anterior ao da Apuração (Alocadas em Dez) | Linha 274 | Linha 29 | 61.416.717,30 | 
| 4\. Inativos e Pensionistas com Recursos Vinculados (Fontes `800` a `804` Líquidas) | Linha 286 | Linha 30 | 3.017.234.633,33 | 
| 5\. Piso Salarial da Enfermagem (`72%` da Fonte `X.605` — EC nº 127/2022, art. 38, § 2º, ADCT) | Linha 334 | Linha 31 | 22.880.329,88 | 
| 6\. Agentes Comunitários de Saúde e de Combate às Endemias (Fonte `X.604` — EC nº 120/2022) | Linha 339 | Linha 32 | 0,00 | 
| **DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)** | **Linha 251** | **Linha 33** | **9.285.516.174,73** | 

## 3. Fundamentação Legal e Normativa Transcrita Integralmente

Em estrita observância ao rigor técnico-jurídico e contábil, transcrevem-se a seguir, na íntegra e literalmente, os dispositivos da **Lei Complementar nº 101/2000 (LRF)** e do **Manual de Demonstrativos Fiscais (MDF — 15ª Edição, 3ª Versão, Setembro/2026)** utilizados na construção do modelo, com a respectiva localização nos documentos da pasta [TESTE_BI_DESPESA_COM_PESSOAL](https://drive.google.com/drive/folders/1q59a3jqo7MDJtxXtX6cGmqQefAbh7cp9).

### 3.1. Lei Complementar nº 101, de 4 de maio de 2000 — Documento: [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk)

#### A. Conceito de Receita Corrente Líquida (Localização em [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk): Capítulo I — Disposições Preliminares, Art. 2º, inciso IV e §§ 1º a 3º, linhas 26 a 42)

> "Art. 2o Para os efeitos desta Lei Complementar, entende-se como:
>
> (...)
>
> IV - receita corrente líquida: somatório das receitas tributárias, de contribuições, patrimoniais, industriais, agropecuárias, de serviços, transferências correntes e outras receitas também correntes, deduzidos:
>
> a) na União, os valores transferidos aos Estados e Municípios por determinação constitucional ou legal, e as contribuições mencionadas na alínea a do inciso I e no inciso II do art. 195, e no art. 239 da Constituição;
>
> b) nos Estados, as parcelas entregues aos Municípios por determinação constitucional;
>
> c) na União, nos Estados e nos Municípios, a contribuição dos servidores para o custeio do seu sistema de previdência e assistência social e as receitas provenientes da compensação financeira citada no § 9o do art. 201 da Constituição.
>
> § 1o Serão computados no cálculo da receita corrente líquida os valores pagos e recebidos em decorrência da Lei Complementar no 87, de 13 de setembro de 1996, e do fundo previsto pelo art. 60 do Ato das Disposições Constitucionais Transitórias.
>
> § 2o Não serão considerados na receita corrente líquida do Distrito Federal e dos Estados do Amapá e de Roraima os recursos recebidos da União para atendimento das despesas de que trata o inciso V do § 1o do art. 19.
>
> § 3o A receita corrente líquida será apurada somando-se as receitas arrecadadas no mês em referência e nos onze anteriores, excluídas as duplicidades."

#### B. Definição de Despesa Total com Pessoal, Terceirização, Regime de Competência e Remuneração Bruta (Localização em [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk): Capítulo IV — Da Despesa Pública, Seção II — Das Despesas com Pessoal, Subseção I — Definições e Limites, Art. 18, caput e §§ 1º a 3º, linhas 232 a 242)

> "Art. 18. Para os efeitos desta Lei Complementar, entende-se como despesa total com pessoal: o somatório dos gastos do ente da Federação com os ativos, os inativos e os pensionistas, relativos a mandatos eletivos, cargos, funções ou empregos, civis, militares e de membros de Poder, com quaisquer espécies remuneratórias, tais como vencimentos e vantagens, fixas e variáveis, subsídios, proventos da aposentadoria, reformas e pensões, inclusive adicionais, gratificações, horas extras e vantagens pessoais de qualquer natureza, bem como encargos sociais e contribuições recolhidas pelo ente às entidades de previdência.
>
> § 1o Os valores dos contratos de terceirização de mão-de-obra que se referem à substituição de servidores e empregados públicos serão contabilizados como "Outras Despesas de Pessoal".
>
> § 2º A despesa total com pessoal será apurada somando-se a realizada no mês em referência com as dos 11 (onze) imediatamente anteriores, adotando-se o regime de competência, independentemente de empenho. (Redação dada pela Lei Complementar nº 178, de 2021)
>
> § 3º Para a apuração da despesa total com pessoal, será observada a remuneração bruta do servidor, sem qualquer dedução ou retenção, ressalvada a redução para atendimento ao disposto no art. 37, inciso XI, da Constituição Federal. (Incluído pela Lei Complementar nº 178, de 2021)"

#### C. Limite Global Estadual, Despesas Não Computadas e Vedação de Dedução do Déficit Financeiro do RPPS (Localização em [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk): Capítulo IV, Seção II, Subseção I, Art. 19, caput, inciso II e §§ 1º a 3º, linhas 244 a 272)

> "Art. 19. Para os fins do disposto no caput do art. 169 da Constituição, a despesa total com pessoal, em cada período de apuração e em cada ente da Federação, não poderá exceder os percentuais da receita corrente líquida, a seguir discriminados:
>
> I - União: 50% (cinqüenta por cento);
>
> II - Estados: 60% (sessenta por cento);
>
> III - Municípios: 60% (sessenta por cento).
>
> § 1o Na verificação do atendimento dos limites definidos neste artigo, não serão computadas as despesas:
>
> I - de indenização por demissão de servidores ou empregados;
>
> II - relativas a incentivos à demissão voluntária;
>
> III - derivadas da aplicação do disposto no inciso II do § 6o do art. 57 da Constituição;
>
> IV - decorrentes de decisão judicial e da competência de período anterior ao da apuração a que se refere o § 2o do art. 18;
>
> V - com pessoal, do Distrito Federal e dos Estados do Amapá e Roraima, custeadas com recursos transferidos pela União na forma dos incisos XIII e XIV do art. 21 da Constituição e do art. 31 da Emenda Constitucional no 19;
>
> VI - com inativos e pensionistas, ainda que pagas por intermédio de unidade gestora única ou fundo previsto no art. 249 da Constituição Federal, quanto à parcela custeada por recursos provenientes: (Redação dada pela Lei Complementar nº 178, de 2021)
>
> a) da arrecadação de contribuições dos segurados;
>
> b) da compensação financeira de que trata o § 9o do art. 201 da Constituição;
>
> c) de transferências destinadas a promover o equilíbrio atuarial do regime de previdência, na forma definida pelo órgão do Poder Executivo federal responsável pela orientação, pela supervisão e pelo acompanhamento dos regimes próprios de previdência social dos servidores públicos. (Redação dada pela Lei Complementar nº 178, de 2021)
>
> § 2o Observado o disposto no inciso IV do § 1o, as despesas com pessoal decorrentes de sentenças judiciais serão incluídas no limite do respectivo Poder ou órgão referido no art. 20.
>
> § 3º Na verificação do atendimento dos limites definidos neste artigo, é vedada a dedução da parcela custeada com recursos aportados para a cobertura do déficit financeiro dos regimes de previdência. (Incluído pela Lei Complementar nº 178, de 2021)"

#### D. Repartição dos Limites na Esfera Estadual e Segregação Obrigatória de Inativos e Pensionistas por Poder (Localização em [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk): Capítulo IV, Seção II, Subseção I, Art. 20, caput, inciso II e § 7º, linhas 274 a 342)

> "Art. 20. A repartição dos limites globais do art. 19 não poderá exceder os seguintes percentuais:
>
> (...)
>
> II - na esfera estadual:
>
> a) 3% (três por cento) para o Legislativo, incluído o Tribunal de Contas do Estado;
>
> b) 6% (seis por cento) para o Judiciário;
>
> c) 49% (quarenta e nove por cento) para o Executivo;
>
> d) 2% (dois por cento) para o Ministério Público dos Estados;
>
> (...)
>
> § 7º Os Poderes e órgãos referidos neste artigo deverão apurar, de forma segregada para aplicação dos limites de que trata este artigo, a integralidade das despesas com pessoal dos respectivos servidores inativos e pensionistas, mesmo que o custeio dessas despesas esteja a cargo de outro Poder ou órgão. (Incluído pela Lei Complementar nº 178, de 2021)"

#### E. Limite Prudencial (95%), Limite de Alerta (90%) e Obrigatoriedade do Demonstrativo no RGF (Localização em [LRF.docx.md](https://drive.google.com/file/d/1rQI7u2XCvjARgk8JaDwr0rendDGQwUxB/view?usp=drivesdk): Art. 22, parágrafo único; Art. 54, caput; Art. 55, inciso I, alínea "a"; e Art. 59, § 1º, inciso II, linhas 355 a 382 e 755 a 835)

> "Art. 22. A verificação do cumprimento dos limites estabelecidos nos arts. 19 e 20 será realizada ao final de cada quadrimestre.
>
> Parágrafo único. Se a despesa total com pessoal exceder a 95% (noventa e cinco por cento) do limite, são vedados ao Poder ou órgão referido no art. 20 que houver incorrido no excesso: (...)"
>
> "Art. 55. O relatório conterá:
>
> I - comparativo com os limites de que trata esta Lei Complementar, dos seguintes montantes:
>
> a) despesa total com pessoal, distinguindo a com inativos e pensionistas; (...)"
>
> "Art. 59. (...) § 1o Os Tribunais de Contas alertarão os Poderes ou órgãos referidos no art. 20 quando constatarem: (...)
>
> II - que o montante da despesa total com pessoal ultrapassou 90% (noventa por cento) do limite;"

### 3.2. Manual de Demonstrativos Fiscais — MDF 15ª Edição (3ª Versão — Setembro/2026) — Documento: [MDF  MDF 15 edição.docx.md](https://drive.google.com/file/d/1qYhBrhuP1nPGDKIcmfAAMaNpgXmo4wOj/view?usp=drivesdk)

#### A. Conceito de Operações Intraorçamentárias (Modalidade de Aplicação `91`) e Estágios da Execução da Despesa (Localização em [MDF  MDF 15 edição.docx.md](https://drive.google.com/file/d/1qYhBrhuP1nPGDKIcmfAAMaNpgXmo4wOj/view?usp=drivesdk): Parte Geral — Procedimentos Contábeis Orçamentários, páginas 54 e 57–58)

> "OPERAÇÕES INTRAORÇAMENTÁRIAS
>
> Operações intraorçamentárias são aquelas realizadas entre órgãos e demais entidades da Administração Pública integrantes do orçamento fiscal e do orçamento da seguridade social do mesmo ente federativo; por isso, não representam novas entradas de recursos nos cofres públicos do ente, mas apenas movimentação de receitas entre seus órgãos. As despesas intraorçamentárias são executadas por meio da modalidade de aplicação 91 (Aplicação Direta Decorrente de Operação entre Órgãos, Fundos e Entidades Integrantes dos Orçamentos Fiscal e da Seguridade Social), e a sua contrapartida na receita se dá por meio das naturezas de receita intraorçamentárias (categorias econômicas 7 e 8)." (página 54)
>
> "DESPESA LIQUIDADA
>
> Considera-se despesa liquidada os valores oriundos da verificação do direito adquirido pelo credor, tendo por base os títulos e documentos comprobatórios do respectivo crédito no exercício financeiro corrente." (página 57)

#### B. Regras Gerais do Anexo 1 do RGF — Demonstrativo da Despesa com Pessoal (Localização em [MDF  MDF 15 edição.docx.md](https://drive.google.com/file/d/1qYhBrhuP1nPGDKIcmfAAMaNpgXmo4wOj/view?usp=drivesdk): Parte IV — Relatório de Gestão Fiscal, Item `04.01.00. ANEXO 1 – DEMONSTRATIVO DA DESPESA COM PESSOAL`, páginas 495 a 552)

* **Piso Salarial Nacional da Enfermagem (Emenda Constitucional nº 127/2022 — ADCT, art. 38, § 2º, página 496 do MDF 15ª Ed.):**

  > "Nos termos do § 2º do art. 38 do ADCT, incluído pela EC nº 127/2022, para fins de verificação do cumprimento dos limites da despesa total com pessoal previstos nos arts. 19 e 20 da LRF, as despesas com pessoal decorrentes do cumprimento do piso salarial nacional de enfermeiros, técnicos de enfermagem, auxiliares de enfermagem e parteiras, até o limite do montante transferido pela União a título de assistência financeira complementar, serão computadas na seguinte proporção: I - 0% (zero por cento) em 2023; II - 10% (dez por cento) em 2024; III - 20% (vinte por cento) em 2025; IV - 28% (vinte e oito por cento) em 2026; e acrescidos de 10 (dez) pontos percentuais a cada ano, de 2027 a 2033, até atingir 100%."

* **Despesa com Pessoal Não Executada Orçamentariamente (páginas 514 a 516 do MDF 15ª Ed.):**

  > "Na linha Despesa com Pessoal não Executada Orçamentariamente deverão ser registrados os valores das despesas com pessoal cujo fato gerador tenha ocorrido no período de apuração, mas que não tenham sido submetidas à execução orçamentária (empenho e liquidação) no respectivo mês de competência. Quando ocorrer a execução orçamentária dessa despesa em meses subsequentes, o valor anteriormente incluído nessa linha deverá ser subtraído no mês da execução orçamentária, de modo a evitar a dupla contagem da despesa no período móvel de doze meses."

## 4. O Prompt Mestre Reutilizável (Passo a Passo Algorítmico para Reconstruir ou Atualizar o Relatório)

Abaixo está o **Prompt Mestre completo e autocontido**. Você pode copiá-lo e utilizá-lo diretamente em qualquer sessão futura ou agente de IA/Python para gerar, auditar ou estender o relatório aos meses subsequentes (`Novembro/2026`, `Dezembro/2026` e exercícios seguintes):

```
# PROMPT MESTRE: CONSTRUÇÃO E AUDITORIA DO DEMONSTRATIVO DA DESPESA COM PESSOAL (RGF — ANEXO 1) DO PODER EXECUTIVO DO ESTADO DO RIO GRANDE DO NORTE

## 1. CONTEXTO E PAPEL DO AGENTE
Você atuará como Auditor de Finanças e Controle especialista em Contabilidade Aplicada ao Setor Público (CASP), Direito Financeiro (Lei Complementar nº 101/2000 — LRF, atualizada pela LC nº 178/2021) e no Manual de Demonstrativos Fiscais da Secretaria do Tesouro Nacional (MDF — 15ª Edição, 3ª Versão).
Sua tarefa é construir, conciliar e auditar a planilha eletrônica do **Demonstrativo da Despesa com Pessoal (Anexo 1 do Relatório de Gestão Fiscal — RGF)** do **Poder Executivo do Estado do Rio Grande do Norte**, composta por duas abas integradas:
1. Aba `MAPA` (344 linhas): memória de cálculo analítica mês a mês (janela de 12 meses, colunas `C` a `O`, e coluna `P` de totalização acumulada);
2. Aba `QUADRO` (43 linhas): demonstrativo oficial no leiaute do MDF 15ª Edição (Seção 1: Despesa com Pessoal I, II e III; Seção 2: Apuração do Cumprimento do Limite Legal com RCL, RCL Ajustada e Limites Máximo de 49,00%, Prudencial de 46,55% e de Alerta de 44,10%).

## 2. INSUMOS DOCUMENTAIS OBRIGATÓRIOS (EXTRAÍDOS DO SIGEF/RN)
Para cada mês de apuração, você deverá processar quatro famílias de relatórios extraídos do SIGEF/RN:
1. **Comparativo Mensal da Despesa do Poder Executivo (`Comparativo Despesa Autorizada Empenhada Liquidada e Paga_<Mês>.pdf`):**
   - Filtro SIGEF: `Ano Base: 2026 | Mês Referência: <Mês> | Poder: Executivo | Apresentar UG Administrativa: Não`.
   - Regra de leitura: extrair SEMPRE a coluna **`Liquidada no mês (D)`** (regime de competência do art. 18, § 2º, da LRF). Usar a coluna `Liquidada até o mês (E)` do último mês como trava de controle do acumulado.
2. **IEO Mensal do FUNFIRN (`Imprimir Execução Orçamentária - IEO_162233_<Mês>.pdf`):**
   - Filtro SIGEF: `Unidade Gestora: 162233 - FUNDO FINANCEIRO DO ESTADO DO RN | Gestão: 16233 - FUNFIRN | Valores Consulta: No mês | Agrupamento: Subação / Fonte Recurso / Elemento Despesa`.
   - Regra de leitura: extrair a coluna **`Liquidado`** das Subações dos demais Poderes:
     - `408501` (ALRN), `408601` (DPRN), `408701` (MPRN), `408801` (TJRN) e `408901` (TCE/RN).
3. **IEO Mensal do IPERN (`Imprimir Execução Orçamentária - IEO_162011_<Mês>.pdf`):**
   - Filtro SIGEF: `Unidade Gestora: 162011 - INSTITUTO DE PREV. DOS SERV. DO ESTADO | Gestão: 00001 - GESTAO TESOURO | Valores Consulta: No mês | Agrupamento: Subação / Fonte Recurso / Elemento Despesa`.
   - Regra de leitura: extrair a coluna **`Liquidado`** das Subações de pensões dos demais Poderes na Fonte `0.8.04.000105` (e `0.5.00` se houver):
     - `408502` (ALRN), `408602` (DPRN), `408702` (MPRN), `408802` (TJRN) e `408902` (TCE/RN).
4. **Balancetes Mensais da Despesa com Pessoal Não Executada Orçamentariamente (`Relatorio_<timestamp>.pdf`):**
   - Filtro SIGEF: Contas contábeis `8.6.3.3.1.01.00.00 - SALÁRIOS` e `8.6.3.3.1.02.00.00 - DÉCIMO TERCEIRO` (mês `Abertura` e meses de `Janeiro` em diante) + Relatório IEO de execução de restos/competência anterior da UG `162233` (`Imprimir Execução Orçamentária_Despesas_n_Executadas_orça.pdf`).

## 3. PASSO A PASSO ALGORÍTMICO DE PREENCHIMENTO DA ABA `MAPA`

### PASSO 1 — Linha de Controle do GND 31 (Linhas 4 e 5)
- Na **Linha 5 (`GND 31 SIGEF`)**, insira para cada mês o total da linha sintética `3.1 - Pessoal e Encargos Sociais` (coluna `Liquidada no mês (D)`) do `Comparativo da Despesa`.
- Na **Linha 4 (`VERIFICAÇÃO`)**, aplique a fórmula `=D5-D6`, que mede a diferença exata entre o GND 31 total do SIGEF e a Despesa Bruta com Pessoal do Executivo após reclassificações, inclusão de terceirização (GND 33), ajuste da conta `8.6.3.3.1.00.00` e expurgo dos demais Poderes.

### PASSO 2 — Pessoal Ativo: Vencimentos, Vantagens e Outras Despesas Variáveis (Linhas 8 a 101)
1. Nas **Linhas 11 a 101**, extraia do `Comparativo da Despesa` a soma de todas as fontes de recursos (coluna `Liquidada no mês (D)`) de cada subelemento (8 dígitos) pertencente aos elementos:
   - `31.90.04.xx` (Contratação por Tempo Determinado);
   - `31.90.05.xx` (Outros Benefícios Previdenciários do Ativo — exceto `.03` Pensão Especial);
   - `31.90.07.03` (Contribuição a Entidades Fechadas de Previdência);
   - `31.90.08.xx` (Outros Benefícios Assistenciais);
   - `31.90.11.xx` (Vencimentos e Vantagens Fixas — Pessoal Civil);
   - `31.90.12.xx` (Vencimentos e Vantagens Fixas — Pessoal Militar);
   - `31.90.13.08` (Plano de Saúde — classificado em Vencimentos e Vantagens na linha 54);
   - `31.90.16.xx` (Outras Despesas Variáveis — Pessoal Civil);
   - `31.90.17.xx` (Outras Despesas Variáveis — Pessoal Militar);
   - `31.90.91.xx` (Sentenças Judiciais de Ativos — **EXCLUINDO obrigatoriamente `31.90.91.02` Aposentadorias e `31.90.91.03` Pensões**);
   - `31.90.92.xx` (DEA de Ativos — **EXCLUINDO obrigatoriamente `31.90.92.02` Aposentadorias e `31.90.92.03` Pensões**);
   - `31.90.94.xx` (Indenizações e Restituições Trabalhistas);
   - `31.90.96.xx` (Ressarcimento de Despesas de Pessoal Requisitado).
2. **Reclassificação Interna de `31.90.92.97 (Obrigações Patronais)`:** Como a linha `93` captura `31.90.92.97`, vincule a **Linha 10 (`(-) 31.90.92.97 - OBRIGAÇÕES PATRONAIS`)** como `=D93` e aplique na **Linha 8** a fórmula `=SUM(D11:D101)+D9-D10`.

### PASSO 3 — Pessoal Ativo: Obrigações Patronais Líquidas do Executivo (Linhas 102 a 180)
1. **Obrigações Patronais Brutas (Linhas 103 a 163):**
   - Extraia todos os subelementos de `31.90.13.xx` (**exceto `31.90.13.08`**);
   - Na **Linha 134 (`31.90.92.97 - OBRIGAÇÕES PATRONAIS`)**, vincule `=D93` (reclassificado do bloco anterior);
   - Extraia todos os subelementos de `31.91.13.xx` (Obrigações Patronais Intraorçamentárias), `31.91.91.xx` e `31.91.92.xx`.
2. **Expurgo das Obrigações Patronais dos Demais Poderes (Linhas 164 a 180):**
   - Vincule diretamente às linhas correspondentes do bloco bruto todos os subelementos terminados em `.71` (TJ), `.72` (AL), `.73` (TCE), `.74` (DPE) e `.75` (MP) dentro de `31.90.13`, `31.90.92`, `31.91.13`, `31.91.91` e `31.91.92` (`=D124`, `=D125`, `=D135` a `=D139`, `=D152` a `=D156`, `=D162` e `=D163`).
3. Na **Linha 102 (`Obrigações Patronais`)**, aplique a fórmula `=SUM(D103:D163)-SUM(D164:D180)`.

### PASSO 4 — Pessoal Inativo e Pensionistas: Aposentadorias e Pensões Líquidas do Executivo (Linhas 181 a 244)
1. **Aposentadorias, Reserva e Reformas Brutas (Linhas 183 a 202):**
   - Extraia do `Comparativo da Despesa` todos os subelementos de `31.90.01.xx`, mais `31.90.07.01`, `31.90.07.02`, `31.90.91.02` e `31.90.92.02`.
2. **Expurgo Bruto de Aposentadorias dos Demais Poderes (Linhas 203 a 208):**
   - Nos relatórios `IEO_162233_<Mês>.pdf` (FUNFIRN), some os valores **Liquidados** em **TODAS as fontes (`0.5.00 + 0.8.00`)** nas subações `408501` (ALRN), `408601` (DPRN), `408701` (MPRN), `408801` (TJRN) e `408901` (TCE/RN) para os elementos `31.90.01`, `31.90.91.02` e `31.90.92.02`.
   - Na **Linha 182**, aplique `=SUM(D183:D202)-SUM(D203:D208)`.
3. **Pensões Brutas (Linhas 210 a 227):**
   - Extraia do `Comparativo da Despesa` todos os subelementos de `31.90.03.xx`, mais `31.90.05.03`, `31.90.91.03` e `31.90.92.03`.
4. **Expurgo Bruto de Pensões dos Demais Poderes (Linhas 228 a 244):**
   - **Linhas 228 a 232 (FUNFIRN `162233` — `31.90.03`):** Some no `IEO_162233` os valores **Liquidados** nas fontes **`0.5.00 + 0.8.00`** para `31.90.03` nas subações `408501` a `408901`.
   - **Linhas 233 a 239 (IPERN `162011` — `31.90.03` e `31.90.92.03`):** Extraia no `IEO_162011` os valores **Liquidados** na fonte **`0.8.04.000105`** (e `0.5.00` para DEA) nas subações `408502` a `408902`.
   - **Linhas 240 a 244 (FUNFIRN `162233` — `31.90.91.03` e `31.90.92.03`):** Some no `IEO_162233` os valores **Liquidados** nas fontes **`0.5.00 + 0.8.00`** para `31.90.91.03` e `31.90.92.03` nas subações `408501` a `408901` (mantendo estritamente a coluna `Liquidado`, inclusive os `R$ 92.094,19` da fonte `0.5.00` + `R$ 29.377,60` da fonte `0.8.00` = `R$ 121.471,79` em Abril/2026 na subação `408801` TJRN).
   - Na **Linha 209**, aplique `=SUM(D210:D227)-SUM(D228:D244)`.

### PASSO 5 — Outras Despesas de Pessoal (Terceirização — Linhas 245 a 249)
- Extraia do `Comparativo da Despesa` (dentro do grupo `3.3 - Outras Despesas Correntes`) a coluna `Liquidada no mês (D)` dos subelementos de `3.3.90.34.xx` (Linhas 246 e 247) e do subelemento `3.3.90.92.34` (Linha 249).
- Na **Linha 245**, aplique `=SUM(D246:D249)`.

### PASSO 6 — Despesa com Pessoal Não Executada Orçamentariamente (Linha 250)
- A partir dos balancetes mensais das contas `8.6.3.3.1.01.00.00 (SALÁRIOS)` e `8.6.3.3.1.02.00.00 (DÉCIMO TERCEIRO)`:
  1. Na coluna de abertura/dezembro anterior (`Coluna C`), some os saldos credores de encerramento do exercício anterior de ambas as contas, **expurgando** a parcela de encargos patronais de outros Poderes (`31.91.13.71/.72/.73/.75`) contida na UG `162233` (`R$ 623.792.553,08 - R$ 1.337.759,24 = R$ 622.454.793,84`).
  2. Em cada mês de janeiro em diante (`Colunas D a O`), calcule a variação líquida mensal:
     $$\text{Linha 250}_{\text{mês}} = (\text{Movimento Credor}_{01} + \text{Movimento Credor}_{02}) - (\text{Movimento Devedor}_{01} + \text{Movimento Devedor}_{02} - \text{Baixa Outros Poderes}_{162233})$$
  3. Verifique se, ao zerarem os saldos das contas `8.6.3.3.1.01` e `8.6.3.3.1.02`, a soma das variações mensais do exercício anula exatamente o saldo inicial de dezembro do ano anterior (`-R$ 622.454.793,84`).

### PASSO 7 — Quadro II: Despesas Não Computadas (Linhas 252 a 344 — Art. 19, § 1º, LRF e EC 120/127)
1. **Indenizações por Demissão e PDV (Linhas 253 a 261):**
   - Vincule `31.90.94.xx` (`=D96` a `=D99`) e subtraia na Linha 261 eventual parcela executada na Fonte `X.604`. Fórmula da Linha 253: `=SUM(D254:D260)-D261`.
2. **Decorrentes de Decisão Judicial de Período Anterior (Linhas 262 a 273):**
   - Vincule os subelementos de `31.90.91.xx` de ativos (`=D70` a `=D74`), `31.91.91.xx` (`=D158`, `=D159`), `31.90.91.02` (`=D199`) e `31.90.91.03` (`=D224`), subtraia os subelementos de outros Poderes (`=D175`) e, na **Linha 273 (`(-) 31.90.91.00 - SENTENÇAS JUDICIAIS (FR X.800)`)**, vincule `=D307+D308+D333` para impedir dupla dedução com o bloco de Inativos Vinculados. Fórmula da Linha 262: `=SUM(D263:D270)-SUM(D271:D273)`.
3. **Despesas de Exercícios Anteriores — DEA (Linhas 274 a 285 — ALOCAÇÃO EXCLUSIVA NA COLUNA `O` / DEZEMBRO):**
   - Mantenha as colunas `D` a `N` com `0,00` e concentre na **Coluna `O` (`DEZ/2026`)** o acumulado de `31.90.92.xx` (ativos, patronais e inativos do Executivo), `31.91.92.xx` (líquido de outros Poderes) e `33.90.92.34` (terceirização de exercícios anteriores), subtraindo obrigatoriamente:
     - **Linha 283 (`(-) 31.90.92.00 - DEA (FR X.800 e X.804)`):** parcela de DEA de inativos/pensionistas custeada por recursos vinculados do RPPS (`R$ 4.191,42`);
     - **Linha 284 (`(-) 31.90.92.00 - DEA (FR X.605)`):** parcela de DEA custeada pela fonte do Piso da Enfermagem (`=P337`, `R$ 1.123.833,39`);
     - **Linha 285 (`(-) 31.90.92.00 - DEA (FR X.604)`):** parcela de DEA custeada pela fonte de ACS/ACE (`=P342`).
4. **Inativos e Pensionistas com Recursos Vinculados (Linhas 286 a 333 — Fontes `800, 801, 802, 803 e 804`):**
   - **Aposentadorias Brutas Vinculadas (Linhas 288 a 298):** Extraia do `Comparativo da Despesa` os valores liquidados em `31.90.01.01`, `31.90.01.02` e `31.90.92.02` **exclusivamente nas Fontes `0.8.00 / 4.8.00 / 0.8.01 / 0.8.02 / 0.8.03 / 0.8.04 / 4.8.04`** (NUNCA inclua a Fonte `500`, por vedação do art. 19, § 3º, da LRF).
   - **Expurgo de Aposentadorias Vinculadas dos Demais Poderes (Linhas 299 a 306):** Extraia do `IEO_162233` os valores liquidados nas subações `408501` a `408901` **exclusivamente na Fonte `0.8.00 / 4.8.00`**.
   - **Sentenças Judiciais de Aposentadorias na Fonte `800` (Linhas 307 e 308):** Extraia `31.90.91.02` na Fonte `X.800` (`+`) e subtraia o que pertencer a outros Poderes na Fonte `X.800` (`-`).
   - **Pensões Brutas Vinculadas (Linhas 309 a 315):** Extraia do `Comparativo da Despesa` os valores liquidados em `31.90.03.01`, `31.90.03.02` e `31.90.92.03` **exclusivamente nas Fontes `800, 802, 803 e 804`**.
   - **Expurgo de Pensões Vinculadas dos Demais Poderes (Linhas 316 a 332):** Extraia do `IEO_162233` apenas a **Fonte `0.8.00 / 4.8.00`** nas subações `408501` a `408901` (Linhas 316 a 320 e 328 a 332) e extraia do `IEO_162011` a **Fonte `0.8.04.000105`** nas subações `408502` a `408902` (Linhas 321 a 327).
   - **Sentenças Judiciais de Pensões na Fonte `800` (Linha 333):** Extraia `31.90.91.03` na Fonte `X.800` líquido de outros Poderes.
5. **Piso Salarial da Enfermagem — EC nº 127/2022 (Linhas 334 a 338):**
   - Nas Linhas `335 a 338`, extraia do `Comparativo da Despesa` os valores liquidados na **Fonte `0.6.05.000000 / 4.6.05.000000`** nos elementos `31.90.11`, `31.90.13`, `31.90.92` e `31.91.13`.
   - Na **Linha 334**, aplique o percentual de dedução constitucional de **72%** vigente para o exercício de **2026** (ADCT, art. 38, § 2º, inciso IV): `=ROUND(SUM(D335:D338)*0.72, 2)`. (Para 2027, alterar o fator para `0.62`; para 2028, `0.52`, e assim sucessivamente).
6. **Agentes Comunitários de Saúde e Endemias — EC nº 120/2022 (Linhas 339 a 344):**
   - Extraia os valores liquidados na **Fonte `0.6.04.000000 / 4.6.04.000000`** nos elementos `31.90.11`, `31.90.13`, `31.90.92`, `31.90.94` e `31.91.13`. Fórmula da Linha 339: `=SUM(D340:D344)`.

### PASSO 8 — Consolidação na Aba `QUADRO` e Checklist de Auditoria Final
1. Vincule todas as células mensais e totais da aba `QUADRO` (Linhas 17 a 33) diretamente às linhas sintéticas da aba `MAPA` (`=MAPA!D6`, `=MAPA!D7`, `=MAPA!D8`, `=MAPA!D102`, `=MAPA!D181`, `=MAPA!D182`, `=MAPA!D209`, `=MAPA!D245`, `=MAPA!D250`, `=MAPA!D252`, `=MAPA!D253`, `=MAPA!D262`, `=MAPA!D274`, `=MAPA!D286`, `=MAPA!D334`, `=MAPA!D339` e `=MAPA!D251`).
2. Na Seção de Limites da aba `QUADRO` (Linhas 34 a 43), insira a Receita Corrente Líquida (RCL), as transferências obrigatórias da União relativas às ECs nº 120/2022 e nº 127/2022 para apurar a **RCL Ajustada**, e calcule os percentuais em relação à RCL Ajustada para os limites do Poder Executivo Estadual:
   - **Limite Máximo (art. 20, II, "c", LRF):** `49,00%` (`=RCL_Ajustada * 0,49`)
   - **Limite Prudencial (art. 22, parágrafo único, LRF — 95%):** `46,55%` (`=Limite_Maximo * 0,95`)
   - **Limite de Alerta (art. 59, § 1º, II, LRF — 90%):** `44,10%` (`=Limite_Maximo * 0,90`)
3. Execute as 4 travas finais de auditoria antes de homologar o relatório:
   - **Trava 1:** A soma de `MAPA!D5:M5` deve ser idêntica à coluna `Liquidada até o mês (E)` da linha `3.1 - Pessoal e Encargos Sociais` na página 1 do `Comparativo da Despesa` do último mês apurado.
   - **Trava 2:** A soma das variações mensais de janeiro a maio na Linha 250 (`Despesa Não Executada Orçamentariamente`) deve zerar exatamente o saldo de abertura do exercício anterior (após o expurgo de `R$ 1.337.759,24` dos demais Poderes na UG `162233`).
   - **Trava 3:** Nenhum valor da Fonte `500` pode constar nas linhas `288 a 333` (bloco de Recursos Vinculados do RPPS).
   - **Trava 4:** Toda execução de `31.XX.91` e `31.XX.92` nas Fontes `800/804` ou `605` deve estar expurgada nas linhas `273`, `283` e `284` para impedir dupla dedução no Quadro II.

```