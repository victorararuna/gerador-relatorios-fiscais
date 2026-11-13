# Coleta pela API do Siconfi — o que o seu motor destravou

O `siconfi_brasil_completo.py` foi a chave. Eu vinha testando a API com
parâmetros incompletos e recebendo zero linhas.

---

## 1. O erro que eu cometia

Eu chamava:

```
/tt/rgf?an_exercicio=2024&nr_periodo=3&id_ente=24
```

A API responde **200 com `count: 0`** — sem erro, o que me fez concluir que não
havia dados.

O seu motor usa o conjunto completo:

```python
{
  "id_ente": 24,
  "an_exercicio": 2024,
  "nr_periodo": 3,
  "in_periodicidade": "Q",          # ← faltava
  "co_tipo_demonstrativo": "RGF",   # ← faltava
  "no_anexo": "RGF-Anexo 02",       # ← faltava
  "co_esfera": "E",                 # ← faltava
  "co_poder": "E"                   # ← faltava (eu passava em alguns testes)
}
```

Com esses oito parâmetros, o mesmo anexo devolve **123 linhas**.

---

## 2. O que foi adaptado

`app/coleta_siconfi.py` — do seu script, mantive:

- a **paginação manual** por `offset` (a API limita a 5000 por página e o link
  interno da Oracle aponta para um hostname que não resolve);
- a **retomada** (pula arquivo já baixado);
- o **manifesto** e a pausa entre requisições;
- o tratamento de `RuntimeError` para distinguir "sem dados" de erro.

Mudei:

| no seu | aqui |
|---|---|
| 27 estados + 27 capitais + 50 municípios | **só o RN** (ente 24), recorte do projeto |
| RGF Anexo 02, RREO 01 e 06 | **todos os anexos** do RGF (1-6) e do RREO (11) |
| 4 anos × 2 períodos | **período único** por execução |
| saída na pasta do script | `dados/siconfi/` |
| `requests` | `urllib` (sem dependência externa) |

---

## 3. O que a API entrega

Diagnóstico para o RN, 2025:

| anexo | linhas |
|---|---:|
| RGF-Anexo 01 — Pessoal | 235 |
| RGF-Anexo 02 — DCL | 120 |
| RGF-Anexo 03 — Garantias | 20 |
| RGF-Anexo 04 — Operações | 19 |
| RGF-Anexo 05 — Disponibilidade | 169 |
| RGF-Anexo 06 — Simplificado | 25 |
| RREO-Anexo 01 — Balanço | 530 |
| RREO-Anexo 02 — Função | 1.686 |
| RREO-Anexo 03 — **RCL** | 417 |
| RREO-Anexo 04 — Previdenciário | 134 |
| RREO-Anexo 06 — Resultado | 207 |
| RREO-Anexo 07 — Restos a Pagar | 155 |
| RREO-Anexo 09 — Operações | 21 |
| RREO-Anexo 11 — Alienação | 26 |
| RREO-Anexo 13 — PPP | 58 |
| RREO-Anexo 14 — Simplificado | 120 |

O **Anexo 10** devolve 0 — o nome do anexo na API deve ser diferente
(`RREO-Anexo 10 - RPPS`, talvez).

Formato: uma linha por (conta, coluna), com `rotulo`, `coluna`, `conta`,
`cod_conta` e `valor`. É a mesma estrutura do `.xls`, em formato longo — e
**com os rótulos**, que era o que faltava no arquivo consolidado.

---

## 4. A comparação real — 2025 Q3

Agora contra o **homologado**, não contra desvios de referência:

| linha | apurado | homologado | dif | % |
|---|---:|---:|---:|---:|
| Vencimentos | 6.914.271.022 | 6.552.405.215 | +361.865.807 | **+5,52%** |
| Obrigações Patronais | 2.411.358.188 | 2.405.400.639 | +5.957.549 | +0,25% |
| Aposentadorias | 4.882.968.816 | 5.281.577.892 | −398.609.076 | **−7,55%** |
| Pensões | 820.116.992 | 890.961.409 | −70.844.417 | **−7,95%** |
| Terceirização | 180.493.012 | 180.764.418 | −271.406 | −0,15% |
| **Não executada** | 168.849.452 | 167.511.693 | +1.337.759 | **+0,80%** |
| **DESPESA BRUTA** | **15.378.057.482** | **15.478.621.265** | −100.563.783 | **−0,65%** |
| Vinculados | 3.539.334.658 | 3.538.152.718 | +1.181.940 | **+0,03%** |
| Piso Enfermagem | 48.755.181 | 49.364.621 | −609.440 | −1,23% |

### O que fecha

- **Vinculados: +0,03%** — a regra FR 18xx **e** CO de benefício está certa.
- **Não executada: +0,80%** — o balancete confirma a regra (movimento, não saldo).
- **Patronais: +0,25%** e **Terceirização: −0,15%**.

### O que não fecha

**Vencimentos +5,52% e Aposentadorias −7,55%** — somam −36,7 milhões de resíduo,
mas individualmente erram R$ 362 mi para cima e R$ 399 mi para baixo. É
**reclassificação entre as duas linhas**, não falta de valor — o mesmo padrão que
a calibração de 2026 já apontava.

**Pensões −7,95%**: o homologado tem R$ 890,9 mi e a matriz apura R$ 820,1 mi.
A exclusão de `3.1.90.03.05` que fecha 2025 na outra fase **não** foi aplicada
aqui — vale testar se ela muda o resultado neste acervo.

---

## 5. O que já dá para fazer

Com o RREO Anexo 3 baixado, a **RCL de 2025** está disponível — e ela é a base
dos Anexos 3, 4 e 6 do RGF.

| bloco | antes | agora |
|---|---|---|
| Anexo 1 — valores homologados | ❌ | ✅ |
| Anexo 2 a 6 — valores homologados | ❌ | ✅ |
| RREO completo | ❌ | ✅ |
| RCL para os limites | ❌ | ✅ |
| Rótulos de todos os anexos | ❌ | ✅ |

**Todos os insumos que faltavam estão na pasta `dados/siconfi/`.**
