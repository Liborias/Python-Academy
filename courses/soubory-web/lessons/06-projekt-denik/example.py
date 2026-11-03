def pridej(nazev, text):
    with open(nazev, "a", encoding="utf-8") as soubor:      # "a" přidá řádek na konec, nic nesmaže
        soubor.write(text + "\n")


def pocet_radku(nazev):
    with open(nazev, encoding="utf-8") as soubor:
        return len(soubor.readlines())                       # readlines vrátí seznam všech řádků


pridej("test_denik.txt", "2026-10-25 | první zápis")
pridej("test_denik.txt", "2026-10-26 | druhý zápis")
print(pocet_radku("test_denik.txt"))                         # 2
datum, text = "2026-10-26 | a | b".split(" | ", 1)           # rozdělí jen na prvním oddělovači
print(datum, "/", text)                                      # 2026-10-26 / a | b
