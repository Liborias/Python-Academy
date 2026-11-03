def cena(ceny, zbozi):
    return ceny.get(zbozi, 0)


def celkem(ceny):
    return sum(ceny.values())


def drahe(ceny, limit):
    vysledek = []
    for zbozi, c in ceny.items():
        if c > limit:
            vysledek.append(zbozi)
    return vysledek
