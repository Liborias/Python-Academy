DPH = 0.21


def pridej_dph(cena):
    return cena * (1 + DPH)


def soucet_seznamu(seznam):
    soucet = 0
    for x in seznam:
        soucet += x
    return soucet
