class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet

    def pridej(self, kolik=1):
        self.pocet += kolik
        return self.pocet

    def celkem(self):
        return self.cena_za_kus * self.pocet


if __name__ == "__main__":
    kniha = Polozka("Průvodce Pythonem", 250, 2)
    print("Na začátku:", kniha.celkem())
    print("Nový počet:", kniha.pridej())
    print("Po přidání:", kniha.celkem())
