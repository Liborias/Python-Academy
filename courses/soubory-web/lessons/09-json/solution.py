import json


def nacti_json(nazev):
    with open(nazev, encoding="utf-8") as soubor:
        return json.load(soubor)


def uloz_json(nazev, data):
    with open(nazev, "w", encoding="utf-8") as soubor:
        json.dump(data, soubor, ensure_ascii=False, indent=2)


def nastav_hodnotu(nazev, klic, hodnota):
    try:
        data = nacti_json(nazev)
    except FileNotFoundError:
        data = {}
    data[klic] = hodnota
    uloz_json(nazev, data)
    return data


def pocet_hotovych(nazev):
    pocet = 0
    for ukol in nacti_json(nazev):
        if ukol["hotovo"]:
            pocet += 1
    return pocet
