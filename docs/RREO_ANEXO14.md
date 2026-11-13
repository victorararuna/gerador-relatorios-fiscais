# RREO Anexo 14 — Demonstrativo Simplificado

2025 B6. Reproduzir com `python rreo_anexo14.py`.

---

## 1. Resultado

| linha | homologado | MSC | desvio |
|---|---:|---:|---:|
| Despesas Empenhadas | 23.874.415.460,69 | 23.874.415.460,69 | **0,00** |
| Despesas Liquidadas | 23.361.499.529,63 | 23.361.499.529,63 | **0,00** |
| Despesas Pagas | 21.945.141.150,86 | 21.945.141.150,86 | **0,00** |
| Receita Corrente Líquida | 19.513.846.659,98 | 19.513.846.659,98 | **0,00** |
| RCL ajustada (endividamento) | 19.509.346.803,92 | 19.509.346.803,92 | **0,00** |
| RCL ajustada (pessoal) | 19.507.449.078,52 | 19.507.449.078,52 | **0,00** |

**6 de 6 linhas exatas.**

## 2. As contas

| linha | composição |
|---|---|
| Empenhadas | soma de **todas** as contas `62213*` (01 a 07) |
| Liquidadas | `622130300` + `622130400` + `622130700` |
| Pagas | `622130400` (liquidado pago) |
| RCL e ajustadas | RREO Anexo 3 |

Identidade que confirma o conjunto:

```
Liquidadas − RP inscritos no exercício (632700000) = Pagas
23.361.499.529,63 − 1.416.358.378,77 = 21.945.141.150,86
```

O `62213*` completo é o empenhado; o subconjunto 03/04/07 é o liquidado; o 04 é o
pago. Cada nível do demonstrativo é um recorte da mesma família de contas.

## 3. O que não fecha

- **Receitas Realizadas**: o simplificado traz 23.648.298.748,99; a matriz apura
  24.872.967.329,22 (diferença de R$ 1,22 bi, a mesma das deduções da receita).
- **Previdenciárias** e **Resultado Primário**: dependem do Anexo 4 e das
  deduções da receita.
