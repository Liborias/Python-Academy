from skladova_karta import SkladovaKarta


class Sklad:
    def __init__(self):
        self._karty = {}

    def pridej(self, kod, nazev, celkem):
        # Zabraňte duplicitě, pak přidejte novou platnou kartu.
        pass

    def prehled(self):
        # Vraťte nový slovník kódů a dostupných celých počtů.
        pass

    def rezervuj(self, pozadavek):
        # Nejprve ověřte celý požadavek, pak rezervujte na kartách.
        pass


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
