def uloz_radky(nazev, radky):
    with open(nazev, "w", encoding="utf-8") as soubor:
        for radek in radky:
            soubor.write(radek + "\n")


def pridej_radek(nazev, text):
    with open(nazev, "a", encoding="utf-8") as soubor:
        soubor.write(text + "\n")


def zkopiruj(zdroj, cil):
    with open(zdroj, encoding="utf-8") as soubor:
        obsah = soubor.read()
    with open(cil, "w", encoding="utf-8") as soubor:
        soubor.write(obsah)
