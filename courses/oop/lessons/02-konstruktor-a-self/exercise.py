class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        # Uložte všechny tři hodnoty do atributů této instance.
        pass


if __name__ == "__main__":
    kniha = Polozka("Průvodce Pythonem", 250, 2)
    obal = Polozka("Dárkový obal", 30)
    print(kniha.nazev, kniha.cena_za_kus, kniha.pocet)
    print(obal.nazev, obal.cena_za_kus, obal.pocet)
