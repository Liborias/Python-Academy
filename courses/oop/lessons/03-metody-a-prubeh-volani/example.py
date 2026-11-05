class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet

    def pridej(self, kolik=1):
        self.pocet += kolik
        return self.pocet

    def celkem(self):
        # Čtení ceny nic nepřidává ani neodebírá.
        return self.cena_za_kus * self.pocet


kniha = Polozka("Průvodce Pythonem", 250, 2)
print("Na začátku:", kniha.celkem())
# Metoda dostane instanci automaticky a vrátí nový počet.
novy_pocet = kniha.pridej()
print("Nový počet:", novy_pocet)
print("Po přidání:", kniha.celkem())
print("Druhé čtení:", kniha.celkem())
