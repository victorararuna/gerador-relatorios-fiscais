# -*- coding: utf-8 -*-
"""RGF Anexo 2 (DCL) apurado no balancete, com a base de contas da equipe.

Duas descobertas guiam este módulo:

1. a aba "Anexo 2 - RGF BASE" lista as contas de cada linha do demonstrativo;
2. a aba CONTAS do arquivo de trabalho é um `VLOOKUP` no BALANCETE, coluna
   *Saldo Restante* — ou seja, o DCL nasce do balancete, não da MSC.

Sinal: passivo (classe 2) entra pelo **saldo credor positivo**. O balancete traz
"C" como negativo, então contas da classe 2 têm o sinal invertido; contas da
classe 1 entram como estão (a disponibilidade deduz).
"""
from __future__ import annotations

import os
import re
import sys
from collections import OrderedDict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))

BALANCETE = os.path.join(AQUI, "dados", "fontes", "13nov",
                         "balancete_2025_encerramento.xls")
PLANILHA = (r"C:\Users\victo\Downloads\RELATÓRIOS CONTAG\Demonstrativos Fiscais 2025"
            r"\RGF 2025\3º QUADRIMESTRE\PRONTOS\EXCEL"
            r"\RGF 2025_3Q_02 - DEMONSTRATIVO DA DÍVIDA CONSOLIDADA LÍQUIDA.xlsx")

RE_CONTA = re.compile(r"^\d(\.\d+)+$")

#: valores oficiais da aba Base (2025 Q3)
OFICIAL = {
    "Dívida Mobiliária": 0.0,
    "Empréstimos Internos": 849_909_956.58,
    "Empréstimos Externos": 1_532_683_584.76,
    "Reestruturação da Dívida de Estados e Municípios": 678_224_099.41,
    "De Tributos": 16_905_273.05,
    "De Contribuições Previdenciárias": 1_806_971.92,
    "De Demais Contribuições Sociais": 0.0,
    "Do FGTS": 0.0,
    "Com Instituição Não financeira": 124_734_143.25,
    "Demais Dívidas Contratuais": 0.0,
    "Precatórios Posteriores a 05/05/2000 (inclusive) - Vencidos e não pago": 5_595_401_507.77,
    "Outras Dívidas": 942_088_822.97,
    "Disponibilidade de Caixa Bruta": 1_549_181_365.36,
    "(-) Restos a Pagar Processados (Exceto Precatórios)": 752_059_517.25,
    "(-) Depósitos Restituíves e Valores Vinculados": 797_121_848.11,
    "Demais Haveres Financeiros": 269_314_515.89,
}


def _num(v) -> float:
    if v is None:
        return 0.0
    s = str(v).replace(".", "").replace(",", ".").strip()
    negativo = s.rstrip().endswith("C")
    s = s.rstrip("DC").strip()
    try:
        x = float(s)
    except ValueError:
        return 0.0
    return -x if negativo else x


def ler_balancete(caminho: str) -> dict:
    """conta (8 segmentos) -> saldo restante, com C negativo."""
    import leitor_xls as LX

    aba = list(LX.ler_xls(caminho).abas.values())[0]
    linhas = aba.linhas()
    saldo = {}
    for i in range(len(linhas) - 1):
        c = str(linhas[i][2]).strip() if len(linhas[i]) > 2 else ""
        m = re.match(r"^([\d.]+)\s+\S", c)
        if not m:
            continue
        valores = linhas[i + 1]
        if len(valores) > 23:
            saldo[m.group(1)] = _num(valores[23])
    return saldo


def ler_base(caminho: str) -> "OrderedDict[str, list]":
    from openpyxl import load_workbook

    ws = load_workbook(caminho, data_only=True)["Anexo 2 - RGF BASE"]
    secoes: "OrderedDict[str, list]" = OrderedDict()
    atual = "(início)"
    for r in range(1, ws.max_row + 1):
        a = ws.cell(r, 1).value
        if not isinstance(a, str):
            continue
        t = a.strip()
        sinal = 1
        if t.startswith("(-)"):
            t = t[3:].strip()
            sinal = -1
        if RE_CONTA.match(t):
            secoes.setdefault(atual, []).append((t, sinal))
        elif t:
            atual = a.strip()
            secoes.setdefault(atual, [])
    return secoes


def _buscar(saldo: dict, conta: str) -> float | None:
    for k in (conta, conta + ".00"):
        if k in saldo:
            return saldo[k]
    return None


def apurar_secao(saldo: dict, contas: list) -> float:
    total = 0.0
    for c, s in contas:
        v = _buscar(saldo, c)
        if v is None:
            continue
        # classe 2 (passivo): credor é positivo
        total += s * (-v if c.startswith("2") else v)
    return total


def main() -> int:
    saldo = ler_balancete(BALANCETE)
    secoes = ler_base(PLANILHA)
    print(f"contas no balancete: {len(saldo)}\n")
    print(f"{'seção':<52}{'nosso':>18}{'oficial':>18}{'dif':>8}")
    acertos = comparados = 0
    for nome, contas in secoes.items():
        if not contas:
            continue
        v = apurar_secao(saldo, contas)
        of = OFICIAL.get(nome)
        if of is None:
            continue
        comparados += 1
        ok = abs(v - of) < 0.01
        acertos += ok
        marca = "OK" if ok else f"{v - of:,.0f}"
        print(f"{nome[:50]:<52}{v:>18,.2f}{of:>18,.2f}{marca:>8}")
    print(f"\n{acertos} de {comparados} linhas exatas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
