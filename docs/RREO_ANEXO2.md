# RREO Anexo 2 — despesa por função a partir da MSC

> **Documento histórico.** Escrito quando o trabalho era sobre o **RGF 2024**.
> Os números e as pendências abaixo **não valem mais**: o Anexo 1 passou a fechar
> em 10 de 10 meses, o Anexo 5 chegou a 90 de 90 células e o Anexo 4 fechou.
>
> **Para o estado atual, leia [`REVISAO_GERAL.md`](REVISAO_GERAL.md), seção 2** —
> ou, melhor, abra `saida/verificacao_anexos.xlsx`, que é gerado do código.

---


Reproduzir com `python rreo_anexo2_intra.py` (2025 B6).

---

## 1. O que o anexo pede

Despesa liquidada por função e subfunção, em três blocos: **exceto
intra-orçamentárias (I)**, **intra-orçamentárias (II)** e **total (III)**.

O Siconfi **não publica a intra por função**: no arquivo homologado, o bloco II
traz apenas o cabeçalho e o total (R$ 2.664.925.314,43), sem as 23 funções.

## 2. O que a MSC entrega

A matriz nova traz `funcao` (2 dígitos) e `subfuncao` (3) em cada linha. Somando
o movimento líquido das contas de liquidação por função:

| | |
|---|---:|
| 23 funções apuradas | 23.361.499.529,63 |
| Total do RREO Anexo 2 | 23.361.499.529,63 |
| **Diferença** | **0,00** |

## 3. O teste que valida o atributo

Subtraindo de cada função o valor "exceto intra" do homologado:

| função | exceto intra (oficial) | MSC total | intra derivada |
|---|---:|---:|---:|
| Previdência Social | 6.624.107.037,38 | 8.056.629.944,14 | 1.432.522.906,76 |
| Educação | 3.409.062.375,91 | 3.854.466.345,29 | 445.403.969,38 |
| Saúde | 2.894.724.058,53 | 3.158.350.287,98 | 263.626.229,45 |
| Judiciária | 1.402.106.685,33 | 1.563.159.798,51 | 161.053.113,18 |
| Segurança Pública | 1.888.102.012,41 | 1.983.489.698,87 | 95.387.686,46 |
| Essencial à Justiça | 538.476.929,62 | 599.655.158,04 | 61.178.228,42 |
| Administração | 641.021.958,87 | 697.182.773,21 | 56.160.814,34 |
| Direitos da Cidadania | 364.829.678,24 | 419.886.542,31 | 55.056.864,07 |
| Encargos Especiais | 1.262.997.664,51 | 1.308.571.903,27 | 45.574.238,76 |
| Legislativa | 640.322.364,39 | 660.360.268,93 | 20.037.904,54 |
| Transporte | 360.534.940,99 | 372.760.621,06 | 12.225.680,07 |
| (demais 12 funções) | — | — | 19.706.711,41 |
| **TOTAL** | **20.696.574.215,20** | **23.361.499.529,63** | **2.664.925.314,43** |

Duas conclusões:

1. **Nenhuma função tem delta negativo** — ou seja, em todas as 23 o total da
   matriz é maior ou igual ao "exceto intra" homologado, como tem de ser.
2. A soma dos deltas é **exatamente** a intra declarada no Anexo 1
   (R$ 2.664.925.314,43).

O perfil da intra derivada é coerente: **Previdência Social concentra 54%**
(R$ 1,43 bi) — é a transferência do Tesouro ao RPPS, a mesma dupla contagem que
persegue o Anexo 1 do RGF desde 2024.

## 4. Como usar

- Comparar linha a linha contra o homologado: usar a coluna **intra derivada**
  como critério declarado, não como dado oficial.
- A função é atributo confiável da matriz: o total fecha ao centavo e nenhum
  delta é negativo.
- O que continua sem verificação independente é a **distribuição** da intra entre
  funções — o Siconfi não a publica.
