import json


def nacti_kontakty(nazev):
    try:
        with open(nazev, encoding="utf-8") as soubor:
            return json.load(soubor)
    except FileNotFoundError:
        return []


def uloz_kontakty(nazev, kontakty):
    with open(nazev, "w", encoding="utf-8") as soubor:
        json.dump(kontakty, soubor, ensure_ascii=False, indent=2)


def pridej_kontakt(nazev, jmeno, telefon, email=""):
    kontakty = nacti_kontakty(nazev)
    for kontakt in kontakty:
        if kontakt["jmeno"].lower() == jmeno.lower():
            return False
    kontakty.append({"jmeno": jmeno, "telefon": telefon, "email": email})
    uloz_kontakty(nazev, kontakty)
    return True


def najdi(nazev, text):
    nalezene = []
    for kontakt in nacti_kontakty(nazev):
        if text.lower() in kontakt["jmeno"].lower():
            nalezene.append(kontakt)
    return nalezene


def smaz_kontakt(nazev, jmeno):
    kontakty = nacti_kontakty(nazev)
    zbyle = []
    for kontakt in kontakty:
        if kontakt["jmeno"].lower() != jmeno.lower():
            zbyle.append(kontakt)
    if len(zbyle) == len(kontakty):
        return False
    uloz_kontakty(nazev, zbyle)
    return True


def vypis(nazev):
    kontakty = sorted(nacti_kontakty(nazev), key=lambda k: k["jmeno"])
    if not kontakty:
        return "Žádné kontakty."
    radky = []
    for kontakt in kontakty:
        radky.append(f"{kontakt['jmeno']}: {kontakt['telefon']}")
    return "\n".join(radky)
