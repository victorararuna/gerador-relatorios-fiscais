# Plano de trabalho — Aplicação de Relatórios Fiscais do RN (MDF/Siconfi)

> **Documento histórico.** Escrito em 11/11/2026, quando o plano era uma
> **aplicação de mesa com interface**. O que existe hoje é diferente: um conjunto
> de módulos de apuração com livro de verificação, sem interface gráfica.
>
> Números e fases abaixo **não descrevem o estado atual**.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2.**

---


**Situação:** fases 1 e 2 concluídas (núcleo gerador, conferência, interface e catálogo de rótulos).
**Cobertura:** 12 demonstrativos por período (RREO 1, 2, 3, 4, 6, 7, 13 e RGF 1, 2, 3, 4, 6).
**Data:** 11/11/2026 · **Ente:** 24 – Rio Grande do Norte · **Instituição:** 171 – Governo do Estado

---

## 1. Objetivo

Transformar o processo manual de montagem do **RREO** e do **RGF** do Estado em uma
aplicação de mesa que:

1. recebe os **rascunhos do Siconfi** (`.xls` por anexo) e as planilhas de conferência;
2. **gera** os demonstrativos em formato de publicação (XLSX + HTML/PDF);
3. **confere** os números antes de gerar (aritmética, totais, percentuais, limites);
4. **valida contra o Siconfi** (o que foi transmitido) e contra os artefatos internos;
5. oferece um **painel de parâmetros fiscais** para acompanhamento ao longo do exercício.

A régua de qualidade é uma só: *o demonstrativo gerado tem que poder ser publicado sem
retrabalho* — e, quando não puder, a aplicação precisa dizer exatamente por quê.

---

## 2. O que existe hoje (diagnóstico do material recebido)

| Artefato | Papel no processo | Observação |
|---|---|---|
| `RASCUNHO RREO.xls` (B2), `planilha_auditoria (1).xls` (B4) | dados do RREO por anexo | formato Siconfi v14, vigência 05/01/2026, 8 anexos |
| `RASCUNHO RGF.xls` (Q1), `planilha_auditoria.xls` (Q2) | dados do RGF por anexo | 5 anexos |
| `SICONFI_RREO_24_20260105_v14.xls` / `SICONFI_RGF_...` | template oficial de importação | **criptografado (FILEPASS/RC4)**, senha não é a padrão de reserva |
| `RREO 2026_B*_*.xlsx` (16 abas cada) | planilha de trabalho por anexo | traz MAPEAMENTO, CONSOLIDADO, conferências cruzadas (BO×RCL, BO×Anexo 6/9, SIAI, DCC) |
| `RREO 2026_B4_03 – RCL.xlsx` (30 abas) | apuração da RCL por poder | Executivo, TCE, DP, MP, AL, FDM, TJ, consolidado, SIGEF |
| PDFs por anexo | saída publicada | formato de referência |

**Conclusão do diagnóstico:** o dado já chega *consolidado* no rascunho; o trabalho que
consome tempo é (a) montar/formatar o demonstrativo, (b) repetir as conferências, (c)
refazer tudo a cada período. É exatamente onde a aplicação atua.

---

## 3. Escopo

### Dentro do escopo
- RREO Anexos 1, 2, 3, 4, 6, 7, 13, 14 · RGF Anexos 1, 2, 3, 4, 6
- Geração XLSX + HTML (impressão em PDF pelo navegador)
- Conferência automática (aritmética, totais, percentuais, totais mensais)
- Leitura de `.xls` **sem depender de Excel, LibreOffice ou xlrd** (leitor próprio)
- Interface desktop para servidores, sem instalação de banco

### Fora do escopo (por ora)
- Assinatura digital / transmissão automática ao Siconfi
- Substituir o sistema contábil (SIAFEM) ou o SIAI/TCE
- Multi-ente (a aplicação é parametrizada, mas o alvo é o Estado)

---

## 4. Fases

### Fase 0 — Infraestrutura de leitura ✅
Leitor CFB/OLE2 + BIFF8 em Python puro (`app/leitor_xls.py`), incluindo BIFF5 e strings
Unicode. Motivo: o ambiente não tem `xlrd`, o Excel via COM é bloqueado por política e
não há LibreOffice. **Entregue e testado** nos 8 arquivos recebidos.

### Fase 1 — Núcleo gerador ✅ (esta entrega)
- `app/modelo.py` — domínio (Documento, Anexo, Bloco, Linha, Coluna)
- `app/rascunho.py` — parser dos rascunhos (metadados + blocos + cabeçalho de colunas)
- `app/anexos.py` — catálogo (título, base legal, nota de rodapé) dos 13 anexos
- `app/gerador.py` — demonstrativo XLSX formatado + HTML de impressão
- `app/validacao.py` — motor de conferência
- `app/ui.py` + `main.py` — interface e CLI

**Critério de aceite:** gerar os 4 períodos recebidos sem erro de execução; nenhum
"erro" de conferência nos dados consolidados; alertas explicados.

### Fase 2 — Catálogo de rótulos dos anexos "sem rótulo" ✅
RREO 3, 4, 6, 7 e 13 chegam do Siconfi **apenas com valores**. Os rótulos oficiais foram
minerados das planilhas de trabalho já existentes (caminho 3), sem depender de senha nem
de terceiros.

**Método** (`ferramentas/descobrir_rotulos.py`): para cada quadro do anexo, procura-se a
aba e a coluna cujos valores acompanham, na mesma ordem, os do rascunho. O alinhamento
ancora no primeiro valor e segue em sequência, tolerando buracos (linhas vazias que a
exportação do Siconfi descarta). Há um fallback posicional para quadros pequenos cujos
valores divergem (anexo 13). A aba é escolhida por nota: casamento × cobertura de rótulos
× preferência de nome (SICONFI, Rascunho, Matriz).

**Resultado:** 26 de 26 quadros cobertos; catálogos em `dados/catalogo/*.json` com
rastreabilidade (aba, coluna e nota de cada quadro).

| Anexo | Fonte | Linhas rotuladas |
|---|---|---|
| RREO 3 | `SICONFI` | 100% |
| RREO 4 | `SICONFI` / `Rascunho` | 94% |
| RREO 6 | `MATRIZ-SICONF` | 99% |
| RREO 7 | `Anexo 07 - 4° bimestre` | 100% |
| RREO 13 | `SICONFI` | 100% |

O parser aplica o catálogo automaticamente (`app/catalogo.py`). O Anexo 14 foi marcado
como **não aplicável** ao Estado: é o demonstrativo simplificado do art. 63 da LRF,
exclusivo de municípios com menos de 50 mil habitantes.

**Critério de aceite:** os anexos antes bloqueados passam a gerar com rótulos oficiais,
conferíveis contra o PDF publicado. Atendido, com uma ressalva registrada em Limitações.

### Fase 3 — PDF de publicação ⏳
Hoje o PDF sai por impressão do HTML (Ctrl+P, A4 paisagem, já formatado). Evoluir para
geração direta (motor próprio ou LibreOffice headless), com:
- quebra de página por bloco, cabeçalho repetido;
- marca d'água "RASCUNHO" configurável;
- conferência visual automática (comparar com o PDF publicado).

### Fase 4 — Conferência cruzada e Siconfi ⏳
- Comparar o gerado com o **export do Siconfi** do período (o que foi transmitido).
- Regras por anexo: RCL (Anexo 3) × RGF Anexo 6; Balanço Orçamentário × RCL;
  Anexo 2 (função) × Anexo 1 (despesa); Dívida (RGF 2) × Garantias (RGF 3) ×
  Operações de crédito (RGF 4).
- Limites da LRF: pessoal (60% da RCL — art. 20, II, "c"), dívida (200% — Res. SF 40),
  operações de crédito (16% — Res. SF 43), garantias (22%).
- Gerar o arquivo de importação do Siconfi (depende da Fase 2).

**Critério de aceite:** rodar um exercício fechado (2025) e reproduzir os números
publicados, divergência zero.

### Fase 5 — Painel de parâmetros fiscais ⏳
Dashboard na própria aplicação, com a série dos períodos carregados:
- RCL, despesa com pessoal (% da RCL e limite), dívida consolidada líquida (% da RCL),
  operações de crédito, garantias, resultado primário/nominal, restos a pagar;
- semáforo de limite (confortável / alerta 90% / excedido);
- tendência por período e comparativo com o mesmo período do ano anterior;
- exportação dos indicadores em XLSX/CSV para o gabinete.

---

## 5. Arquitetura

```
                 ┌──────────────────────────────┐
  .xls rascunho  │ app/leitor_xls.py            │  CFB/OLE2 + BIFF8, sem dependências
  (Siconfi v14)  │  (leitor próprio)            │
                 └──────────────┬───────────────┘
                                ▼
                 ┌──────────────────────────────┐
                 │ app/rascunho.py              │  metadados, blocos, colunas, linhas
                 │  → Documento/Anexo/Bloco     │  (app/modelo.py)
                 └──────────────┬───────────────┘
                    ┌───────────┴────────────┐
                    ▼                        ▼
     ┌────────────────────────┐   ┌────────────────────────┐
     │ app/validacao.py       │   │ app/gerador.py         │
     │  aritmética, totais,   │   │  XLSX + HTML (PDF)     │
     │  percentuais, mensal   │   │  com enquadramento MDF │
     └───────────┬────────────┘   └───────────┬────────────┘
                 └───────────┬────────────────┘
                             ▼
                 ┌──────────────────────────────┐
                 │ app/ui.py (Tkinter)          │
                 │  Entradas | Conferência |    │
                 │  Demonstrativos | (Painel)   │
                 └──────────────────────────────┘
```

**Decisões de projeto**

| Decisão | Motivo |
|---|---|
| Leitor `.xls` próprio | ambiente sem xlrd/LibreOffice e com COM bloqueado; além disso, o app roda em máquina de servidor sem depender de Office |
| Layout lido do próprio rascunho | o cabeçalho de colunas vem no arquivo; mudou o layout, o app acusa em vez de gerar errado |
| Catálogo só com o que falta (título, base legal, nota) | evita duplicar 13 layouts e reduz o risco de divergência |
| Gerar XLSX **e** HTML | XLSX para edição/publicação; HTML resolve o PDF sem motor extra |
| Conferência separada da geração | o mesmo motor serve para auditoria de períodos passados |

---

## 6. Regras de conferência implementadas

| # | Regra | Severidade |
|---|---|---|
| 1 | `% (a/b)` recalculado a partir das colunas marcadas (a), (b)… | **erro** (tolerância 0,05 p.p.) |
| 2 | `SALDO (a-c)` = a − c | **erro** (tolerância R$ 0,01) |
| 3 | Linha de total = soma dos subordinados (filhos diretos **ou** folhas) | alerta |
| 4 | Coluna `TOTAL` = soma das 12 colunas mensais `<MR-...>` | alerta (admite ajuste de RP) |

Alertas conhecidos nos dados atuais, todos explicáveis:
- **RGF Anexo 1** — "Despesa Líquida com Pessoal (III)": a coluna *Total (últimos 12 meses)*
  não é a soma dos meses, porque carrega o ajuste de **despesa não executada / RP não
  processados** (R$ 1.272.570,46 no 2º quadrimestre). Comportamento previsto na regra.
- **RREO Anexo 2** — a soma das funções listadas no rascunho não fecha com o total (I);
  o rascunho traz 12 funções e o total considera a estrutura completa. **Item a investigar
  na Fase 2**, antes de publicar.

---

## 7. Pendências e riscos

| Item | Impacto | Encaminhamento |
|---|---|---|
| ~~Anexos 3, 4, 6, 7, 13 sem rótulos no rascunho~~ | resolvido | Fase 2 concluída (mineração das planilhas de trabalho) |
| Cabeçalho das colunas nos anexos 4, 6 e 7 | títulos genéricos ("Valor 1…N") | Fase 3 — extrair do MDF ou do template Siconfi |
| Anexo 14 (RREO) | não se aplica ao Estado | fora de escopo por definição legal |
| Template Siconfi criptografado | bloqueia o caminho mais fiel | solicitar a senha à SUCONF/STN ou ao setor que gerou |
| Anexo 2 não fecha | risco de publicar total inconsistente | investigar na Fase 2; conferir contra o Siconfi do período |
| Sem motor de PDF nativo | PDF depende do navegador | Fase 3 |
| `RCL` tem apuração própria por poder (30 abas) | não caberá no gerador genérico | criar gerador específico do Anexo 3 na Fase 2 |

---

## 8. Como executar

```powershell
# interface
python main.py

# linha de comando (lote)
python main.py --cli --entrada dados --saida saida
```

Saída organizada por período: `saida/RREO_2026_P2/…` e `saida/RGF_2026_P2/…`,
com um XLSX e um HTML por anexo.
