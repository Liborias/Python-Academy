# Model skladu se ovládá přes veřejné metody a vypočítané údaje.
# Ukázka ukazuje skutečný stav před operací i po ní.
class Zasoba:
    def __init__(self, nazev, pocet=0):
        self.nazev = nazev
        self._pocet = pocet

    def stav(self):
        return self._pocet

    def prijmi(self, kolik):
        self._pocet += kolik
        return self._pocet

    def vydej(self, kolik):
        self._pocet -= kolik
        return self._pocet


if __name__ == "__main__":
    knihy = Zasoba("Průvodce Pythonem", 5)
    obaly = Zasoba("Dárkový obal", 2)
    print("Na začátku:", knihy.stav())
    print("Po příjmu:", knihy.prijmi(3))
    print("Po výdeji:", knihy.vydej(2))
    print("Obaly zůstaly:", obaly.stav())
