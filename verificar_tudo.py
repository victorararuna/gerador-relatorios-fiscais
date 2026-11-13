# -*- coding: utf-8 -*-
"""Verificação de ponta a ponta: roda todas as conferências e diz o que passa.

    python verificar_tudo.py

Sai com código 0 se todos os testes obrigatórios passarem.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import app.anexo1_msc as M  # noqa: E402
import app.anexo3_msc as A3  # noqa: E402
import app.anexo4_msc as A4  # noqa: E402
import app.anexo6_msc as A6  # noqa: E402
from app.relatorio_anexo1 import ler_oficiais, linhas_anexo1  # noqa: E402

MSC = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn_msc"
BASE = r"C:\Users\victo\AppData\Local\Programs\Microsoft VS Code\siconfi_rn"

resultados = []


def checar(nome: str, valor, esperado, tolerancia=0.005, obrigatorio=True):
    """tolerancia relativa; 0 significa exigir igualdade ao centavo."""
    ok = abs(valor - esperado) <= max(abs(esperado) * tolerancia, 0.01)
    resultados.append((nome, ok, valor, esperado, obrigatorio))
    return ok


def relatorio():
    print(f"{'verificação':<52}{'resultado':>10}{'apurado':>18}{'esperado':>18}")
    falhas = 0
    for nome, ok, valor, esperado, obrig in resultados:
        marca = "OK" if ok else ("FALHA" if obrig else "aviso")
        if not ok and obrig:
            falhas += 1
        print(f"{nome[:50]:<52}{marca:>10}{valor:>18,.2f}{esperado:>18,.2f}")
    print()
    print(f"{len(resultados) - falhas} de {len(resultados)} verificações passaram")
    return falhas


def main() -> int:
    # 1. motor: soma dos movimentos = saldo de dezembro
    acervo = M.Acervo(MSC)
    divergentes = acervo.conferir_fluxo_estoque(2025)
    criticas = [d for d in divergentes if not d[0].startswith(("6311", "6312", "6321"))]
    checar("motor: saldo x movimento (contas de resultado à parte)",
           float(len(criticas)), 0.0)

    # 2. RREO: total liquidado
    pares = M.periodos_janela(2025, 12)
    total = 0.0
    for mes in range(1, 13):
        for r in acervo.ler(2025, mes):
            if r.conta in M.CONTAS_LIQUIDACAO:
                total += r.liquido
    checar("RREO: total liquidado = Balanço Orçamentário",
           total, 23_361_499_529.63)

    # 3. RGF Anexo 1 — despesa bruta
    res = M.apurar_janela(acervo, 2025, 12)
    ded = M.deducoes(acervo, pares)
    ne = M.nao_executada(acervo, pares)
    v = {ln.chave: ln.valor for ln in linhas_anexo1(res, ded, ne)}
    oficial = ler_oficiais(os.path.join(BASE, r"RGF\2025\RGF_24_2025_quad3_anexo01.csv"))
    checar("RGF Anexo 1: despesa bruta (I)",
           v["I"], oficial["DESPESA BRUTA COM PESSOAL (I)"], 0.005)
    checar("RGF Anexo 1: despesa líquida (III)",
           v["III"], oficial["DESPESA LÍQUIDA COM PESSOAL (III) = (I - II)"], 0.01)

    # 4. Anexo 3 e limites
    rcl = A3.ler_rcl(os.path.join(BASE, r"RREO\2025\RREO_24_2025_bim6_anexo03.csv"))
    checar("RREO Anexo 3: RCL", rcl.rcl, 19_513_846_659.98)
    lim3 = A3.linhas_anexo3(rcl)
    checar("RGF Anexo 3: limite do Senado (22%)",
           lim3[3][1], 4_292_056_296.86, 0.0)
    lim4 = A4.limites(rcl)
    checar("RGF Anexo 4: limite geral (16%)",
           lim4["geral"], 3_121_495_488.63, 0.0)
    lim6 = A6.limites(rcl)
    checar("RGF Anexo 6: limite máximo (49%)",
           lim6["maximo"], 9_558_650_048.47, 0.0)

    # 5. RREO Anexo 2 — total por função
    import rreo_anexo2 as R2
    ms = R2.nosso_por_funcao()
    checar("RREO Anexo 2: soma das 23 funções",
           sum(ms.values()), 23_361_499_529.63)

    # 6. RREO Anexo 1 — grupos sem intra
    import rreo_anexo1_grupos as R1
    ofg, msg = R1.oficial(), R1.nosso()
    for pref, nome in (("32", "JUROS E ENCARGOS DA DÍVIDA"),
                       ("44", "INVESTIMENTOS"),
                       ("46", "AMORTIZAÇÃO DA DÍVIDA")):
        checar(f"RREO Anexo 1: grupo sem intra — {nome[:26]}",
               msg.get(pref, 0.0), ofg.get(nome, 0.0), 0.0)

    # 7. RREO Anexo 7 — restos a pagar
    import rreo_anexo7 as R7
    of7, ms7 = R7.oficial(), R7.matriz()
    for chave in R7.CONTAS:
        checar(f"RREO Anexo 7: {chave}",
               ms7.get(chave, 0.0), of7.get(chave, 0.0), 0.0)

    # 8. RREO Anexo 14 — linhas de despesa e RCL
    import rreo_anexo14 as R14
    of14, ms14 = R14.oficial(), R14.matriz()
    for chave in R14.LINHAS:
        checar(f"RREO Anexo 14: {chave}",
               ms14.get(chave, 0.0), of14.get(chave, 0.0), 0.0)

    # 9. RREO Anexo 9 — despesa de capital empenhada
    import rreo_anexo9 as R9
    of9, ms9 = R9.oficial(), R9.matriz()
    for chave in R9.LINHAS:
        checar(f"RREO Anexo 9: {chave}",
               ms9.get(chave, 0.0), of9.get(chave, 0.0), 0.0)

    falhas = relatorio()
    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
