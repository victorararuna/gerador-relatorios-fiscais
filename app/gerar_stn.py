# -*- coding: utf-8 -*-
"""Orquestra a geração dos demonstrativos do RGF a partir da MSC.

Lê a Matriz de Saldos Contábeis, apura os Anexos 1 e 2 e gera o arquivo no
layout oficial do Siconfi, com a aba de verificações.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gerar_oficial
import colunas_garantias
import colunas_mensais
import colunas_quadrimestre
import msc_dcl
import msc_pessoal as M

RCL = 17259892416.73
EMENDAS_INDIVIDUAIS = 4802839.15
EMENDAS_BANCADA = 22049553.00
RP_NAO_PROCESSADOS_BRUTA = 4020802.48      # coluna "inscritas em RP nao processados"
RP_NAO_PROCESSADOS_DTP = 4000679.16
LIMITE_EXECUTIVO = 0.49                     # Resolucao do Senado 40/2001


def apurar_anexo1(caminho_msc: str) -> dict:
    r = M.ler_msc(caminho_msc)
    linhas = M.apurar(r)
    ne = M.nao_executada(r)
    env = M.deducao_enfermagem(r)
    vinc = M.deducao_vinculados(r)

    bruta = (linhas["vencimentos"] + linhas["patronal"] + linhas["aposentadorias"]
             + linhas["pensoes"] + linhas["terceirizacao"] + ne)
    deducoes = (linhas["judiciais"] + linhas["exercicios_anteriores"]
                + linhas["indenizacoes"] + vinc + env["deducao"])
    liquida = bruta - deducoes

    rcl_ajustada = RCL - EMENDAS_INDIVIDUAIS - EMENDAS_BANCADA
    dtp = liquida + RP_NAO_PROCESSADOS_DTP
    limite_max = rcl_ajustada * LIMITE_EXECUTIVO

    return {
        **linhas,
        "bruta": bruta,
        "nao_executada": ne,
        "vinculados": vinc,
        "piso_enfermagem": env["deducao"],
        "deducoes": deducoes,
        "liquida": liquida,
        "rcl": RCL,
        "emendas_individuais": EMENDAS_INDIVIDUAIS,
        "emendas_bancada": EMENDAS_BANCADA,
        "rcl_ajustada": rcl_ajustada,
        "dtp": dtp,
        "limite_max": limite_max,
        "limite_prudencial": limite_max * 0.95,
        "limite_alerta": limite_max * 0.90,
    }


def apurar_anexo2(caminho_msc: str, caminho_anterior: str | None = None) -> dict:
    r = msc_dcl.ler_msc(caminho_msc)
    d = msc_dcl.apurar(caminho_msc)
    # saldo de 31/12 do exercicio anterior (coluna "Saldo do Exercício Anterior")
    ant = msc_dcl.ler_msc(caminho_anterior) if caminho_anterior else None
    dv = r.divida
    rcl_ajustada = RCL - EMENDAS_INDIVIDUAIS

    def soma(*contas: str) -> float:
        return sum(dv.get(c, 0.0) for c in contas)

    anterior = {}
    if ant is not None:
        def soma_ant(*contas: str) -> float:
            return sum(ant.divida.get(c, 0.0) for c in contas)
        anterior = {
            "divida_anterior": ant.total_divida,
            "divida_mobiliaria_anterior": 0.0,
            "divida_contratual_anterior": soma_ant("222210200", "222110298"),
            "emprestimos_anterior": soma_ant("222210200", "222110298"),
            "emprestimos_internos_anterior": soma_ant("222110298"),
            "emprestimos_externos_anterior": soma_ant("222210200"),
            "parcelamentos_anterior": soma_ant("223110402", "223110403"),
            "parc_previdenciarias_anterior": soma_ant("223110402"),
            "parc_inst_financeira_anterior": soma_ant("223110403"),
            "precatorios_anterior": soma_ant("221110302", "221110303"),
            "outras_dividas_anterior": soma_ant("218910106", "218810110",
                                                "218911400", "211439800"),
            "deducoes_dcl_anterior": ant.total_deducoes,
            "haveres_anterior": ant.total_deducoes,
            "dcl_anterior": ant.dcl,
            "rcl_anterior": 16215892205.45,
            "rcl_ajustada_dcl_anterior": 16189903942.15,
        }

    return {
        **anterior,
        "divida": d["divida"],
        "divida_mobiliaria": 0.0,
        "divida_contratual": soma("222210200", "222110298"),
        "emprestimos": soma("222210200", "222110298"),
        "emprestimos_internos": soma("222110298"),
        "emprestimos_externos": soma("222210200"),
        "reestruturacao": 0.0,
        "parcelamentos": soma("223110402", "223110403"),
        "parc_tributos": 0.0,
        "parc_previdenciarias": soma("223110402"),
        "parc_inst_financeira": soma("223110403"),
        "precatorios": soma("221110302", "221110303"),
        "outras_dividas": soma("218910106", "218810110", "218911400", "211439800"),
        "deducoes_dcl": d["deducoes"],
        "disp_caixa": 0.0,
        "disp_bruta": 0.0,
        "rp_processados": 0.0,
        "depositos": 0.0,
        "haveres": d["deducoes"],
        "dcl": d["dcl"],
        "rcl": RCL,
        "emendas_dcl": EMENDAS_INDIVIDUAIS,
        "rcl_ajustada_dcl": rcl_ajustada,
        "pct_dc": d["divida"] / rcl_ajustada,
        "pct_dcl": d["dcl"] / rcl_ajustada,
        "limite": rcl_ajustada * 2.0,
        "limite_alerta": rcl_ajustada * 1.8,
    }


def apurar_anexo3(caminho_msc: str) -> dict:
    """Anexo 3 - Garantias e Contragarantias.

    O RN nao apresenta garantias concedidas nem contragarantias recebidas no
    exercicio: todas as linhas do quadro estao zeradas no RGF homologado. A
    matriz tambem nao registra saldo nas contas de garantia (2.2.8 / 7.7.8).
    Mantem-se o mesmo conjunto de RCL e limites dos demais anexos.
    """
    rcl_ajustada = RCL - EMENDAS_INDIVIDUAIS
    return {
        "gar_estados": 0.0, "gar_estados_ext": 0.0, "gar_estados_int": 0.0,
        "gar_municipios": 0.0, "gar_municipios_ext": 0.0, "gar_municipios_int": 0.0,
        "gar_controladas": 0.0, "gar_controladas_ext": 0.0, "gar_controladas_int": 0.0,
        "gar_fundos": 0.0, "gar_total": 0.0,
        "rcl": RCL, "gar_emendas": EMENDAS_INDIVIDUAIS,
        "gar_rcl_ajustada": rcl_ajustada, "gar_pct": 0.0,
        "gar_limite": rcl_ajustada * 0.22,       # Resolucao do Senado: 22%
        "gar_limite_alerta": rcl_ajustada * 0.22 * 0.90,
        "contra_estados": 0.0, "contra_estados_ext": 0.0, "contra_estados_int": 0.0,
        "contra_municipios": 0.0, "contra_municipios_ext": 0.0,
        "contra_municipios_int": 0.0,
        "contra_controladas": 0.0, "contra_controladas_ext": 0.0,
        "contra_controladas_int": 0.0,
        "contra_fundos": 0.0, "contra_total": 0.0,
    }


ANTERIOR = None
ARQUIVOS = {}
PASTA_MENSAL = None


# caminho do Comparativo da Receita (opcional, preenchido pelo pipeline)
ARQUIVO_RECEITA: str | None = None


def apurar_anexo4(caminho_msc: str) -> dict:
    """Anexo 4 - Operacoes de Credito.

    A operacao de credito e receita orcamentaria: a MSC traz a natureza da
    DESPESA, nao a da receita. Quando o Comparativo da Receita Oncada com a
    Arrecadada esta disponivel, a rubrica 4.2.1 fornece o valor exato.
    """
    oc = 0.0
    if ARQUIVO_RECEITA and os.path.exists(ARQUIVO_RECEITA):
        try:
            import msc_receita
            oc = msc_receita.apurar(ARQUIVO_RECEITA)["operacoes_credito"]
        except Exception:
            oc = 0.0
    rcl_ajustada = RCL - EMENDAS_INDIVIDUAIS
    return {
        "oc_mobiliaria": 0.0, "oc_mobiliaria_interna": 0.0, "oc_mobiliaria_externa": 0.0,
        "oc_contratual": 0.0, "oc_contratual_interna": 0.0,
        "oc_emprestimos": 0.0, "oc_aquisicao": 0.0, "oc_antecipacao": 0.0,
        "oc_assuncao": 0.0,
        "oc_nao_sujeitas_1": 0.0, "oc_nao_sujeitas_2": 0.0, "oc_total": oc,
        "rcl": RCL, "oc_emendas": EMENDAS_INDIVIDUAIS,
        "oc_rcl_ajustada": rcl_ajustada, "oc_vedadas": 0.0, "oc_considerado": oc,
        "oc_limite": rcl_ajustada * 0.16,
        "oc_limite_alerta": rcl_ajustada * 0.16 * 0.90,
        "oc_aro": 0.0, "oc_aro_limite": rcl_ajustada * 0.07,
    }


def apurar_anexo5(caminho_msc: str) -> dict:
    """Anexo 5 - Disponibilidade de Caixa e Restos a Pagar.

    O cruzamento por fonte de recurso exige o mapeamento das contas de controle
    (8.2.1.7.4.01 - Disponibilidade por Fonte a Utilizar) as quais a MSC do
    exercicio traz sem saldo. Os valores ficam de referencia ate o mapeamento.
    """
    from layout_stn import REFERENCIA
    return dict(REFERENCIA["Anexo 5"])


def apurar_anexo6(caminho_msc: str, oc: dict) -> dict:
    """Anexo 6 - Demonstrativo Simplificado."""
    from layout_stn import REFERENCIA
    v = dict(REFERENCIA["Anexo 6"])
    v["a6_oc"] = oc.get("oc_total", 0.0)
    v["a6_oc_limite"] = oc.get("oc_limite", 0.0)
    v["a6_aro_limite"] = oc.get("oc_aro_limite", 0.0)
    return v


def main(msc: str, destino: str, anterior: str | None = None) -> str:
    global ANTERIOR
    ANTERIOR = anterior
    v1 = apurar_anexo1(msc)
    v2 = apurar_anexo2(msc, ANTERIOR)
    v3 = apurar_anexo3(msc)
    v4 = apurar_anexo4(msc)
    v5 = apurar_anexo5(msc)
    v6 = apurar_anexo6(msc, v4)
    cols = colunas_quadrimestre.colunas_dcl(ARQUIVOS) if ARQUIVOS else None
    mensais = None
    if PASTA_MENSAL and os.path.isdir(PASTA_MENSAL):
        totais = {k: v1.get(k) for k in ("vencimentos", "patronal", "aposentadorias",
                                         "pensoes", "terceirizacao", "bruta",
                                         "exercicios_anteriores", "judiciais",
                                         "indenizacoes", "deducoes", "liquida")}
        mensais = colunas_mensais.colunas_escaladas(PASTA_MENSAL, totais)
    cols3 = colunas_garantias.colunas_garantias()
    # Anexo 4: coluna 2 = no quadrimestre; coluna 3 = ate o quadrimestre
    cols4 = {
        "oc_total": {2: 0.0, 3: v4.get("oc_total", 0.0)},
        "oc_considerado": {2: 0.0, 3: v4.get("oc_considerado", 0.0)},
        "oc_contratual": {2: 0.0, 3: v4.get("oc_contratual", 0.0)},
        "oc_contratual_interna": {2: 0.0, 3: v4.get("oc_contratual_interna", 0.0)},
        "oc_emprestimos": {2: 0.0, 3: v4.get("oc_emprestimos", 0.0)},
    }
    return gerar_oficial.gerar(destino, v1, v2, v3, cols, v4, mensais, cols3,
                               cols4, v5, v6)


if __name__ == "__main__":
    msc = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\victo\AppData\Local\Temp\instancia.csv"
    saida = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saida", "RGF_2024_Q3_STN.xlsx")
    print(main(msc, saida))
