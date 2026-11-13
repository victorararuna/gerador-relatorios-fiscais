# -*- coding: utf-8 -*-
"""
Leitor de planilhas .xls (BIFF8) em Python puro.

Implementa o minimo necessario para ler as planilhas usadas na aplicacao:
  - conteiner CFB/OLE2 (compound file)  -> stream "Workbook"
  - registros BIFF8 de valor            -> BOUNDSHEET, SST, LABELSST, LABEL,
                                           NUMBER, RK, MULRK, FORMULA, STRING,
                                           BOOLERR, MULBLANK

Uso:
    from leitor_xls import ler_xls
    wb = ler_xls("arquivo.xls")
    wb.abas                      # {nome: Aba}
    wb.abas["RREO"].valor(10, 3) # valor da linha 10, coluna C (1-based)
    wb.abas["RREO"].linhas()     # lista de listas

Nao depende de xlrd/excel/libreoffice.
"""
from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

__all__ = ["ler_xls", "Workbook", "Aba", "ErroXls"]


class ErroXls(Exception):
    pass


# --------------------------------------------------------------------------
# CFB / OLE2
# --------------------------------------------------------------------------
_CFB_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
_TAM_SETOR_MINI = 64
_CORTE_MINI = 4096
_FIM_CADEIA = 0xFFFFFFFE
_SETOR_LIVRE = 0xFFFFFFFF


class _Cfb:
    def __init__(self, dados: bytes):
        if dados[:8] != _CFB_MAGIC:
            raise ErroXls("arquivo nao e um CFB/OLE2 (.xls) valido")
        self.d = dados
        # cabecalho CFB (offsets fixos)
        self.versao = struct.unpack_from("<H", dados, 0x18)[0]
        self.tam_setor = 1 << struct.unpack_from("<H", dados, 0x1E)[0]
        self.tam_mini = 1 << struct.unpack_from("<H", dados, 0x20)[0]
        self.dir_inicio = struct.unpack_from("<I", dados, 0x30)[0]
        self.corte_mini = struct.unpack_from("<I", dados, 0x38)[0]
        self.minifat_inicio = struct.unpack_from("<I", dados, 0x3C)[0]
        self.n_minifat = struct.unpack_from("<I", dados, 0x40)[0]
        self.difat_inicio = struct.unpack_from("<I", dados, 0x44)[0]
        self.n_difat = struct.unpack_from("<I", dados, 0x48)[0]

        self.tam_setor = self.tam_setor or 512
        self.tam_mini = self.tam_mini or 64
        self.corte_mini = self.corte_mini or _CORTE_MINI
        self._fat = self._ler_fat()
        self._minifat = self._ler_minifat()
        self._entradas = self._ler_diretorio()
        self._mini_stream = None

    # -- setores -----------------------------------------------------------
    def _offset_setor(self, n: int) -> int:
        return (n + 1) * self.tam_setor

    def _setor(self, n: int) -> bytes:
        off = self._offset_setor(n)
        return self.d[off:off + self.tam_setor]

    def _ler_fat(self) -> List[int]:
        setores_difat = []
        # 109 primeiros vem do cabecalho
        for i in range(109):
            v = struct.unpack_from("<I", self.d, 0x4C + i * 4)[0]
            if v == _SETOR_LIVRE:
                break
            setores_difat.append(v)
        # cadeia DIFAT
        prox = self.difat_inicio
        proteg = 0
        while prox not in (_FIM_CADEIA, _SETOR_LIVRE) and proteg < 10000:
            s = self._setor(prox)
            n = self.tam_setor // 4
            vals = struct.unpack_from("<%dI" % n, s, 0)
            setores_difat.extend(v for v in vals[:-1] if v != _SETOR_LIVRE)
            prox = vals[-1]
            proteg += 1

        fat: List[int] = []
        for s in setores_difat:
            if s == _SETOR_LIVRE:
                continue
            bloco = self._setor(s)
            fat.extend(struct.unpack_from("<%dI" % (self.tam_setor // 4), bloco, 0))
        return fat

    def _ler_minifat(self) -> List[int]:
        if self.minifat_inicio in (_FIM_CADEIA, _SETOR_LIVRE):
            return []
        dados = self._ler_cadeia(self.minifat_inicio)
        n = len(dados) // 4
        return list(struct.unpack_from("<%dI" % n, dados, 0))

    def _ler_cadeia(self, inicio: int) -> bytes:
        partes = []
        s = inicio
        proteg = 0
        while s not in (_FIM_CADEIA, _SETOR_LIVRE) and proteg < 1_000_000:
            partes.append(self._setor(s))
            if s >= len(self._fat):
                break
            s = self._fat[s]
            proteg += 1
        return b"".join(partes)

    def _ler_cadeia_mini(self, inicio: int) -> bytes:
        if self._mini_stream is None:
            raiz = next(e for e in self._entradas if e["tipo"] == 5)
            self._mini_stream = self._ler_cadeia(raiz["inicio"])
        partes = []
        s = inicio
        proteg = 0
        while s not in (_FIM_CADEIA, _SETOR_LIVRE) and proteg < 1_000_000:
            off = s * self.tam_mini
            partes.append(self._mini_stream[off:off + self.tam_mini])
            if s >= len(self._minifat):
                break
            s = self._minifat[s]
            proteg += 1
        return b"".join(partes)

    # -- diretorio ---------------------------------------------------------
    def _ler_diretorio(self) -> List[dict]:
        dados = self._ler_cadeia(self.dir_inicio)
        entradas = []
        for i in range(0, len(dados) - 127, 128):
            e = dados[i:i + 128]
            tam_nome = struct.unpack_from("<H", e, 64)[0]
            if tam_nome == 0:
                continue
            nome = e[:max(0, tam_nome - 2)].decode("utf-16-le", "ignore")
            tipo = e[66]
            inicio = struct.unpack_from("<I", e, 116)[0]
            tam = struct.unpack_from("<I", e, 120)[0]
            entradas.append(dict(nome=nome, tipo=tipo, inicio=inicio, tamanho=tam))
        return entradas

    def stream(self, nome: str) -> bytes:
        for e in self._entradas:
            if e["tipo"] == 2 and e["nome"].lower() == nome.lower():
                if e["tamanho"] < self.corte_mini:
                    dados = self._ler_cadeia_mini(e["inicio"])
                else:
                    dados = self._ler_cadeia(e["inicio"])
                return dados[:e["tamanho"]]
        raise ErroXls(f"stream '{nome}' nao encontrado")


# --------------------------------------------------------------------------
# BIFF8
# --------------------------------------------------------------------------
def _unicode(curto: bool, dados: bytes, pos: int, biff8: bool = True) -> Tuple[str, int]:
    """Le string BIFF. biff8: Unicode com byte de flags; biff5: bytes puros."""
    if curto:
        cch = dados[pos]
        pos += 1
    else:
        cch = struct.unpack_from("<H", dados, pos)[0]
        pos += 2
    if not biff8:
        return dados[pos:pos + cch].decode("cp1252", "replace"), pos + cch
    flags = dados[pos]
    pos += 1
    alto_byte = bool(flags & 0x01)
    tem_fonetica = bool(flags & 0x04)
    tem_rt = bool(flags & 0x08)
    n_rt = 0
    tam_fonetica = 0
    if tem_rt:
        n_rt = struct.unpack_from("<H", dados, pos)[0]
        pos += 2
    if tem_fonetica:
        tam_fonetica = struct.unpack_from("<I", dados, pos)[0]
        pos += 4
    if alto_byte:
        bruto = dados[pos:pos + cch * 2]
        texto = bruto.decode("utf-16-le", "replace")
        pos += cch * 2
    else:
        bruto = dados[pos:pos + cch]
        texto = bruto.decode("latin-1", "replace")
        pos += cch
    pos += n_rt * 4 + tam_fonetica
    return texto, pos


def _rk(valor: int) -> float:
    if valor & 0x02:                      # inteiro
        v = valor >> 2
        if v & 0x20000000:                # sinal
            v -= 0x40000000
        num = float(v)
    else:                                 # double truncado
        num = struct.unpack("<d", struct.pack("<Q", (valor & 0xFFFFFFFC) << 32))[0]
    if valor & 0x01:                      # dividido por 100
        num /= 100.0
    return num


@dataclass
class Aba:
    nome: str
    _celulas: Dict[Tuple[int, int], Any] = field(default_factory=dict)
    max_lin: int = 0
    max_col: int = 0
    oculta: bool = False

    def valor(self, lin: int, col: int, padrao: Any = None) -> Any:
        """lin/col em base 1 (igual ao Excel)."""
        return self._celulas.get((lin, col), padrao)

    def definir(self, lin: int, col: int, v: Any) -> None:
        self._celulas[(lin, col)] = v
        self.max_lin = max(self.max_lin, lin)
        self.max_col = max(self.max_col, col)

    def linhas(self, ate_col: Optional[int] = None) -> List[List[Any]]:
        col = ate_col or self.max_col
        return [[self.valor(i, j) for j in range(1, col + 1)]
                for i in range(1, self.max_lin + 1)]

    def texto(self, lin: int, col: int) -> str:
        v = self.valor(lin, col)
        return "" if v is None else str(v).strip()

    def __repr__(self) -> str:
        return f"<Aba {self.nome!r} {self.max_lin}x{self.max_col}>"


@dataclass
class Workbook:
    abas: Dict[str, Aba]

    def aba(self, nome: str) -> Aba:
        if nome in self.abas:
            return self.abas[nome]
        alvo = nome.lower().strip()
        for k, v in self.abas.items():
            if k.lower().strip() == alvo:
                return v
        raise KeyError(f"aba {nome!r} inexistente; abas: {list(self.abas)}")

    def get(self, nome: str) -> Optional[Aba]:
        try:
            return self.aba(nome)
        except KeyError:
            return None

    @property
    def nomes(self) -> List[str]:
        return list(self.abas)


def ler_xls(caminho: str) -> Workbook:
    with open(caminho, "rb") as f:
        cfb = _Cfb(f.read())
    try:
        stream = cfb.stream("Workbook")
    except ErroXls:
        stream = cfb.stream("Book")
    return _ler_biff(stream)


def _ler_biff(dados: bytes) -> Workbook:
    # ---------- 0: versao (BIFF8 = 0x0600) ----------
    biff8 = True
    if len(dados) >= 6 and struct.unpack_from("<H", dados, 0)[0] in (0x0809, 0x0409, 0x0209):
        try:
            biff8 = struct.unpack_from("<H", dados, 4)[0] >= 0x0600
        except struct.error:
            biff8 = True

    # ---------- 1a passada: indice de abas e SST ----------
    abas_meta: List[Tuple[int, str, bool]] = []
    sst: List[str] = []
    pos = 0
    n = len(dados)

    while pos + 4 <= n:
        rid, rlen = struct.unpack_from("<HH", dados, pos)
        corpo = pos + 4
        if rid == 0x0085:                                    # BOUNDSHEET
            off = struct.unpack_from("<I", dados, corpo)[0]
            vis = dados[corpo + 4]
            nome, _ = _unicode(True, dados, corpo + 6, biff8)
            abas_meta.append((off, nome, bool(vis & 0x03)))
        elif rid == 0x00FC:                                  # SST
            sst = _ler_sst(dados, corpo, rlen, biff8)
        pos = corpo + rlen

    if not abas_meta:
        raise ErroXls("nenhuma aba (BOUNDSHEET) encontrada")

    # ---------- 2a passada: valores por aba ----------
    wb = Workbook(abas={})
    ordenadas = sorted(abas_meta, key=lambda t: t[0])
    for i, (off, nome, oculta) in enumerate(ordenadas):
        fim = ordenadas[i + 1][0] if i + 1 < len(ordenadas) else n
        aba = Aba(nome=nome, oculta=oculta)
        _ler_aba(dados, off, fim, aba, sst, biff8)
        base, contador = nome, 2
        while base in wb.abas:                # nomes duplicados
            base = f"{nome}_{contador}"
            contador += 1
        wb.abas[base] = aba
    return wb


def _ler_sst(dados: bytes, corpo: int, tam: int, biff8: bool = True) -> List[str]:
    """SST + CONTINUE.

    Cada registro CONTINUE recomeca com um byte de flags: o trecho que continua
    pode mudar de comprimido (1 byte/caractere) para UTF-16 (2 bytes). Concatenar
    os pedacos antes de interpretar corrompe todas as strings seguintes — era o
    que acontecia com as receitas de capital do comparativo da receita.
    """
    pedacos = [dados[corpo:corpo + tam]]
    pos = corpo + tam
    n = len(dados)
    while pos + 4 <= n:
        rid, rlen = struct.unpack_from("<HH", dados, pos)
        if rid != 0x003C:                     # CONTINUE
            break
        pedacos.append(dados[pos + 4:pos + 4 + rlen])
        pos += 4 + rlen

    try:
        _total, unicos = struct.unpack_from("<II", pedacos[0], 0)
    except struct.error:
        return []

    strings: List[str] = []
    ped = 0
    p = 8

    def _avancar() -> bool:
        nonlocal ped, p
        ped += 1
        p = 0
        return ped < len(pedacos)

    for _ in range(unicos):
        buf = pedacos[ped]
        # comprimento da string
        if p + 2 > len(buf):
            if not _avancar():
                break
            buf = pedacos[ped]
        if p + 2 > len(buf):
            break
        cch = struct.unpack_from("<H", buf, p)[0]
        p += 2
        # flags
        if p >= len(buf):
            if not _avancar():
                break
            buf = pedacos[ped]
        flags = buf[p]
        p += 1
        alto = bool(flags & 0x01)
        tem_fonetica = bool(flags & 0x04)
        tem_rt = bool(flags & 0x08)
        n_rt = 0
        tam_fonetica = 0
        if tem_rt:
            if p + 2 > len(buf):
                if not _avancar():
                    break
                buf = pedacos[ped]
            n_rt = struct.unpack_from("<H", buf, p)[0]
            p += 2
        if tem_fonetica:
            if p + 4 > len(buf):
                if not _avancar():
                    break
                buf = pedacos[ped]
            tam_fonetica = struct.unpack_from("<I", buf, p)[0]
            p += 4

        partes: List[str] = []
        restante = cch
        while restante > 0:
            buf = pedacos[ped]
            disp = len(buf) - p
            if disp <= 0:
                if not _avancar():
                    break
                buf = pedacos[ped]
                flags = buf[0]
                p = 1
                alto = bool(flags & 0x01)
                continue
            if alto:
                n = min(restante, disp // 2)
                if n <= 0:
                    if not _avancar():
                        break
                    buf = pedacos[ped]
                    flags = buf[0]
                    p = 1
                    alto = bool(flags & 0x01)
                    continue
                partes.append(buf[p:p + n * 2].decode("utf-16-le", "replace"))
                p += n * 2
            else:
                n = min(restante, disp)
                partes.append(buf[p:p + n].decode("latin-1", "replace"))
                p += n
            restante -= n
            if restante > 0:
                if not _avancar():
                    break
                flags = pedacos[ped][0]
                p = 1
                alto = bool(flags & 0x01)

        strings.append("".join(partes))
        p += n_rt * 4 + tam_fonetica

    return strings


def _ler_aba(dados: bytes, inicio: int, fim: int, aba: Aba, sst: List[str], biff8: bool = True) -> None:
    pos = inicio
    pendente_string: Optional[Tuple[int, int]] = None
    while pos + 4 <= fim:
        rid, rlen = struct.unpack_from("<HH", dados, pos)
        c = pos + 4
        try:
            if rid == 0x00FD:                                   # LABELSST
                lin, col, _xf, isst = struct.unpack_from("<HHHI", dados, c)
                aba.definir(lin + 1, col + 1, sst[isst] if isst < len(sst) else "")
            elif rid == 0x0204:                                 # LABEL
                lin, col, _xf = struct.unpack_from("<HHH", dados, c)
                s, _ = _unicode(False, dados, c + 6, biff8)
                aba.definir(lin + 1, col + 1, s)
            elif rid == 0x0203:                                 # NUMBER
                lin, col, _xf, v = struct.unpack_from("<HHHd", dados, c)
                aba.definir(lin + 1, col + 1, v)
            elif rid == 0x027E:                                 # RK
                lin, col, _xf, rk = struct.unpack_from("<HHHI", dados, c)
                aba.definir(lin + 1, col + 1, _rk(rk))
            elif rid == 0x00BD:                                 # MULRK
                lin, col1 = struct.unpack_from("<HH", dados, c)
                qtd = (rlen - 6) // 6
                for k in range(qtd):
                    rk = struct.unpack_from("<I", dados, c + 4 + k * 6 + 2)[0]
                    aba.definir(lin + 1, col1 + k + 1, _rk(rk))
            elif rid == 0x0006:                                 # FORMULA
                lin, col, _xf = struct.unpack_from("<HHH", dados, c)
                res = dados[c + 6:c + 14]
                if res[6:8] == b"\xff\xff":
                    tipo = res[0]
                    if tipo == 0x00:                            # string -> STRING
                        pendente_string = (lin + 1, col + 1)
                    elif tipo == 0x01:                          # boolean
                        aba.definir(lin + 1, col + 1, bool(res[2]))
                    elif tipo == 0x03:
                        aba.definir(lin + 1, col + 1, "")
                    # 0x02 erro: ignora
                else:
                    v = struct.unpack("<d", res)[0]
                    aba.definir(lin + 1, col + 1, v)
            elif rid == 0x0207 and pendente_string:             # STRING
                s, _ = _unicode(False, dados, c, biff8)
                aba.definir(pendente_string[0], pendente_string[1], s)
                pendente_string = None
            elif rid == 0x0205:                                 # BOOLERR
                lin, col, _xf, v, ferr = struct.unpack_from("<HHHBB", dados, c)
                aba.definir(lin + 1, col + 1, bool(v) if not ferr else None)
            elif rid == 0x000A:                                 # EOF
                break
        except struct.error:
            pass
        pos = c + rlen


# --------------------------------------------------------------------------
# atalho de conveniencia
# --------------------------------------------------------------------------
def resumo(caminho: str, max_lin: int = 0) -> str:
    wb = ler_xls(caminho)
    out = [f"{caminho}", f"abas: {len(wb.abas)}"]
    for nome, aba in wb.abas.items():
        out.append(f"  - {nome!r}: {aba.max_lin} linhas x {aba.max_col} colunas"
                   + (" (oculta)" if aba.oculta else ""))
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(resumo(arg))
        print()


