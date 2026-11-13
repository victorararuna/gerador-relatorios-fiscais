# RREO Anexo 7 — Restos a Pagar

2025 B6. Reproduzir com `python rreo_anexo7.py`.

---

## 1. As contas

As linhas do demonstrativo são as contas de controle `6.3.1` e `6.3.2` da
matriz, com correspondência exata (não aproximada):

| linha do Anexo 7 | conta | valor |
|---|---|---:|
| RP processados pagos (c) | `632200000` | 1.009.808.236,48 |
| RP processados cancelados (d) | `632910000` | 49.997.069,58 |
| Saldo de RP processados (e) | `632100000` | 470.465.377,32 |
| RP não processados pagos (i) | `631400000` | 217.231.892,52 |
| RP não processados cancelados (j) | `631990000` | 188.293.949,99 |

## 2. Resultado

| linha | homologado | MSC | desvio |
|---|---:|---:|---:|
| RP processados pagos | 1.009.808.236,48 | 1.009.808.236,48 | **0,00** |
| RP processados cancelados | 49.997.069,58 | 49.997.069,58 | **0,00** |
| Saldo de RP processados | 470.465.377,32 | 470.465.377,32 | **0,00** |
| RP não processados pagos | 217.231.892,52 | 217.231.892,52 | **0,00** |
| RP não processados cancelados | 188.293.949,99 | 188.293.949,99 | **0,00** |

**5 de 5 linhas exatas.**

## 3. O que não é reproduzível

As colunas de abertura — "Em Exercícios Anteriores (a)" e "Em 31 de dezembro de
2024 (b)" — são saldos de 2024, e a matriz de 2024 não está no acervo.

O **total** delas, porém, é derivável da própria equação do anexo:

```
RP processados:  a + b = e + c + d = 470.465.377,32 + 1.009.808.236,48
                          + 49.997.069,58 = 1.530.270.683,38
               (homologado: 302.552.668,91 + 1.227.718.014,47 = 1.530.270.683,38)
```

Confere ao centavo — mas a **divisão** entre "exercícios anteriores" e "31 de
dezembro" exige o saldo de abertura, que só a matriz de 2024 fornece.

## 4. Por que isso importa

O Anexo 7 era um dos que a documentação de 2024 dava como inviável ("a matriz
não abre restos a pagar"). Não é: as contas `6.3.1`/`6.3.2` carregam exatamente
os movimentos e saldos que o demonstrativo pede.

É o segundo anexo do RREO a fechar por inteiro, junto com o Anexo 3.
