from objednavka import Objednavka
from polozka import Polozka


class NakupniObjednavka:
    def __init__(self, cislo):
        if not isinstance(cislo, str) or not cislo.strip():
            raise ValueError("Objednávka potřebuje číslo")
        self._model = Objednavka(cislo)
        self._pozadavek = {}
        self._uzavrena = False

    @property
    def cislo(self):
        return self._model.cislo

    @property
    def uzavrena(self):
        return self._uzavrena

    def pridej(self, kod, nazev, cena, pocet=1):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def celkem(self):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def pozadavek(self):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def uzavri(self):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass


if __name__ == "__main__":
    objednavka = NakupniObjednavka("OBJ-1")
    objednavka.pridej("KNIHA", "Průvodce Pythonem", 250, 2)
    objednavka.pridej("KNIHA", "Průvodce Pythonem", 250)
    objednavka.pridej("OBAL", "Dárkový obal", 30)
    print("Zboží celkem:", objednavka.celkem())
    print("Požadavek:", objednavka.pozadavek())
    kopie = objednavka.pozadavek()
    kopie["KNIHA"] = 99
    objednavka.uzavri()
    try:
        objednavka.pridej("OBAL", "Dárkový obal", 30)
    except ValueError:
        print("Po uzavření:", objednavka.pozadavek())
