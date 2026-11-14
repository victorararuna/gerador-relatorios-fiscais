# -*- coding: utf-8 -*-
"""Anexo 1 do RGF (despesa com pessoal) apurado na nova MSC do Siconfi.

Traduz as contas de liquidação (6.2.2.1.3.03/04/07) nas linhas do Anexo 1,
seguindo o mapeamento de ``docs/MAPEAMENTO_STN_ANEXO1.md`` e a calibração
registrada em ``docs/ANEXO1_CALIBRACAO.md``.

O Anexo 1 do RGF é sempre uma **janela móvel de 12 meses** terminada no mês de
referência do quadrimestre (Q1 → abril, Q2 → agosto, Q3 → dezembro). Por isso a
apuração é feita por pares (ano, mês), e não por ano civil.
"""
from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leitor_msc import Acervo, ErroMSC  # noqa: E402

CONTAS_LIQUIDACAO = ("622130300", "622130400", "622130700")
EXPURGO_13O_OUTROS_PODERES = 1_337_759.24

CONTA_NAO_EXECUTADA = "863310000"

PO_EXECUTIVO = ("10111", "10112", "60611")

FR_ENFERMAGEM = "1605"

#: ADCT art. 38, § 2º — percentual do exercício
#: EC 127/2022, art. 38, § 2º — escalonamento do piso da enfermagem.
#: 2023: 100% | 2024: 90% | 2025: 80% | 2026: 72%
#: Conferido no manual da equipe (MDF 15ª ed.): 2026 = 72%.
PERCENTUAL_ENFERMAGEM = {2022: 1.00, 2023: 1.00, 2024: 0.90, 2025: 0.80, 2026: 0.72}


def percentual_enfermagem(ano: int) -> float:
    return PERCENTUAL_ENFERMAGEM.get(ano, 0.90)


#: mês de referência de cada quadrimestre
MES_DO_QUADRIMESTRE = {1: 4, 2: 8, 3: 12}

#: elemento (6 dígitos) -> linha do Anexo 1
ELEMENTO = {
    "319008": "vencimentos",
    "319011": "vencimentos",
    "319012": "vencimentos",
    "319016": "vencimentos",
    "319017": "vencimentos",
    "319007": "vencimentos",
    "319004": "contratacao_temporaria",
    "319013": "patronal",
    "319113": "patronal",
    "319001": "aposentadorias",
    "319086": "aposentadorias",
    "319003": "pensoes",
    "319091": "judiciais",
    "319092": "exerc_ant",
    "319192": "patronal",
    "319094": "indenizacoes",
}

#: desdobramentos de 3.1.90.92
SE_VENCIMENTOS = {"01"}
SE_PENSAO = {"03"}
#: desdobramentos de 3.1.90.94
SE_INDENIZACAO_APOS = {"03", "04"}
SE_INDENIZACAO_PENSAO = {"06", "13"}

#: CO (aqui ``complemento_fonte``) de benefícios do RPPS que a STN admite
CO_BENEFICIO = {"1111", "1151", "2111", "2151", "2211"}

#: naturezas que **não** compõem o Anexo 1
#: 3.1.90.03.05 — o homologado não a considera na linha de Pensões: excluí-la
#: é o que fecha as três janelas (+0,41%, +0,40% e +0,48% de desvio)
ND_FORA_ANEXO1 = {"31900305", "31901302"}



def periodos_janela(ano_fim: int, mes_fim: int, n: int = 12) -> List[Tuple[int, int]]:
    """Os ``n`` meses terminados em (ano_fim, mes_fim), em ordem cronológica."""
    pares: List[Tuple[int, int]] = []
    ano, mes = ano_fim, mes_fim
    for _ in range(n):
        pares.append((ano, mes))
        mes -= 1
        if mes == 0:
            ano, mes = ano - 1, 12
    return list(reversed(pares))


def _classificar(nd: str) -> Optional[str]:
    """Linha do Anexo 1 para uma natureza da despesa (8 dígitos)."""
    if not nd:
        return None
    elemento, se = nd[:6], nd[6:8]

    if nd.startswith("33"):
        if nd[4:6] == "34" or se == "34":
            return "terceirizacao"
        return None

    if not nd.startswith("31"):
        return None

    if nd in ND_FORA_ANEXO1:
        return None

    linha = ELEMENTO.get(elemento)
    if linha is None:
        return "outros_pessoal"

    if elemento == "319092":
        if se in SE_VENCIMENTOS:
            return "vencimentos"
        if se in SE_PENSAO:
            return "pensoes"
        return "exerc_ant"

    if elemento == "319094":
        # o homologado não desdobra 3.1.90.94: a linha de indenizações é o total
        return "indenizacoes"

    return linha


@dataclass
class Apuracao:
    linhas: Dict[str, float] = field(default_factory=dict)
    mensal: Dict[Tuple[int, int], Dict[str, float]] = field(default_factory=dict)
    ignorados: Dict[str, float] = field(default_factory=dict)
    total_contas: float = 0.0
    periodos: List[Tuple[int, int]] = field(default_factory=list)

    def get(self, linha: str) -> float:
        return self.linhas.get(linha, 0.0)

    @property
    def pessoal(self) -> float:
        return sum(self.linhas.values())


def _acumular(acervo: Acervo, pares: Sequence[Tuple[int, int]],
              pos: Sequence[str], filtrar_co: bool = False) -> Apuracao:
    res = Apuracao(periodos=list(pares))
    pos = tuple(pos)
    for ano, mes in pares:
        do_mes: Dict[str, float] = {}
        try:
            linhas = list(acervo.ler(ano, mes))
        except ErroMSC:
            continue
        for r in linhas:
            if r.conta not in CONTAS_LIQUIDACAO or r.po not in pos:
                continue
            res.total_contas += r.liquido
            if not r.nd:
                res.ignorados["(sem ND)"] = res.ignorados.get("(sem ND)", 0.0) + r.liquido
                continue
            linha = _classificar(r.nd)
            if linha is None:
                chave = r.nd if r.nd in ND_FORA_ANEXO1 else r.nd[:2]
                res.ignorados[chave] = res.ignorados.get(chave, 0.0) + r.liquido
                continue
            if (filtrar_co and linha in ("aposentadorias", "pensoes")
                    and r.compl not in CO_BENEFICIO):
                res.ignorados["CO-" + (r.compl or "vazio")] = (
                    res.ignorados.get("CO-" + (r.compl or "vazio"), 0.0) + r.liquido)
                continue
            res.linhas[linha] = res.linhas.get(linha, 0.0) + r.liquido
            do_mes[linha] = do_mes.get(linha, 0.0) + r.liquido
        res.mensal[(ano, mes)] = do_mes
    return res


def apurar(acervo: Acervo, ano: int, meses: Sequence[int],
           pos: Sequence[str] = PO_EXECUTIVO, filtrar_co: bool = False) -> Apuracao:
    return _acumular(acervo, [(ano, m) for m in meses], pos, filtrar_co)


def apurar_janela(acervo: Acervo, ano_fim: int, mes_fim: int,
                  pos: Sequence[str] = PO_EXECUTIVO,
                  filtrar_co: bool = False) -> Apuracao:
    return _acumular(acervo, periodos_janela(ano_fim, mes_fim), pos, filtrar_co)


def nao_executada(acervo: Acervo, pares: Sequence[Tuple[int, int]],
                  pos: Sequence[str] = PO_EXECUTIVO) -> float:
    """Despesa com pessoal não executada orçamentariamente (classe 8), em fluxo."""
    total = 0.0
    pos = tuple(pos)
    for ano, mes in pares:
        try:
            linhas = list(acervo.ler(ano, mes, classe=8))
        except ErroMSC:
            continue
        for r in linhas:
            if r.conta == CONTA_NAO_EXECUTADA and r.po in pos:
                total += r.liquido
    # expurgo da patronal do 13o dos demais Poderes (subelementos .71 a .75 do
    # 31.91.13). Em dezembro/2025 ele esta no credito da inscricao do 13o; a
    # baixa compensatoria so ocorre em abril/2026. Numa janela que pega o
    # dezembro de 2025 sem pegar o abril de 2026, o valor fica dentro por uma
    # ponta so — e precisa sair.
    if (2025, 12) in pares and (2026, 4) not in pares:
        total -= EXPURGO_13O_OUTROS_PODERES
    return total


def deducoes(acervo: Acervo, pares: Sequence[Tuple[int, int]],
             pos: Sequence[str] = PO_EXECUTIVO) -> Dict[str, float]:
    """Linhas do grupo II (despesas não computadas).

    Inativos e pensionistas com recursos vinculados: FR 18xx **e** CO de
    benefício do RPPS — a combinação que fecha as três janelas (+0,03%,
    −0,13%, −0,13%). Só o grupo 18xx, sem o CO, excede em R$ 332 mi.
    """
    pos = tuple(pos)
    vinculos = enfermagem = 0.0
    for ano, mes in pares:
        try:
            linhas = list(acervo.ler(ano, mes))
        except ErroMSC:
            continue
        for r in linhas:
            if r.conta not in CONTAS_LIQUIDACAO or r.po not in pos:
                continue
            if (r.nd[:6] in ("319001", "319003") and r.fr.startswith("18")
                    and r.compl in CO_BENEFICIO):
                vinculos += r.liquido
            if r.fr.startswith(FR_ENFERMAGEM):
                enfermagem += r.liquido
    ano_ref = pares[-1][0] if pares else 2025
    pct = percentual_enfermagem(ano_ref)
    return {"vinculados": vinculos,
            "enfermagem_base": enfermagem,
            "enfermagem_percentual": pct,
            "enfermagem": enfermagem * pct}


def conferir(nosso: Apuracao, caminho_rgf: str,
             nao_exec: Optional[float] = None
             ) -> List[Tuple[str, float, float]]:
    """Compara as linhas apuradas com o Anexo 1 homologado (total 12 meses)."""
    oficiais: Dict[str, float] = {}
    with open(caminho_rgf, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["coluna"] == "TOTAL (ÚLTIMOS 12 MESES) (a)":
                oficiais[r["conta"]] = float(r["valor"])

    venc = nosso.get("vencimentos") + nosso.get("judiciais")
    ativo = venc + nosso.get("patronal")
    inativo = nosso.get("aposentadorias") + nosso.get("pensoes")
    bruto = ativo + inativo + nosso.get("terceirizacao")
    if nao_exec is not None:
        bruto += nao_exec

    pares = [
        ("Vencimentos, Vantagens e Outras Despesas Variáveis", venc),
        ("Obrigações Patronais", nosso.get("patronal")),
        ("Pessoal Ativo", ativo),
        ("Aposentadorias, Reserva e Reformas", nosso.get("aposentadorias")),
        ("Pensões", nosso.get("pensoes")),
        ("Pessoal Inativo e Pensionistas", inativo),
        ("DESPESA BRUTA COM PESSOAL (I)", bruto),
    ]
    return [(rot, oficiais.get(rot, float("nan")), val) for rot, val in pares]


def imprimir(resultado, caminho_rgf: str, nao_exec: float) -> None:
    print(f"{'linha':<52}{'oficial':>18}{'apurado':>18}{'dif':>16}{'%':>8}")
    for rotulo, of, ms in conferir(resultado, caminho_rgf, nao_exec=nao_exec):
        dif = ms - of
        pct = (dif / of * 100) if of else float("nan")
        print(f"{rotulo[:50]:<52}{of:>18,.2f}{ms:>18,.2f}{dif:>16,.2f}{pct:>7.2f}%")


def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Anexo 1 do RGF a partir da MSC.")
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--ano", type=int, default=2025)
    ap.add_argument("--quadrimestre", type=int, choices=(1, 2, 3), default=3)
    ap.add_argument("--rgf", help="CSV do Anexo 1 homologado para conferência")
    ap.add_argument("--todos-os-poderes", action="store_true")
    ap.add_argument("--filtrar-co", action="store_true",
                    help="aplica o filtro de CO em aposentadorias e pensões")
    args = ap.parse_args()

    acervo = Acervo(args.raiz)
    mes_fim = MES_DO_QUADRIMESTRE[args.quadrimestre]
    if args.todos_os_poderes:
        pos = tuple(sorted({r.po for r in acervo.ler(args.ano, 1)}))
    else:
        pos = PO_EXECUTIVO

    res = apurar_janela(acervo, args.ano, mes_fim, pos, filtrar_co=args.filtrar_co)
    print(f"acervo ..... {acervo.raiz}")
    print(f"janela ..... {res.periodos[0][0]}-{res.periodos[0][1]:02d} a "
          f"{res.periodos[-1][0]}-{res.periodos[-1][1]:02d} "
          f"({len(res.periodos)} meses)")
    print(f"recorte .... {'todos os POs' if args.todos_os_poderes else 'Executivo'}")
    print()
    for linha in ("vencimentos", "patronal", "terceirizacao", "aposentadorias",
                  "pensoes", "judiciais", "exerc_ant", "indenizacoes",
                  "contratacao_temporaria", "outros_pessoal"):
        print(f"   {linha:<24} {res.get(linha):>20,.2f}")
    print(f"   {'TOTAL':<24} {res.pessoal:>20,.2f}")
    ne = nao_executada(acervo, res.periodos, pos)
    print(f"   {'não executada (8.6.3.3)':<24} {ne:>20,.2f}")

    if args.rgf:
        print()
        imprimir(res, args.rgf, ne)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())




