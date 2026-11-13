# Leitor da nova MSC (formato longo)

A partir de 2025 o Siconfi não entrega mais o `instancia.csv`. A matriz vem
quebrada em **um arquivo por classe, por mês e por tipo de saldo**:

```
<ano>/MSC_24_<ano>_m<mm>_<MSCC|MSCE>_msc_<grupo>_classe<n>_<ending_balance|period_change>.csv
```

`app/leitor_msc.py` indexa e lê esse acervo.

---

## 1. Duas regras que os números obrigam

### 1.1 `ending_balance` × `period_change`

| arquivo | o que é |
|---|---|
| `ending_balance` | saldo de fechamento do mês |
| `period_change` | movimento do mês (é onde aparecem os **débitos**) |

Nas contas de liquidação (6.2.2.1.3.03/04/07) o `ending_balance` traz **apenas
natureza C**. Os débitos — estornos e baixas por pagamento — só existem no
`period_change`. Logo:

* despesa **bruta** (só créditos) pode sair do saldo;
* despesa **líquida** (créditos − débitos) **só** sai do movimento.

### 1.2 O saldo de dezembro é o movimento do exercício

Conferido no RN/2025: a soma dos 12 `period_change` mensais é **idêntica** ao
`ending_balance` de dezembro, ao centavo (R$ 23.361.499.529,63 nas classes 6).

Exceção: as contas de resultado `6.3.1.1`, `6.3.1.2` e `6.3.2.1`, que são
encerradas contra o patrimônio no fim do exercício e por isso não amarram.

A conta `622130300` **desaparece do saldo de dezembro** (zera no ano) e só
aparece no `period_change` — não é erro de exportação.

---

## 2. Uso

```python
from leitor_msc import Acervo

acervo = Acervo(r"C:\...\siconfi_rn_msc")
acervo.anos                      # [2025, 2026]
acervo.meses(2025)               # [1..12] (saldos)

# despesa liquidada do Executivo no ano
total = acervo.total(
    2025, acervo.meses(2025, tipo_valor="period_change"),
    contas=("622130300", "622130400", "622130700"),
    filtro=lambda r: r.po in ("10111", "10112", "60611"),
)

# por Poder
por_po = acervo.agregar(2025, [12], contas=("62213",), chave=("po",))
```

`contas` casa por **prefixo**; `chave` aceita `po`, `nd`, `elemento`, `conta`,
`fr`, `compl`, `funcao`, `receita`, `inscricao`, `mes`; `bruto=True` soma valor
absoluto em vez do líquido.

### Conferência de amarração

```python
acervo.conferir_fluxo_estoque(2025)   # [] = tudo amarrado
```

CLI:

```
python app/leitor_msc.py --raiz "C:\...\siconfi_rn_msc" --ano 2025 --classe 6
```

---

## 3. Esquema tolerante

Os cabeçalhos variam por classe:

| classe | colunas próprias |
|---|---|
| 1, 2, 3, 4 | `financeiro_permanente`, `divida_consolidada`; **sem** `natureza_despesa`, `funcao`, `natureza_receita` |
| 5, 6, 7 | `natureza_despesa`, `natureza_receita`, `funcao`, `ano_inscricao` |
| 8 | sem `natureza_receita` |

O leitor usa `DictReader` e devolve `""` para coluna ausente — nenhum de-para
posicional, como no formato antigo.

---

## 4. Testes

```
python tests/test_leitor_msc.py          # 14 testes, sem dependência externa
python verificar_anexo1.py               # integração contra o acervo real
```

O segundo reproduz a apuração de pessoal de 2025 e compara com o RGF Q3
homologado — serve de regressão quando o de-para do Anexo 1 for recalibrado.
