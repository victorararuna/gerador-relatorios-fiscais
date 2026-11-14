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
    # linhas do DCL publicado (3o quadrimestre de 2025) que a aba Base tambem tem
    "Precatórios Posteriores a 05/05/2000 (inclusive) - Vencidos e não pagos":
        5_595_401_507.77,
    "PASSIVO ATUARIAL": 84_052_803_127.13,
    "DÍVIDA CONTRATUAL DE PPP": 215_455_288.93,
    # nao e linha do DCL publicado: as contas 2.1.8.1.1 e 2.2.8.1.1 entram em
    # "Outras Dividas" (941.926.197,62). Comparar contra zero seria comparar
    # contra a planilha da equipe, nao contra o homologado.
    "Demais Dívidas Contratuais": None,
    "Precatórios Posteriores a 05/05/2000 (inclusive) - Vencidos e não pago": 5_595_401_507.77,
    "Outras Dívidas": 941_926_197.62,
    "Disponibilidade de Caixa Bruta": 1_549_181_365.36,
    "(-) Restos a Pagar Processados (Exceto Precatórios)": 750_866_596.13,
    "(-) Depósitos Restituíves e Valores Vinculados": 798_314_769.23,
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


def _pai(conta: str) -> str | None:
    """Conta-pai de nível 7 (ex.: 2.1.2.1.1.02.01.00 -> 2.1.2.1.1.02.00.00).

    O critério da STN enumera os filhos terminais, mas o plano de contas do RN
    não tem todos eles (não existe o .02.98, e o ".02.02 - Contratos do
    Exercício" fica de fora da lista). Usar o pai captura o que o filho deixa
    escapar — em 31/12/2025 são R$ 32.878.296,36.
    """
    partes = conta.split(".")
    if len(partes) < 7:
        return None
    return ".".join(partes[:6] + ["00", "00"])


#: contas em que se usa o pai de nível 7 em vez do filho terminal: o critério da
#: STN enumera filhos que o plano de contas do RN não tem (o ".02.98"), e o
#: ".02.02 - Contratos do Exercício" fica de fora. Em 31/12/2025 são 32,9 mi.
USAR_PAI = ("2.1.2.1.1.02", "2.1.2.1.3.02")


def apurar_secao(saldo: dict, contas: list) -> float:
    total = 0.0
    usados = set()
    for c, s in contas:
        chave = c
        if c.startswith(USAR_PAI):
            pai = _pai(c)
            if pai and pai in saldo and pai not in usados:
                chave = pai
                usados.add(pai)
        v = _buscar(saldo, chave)
        if v is None:
            continue
        # classe 2 (passivo): credor é positivo
        total += s * (-v if chave.startswith("2") else v)
    return total


#: seções que NÃO saem do balancete consolidado: a linha do anexo tem escopo
#: próprio, e o cabeçalho da aba da equipe é que o define.
SECOES_MSC = {
    # "EXECUTIVO (SEM RPPS)": 73 contas-folha, só o PO 10111 na MSC
    "Demais Haveres Financeiros": ("D+ Haveres", 1, "10111"),
}

#: o bloco IPERN dos depósitos (contas .01.08 a .01.14 em FR 800/802) é
#: deduzido do total: a aba o soma em separado e o CONTAS subtrai (D253 = D42)
CONTAS_IPERN = ("2188101080", "2188101100", "2188101110", "2188101130",
                "2188101140", "2188101180", "2188101200", "2188101210",
                "2188101230", "2188101240", "2188101320", "2188101990",
                "2188102020", "2188104010", "2188104030", "2188104120",
                "2188199010", "2188199020", "2188199030", "2188199060",
                "2188301020", "2188301021", "2188501080")


#: contas da disponibilidade de caixa bruta (aba CONTAS, linhas 230 a 242)
CONTAS_DISPONIBILIDADE = (
    "111110100", "111110200", "111110600", "111111900", "111113000",
    "111115000", "111115100", "111115200", "111115300",
    "111210100", "111210200", "111210300", "111310000",
)
#: fontes do RPPS, excluídas da disponibilidade (a aba chama de "sem RPPS")
FONTES_RPPS = ("800", "801", "802")


def disponibilidade(ano: int = 2025, mes: int = 12) -> float:
    """Disponibilidade de caixa bruta: as 13 contas, sem as fontes do RPPS.

    A aba "CONTAS" (linha 243) faz `C - D`, com D vindo da aba "Disponibilidade"
    (B23). Conferido: as 13 contas somam 1.559.285.389,89; sem 800/801/802 dão
    **1.549.181.365,36**, exatamente o publicado.
    """
    import sys as _sys

    raiz = os.path.dirname(os.path.abspath(__file__))
    if os.path.join(raiz, "app") not in _sys.path:
        _sys.path.insert(0, os.path.join(raiz, "app"))
    from acervo import Acervo

    ac = Acervo(os.path.join(raiz, "dados", "acervo"))
    total = 0.0
    for r in ac.ler(ano, mes, classe=1, tipo_valor="ending_balance"):
        if not r.conta.startswith(CONTAS_DISPONIBILIDADE):
            continue
        if (r.fr or "")[1:4] in FONTES_RPPS:
            continue
        total -= r.liquido
    return total


def depositos(ano: int = 2025, mes: int = 12) -> float:
    """Depósitos restituíveis: as 8 contas, sem as fontes do RPPS.

    Conferido contra o DCL **publicado**: 798.314.769,23, exato. A planilha da
    equipe traz 797.121.848,11 — é ela que diverge, não a apuracao.
    """
    import sys as _sys

    raiz = os.path.dirname(os.path.abspath(__file__))
    if os.path.join(raiz, "app") not in _sys.path:
        _sys.path.insert(0, os.path.join(raiz, "app"))
    from acervo import Acervo

    pref = ("21881", "21883", "21884", "21885",
            "22881", "22883", "22884", "22885")
    ac = Acervo(os.path.join(raiz, "dados", "acervo"))
    total = 0.0
    for r in ac.ler(ano, mes, classe=2, tipo_valor="ending_balance"):
        if not r.conta.startswith(pref):
            continue
        if (r.fr or "")[1:4] in ("800", "802"):
            continue
        total += r.liquido
    return total


#: contas que a MSC agrega num sufixo diferente do que a aba lista
EQUIVALENTES = {"121310100": "121310199"}


def contas_da_aba(nome: str) -> list:
    """Prefixos de 6 dígitos das contas de uma aba da planilha da equipe.

    A aba lista contas de 8 segmentos. A MSC agrega **uma** delas no sufixo .99:
    a 1.2.1.3.1.01 aparece como 121310199 (R$ 40.722,00 em 2025). O mapa abaixo
    trata o caso sem abrir o prefixo para a família inteira — que capturaria
    contas fora da linha.
    """
    from openpyxl import load_workbook

    ws = load_workbook(PLANILHA, data_only=True)[nome]
    saida = set()
    for r in range(1, ws.max_row + 1):
        c = ws.cell(r, 1).value
        if isinstance(c, str) and c[:1].isdigit() and c.count(".") >= 6:
            chave = c.replace(".", "")[:9]
            saida.add(EQUIVALENTES.get(chave, chave))
    return sorted(saida)


def apurar_msc(aba: str, classe: int, po: str,
               ano: int = 2025, mes: int = 12) -> float:
    """Soma o saldo de uma aba na MSC, restrito a um Poder."""
    import sys as _sys

    raiz = os.path.dirname(os.path.abspath(__file__))
    if os.path.join(raiz, "app") not in _sys.path:
        _sys.path.insert(0, os.path.join(raiz, "app"))
    from acervo import Acervo

    contas = contas_da_aba(aba)
    ac = Acervo(os.path.join(raiz, "dados", "acervo"))
    total = 0.0
    for r in ac.ler(ano, mes, classe=classe, tipo_valor="ending_balance"):
        if r.po != po:
            continue
        if any(r.conta.startswith(p) for p in contas):
            total -= r.liquido
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
        if nome.startswith("Disponibilidade de Caixa Bruta"):
            v = disponibilidade()
        elif nome.startswith("(-) Depósitos"):
            v = depositos()
        elif nome in SECOES_MSC:
            aba, classe, po = SECOES_MSC[nome]
            v = apurar_msc(aba, classe, po)
        else:
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
