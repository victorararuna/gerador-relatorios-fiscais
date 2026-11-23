# -*- coding: utf-8 -*-
"""Confere os anexos de AL (2026 B4) contra o publicado, com as calibracoes."""
import csv
import json
import os
import sys
from collections import defaultdict

R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, R)
sys.path.insert(0, os.path.join(R, "app"))

MSC = os.path.join(R, "dados", "al_msc")
PUB = os.path.join(R, "dados", "al_rreo_pub", "2026")
MAP = os.path.join(R, "dados", "mapeamentos")


def calib(nome):
    p = os.path.join(MAP, nome)
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    return d.get("subcategorias", d) if nome.startswith("anexo1") else d


def cmp_bloco(rotulo, cel, anexo):
    f = os.path.join(PUB, f"RREO_27_2026_bim4_anexo{anexo}.csv")
    if not os.path.exists(f):
        return f"{rotulo}: sem publicado"
    import rreo_layout_oficial as LO
    bloco = 0
    ok = dif = 0
    piores = []
    for x in csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"):
        b = LO._bloco(x["conta"])
        if b is not None:
            bloco = b
            continue
        nosso = cel.get((x["conta"], x["coluna"], bloco))
        if nosso is None:
            continue
        v = float(x["valor"])
        if abs(nosso - v) < 1.0:
            ok += 1
        else:
            dif += 1
            piores.append((x["conta"], x["coluna"], nosso, v))
    s = f"{rotulo}: exatas {ok} | divergentes {dif}"
    for c, col, n, v in sorted(piores, key=lambda y: -abs(y[2] - y[3]))[:3]:
        s += f"\n      {c[:34]:<36}{col[:20]:<22}{n:>15,.0f}{v:>15,.0f}{n - v:>13,.0f}"
    return s


def cmp_cod(rotulo, cel, anexo):
    """Compara por cod_conta (Anexo 4 e 6)."""
    f = os.path.join(PUB, f"RREO_27_2026_bim4_anexo{anexo}.csv")
    if not os.path.exists(f):
        return f"{rotulo}: sem publicado"
    pub = {}
    for x in csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"):
        cod = (x.get("cod_conta") or x["conta"]).strip()
        pub.setdefault((cod, x["coluna"]), float(x["valor"]))
    achou = {(c, col): v for (c, col, _b), v in cel.items()}
    ok = dif = 0
    piores = []
    for k, v in pub.items():
        if k in achou:
            if abs(achou[k] - v) < 1.0:
                ok += 1
            else:
                dif += 1
                piores.append((k[0], k[1], achou[k], v))
    s = f"{rotulo}: exatas {ok} | divergentes {dif}"
    for c, col, n, v in sorted(piores, key=lambda y: -abs(y[2] - y[3]))[:3]:
        s += f"\n      {str(c)[:34]:<36}{col[:20]:<22}{n:>15,.0f}{v:>15,.0f}{n - v:>13,.0f}"
    return s


def main():
    import rreo_anexo1_completo as A1
    import rreo_anexo4_completo as A4
    import rreo_anexo6_completo as A6

    print(cmp_bloco("Anexo 1", A1.celulas(MSC, 2026, 4, subcategorias=calib("anexo1_subcategorias_al.json")), "01"))

    pub4 = os.path.join(PUB, "RREO_27_2026_bim4_anexo04.csv")
    pubdict = {}
    for x in csv.DictReader(open(pub4, encoding="utf-8-sig"), delimiter=";"):
        cod = (x.get("cod_conta") or x["conta"]).strip()
        pubdict.setdefault((cod, x["coluna"]), float(x["valor"]))
    print(cmp_cod("Anexo 4", A4.celulas(MSC, 2026, 4, publicado=pubdict,
                                        calibracao=calib("anexo4_al.json")), "04"))

    print(cmp_cod("Anexo 6", A6.celulas(MSC, 2026, 4, calibracao=calib("anexo6_al.json"),
                                        chaves_cod=True), "06"))


if __name__ == "__main__":
    main()
