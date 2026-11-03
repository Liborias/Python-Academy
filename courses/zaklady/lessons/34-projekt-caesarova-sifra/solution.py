ABECEDA = "abcdefghijklmnopqrstuvwxyz"


def posun_pismeno(znak, posun):
    male = znak.lower()
    if male not in ABECEDA:
        return znak
    nova = ABECEDA[(ABECEDA.index(male) + posun) % len(ABECEDA)]
    if znak.isupper():
        return nova.upper()
    return nova


def zasifruj(text, posun):
    vysledek = ""
    for znak in text:
        vysledek += posun_pismeno(znak, posun)
    return vysledek


def desifruj(text, posun):
    return zasifruj(text, -posun)


def rozlam(sifra, slovo):
    for posun in range(1, 26):
        if slovo in desifruj(sifra, posun).lower():
            return posun
    return None
