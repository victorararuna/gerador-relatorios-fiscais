# -*- coding: utf-8 -*-
"""Catálogo dos anexos do RREO e do RGF (MDF 15ª edição / Siconfi v14).

Fornece o "enquadramento" oficial de cada anexo: título, base legal e nota de
rodapé. As colunas e as linhas vêm do próprio rascunho (ou do catálogo de
rótulos minerado, quando o Siconfi não os traz).

`precisa_rotulos = True` marca os anexos cujo rascunho vem apenas com valores.
`aplica_estado = False` marca anexos que não se aplicam a um Estado (são versões
simplificadas para municípios de pequeno porte).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class AnexoInfo:
    documento: str
    numero: int
    titulo: str
    subtitulo: str
    base_legal: str
    nota: str = ""
    precisa_rotulos: bool = False
    aplica_estado: bool = True

    @property
    def chave(self) -> str:
        return f"{self.documento}-Anexo {self.numero:02d}"


_RREO = [
    AnexoInfo("RREO", 1, "BALANÇO ORÇAMENTÁRIO", "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RREO – Anexo 1 (LRF, Art. 52, inciso I, alíneas “a” e “b”)",
              "FONTE: Sistema de Administração Financeira do Estado (SIAFEM/RN), "
              "Consolidação das Contas Públicas."),
    AnexoInfo("RREO", 2, "DEMONSTRATIVO DA EXECUÇÃO DAS DESPESAS POR FUNÇÃO/SUBFUNÇÃO",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RREO – Anexo 2 (LRF, Art. 52, inciso II, alínea “c”)",
              "FONTE: SIAFEM/RN. A classificação funcional é a da Portaria MOG nº 42/1999."),
    AnexoInfo("RREO", 3, "DEMONSTRATIVO DA RECEITA CORRENTE LÍQUIDA", "",
              "RREO – Anexo 3 (LRF, Art. 53, inciso I)",
              "FONTE: SIAFEM/RN. A RCL é apurada conforme o art. 2º, inciso IV, da LRF.",
              precisa_rotulos=True),
    AnexoInfo("RREO", 4, "DEMONSTRATIVO DAS RECEITAS E DESPESAS PREVIDENCIÁRIAS",
              "REGIME PRÓPRIO DE PREVIDÊNCIA SOCIAL",
              "RREO – Anexo 4 (LRF, Art. 53, inciso II)",
              "FONTE: SIAFEM/RN e RPPS.",
              precisa_rotulos=True),
    AnexoInfo("RREO", 6, "DEMONSTRATIVO DOS RESULTADOS PRIMÁRIO E NOMINAL",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RREO – Anexo 6 (LRF, Art. 53, inciso III)",
              "FONTE: SIAFEM/RN.",
              precisa_rotulos=True),
    AnexoInfo("RREO", 7, "DEMONSTRATIVO DOS RESTOS A PAGAR POR PODER E ÓRGÃO",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RREO – Anexo 7 (LRF, Art. 53, inciso V)",
              "FONTE: SIAFEM/RN.",
              precisa_rotulos=True),
    AnexoInfo("RREO", 13, "DEMONSTRATIVO DAS PARCERIAS PÚBLICO-PRIVADAS",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RREO – Anexo 13 (LRF, Art. 53, § 1º, inciso I)",
              "FONTE: SIAFEM/RN e contratos de PPP.",
              precisa_rotulos=True),
    AnexoInfo("RREO", 14, "DEMONSTRATIVO SIMPLIFICADO DO RELATÓRIO RESUMIDO DA EXECUÇÃO ORÇAMENTÁRIA",
              "MUNICÍPIOS COM POPULAÇÃO INFERIOR A 50 MIL HABITANTES",
              "RREO – Anexo 14 (LRF, Art. 63)",
              "Anexo simplificado, exclusivo de municípios com menos de 50 mil habitantes.",
              precisa_rotulos=True, aplica_estado=False),
]

_RGF = [
    AnexoInfo("RGF", 1, "DEMONSTRATIVO DA DESPESA COM PESSOAL",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RGF – Anexo 1 (LRF, Art. 55, inciso I, alínea “a”)",
              "FONTE: SIAFEM/RN. Limite: art. 20, inciso II, alínea “c”, da LRF."),
    AnexoInfo("RGF", 2, "DEMONSTRATIVO DA DÍVIDA CONSOLIDADA LÍQUIDA",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RGF – Anexo 2 (LRF, Art. 55, inciso I, alínea “b”)",
              "FONTE: SIAFEM/RN e Boletim da Dívida Pública."),
    AnexoInfo("RGF", 3, "DEMONSTRATIVO DAS GARANTIAS E CONTRAGARANTIAS DE VALORES",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RGF – Anexo 3 (LRF, Art. 55, inciso I, alínea “c”)",
              "FONTE: SIAFEM/RN."),
    AnexoInfo("RGF", 4, "DEMONSTRATIVO DAS OPERAÇÕES DE CRÉDITO",
              "ORÇAMENTOS FISCAL E DA SEGURIDADE SOCIAL",
              "RGF – Anexo 4 (LRF, Art. 55, inciso I, alínea “d”)",
              "FONTE: SIAFEM/RN."),
    AnexoInfo("RGF", 6, "DEMONSTRATIVO SIMPLIFICADO DO RELATÓRIO DE GESTÃO FISCAL",
              "MUNICÍPIOS COM POPULAÇÃO INFERIOR A 50 MIL HABITANTES",
              "RGF – Anexo 6 (LRF, Art. 63)",
              "FONTE: SIAFEM/RN."),
]

CATALOGO: Dict[str, AnexoInfo] = {a.chave: a for a in (_RREO + _RGF)}


def info(documento: str, numero: int) -> Optional[AnexoInfo]:
    return CATALOGO.get(f"{documento}-Anexo {numero:02d}")


def anexos_de(documento: str) -> List[AnexoInfo]:
    return list(_RREO if documento.upper() == "RREO" else _RGF)
