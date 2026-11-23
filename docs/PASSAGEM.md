# Documento de passagem

Para quem continuar este trabalho. Estado em **2026-11-23**.

---

## O que o sistema faz

Apura os demonstrativos fiscais do **Rio Grande do Norte** (RREO e RGF) a partir
da **Matriz de Saldos Contábeis (MSC)** do Siconfi e dos relatórios do
**SIGEF/RN**, e confere cada célula contra o arquivo **publicado no Siconfi** —
não contra a planilha de trabalho da equipe.

O produto é do RN. Os testes em outros estados serviram de diagnóstico (acharam
bugs reais), mas não são requisito.

```bash
python verificar_tudo.py   # 30 de 30 conferências ponta a ponta
python verificacao.py      # livro (608 células), divergências, certificado
python rodar_testes.py     # 134 testes
python placar_relatorios.py  # docs/PLACAR.md — acerto por relatório
```

**Placar: 605 de 608 células exatas (99,5%).** As 3 divergências são o mesmo erro
de R$ 5.241,65 no arquivo publicado de abril/2026 — provado no MAPA do próprio
auditor e no quadro de 2026. **Nenhuma divergência é nossa.**

---

## O caminho que funciona

Toda descoberta deste projeto veio na mesma ordem:

```
1. MDF, no capítulo do anexo
2. mapeamento da STN em dados/mapeamentos/
3. manual dos auditores (etonjones) e planilhas da equipe
4. teste que trava o achado
```

**Nunca comece pelo código.** Cada vez que comecei, perdi uma rodada.

---

## A regra que explica tudo

> **Quando a dimensão existe na matriz, o anexo fecha.
> Quando não existe, não fecha — e nenhuma fórmula resolve.**

| frente | dimensão que falta | onde ela existe |
|---|---|---|
| RGF Anexo 1 — expurgo patronal | subelemento do ND (`.22`, `.43`, `.46`…) | Comparativo (PDF) |
| RGF Anexo 2 — dívida | detalhe da classe 2 (492 contas vs 128 da MSC) | balancete |

**Não é falta de fórmula. É falta de recorte.** O RREO inteiro sai da matriz;
do RGF, saem 4 dos 6 anexos. Os dois que faltam são os dois maiores em células.

---

## O que fecha (por relatório)

| relatório | células | acerto |
|---|---:|---:|
| RGF Anexo 1 — Despesa com Pessoal | 362 | 99,2% |
| RGF Anexo 5 — Disponibilidade de Caixa | 95 | 100% |
| RGF Anexo 2 — DCL | 28 | 100% |
| RREO Anexo 2 — Despesa por Função | 25 | 100% |
| RREO Anexo 7 — RP por Poder | 17 | 100% |
| RREO Anexo 13 — PPP | 13 | 100% |
| RREO Anexo 14 — Simplificado | 12 | 100% |
| RGF Anexo 6 / RREO Anexo 4 / RGF Anexo 4 / RREO Anexo 9 | 9 cada | 100% |
| RGF Anexo 3 — Garantias | 8 | 100% |
| RREO Anexo 11 — Alienação de Ativos | 5 | 100% |
| RREO Anexo 1 — Balanço Orçamentário | 3 | 100% |
| RREO Anexos 3 e 6, motor/batimento | 1–2 | 100% |

Detalhe em `docs/PLACAR.md`.

---

## Os três motores do RGF do RN

Cada aba usa o motor que fecha ao centavo:

| aba | motor | fonte |
|---|---|---|
| Anexo 1 | quadro do auditor / `mapa_anexo1` | Comparativo (PDF) |
| Anexo 2 | `rgf_anexo2_dcl` | balancete de encerramento |
| Anexos 3 a 6 | `pipeline` | MSC |

`gerar_rgf_rn.py` roda o pipeline e **injeta** o Anexo 1 exato (192 células).
A injeção do Anexo 2 está **pendente**: o casamento por nome das seções do
balancete com os rótulos da aba pegava a seção errada e piorava a DC. O motor
exato existe e fecha em 0,00 — falta o de-para de nomes (tabela, não código).

---

## Generalização (diagnóstico, não requisito)

| teste | resultado |
|---|---|
| RREO Anexo 2 nos **27 estados** | **27 de 27 exatos** (R$ 8,7 bi a R$ 369 bi) |
| motor de pessoal em 5 estados | lê sem alterar código |
| RGF Anexo 1 pela matriz, 5 estados | −1,7% (RN) a −18,7% (MG) após correção do CO |

O RREO Anexo 2 é **universal**: a regra vale sem mapa local. O RGF Anexo 1 e 2
precisam de documentos que variam por estado.

---

## Achados que mudaram o jogo

| achado | efeito |
|---|---|
| a RCL é construível da classe 6 (`rcl_msc.py`) | 0,0146% em 2025 |
| a não executada tem sinal (`nao_executada.py`) | jan/2025 = −252 mi |
| o filtro de CO cortava R$ 953 mi das aposentadorias | I do RN: −10,21% → −1,73% |
| 32 e 46 são **naturezas**, não fontes | RP e Outras Dívidas fecham |
| os 942 mi do RP são **cálculo**, não conta | RP = até o caixa disponível |
| a conta `8.6.3.2.2` não existe | era anotação de planilha |
| DTP = III + RPNP (`622130500/600`) | última verificação fechou |
| a aba certa de 2025 é o **Quadro**, não o Mapeamento | 6 linhas exatas |

---

## Armadilhas já pagas

| armadilha | lição |
|---|---|
| nome não é chave | casar por prefixo e posição (Anexos 2, 3, 4, 6) |
| total certo esconde erro | conferir a **parcela**, não só o total |
| total repetido no publicado | bloco intra do RREO 2 aparece 2×; somar uma vez |
| tolerância de 0,5% | exigir o centavo |
| zero silencioso | separador `,` vs `;` devolvia 0 sem erro |
| `<MR>` é dezembro, não o total | o total soma as 12 colunas |
| caminho morto | as pastas de dados mudam de lugar; usar `caminhos.py` |

---

## Ambiente e dados (atualizado em 23/11)

As pastas de dados **não são versionadas** (`.gitignore`). Um clone traz só código
e documentação. Para rodar:

1. `python baixar_msc.py` — baixa a MSC da API para `dados/acervo`.
2. `python reconstruir_msc.py` — reconstroi `dados/siconfi_rn_msc` (formato antigo).
3. `python reconstruir_siconfi.py` — reconstroi `dados/siconfi_rn` (publicados).

Os módulos do caminho atual resolvem os caminhos por `caminhos.py`
(`msc_antiga()`, `siconfi_publicados()`, `arquivos_etonjones()`,
`relatorios_contag()`). A pasta original em `AppData\...\Microsoft VS Code` sumiu;
os reconstutores a substituem dentro do repo.

**Os ~80 scripts na raiz além do caminho atual são histórico de investigação** —
vários ainda apontam para a pasta morta e não são o caminho atual.

---

## O que falta

| item | depende de |
|---|---|
| de-para de nomes do Anexo 2 (injeção no `gerar_rgf_rn`) | tabela, ~20 linhas |
| RREO no molde do `gerar_rgf_rn` | reaproveitar a estrutura |
| Anexo 1 e 2 só da matriz | subelemento do ND + classe 2 detalhada (pedido ao Estado) |

---

## Documentos que importam

| arquivo | o que é |
|---|---|
| `docs/PLACAR.md` | acerto por relatório (gerado) |
| `docs/DIVERGENCIAS.md` | as 3 divergências, com causa (gerado) |
| `docs/CERTIFICADO.md` | data, commit, contagem (gerado) |
| `docs/REVISAO_GERAL.md` | o diário completo (seções 17.x) |
| `docs/ANEXO1_CRUZAMENTO.md` | MDF × etonjones × nosso código |
| `docs/INDEX.md` | o mapa dos documentos |

---

## Regras de trabalho deste projeto

1. **nunca forçar número para fechar** — divergência com causa vale mais que
   número arredondado;
2. **conferir contra o publicado**, não contra a planilha da equipe;
3. **toda divergência tem causa escrita**, com no mínimo 60 caracteres (há teste);
4. **teste de ausência é teste válido** — documenta o limite;
5. **quando a matriz não tem a dimensão, parar** e pedir a extração;
6. **o modo Siconfi** (`modo_siconfi_q2`) reproduz o erro de abril sob demanda,
   desligado por padrão — publicar número errado é decisão do gestor.
