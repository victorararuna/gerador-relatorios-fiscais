# -*- coding: utf-8 -*-
"""Gera docs/CERTIFICADO.md com o estado verificado (rodada 111).

Um certificado de conferencia precisa dizer: o que foi conferido, contra qual
arquivo, em que data e em que versao do codigo. Sem isso, o numero nao e
rastreavel.
"""
from __future__ import annotations

import datetime
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "app"))


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", "-C", RAIZ, *args], capture_output=True,
                              text=True, timeout=15).stdout.strip()
    except Exception:
        return ""


def main() -> int:
    import verificacao as V

    grupos = V._grupos()
    total = sum(len(l) for l in grupos.values())
    exatas = sum(1 for l in grupos.values() for x in l if x["ok"])
    divergentes = [(nome, x) for nome, l in grupos.items() for x in l if not x["ok"]]

    # conta os testes de verdade, em vez de fixar o numero
    pasta_tests = os.path.join(RAIZ, "tests")
    arquivos = sorted(x for x in os.listdir(pasta_tests) if x.startswith("test_"))
    n_arquivos = len(arquivos)
    n_testes = 0
    for nome in arquivos:
        with open(os.path.join(pasta_tests, nome), encoding="utf-8") as fh:
            n_testes += fh.read().count("def test_")

    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    commit = _git("rev-parse", "--short", "HEAD") or "(sem git)"
    assunto = _git("log", "-1", "--format=%s") or ""
    branch = _git("rev-parse", "--abbrev-ref", "HEAD") or ""

    linhas = [
        "# Certificado de verificação",
        "",
        f"Emitido em **{agora}** a partir do código no commit `{commit}`"
        f" (branch `{branch}`).",
        "",
        f"Último commit: *{assunto}*",
        "",
        "---",
        "",
        "## 1. Resultado",
        "",
        f"**{exatas} de {total} células exatas** "
        f"({100 * exatas / total:.1f}%), em {len(grupos)} grupos de verificação.",
        "",
        "Cada célula compara um valor **apurado pelo motor** com o valor do "
        "**arquivo publicado pelo Siconfi** — não com a planilha de trabalho da "
        "equipe.",
        "",
        "## 2. Abas do livro",
        "",
        "| aba | células | exatas |",
        "|---|---:|---:|",
    ]
    for nome, itens in grupos.items():
        ok = sum(1 for x in itens if x["ok"])
        linhas.append(f"| {nome} | {len(itens)} | {ok} |")

    linhas += ["", "## 3. Divergências", ""]
    if divergentes:
        linhas += ["| grupo | item | apurado | referência | desvio |",
                   "|---|---|---:|---:|---:|"]
        for nome, x in divergentes:
            linhas.append(
                f"| {nome} | {x['item'][:44]} | {x['apurado']:,.2f} | "
                f"{x['referencia']:,.2f} | {x['desvio']:,.2f} |")
        linhas += ["", "As causas estão em `docs/DIVERGENCIAS.md` e na coluna "
                       "de observação da própria planilha."]
    else:
        linhas.append("Nenhuma.")

    linhas += [
        "",
        "## 4. O que sustenta o número",
        "",
        "| trava | o que impede |",
        "|---|---|",
        "| `verificar_anos.py` | somar extração de outro exercício |",
        "| `test_layout_stn.py` | publicar a RCL de 2024 como 2026 |",
        "| `test_baseline.py` | usar um valor esperado diferente do publicado |",
        "| `test_rgf_anexo2.py` | linha fechada voltar a abrir |",
        "| `test_coerencia.py` | README, planilha e .md discordarem |",
        "| `test_verificacao.py` | divergência ficar sem causa escrita |",
        "",
        f"Suíte: **{n_testes} testes definidos em {n_arquivos} arquivos**. "
        "Rode `python rodar_testes.py` para ver quantos executam e quantos pulam.",
        "",
        "---",
        "",
        "## 5. Ressalvas",
        "",
    ]
    # as ressalvas saem do estado, nao de uma lista escrita a mao
    if divergentes:
        for nome, x in divergentes:
            percentual = (100 * x["desvio"] / x["referencia"]) if x["referencia"] else 0.0
            linhas.append(
                f"- **{nome} — {x['item'][:48]}**: {x['desvio']:,.2f} de desvio "
                f"({percentual:+.2f}%). {V._causa(x['item'])}")
    else:
        linhas.append("- Nenhuma divergência.")
    linhas += [
        "- **RCL**: é lida do Anexo 3, não apurada — o bloco de deduções do "
        "RPPS não existe na matriz.",
        "",
        "---",
        "",
        "*Este certificado é gerado por `certificado.py`. O número que vale é o "
        "do livro `saida/verificacao_anexos.xlsx`; se este texto divergir dele, "
        "o livro está certo.*",
        "",
    ]

    destino = os.path.join(RAIZ, "docs", "CERTIFICADO.md")
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))
    print(f"ok: {exatas} de {total} em {len(grupos)} grupos -> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
