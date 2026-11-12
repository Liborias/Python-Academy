"""Pravidla cvičného inventáře ověříme před SQL nebo převzetím spojení."""
def nazev_pomucky(nazev):
    if not isinstance(nazev,str) or not nazev.strip() or len(nazev.strip())>100:
        raise ValueError('Název musí mít 1–100 znaků po oříznutí okrajových mezer.')
    return nazev.strip()

def pocet_kusu(kusy):
    if type(kusy) is not int or not 0<=kusy<=1_000_000:
        raise ValueError('Počet musí být celé číslo 0–1000000, ne bool.')
    return kusy

def priprav_davku(pomucky):
    if not isinstance(pomucky,(list,tuple)) or len(pomucky)>100:
        raise ValueError('Dávka je seznam nebo tuple nejvýše 100 dvojic.')
    vysledek = []
    for polozka in pomucky:
        if not isinstance(polozka,(list,tuple)) or len(polozka)!=2:
            raise ValueError('Každá položka je dvojice název a počet.')
        vysledek.append((nazev_pomucky(polozka[0]),pocet_kusu(polozka[1])))
    return vysledek
