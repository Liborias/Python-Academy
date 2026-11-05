from polozka import Polozka


class Objednavka:
    def __init__(self, cislo):
        self.cislo = cislo
        # Vytvořte vlastní prázdný seznam položek.
        pass

    def pridej(self, polozka):
        # Uchovejte předaný objekt a vraťte počet řádků objednávky.
        pass

    def celkem(self):
        # Sečtěte výsledky metody celkem všech položek.
        pass

    def prehled(self):
        # Vraťte kopii seznamu se stejnými objekty položek.
        pass


if __name__ == "__main__":
    kniha = Polozka("Průvodce Pythonem", 250)
    obal = Polozka("Dárkový obal", 30, 2)
    objednavka = Objednavka("OBJ-001")
    objednavka.pridej(kniha)
    objednavka.pridej(obal)
    print("Objednávka:", objednavka.cislo, "celkem:", objednavka.celkem())
    kniha.pridej()
    print("Po změně položky:", objednavka.celkem())
