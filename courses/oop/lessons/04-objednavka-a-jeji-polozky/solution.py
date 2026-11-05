from polozka import Polozka


class Objednavka:
    def __init__(self, cislo):
        self.cislo = cislo
        self.polozky = []

    def pridej(self, polozka):
        self.polozky.append(polozka)
        return len(self.polozky)

    def celkem(self):
        soucet = 0
        for polozka in self.polozky:
            soucet += polozka.celkem()
        return soucet

    def prehled(self):
        return list(self.polozky)


if __name__ == "__main__":
    kniha = Polozka("Průvodce Pythonem", 250)
    obal = Polozka("Dárkový obal", 30, 2)
    objednavka = Objednavka("OBJ-001")
    objednavka.pridej(kniha)
    objednavka.pridej(obal)
    print("Objednávka:", objednavka.cislo, "celkem:", objednavka.celkem())
    kniha.pridej()
    print("Po změně položky:", objednavka.celkem())
