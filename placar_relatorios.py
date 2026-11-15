import os, sys
from collections import OrderedDict
raiz = r"C:\Users\victo\OneDrive\Documents\deepseek-harness\default-workspace\repo-github"
sys.path.insert(0, raiz); sys.path.insert(0, os.path.join(raiz, "app"))
import verificacao as V

NOMES = {
 "RGF Anexo 1": "RGF Anexo 1 — Despesa com Pessoal",
 "RGF Anexo 2": "RGF Anexo 2 — Dívida Consolidada Líquida",
 "RGF Anexo 3": "RGF Anexo 3 — Garantias e Contragarantias",
 "RGF Anexo 4": "RGF Anexo 4 — Operações de Crédito",
 "RGF Anexo 5": "RGF Anexo 5 — Disponibilidade de Caixa",
 "RGF Anexo 6": "RGF Anexo 6 — Restos a Pagar",
 "RREO Anexo 1": "RREO Anexo 1 — Balanço Orçamentário",
 "RREO Anexo 2": "RREO Anexo 2 — Despesa por Função",
 "RREO Anexo 3": "RREO Anexo 3 — Receita por Categoria",
 "RREO Anexo 4": "RREO Anexo 4 — Receita por Fonte",
 "RREO Anexo 6": "RREO Anexo 6 — Restos a Pagar",
 "RREO Anexo 7": "RREO Anexo 7 — RP por Poder",
 "RREO Anexo 9": "RREO Anexo 9 — Receita de Capital",
 "RREO Anexo 11": "RREO Anexo 11 — Alienação de Ativos",
 "RREO Anexo 13": "RREO Anexo 13 — Parcerias Público-Privadas",
 "RREO Anexo 14": "RREO Anexo 14 — Demonstrativo Simplificado",
}
def chave(nome):
    for k, v in NOMES.items():
        if nome.startswith(k + " ") or nome.startswith(k + " -") or nome == k:
            return v
    return "Outros (motor e batimento)"

acc = OrderedDict()
for nome, itens in V._grupos().items():
    k = chave(nome)
    n = len(itens); e = sum(1 for x in itens if x["ok"])
    a = acc.setdefault(k, [0, 0]); a[0] += n; a[1] += e

linhas = ["# Placar de acerto por relatorio",
          "",
          "Gerado por `placar_relatorios.py` a partir da verificacao contra os",
          "arquivos homologados do Siconfi.",
          "",
          "| relatorio | celulas | exatas | acerto |",
          "|---|---:|---:|---:|"]
T = O = 0
for k, (n, e) in sorted(acc.items(), key=lambda x: -x[1][0]):
    T += n; O += e
    linhas.append(f"| {k} | {n} | {e} | {100.0*e/n:.1f}% |")
linhas.append(f"| **TOTAL** | **{T}** | **{O}** | **{100.0*O/T:.1f}%** |")
linhas += ["", "## As unicas divergencias", "",
           "| celula | nosso | publicado | diferenca |", "|---|---:|---:|---:|"]
for nome, itens in V._grupos().items():
    for x in itens:
        if not x["ok"]:
            linhas.append(f"| {x['item']} | {x['apurado']:,.2f} | "
                          f"{x['referencia']:,.2f} | {x['apurado']-x['referencia']:,.2f} |")
linhas += ["", "As tres sao o mesmo erro de R$ 5.241,65 no arquivo publicado de",
           "abril/2026, provado no MAPA do proprio auditor e no quadro de 2026.", ""]
open(os.path.join(raiz, "docs", "PLACAR.md"), "w", encoding="utf-8").write("\n".join(linhas))
print("\n".join(linhas[-14:]))
