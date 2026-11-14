# Documento de passagem

Para quem continuar este trabalho. Estado em 2026-11-14.

---

## O que o sistema faz

Apura os demonstrativos fiscais do RN a partir da **Matriz de Saldos Contábeis**
e confere cada linha contra o arquivo **publicado no Siconfi** — não contra a
planilha de trabalho da equipe.

```bash
python verificar_tudo.py   # 29 de 30 conferencias ponta a ponta
python verificacao.py      # livro (396 celulas), divergencias, certificado
python rodar_testes.py     # 104 testes
```

**Placar: 370 de 396 células exatas (93,4%).**

---

## O caminho que funciona

Toda descoberta deste projeto veio na mesma ordem:

```
1. MDF, no capitulo do anexo
2. mapeamento da STN em dados/mapeamentos/
3. manual dos auditores (etonjones) e planilhas em Downloads
4. teste que trava o achado
```

**Nunca comece pelo código.** Cada vez que comecei, perdi uma rodada.

---

## A regra que explica tudo

> **Quando a dimensão existe na matriz, o anexo fecha.
> Quando não existe, não fecha — e nenhuma fórmula resolve.**

| frente | dimensão que falta | onde ela existe |
|---|---|---|
| Anexo 2 — RP e "Outras Dívidas" | conta `8.6.3.2.2.00.00` | só no SIGEF |
| Anexo 1 — expurgo patronal | subelemento `.71`–`.75` × fonte | Comparativo (sem fonte) |
| Anexo 1 — inativos | **subação** (408501 a 408902) | só no IEO |
| Anexo 1 — 2025 | a regra de Poder daquele ano | não existe no material |
| Anexo 6 — correntes | conceito "exceto RPPS" ampliado | não existe na matriz |

**Não é falta de fórmula. É falta de recorte.**

---

## O que já fecha

| anexo | células | situação |
|---|---:|---|
| RREO 1, 2, 3, 4, 7, 9, 13, 14 | 55 | **100%** |
| RREO 11 | 5 | **100%** (novo) |
| RGF 3, 4, 5 | 112 | **100%** |
| RGF 1 por Poder | 100 | **100%** |
| RGF 1 — limites | 6 | **100%** |
| RGF 6 — limites | 5 | **100%** |
| RGF 2 — 2026 | 6 | **100%** |
| RREO 6 — capital | 1 | **100%** |
| Linha 251 (não executada) | 17 | **100%** (2025 e 2026) |

---

## Os dois achados que mudaram o jogo

### A RCL é construível

O mapeamento da STN mostrou que a receita realizada está na **classe 6**
(`6.2.1.2.0.00.00`), não na 4 — e as deduções na `6.2.1.3.x` e em naturezas de
receita. Quatro dos sete componentes fecham ao centavo; a RCL fica a 0,0146%.

Módulo: `rcl_msc.py`. Teste: `tests/test_rcl_msc.py`.

### A não executada tem sinal

`crédito − débito` das contas `8.6.3.3.1`. Em janeiro/2025 dá **−252 milhões** —
o débito (folha de dezembro/2024 sendo executada) supera o crédito novo.

E o expurgo de 1.337.759,24 tem sinal dependente do mês: **subtrai** em dezembro
(está no crédito) e **soma** em abril (está no débito).

Módulo: `nao_executada.py`. Teste: `tests/test_nao_executada.py`.

---

## O que a equipe precisa entregar

| item | para quê |
|---|---|
| **extração por subação e fonte** | fecha 16 células do expurgo patronal |
| **saldo da conta 8.6.3.2.2 em 31/12/2025** | fecha 5 células do Anexo 2 |
| **MAPA/Comparativo de 2025** | fecha 4 células do Anexo 1 de 2025 |
| **template Siconfi dos anexos** | para preencher e publicar |

Detalhes em `docs/ENTRADAS_NECESSARIAS.md`.

---

## Armadilhas já pagas

| armadilha | onde | lição |
|---|---|---|
| nome não é chave | Anexo 4 ("Pensões" 2×), Anexo 3 (nomes truncados), Anexo 6 (par VALOR/%) | casar por prefixo e posição |
| total certo esconde erro | Anexo 1 rubricas | conferir a **parcela**, não só o total |
| tolerância de 0,5% | verificar_tudo | exigir o centavo |
| sinal do expurgo | linha 251 | depende de onde a parcela está no mês |
| percentual vs valor | Anexo 6 RGF | emparelhar o par antes de comparar |

---

## Documentos que importam

| arquivo | o que é |
|---|---|
| `docs/BATIMENTO.md` | a tabela do que bate, por anexo |
| `docs/DIVERGENCIAS.md` | as 26 divergências, **todas com causa** |
| `docs/PREENCHIMENTO.md` | 396 linhas prontas para preencher |
| `docs/ANEXO1_CRUZAMENTO.md` | MDF × etonjones × nosso código |
| `docs/ANEXO6_PONTE.md` | por que o Anexo 6 não fecha |
| `docs/REVISAO_GERAL.md` | o diário completo (seções 17.x) |

---

## Regras de trabalho deste projeto

1. **nunca forçar número para fechar** — divergência com causa vale mais que
   número arredondado;
2. **conferir contra o publicado**, não contra a planilha da equipe;
3. **toda divergência tem causa escrita**, com no mínimo 60 caracteres
   (há teste para isso);
4. **teste de ausência é teste válido** — documenta o limite e evita perseguir
   de novo o mesmo dado;
5. **quando a matriz não tem a dimensão, parar** e pedir a extração.
