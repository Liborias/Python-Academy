class SkladovaKarta:
    def __init__(self, nazev, celkem=0):
        if type(celkem) is not int or celkem < 0:
            raise ValueError("Celkový počet musí být nezáporné celé číslo")
        self.nazev = nazev
        self._celkem = celkem
        self._rezervovano = 0

    @property
    def celkem(self):
        pass

    @property
    def rezervovano(self):
        pass

    @property
    def dostupne(self):
        # Vypočítejte aktuální rozdíl, nic neukládejte navíc.
        pass

    def rezervuj(self, kolik):
        pass

    def uvolni(self, kolik):
        pass


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
