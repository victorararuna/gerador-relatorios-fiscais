# -*- coding: utf-8 -*-
"""
Descriptografia de planilhas .xls protegidas por FILEPASS (RC4 / XOR), conforme
[MS-OFFCRYPTO] - "Standard Encryption" (RC4, 40 bits) usada pelo Excel.

Por que isso e necessario aqui: os templates oficiais do Siconfi
(SICONFI_RREO_*.xls / SICONFI_RGF_*.xls) vem com FILEPASS. Sem abrir, perdem-se
os rotulos oficiais de cada anexo - que sao justamente o "layout" que a
aplicacao precisa para gerar os demonstrativos.

O Excel grava esses arquivos com a senha padrao de reserva de gravacao
("VelvetSweatshop"), de modo que abrem sem prompt. E essa a chave usada.
"""
from __future__ import annotations

import hashlib
import struct
from typing import List, Optional, Tuple

__all__ = ["descriptografar_workbook", "TemFilePass", "senhas_padrao"]

# senhas tentadas, em ordem de probabilidade
senhas_padrao = ["VelvetSweatshop", ""]


class TemFilePass(Exception):
    pass


def _rc4(chave: bytes, dados: bytes) -> bytes:
    S = list(range(256))
    j = 0
    klen = len(chave)
    for i in range(256):
        j = (j + S[i] + chave[i % klen]) & 0xFF
        S[i], S[j] = S[j], S[i]
    saida = bytearray(len(dados))
    i = j = 0
    for n, b in enumerate(dados):
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        saida[n] = b ^ S[(S[i] + S[j]) & 0xFF]
    return bytes(saida)


def _chave_bloco(base: bytes, bloco: int) -> bytes:
    return hashlib.md5(base + struct.pack("<I", bloco)).digest()[: len(base)]


def _decifrar_rc4(base: bytes, dados: bytes) -> bytes:
    """RC4 'standard encryption': reinicia a cada 1024 bytes, com chave por bloco."""
    saida = bytearray()
    for n in range(0, len(dados), 1024):
        bloco = n // 1024
        saida += _rc4(_chave_bloco(base, bloco), dados[n:n + 1024])
    return bytes(saida)


def _base_rc4(senha: str, salt: bytes) -> bytes:
    return hashlib.md5(salt + senha.encode("utf-16-le")).digest()[:5]


def _testar_senha(payload: bytes, senha: str) -> Optional[bytes]:
    """Retorna a chave-base se a senha confere, senao None."""
    # payload: wEncryptionType(2) + vMajor(1)+vMinor(1)+vMajor2(1)+vMinor2(1) + salt(16)
    if len(payload) < 6 + 16 + 32:
        return None
    tipo = struct.unpack_from("<H", payload, 0)[0]
    if tipo != 0x0001:               # 1 = RC4 standard; 0 = XOR
        return None
    salt = payload[6:22]
    verificador = payload[22:38]
    hash_verif = payload[38:54]
    base = _base_rc4(senha, salt)
    v = _rc4(_chave_bloco(base, 0), verificador)
    h = _rc4(_chave_bloco(base, 0), hash_verif)
    if hashlib.md5(v).digest() == h[:16]:
        return base
    return None


def _xor_decifrar(payload: bytes, dados: bytes) -> Optional[bytes]:
    """FILEPASS tipo 0 (XOR obfuscation) - senha derivada do verificador."""
    if len(payload) < 6:
        return None
    # estrutura XOR: verifier(2) ... - raro nos arquivos do Siconfi; nao suportado
    return None


def localizar_filepass(stream: bytes) -> Optional[Tuple[int, int, int]]:
    """Retorna (inicio_registro, inicio_payload, tamanho_payload) do FILEPASS."""
    pos = 0
    n = len(stream)
    while pos + 4 <= n:
        rid, rlen = struct.unpack_from("<HH", stream, pos)
        if rid == 0x002F:
            return pos, pos + 4, rlen
        if rid == 0x0085:            # BOUNDSHEET: passou dos registros globais
            return None
        pos += 4 + rlen
        if pos > 200_000:
            return None
    return None


def descriptografar_workbook(stream: bytes, senhas: Optional[List[str]] = None) -> bytes:
    """Devolve o stream do Workbook ja decifrado. Levanta TemFilePass se nao houver."""
    achado = localizar_filepass(stream)
    if not achado:
        raise TemFilePass("sem FILEPASS")
    _ini, ini_payload, tam_payload = achado
    payload = stream[ini_payload:ini_payload + tam_payload]

    for senha in (senhas or senhas_padrao):
        base = _testar_senha(payload, senha)
        if base is not None:
            inicio_cifrado = ini_payload + tam_payload
            claro = stream[:inicio_cifrado]
            cifrado = stream[inicio_cifrado:]
            return claro + _decifrar_rc4(base, cifrado)

    raise TemFilePass(
        "FILEPASS presente, mas nenhuma senha padrao funcionou. "
        "Informe a senha do arquivo nas opcoes da aplicacao."
    )
