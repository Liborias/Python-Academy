def na_cislo(text):
    try:
        return int(text)
    except ValueError:
        return None


def bezpecne_deleni(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def soucet_cisel(texty):
    soucet = 0
    for t in texty:
        cislo = na_cislo(t)
        if cislo is not None:
            soucet += cislo
    return soucet
