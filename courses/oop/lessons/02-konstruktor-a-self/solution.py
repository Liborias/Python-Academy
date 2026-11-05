class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet


if __name__ == "__main__":
    kniha = Polozka("Průvodce Pythonem", 250, 2)
    obal = Polozka("Dárkový obal", 30)
    print(kniha.nazev, kniha.cena_za_kus, kniha.pocet)
    print(obal.nazev, obal.cena_za_kus, obal.pocet)
