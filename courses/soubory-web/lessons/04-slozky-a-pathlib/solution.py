from pathlib import Path


def najdi_txt(slozka):
    jmena = []
    for soubor in Path(slozka).glob("*.txt"):
        if soubor.is_file():
            jmena.append(soubor.name)
    return sorted(jmena)


def obsah_slozky(slozka):
    jmena = []
    for polozka in Path(slozka).iterdir():
        jmena.append(polozka.name)
    return sorted(jmena)


def zapis_poznamku(slozka, nazev, text):
    cesta = Path(slozka)
    cesta.mkdir(parents=True, exist_ok=True)
    soubor = cesta / nazev
    soubor.write_text(text, encoding="utf-8")
    return soubor
