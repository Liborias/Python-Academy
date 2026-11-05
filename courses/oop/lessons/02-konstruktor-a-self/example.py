class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        # Self označuje právě připravovanou instanci.
        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet


kniha = Polozka("Průvodce Pythonem", 250, 2)
obal = Polozka("Dárkový obal", 30)
# Vynechaný poslední argument použije výchozí počet 1.
print(kniha.nazev, kniha.cena_za_kus, kniha.pocet)
print(obal.nazev, obal.cena_za_kus, obal.pocet)
kniha.pocet = 3
print("Po změně:", kniha.pocet, obal.pocet)
