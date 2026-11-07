from sklad import Sklad
from nakupni_objednavka import NakupniObjednavka


class RezervacniSklad(Sklad):
    def __init__(self):
        super().__init__()
        self._rezervace = {}

    def rezervuj_objednavku(self, objednavka):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def stav(self, cislo):
        if cislo not in self._rezervace:
            raise ValueError("Neznámá objednávka")
        return self._rezervace[cislo]["stav"]

    def storno(self, cislo):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass


if __name__ == "__main__":
    sklad = RezervacniSklad()
    sklad.pridej("KNIHA", "Průvodce Pythonem", 5)
    prvni = NakupniObjednavka("OBJ-1")
    prvni.pridej("KNIHA", "Průvodce Pythonem", 250, 3)
    druha = NakupniObjednavka("OBJ-2")
    druha.pridej("KNIHA", "Průvodce Pythonem", 250, 2)
    print("Po první rezervaci:", sklad.rezervuj_objednavku(prvni))
    print("Po druhé rezervaci:", sklad.rezervuj_objednavku(druha))
    print("Po stornu první:", sklad.storno("OBJ-1"))
    try:
        sklad.storno("OBJ-1")
    except ValueError:
        print("Druhé storno odmítnuto:", sklad.prehled())
    print("Druhá objednávka:", sklad.stav("OBJ-2"))
