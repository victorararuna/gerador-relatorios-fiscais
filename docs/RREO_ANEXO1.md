# RREO Anexo 1 — despesa por grupo de natureza (Balanço Orçamentário)

Reproduzir com `python rreo_anexo1_grupos.py` (2025 B6).

---

## 1. Resultado

| grupo | exceto intra (oficial) | MSC total | intra derivada |
|---|---:|---:|---:|
| Pessoal e Encargos Sociais | 14.997.034.125,53 | 17.614.509.402,60 | **2.617.475.277,07** |
| Juros e Encargos da Dívida | 216.392.395,30 | 216.392.395,30 | **0,00** |
| Outras Despesas Correntes | 4.525.287.425,81 | 4.572.737.463,17 | 47.450.037,36 |
| Investimentos | 605.189.839,80 | 605.189.839,80 | **0,00** |
| Inversões Financeiras | 70.490.441,54 | 70.490.441,54 | **0,00** |
| Amortização da Dívida | 282.179.987,22 | 282.179.987,22 | **0,00** |
| **TOTAL** | **20.696.574.215,20** | **23.361.499.529,63** | **2.664.925.314,43** |

## 2. O que isso prova

**Quatro dos seis grupos fecham exatamente**, com intra zero: juros, investimentos,
inversões e amortização. Nesses, o total da matriz é idêntico ao homologado — não
houve nem sobra nem falta.

**A intra está inteira em dois grupos**: Pessoal (R$ 2,617 bi) e Outras Despesas
Correntes (R$ 47,45 mi). A soma é exatamente a intra declarada no Anexo 1
(R$ 2.664.925.314,43).

**O perfil confirma a origem**: a intra de Pessoal é a transferência do Tesouro
ao RPPS. É a mesma dupla contagem que aparece no Anexo 2 do RREO, onde a função
Previdência Social concentra 54% da intra (R$ 1,43 bi) — o mesmo dinheiro visto
por dois cortes diferentes: por grupo de natureza (ND 3.1) e por função
(classificado onde o benefício é pago).

## 3. Como usar

- Para os quatro grupos sem intra, a apuração da matriz **é** o valor publicável.
- Para Pessoal e Outras Correntes, a coluna "exceto intra" do relatório deve ser
  `MSC − intra derivada`, com a intra marcada como derivada.
- O total (23.361.499.529,63) fecha ao centavo contra o RREO, sem derivação.

## 4. A cadeia da receita — agora fechada

A comparação por origem revela que **as deduções só incidem em duas linhas**:

| origem | Anexo 1 (líquido) | MSC | Anexo 3 (bruto) |
|---|---:|---:|---:|
| Impostos, taxas e contribuições | 8.475.661.432,56 | 9.037.157.236,60 | 12.637.482.532,38 |
| Contribuições | 1.120.584.186,33 | 1.362.488.461,26 | 1.120.584.186,33 |
| Receita patrimonial | 248.692.954,79 | 237.302.832,39 | 248.692.954,79 |
| Receita industrial | 1.928.430,90 | 4.847.000,00 | 1.928.430,90 |
| Receita de serviços | 105.984.363,38 | 46.772.033,34 | 105.984.363,38 |
| Transferências correntes | 10.123.473.145,67 | 10.389.528.872,70 | 11.870.126.957,94 |
| Outras receitas correntes | 671.005.776,58 | 536.279.822,07 | 671.005.776,58 |

Fora impostos e transferências, **Anexo 1 e Anexo 3 são idênticos ao centavo**.
Só essas duas linhas carregam dedução, e ela é exatamente:

```
Anexo 3 bruto ................ 26.656.696.864,94
(-) transferências constitucionais .. 2.733.005.621,51
(-) FUNDEB ......................... 3.175.469.290,58
= receitas correntes exceto intra .. 20.748.221.952,85   (Anexo 1)
```

E a RCL fecha a cadeia:

```
20.748.221.952,85
(-) contribuição do servidor ....... 1.110.322.676,50
(-) compensações entre regimes ....... 115.005.627,07
(-) rendimentos previdenciários ....... 9.046.989,30
= RCL .............................. 19.513.846.659,98
```

**Toda a receita do RREO está reconciliada.** O que resta é a matriz:

| dedução | oficial | abatida na MSC | faltando |
|---|---:|---:|---:|
| Impostos | 4.161.821.099,82 | 3.600.325.295,78 | 561.495.804,04 |
| Transferências | 1.746.653.812,27 | 1.480.598.085,24 | 266.055.727,03 |
| **Total** | **5.908.474.912,09** | **5.080.923.381,02** | **827.551.531,07** |

A matriz já abate **86% das deduções**; faltam R$ 827,6 mi (15,5%) para ela cair
exatamente na linha do Anexo 1. É esse resíduo — não um erro de mapeamento — que
produz o desvio de +6% que eu vinha atribuindo a base errada.

### 4.1 A receita não serve para análise mensal

A classe 5 da matriz é **controle orçamentário**, não fluxo de arrecadação. O
movimento mensal de todas as suas linhas vai de −R$ 78,0 bi em janeiro a −R$ 4,9
bi em setembro — ordens de grandeza incompatíveis com arrecadação. E a natureza
`11` (impostos) concentra **R$ 8,96 bi em janeiro** e R$ 78 mi em dezembro.

Consequência de método: da matriz, a receita só pode ser lida no **total anual**
(`ending_balance` de dezembro, que confere com a soma dos movimentos). Qualquer
análise mês a mês precisa vir do RREO, não da matriz.

## 5. Pendência da receita

Localizar onde a matriz registra os R$ 827,6 mi restantes de dedução. Candidatos:
parte do FUNDEB retida em conta própria, ou a transferência constitucional
registrada como VPD (classe 6) em vez de dedução da receita.
