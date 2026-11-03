def nacti_cisla(nazev):
    cisla = []
    with open(nazev, encoding="utf-8") as soubor:
        for radek in soubor:
            radek = radek.strip()
            if radek:
                cisla.append(int(radek))
    return cisla


def nejdelsi_radek(nazev):
    nejdelsi = ""
    with open(nazev, encoding="utf-8") as soubor:
        for radek in soubor:
            radek = radek.strip()
            if len(radek) > len(nejdelsi):
                nejdelsi = radek
    return nejdelsi


def teploty(nazev):
    vysledek = {}
    with open(nazev, encoding="utf-8") as soubor:
        for radek in soubor:
            radek = radek.strip()
            if radek:
                den, teplota = radek.split()
                vysledek[den] = int(teplota)
    return vysledek
