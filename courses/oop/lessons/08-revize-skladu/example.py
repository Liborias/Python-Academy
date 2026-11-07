# Model skladu se ovládá přes veřejné metody a vypočítané údaje.
# Ukázka ukazuje skutečný stav před operací i po ní.
from skladova_karta import SkladovaKarta


class Sklad:
    def __init__(self):
        self._karty = {}

    def pridej(self, kod, nazev, celkem):
        if kod in self._karty:
            raise ValueError("Kód už ve skladu existuje")
        karta = SkladovaKarta(nazev, celkem)
        self._karty[kod] = karta
        return karta.dostupne

    def prehled(self):
        vysledek = {}
        for kod, karta in self._karty.items():
            vysledek[kod] = karta.dostupne
        return vysledek

    def rezervuj(self, pozadavek):
        for kod, kolik in pozadavek.items():
            if kod not in self._karty or type(kolik) is not int or kolik <= 0:
                raise ValueError("Neplatný požadavek")
            if kolik > self._karty[kod].dostupne:
                raise ValueError("Nedostatek kusů")
        for kod, kolik in pozadavek.items():
            self._karty[kod].rezervuj(kolik)
        return self.prehled()


if __name__ == "__main__":
    sklad = Sklad()
    sklad.pridej("KNIHA", "Průvodce Pythonem", 5)
    sklad.pridej("OBAL", "Dárkový obal", 2)
    print("Před rezervací:", sklad.prehled())
    try:
        sklad.rezervuj({"KNIHA": 2, "OBAL": 3})
    except ValueError:
        print("Po odmítnutí:", sklad.prehled())
    print("Po úspěchu:", sklad.rezervuj({"KNIHA": 2, "OBAL": 1}))
    kopie = sklad.prehled()
    kopie["KNIHA"] = 999
    print("Skutečný sklad:", sklad.prehled())
