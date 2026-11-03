def nacti(nazev):
    with open(nazev, encoding="utf-8") as soubor:
        return soubor.read()


def pocet_znaku(nazev):
    return len(nacti(nazev))


def slov_v_souboru(nazev):
    return len(nacti(nazev).split())
