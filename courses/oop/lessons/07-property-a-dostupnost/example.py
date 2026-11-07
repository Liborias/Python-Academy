# Model skladu se ovládá přes veřejné metody a vypočítané údaje.
# Ukázka ukazuje skutečný stav před operací i po ní.
class SkladovaKarta:
    def __init__(self, nazev, celkem=0):
        if type(celkem) is not int or celkem < 0:
            raise ValueError("Celkový počet musí být nezáporné celé číslo")
        self.nazev = nazev
        self._celkem = celkem
        self._rezervovano = 0

    @property
    def celkem(self):
        return self._celkem

    @property
    def rezervovano(self):
        return self._rezervovano

    @property
    def dostupne(self):
        return self._celkem - self._rezervovano

    def rezervuj(self, kolik):
        if type(kolik) is not int or kolik <= 0 or kolik > self.dostupne:
            raise ValueError("Neplatná nebo nedostupná rezervace")
        self._rezervovano += kolik
        return self.dostupne

    def uvolni(self, kolik):
        if type(kolik) is not int or kolik <= 0 or kolik > self.rezervovano:
            raise ValueError("Nelze uvolnit tento počet kusů")
        self._rezervovano -= kolik
        return self.dostupne


if __name__ == "__main__":
    karta = SkladovaKarta("Průvodce Pythonem", 5)
    print("Volné kusy:", karta.dostupne)
    print("Po rezervaci:", karta.rezervuj(3))
    print("Celkem a rezervováno:", karta.celkem, karta.rezervovano)
    print("Po uvolnění:", karta.uvolni(1))
    try:
        karta.dostupne = 99
    except AttributeError:
        print("Dostupnost je pouze pro čtení.")
