import csv


def hlavicka(nazev, oddelovac=","):
    with open(nazev, encoding="utf-8", newline="") as soubor:
        return next(csv.reader(soubor, delimiter=oddelovac))


def nacti_radky(nazev, oddelovac=","):
    with open(nazev, encoding="utf-8", newline="") as soubor:
        ctenar = csv.reader(soubor, delimiter=oddelovac)
        next(ctenar)
        radky = []
        for radek in ctenar:
            radky.append(radek)
    return radky


def sloupec(nazev, cislo, oddelovac=","):
    hodnoty = []
    for radek in nacti_radky(nazev, oddelovac):
        hodnoty.append(radek[cislo])
    return hodnoty


def prumer_sloupce(nazev, cislo, oddelovac=","):
    cisla = []
    for text in sloupec(nazev, cislo, oddelovac):
        cisla.append(float(text))
    return sum(cisla) / len(cisla)
