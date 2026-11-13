# -*- coding: utf-8 -*-
"""Leitor das Matrizes de Saldos Contábeis (MSC) do Siconfi — formato longo.

A partir de 2025 o Siconfi deixou de publicar a matriz no formato
``instancia.csv`` (16 colunas, atributos em pares) e passou a entregar **um
arquivo por classe contábil, por mês e por tipo de saldo**:

    MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_ending_balance.csv
    MSC_24_2025_m12_MSCC_msc_orcamentaria_classe6_period_change.csv

Cada arquivo é uma tabela longa com os atributos já em colunas próprias —
``poder_orgao``, ``natureza_despesa``, ``natureza_receita``, ``fonte_recursos``,
``complemento_fonte``, ``funcao``, ``ano_inscricao`` — o que elimina o
de-para posicional do formato antigo.

Duas regras de leitura que os números obrigam:

* ``ending_balance`` é o **saldo de fechamento** do mês. Em dezembro, o saldo
  das contas de despesa é igual à soma dos ``period_change`` do exercício
  (verificado ao centavo no RN/2025).
* ``period_change`` é o **movimento do mês**. É o único arquivo em que
  aparecem as naturezas **D** (débitos) das contas de liquidação; o
  ``ending_balance`` traz apenas C. Logo, a despesa líquida
  (créditos − débitos) só pode ser apurada sobre o ``period_change``.

Uso:

    from leitor_msc import Acervo

    acervo = Acervo(r"C:\\...\\siconfi_rn_msc")
    acervo.meses(2025)                       # [1, 2, ..., 12]

    # despesa liquidada do Executivo no ano, contas 6.2.2.1.3.03/04/07
    total = acervo.total(
        2025, acervo.meses(2025),
        contas=("622130300", "622130400", "622130700"),
        filtro=lambda r: r.po in ("10111", "10112", "60611"),
    )
"""
from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

__all__ = ["Acervo", "Registro", "ErroMSC", "PADRAO"]

#: nome do arquivo: MSC_<ibge>_<ano>_m<mes>_<tipo>_msc_<grupo>_classe<n>_<saldo>.csv
PADRAO = re.compile(
    r"^MSC_(\d+)_(\d{4})_m(\d{2})_(MSCC|MSCE)_msc_"
    r"(orcamentaria|patrimonial|controle)_classe(\d)_"
    r"(ending_balance|period_change)\.csv$",
    re.IGNORECASE,
)

TIPOS_VALOR = ("ending_balance", "period_change")


class ErroMSC(Exception):
    """Erro de acervo: arquivo ausente, nome fora do padrão ou linha corrompida."""


@dataclass(slots=True)
class Registro:
    """Uma linha da matriz, já com o sinal aplicado."""

    ano: int
    mes: int
    tipo: str            # MSCC (consolidada) ou MSCE
    classe: int
    tipo_valor: str      # ending_balance / period_change
    conta: str           # conta_contabil, 9 dígitos
    po: str              # poder_orgao
    nd: str              # natureza_despesa (8 dígitos, vazio na classe 1-4)
    receita: str         # natureza_receita
    fr: str              # fonte_recursos
    compl: str           # complemento_fonte (plano RPPS, detalhe da fonte)
    funcao: str
    subfuncao: str
    inscricao: str       # ano_inscricao (restos a pagar)
    valor: float         # valor absoluto, como no arquivo
    natureza: str        # C ou D

    @property
    def liquido(self) -> float:
        """Valor com sinal: crédito positivo, débito negativo."""
        return self.valor if self.natureza == "C" else -self.valor

    @property
    def elemento(self) -> str:
        """Elemento da natureza da despesa (6 primeiros dígitos)."""
        return self.nd[:6]


class Acervo:
    """Índice e leitor dos arquivos MSC de uma pasta (o ano é subpasta)."""

    def __init__(self, raiz: str, *, mscc: bool = True):
        self.raiz = os.path.abspath(raiz)
        if not os.path.isdir(self.raiz):
            raise ErroMSC(f"pasta do acervo inexistente: {self.raiz}")
        self.mscc = mscc
        self._mapa: Dict[Tuple[int, int, str, int, str], str] = {}
        self._indexar()

    # ------------------------------------------------------------------ índice
    def _indexar(self) -> None:
        for pasta, _, arquivos in os.walk(self.raiz):
            for nome in arquivos:
                m = PADRAO.match(nome)
                if not m:
                    continue
                _, ano, mes, tipo, _grupo, classe, tipo_valor = m.groups()
                if not self.mscc and tipo.upper() == "MSCC":
                    continue
                chave = (int(ano), int(mes), tipo.upper(), int(classe), tipo_valor)
                caminho = os.path.join(pasta, nome)
                anterior = self._mapa.get(chave)
                if anterior and os.path.getsize(caminho) > os.path.getsize(anterior):
                    continue  # mantém o maior (reexportação parcial)
                self._mapa[chave] = caminho

        if not self._mapa:
            raise ErroMSC(
                f"nenhum arquivo MSC reconhecido em {self.raiz}. "
                "Esperado MSC_<ibge>_<ano>_m<mm>_MSCC_msc_<grupo>_classe<n>_"
                "<ending_balance|period_change>.csv"
            )

    @property
    def anos(self) -> List[int]:
        return sorted({c[0] for c in self._mapa})

    def meses(self, ano: int, classe: int = 6,
              tipo_valor: str = "ending_balance",
              tipo: str = "MSCC") -> List[int]:
        return sorted(c[1] for c in self._mapa
                      if c[0] == ano and c[3] == classe
                      and c[4] == tipo_valor and c[2] == tipo.upper())

    def arquivo(self, ano: int, mes: int, classe: int = 6,
                tipo_valor: str = "period_change",
                tipo: str = "MSCC") -> str:
        chave = (ano, mes, tipo.upper(), classe, tipo_valor)
        try:
            return self._mapa[chave]
        except KeyError:
            raise ErroMSC(
                f"matriz ausente: {tipo} {ano}-{mes:02d} classe {classe} "
                f"{tipo_valor}"
            ) from None

    # ------------------------------------------------------------------ leitura
    def ler(self, ano: int, mes: int, classe: int = 6,
            tipo_valor: str = "period_change",
            tipo: str = "MSCC") -> Iterator[Registro]:
        """Percorre as linhas de um arquivo, aplicando sinal e tipos."""
        caminho = self.arquivo(ano, mes, classe, tipo_valor, tipo)
        with open(caminho, encoding="utf-8-sig", newline="") as fh:
            leitor = csv.DictReader(fh, delimiter=";")
            if leitor.fieldnames is None or "conta_contabil" not in leitor.fieldnames:
                raise ErroMSC(f"cabeçalho inesperado em {caminho}")
            for linha in leitor:
                yield self._registro(linha, ano, mes, classe, tipo_valor, tipo)

    def _registro(self, l: Dict[str, str], ano: int, mes: int, classe: int,
                  tipo_valor: str, tipo: str) -> Registro:
        try:
            valor = float(l.get("valor") or 0.0)
        except ValueError:
            raise ErroMSC(
                f"valor inválido em {tipo} {ano}-{mes:02d}: {l.get('valor')!r}"
            ) from None
        natureza = (l.get("natureza_conta") or "").strip().upper()
        if natureza not in ("C", "D"):
            raise ErroMSC(f"natureza_conta inesperada: {natureza!r}")
        return Registro(
            ano=ano, mes=mes, tipo=tipo.upper(), classe=classe,
            tipo_valor=tipo_valor,
            conta=(l.get("conta_contabil") or "").strip(),
            po=(l.get("poder_orgao") or "").strip(),
            nd=(l.get("natureza_despesa") or "").strip(),
            receita=(l.get("natureza_receita") or "").strip(),
            fr=(l.get("fonte_recursos") or "").strip(),
            compl=(l.get("complemento_fonte") or "").strip(),
            funcao=(l.get("funcao") or "").strip(),
            subfuncao=(l.get("subfuncao") or "").strip(),
            inscricao=(l.get("ano_inscricao") or "").strip(),
            valor=valor, natureza=natureza,
        )

    # --------------------------------------------------------------- agregação
    def agregar(self, ano: int, meses: Sequence[int], *,
                classes: Sequence[int] = (6,),
                contas: Optional[Sequence[str]] = None,
                tipo_valor: str = "period_change",
                tipo: str = "MSCC",
                chave: Sequence[str] = ("po",),
                filtro: Optional[Callable[[Registro], bool]] = None,
                bruto: bool = False) -> Dict[Tuple[str, ...], float]:
        """Soma as linhas de vários meses, agrupando por atributos.

        ``contas`` casa por prefixo (``"62213"`` pega 6.2.2.1.3 inteira).
        Por padrão soma o movimento líquido; ``bruto=True`` soma o valor
        absoluto (créditos e débitos sem sinal).
        """
        saida: Dict[Tuple[str, ...], float] = {}
        for classe in classes:
            for mes in meses:
                for r in self.ler(ano, mes, classe, tipo_valor, tipo):
                    if contas and not r.conta.startswith(tuple(contas)):
                        continue
                    if filtro is not None and not filtro(r):
                        continue
                    valor = r.valor if bruto else r.liquido
                    k = tuple(getattr(r, atributo) for atributo in chave)
                    saida[k] = saida.get(k, 0.0) + valor
        return saida

    def total(self, ano: int, meses: Sequence[int], **kwargs) -> float:
        return sum(self.agregar(ano, meses, **kwargs).values())

    # ------------------------------------------------------------- conferência
    def conferir_fluxo_estoque(self, ano: int, classe: int = 6,
                               tipo: str = "MSCC") -> List[Tuple[str, float, float, float]]:
        """Confere se o saldo de dezembro = soma dos movimentos do exercício.

        Devolve as contas divergentes no formato (conta, fluxo, saldo, dif).
        Lista vazia significa que o acervo fecha.
        """
        meses = self.meses(ano, classe, "period_change", tipo)
        if not meses:
            raise ErroMSC(f"sem period_change para {ano} classe {classe}")
        fluxo: Dict[str, float] = {}
        for mes in meses:
            for r in self.ler(ano, mes, classe, "period_change", tipo):
                fluxo[r.conta] = fluxo.get(r.conta, 0.0) + r.liquido
        ultimo = self.meses(ano, classe, "ending_balance", tipo)
        if not ultimo:
            raise ErroMSC(f"sem ending_balance para {ano} classe {classe}")
        ultimo = ultimo[-1]
        saldo: Dict[str, float] = {}
        for r in self.ler(ano, ultimo, classe, "ending_balance", tipo):
            saldo[r.conta] = saldo.get(r.conta, 0.0) + r.liquido
        divergentes = []
        for conta in sorted(set(fluxo) | set(saldo)):
            f = fluxo.get(conta, 0.0)
            s = saldo.get(conta, 0.0)
            if abs(f - s) > 0.01:
                divergentes.append((conta, f, s, f - s))
        return divergentes


# --------------------------------------------------------------------- CLI
def _cli() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Inventário e conferência de um acervo MSC do Siconfi.")
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--ano", type=int)
    ap.add_argument("--classe", type=int, default=6)
    ap.add_argument("--tipo", default="MSCC")
    args = ap.parse_args()

    acervo = Acervo(args.raiz, mscc=(args.tipo.upper() == "MSCC"))
    print(f"acervo: {acervo.raiz}")
    print(f"anos: {acervo.anos}")
    anos = [args.ano] if args.ano else acervo.anos
    for ano in anos:
        saldo = acervo.meses(ano, args.classe, "ending_balance", args.tipo)
        mov = acervo.meses(ano, args.classe, "period_change", args.tipo)
        print(f"  {ano} classe {args.classe}: "
              f"{len(saldo)} saldos {saldo[:3]}... | {len(mov)} movimentos")
        if not saldo or not mov:
            continue
        div = acervo.conferir_fluxo_estoque(ano, args.classe, args.tipo)
        if not div:
            print("    amarração saldo x movimento: OK (0 contas divergentes)")
            continue
        print(f"    amarração saldo x movimento: {len(div)} conta(s) divergente(s)")
        for conta, f, s, d in div[:10]:
            print(f"      {conta}  fluxo={f:>18,.2f}  saldo={s:>18,.2f}  dif={d:>14,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
