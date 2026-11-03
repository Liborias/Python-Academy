def pridej_zapis(nazev, datum, text):
    with open(nazev, "a", encoding="utf-8") as soubor:
        soubor.write(f"{datum} | {text}\n")


def nacti_zapisy(nazev):
    zapisy = []
    try:
        with open(nazev, encoding="utf-8") as soubor:
            for radek in soubor:
                radek = radek.strip()
                if " | " in radek:
                    datum, text = radek.split(" | ", 1)
                    zapisy.append((datum, text))
    except FileNotFoundError:
        return []
    return zapisy


def hledej(nazev, slovo):
    nalezeno = []
    for datum, text in nacti_zapisy(nazev):
        if slovo.lower() in text.lower():
            nalezeno.append((datum, text))
    return nalezeno


def zapisy_podle_dne(nazev):
    pocty = {}
    for datum, text in nacti_zapisy(nazev):
        pocty[datum] = pocty.get(datum, 0) + 1
    return pocty
