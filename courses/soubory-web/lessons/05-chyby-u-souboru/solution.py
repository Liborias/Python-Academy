def nacti_bezpecne(nazev, vychozi=""):
    try:
        with open(nazev, encoding="utf-8") as soubor:
            return soubor.read()
    except OSError:
        return vychozi


def nacti_cisla_bezpecne(nazev):
    cisla = []
    try:
        with open(nazev, encoding="utf-8") as soubor:
            for radek in soubor:
                try:
                    cisla.append(int(radek.strip()))
                except ValueError:
                    continue
    except OSError:
        return []
    return cisla


def zaloha(nazev):
    try:
        with open(nazev, encoding="utf-8") as soubor:
            obsah = soubor.read()
    except FileNotFoundError:
        return False
    with open(nazev + ".bak", "w", encoding="utf-8") as soubor:
        soubor.write(obsah)
    return True
