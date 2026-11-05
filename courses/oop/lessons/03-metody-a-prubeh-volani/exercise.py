class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet

    def pridej(self, kolik=1):
        # Změňte počet této položky a vraťte nový počet.
        pass

    def celkem(self):
        # Vraťte aktuální součin ceny za kus a počtu.
        pass


if __name__ == "__main__":
    kniha = Polozka("Průvodce Pythonem", 250, 2)
    print("Na začátku:", kniha.celkem())
    print("Nový počet:", kniha.pridej())
    print("Po přidání:", kniha.celkem())
