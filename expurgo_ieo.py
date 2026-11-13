# -*- coding: utf-8 -*-
"""Expurgo dos demais Poderes — leitura dos IEO das UGs 162233 e 162011.

O IEO é emitido por Subação / Fonte / Elemento. O expurgo do Anexo 1 soma, por
subação (que identifica o Poder), o **liquidado** de 31.90.01 (aposentadorias) e
31.90.03 (pensões) na fonte 0.8.00, mais a patronal.

Este módulo reconstrói a tabela pela geometria do PDF (y = linha, x = coluna).
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

BASE = r"C:\Users\victo\Downloads\Arquivos etonjones"

RE_SUBACAO = re.compile(r"^\d{6}$")
RE_FONTE = re.compile(r"^\d\.\d\.\d{2}\.\d{6}$")
RE_ELEMENTO = re.compile(r"^\d{2}\.\d{2}\.\d{2}$")
RE_NUMERO = re.compile(r"^-?\d{1,3}(?:\.\d{3})*,\d{2}$|^-?\d+,\d{2}$")


def _num(t: str) -> float:
    return float(t.replace(".", "").replace(",", "."))


def _linhas(pagina):
    """Agrupa os itens por y (linha), ordenados por x."""
    por_y = defaultdict(list)
    for it in pagina.itens:
        por_y[round(it.y, 0)].append(it)
    return [(y, sorted(por_y[y], key=lambda i: i.x)) for y in sorted(por_y)]


def _colunas(linhas):
    """x de cada rótulo do cabeçalho."""
    alvo = ("Empenhado", "Liquidado", "Pago", "Atualizado", "Disponível")
    cols = {}
    for y, itens in linhas:
        for it in itens:
            for nome in alvo:
                if it.texto.strip().startswith(nome) and nome not in cols:
                    cols[nome] = it.x
        if len(cols) == len(alvo):
            break
    return cols


def ler(caminho: str, meses: tuple = ("Setembro",)) -> dict:
    """subação -> {'aposentadorias': x, 'pensoes': y} (liquidado, fonte 0.8.00).

    A tabela do IEO quebra em várias linhas físicas: o código fica numa, os
    números na seguinte. O leitor caminha de cima para baixo mantendo o contexto
    (subação → fonte → elemento) e atribui os números ao contexto corrente.
    """
    import leitor_pdf as LP

    saida = defaultdict(lambda: {"aposentadorias": 0.0, "pensoes": 0.0})
    for pagina in LP.ler_pdf(caminho):
        linhas = _linhas(pagina)
        x_liq = None
        for y, itens in linhas:
            for it in itens:
                if it.texto.strip() == "Liquidado":
                    x_liq = it.x
                    break
            if x_liq is not None:
                break
        if x_liq is None:
            continue

        subacao = fonte = elemento = None
        for y, itens in linhas:
            textos = [i.texto.strip() for i in itens]
            primeiro = textos[0] if textos else ""
            # códigos podem vir colados ao nome ("218401 Pagamento de")
            m_sub = re.match(r"^(\d{6})\s", primeiro) or (RE_SUBACAO.match(primeiro) and primeiro)
            m_fon = re.match(r"^(\d\.\d\.\d{2}\.\d{6})\s", primeiro)
            m_ele = re.match(r"^(\d{2}\.\d{2}\.\d{2})\s", primeiro)
            if m_sub:
                subacao, fonte, elemento = (m_sub.group(1) if hasattr(m_sub, "group") else primeiro), None, None
            elif m_fon:
                fonte, elemento = m_fon.group(1), None
            elif m_ele:
                elemento = m_ele.group(1)

            numeros = [i for i in itens if RE_NUMERO.match(i.texto.strip())]
            if len(numeros) < 3 or elemento is None or subacao is None:
                continue
            if elemento not in ("31.90.01", "31.90.03"):
                continue
            if not (fonte or "").startswith("0.8.00"):
                continue
            escolhido = min(numeros, key=lambda i: abs(i.x - x_liq))
            chave = "aposentadorias" if elemento == "31.90.01" else "pensoes"
            saida[subacao][chave] += _num(escolhido.texto.strip())
    return dict(saida)


def main() -> int:
    mes = sys.argv[1] if len(sys.argv) > 1 else "Setembro"
    for ug in ("162233", "162011"):
        caminho = os.path.join(BASE, f"Imprimir Execução Orçamentária - IEO_{ug}_{mes}.pdf")
        if not os.path.exists(caminho):
            print(f"ausente: {os.path.basename(caminho)}")
            continue
        dados = ler(caminho, (mes,))
        print(f"\n=== UG {ug} — {mes}")
        if not dados:
            print("   nada encontrado")
            continue
        tot_a = tot_p = 0.0
        for sub in sorted(dados):
            v = dados[sub]
            tot_a += v["aposentadorias"]; tot_p += v["pensoes"]
            if v["aposentadorias"] or v["pensoes"]:
                print(f"   subação {sub}: aposentadorias={v['aposentadorias']:>15,.2f}"
                      f"  pensões={v['pensoes']:>14,.2f}")
        print(f"   TOTAL: aposentadorias={tot_a:>15,.2f}  pensões={tot_p:>14,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
