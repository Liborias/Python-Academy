def zdvojnasob(cisla):
    vysledek = []
    for x in cisla:
        vysledek.append(x * 2)
    return vysledek


def jen_kladna(cisla):
    vysledek = []
    for x in cisla:
        if x > 0:
            vysledek.append(x)
    return vysledek
