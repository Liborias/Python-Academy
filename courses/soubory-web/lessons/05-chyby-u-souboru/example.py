def nacti_cislo(nazev):
    try:
        with open(nazev, encoding="utf-8") as soubor:
            return int(soubor.read().strip())       # int může vyvolat ValueError
    except FileNotFoundError:
        print("Soubor", nazev, "neexistuje.")        # chybějící soubor program nezastaví
    except ValueError:
        print("V souboru", nazev, "není číslo.")
    return None


print(nacti_cislo("neexistuje.txt"))                 # Soubor neexistuje. a potom None
