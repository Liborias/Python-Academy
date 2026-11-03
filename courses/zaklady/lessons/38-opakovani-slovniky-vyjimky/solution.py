def obrat_slovnik(slovnik):
    novy = {}
    for klic, hodnota in slovnik.items():
        novy[hodnota] = klic
    return novy


def seskup_podle_delky(slova):
    skupiny = {}
    for slovo in slova:
        delka = len(slovo)
        if delka not in skupiny:
            skupiny[delka] = []
        skupiny[delka].append(slovo)
    return skupiny


def bezpecny_soucet(hodnoty):
    soucet = 0
    for hodnota in hodnoty:
        try:
            soucet += float(hodnota)
        except (ValueError, TypeError):
            continue
    return soucet


def nejcastejsi_hodnota(seznam):
    if not seznam:
        return None
    pocty = {}
    for prvek in seznam:
        pocty[prvek] = pocty.get(prvek, 0) + 1
    return max(pocty, key=pocty.get)
