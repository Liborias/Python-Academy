# Model skladu se ovládá přes veřejné metody a vypočítané údaje.
# Ukázka ukazuje skutečný stav před operací i po ní.
class Zasoba:
    def __init__(self, nazev, pocet=0):
        if type(pocet) is not int or pocet < 0:
            raise ValueError("Počáteční počet musí být nezáporné celé číslo")
        self.nazev = nazev
        self._pocet = pocet

    def stav(self):
        return self._pocet

    def prijmi(self, kolik):
        if type(kolik) is not int or kolik <= 0:
            raise ValueError("Příjem musí být kladný celý počet")
        self._pocet += kolik
        return self._pocet

    def vydej(self, kolik):
        if type(kolik) is not int or kolik <= 0 or kolik > self._pocet:
            raise ValueError("Neplatný nebo nedostupný výdej")
        self._pocet -= kolik
        return self._pocet


if __name__ == "__main__":
    knihy = Zasoba("Průvodce Pythonem", 5)
    try:
        knihy.vydej(6)
    except ValueError:
        print("Nedostupný výdej odmítnut.")
    print("Po odmítnutí:", knihy.stav())
    print("Výdej posledních kusů:", knihy.vydej(5))
    print("Nový příjem:", knihy.prijmi(2))
