from adresa import Adresa
from balik import Balik
from doprava import OsobniOdber, Kuryr
from expedice import Expedice
from nakupni_objednavka import NakupniObjednavka
from rezervacni_sklad import RezervacniSklad
from stitek import ExpedicniStitek


class Cyklodoprava:
    def __init__(self, zona):
        if not isinstance(zona, str) or not zona.strip():
            raise ValueError("Cyklodoprava potřebuje rozvozovou zónu")
        self._zona = zona

    @property
    def zona(self):
        return self._zona

    def cena(self, balik):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass


class ExpedicniCentrum:
    def __init__(self, sklad):
        self._sklad = sklad
        self._zaznamy = {}

    @property
    def sklad(self):
        return self._sklad

    def _najdi(self, cislo):
        if cislo not in self._zaznamy:
            raise ValueError("Centrum tuto objednávku nezná")
        return self._zaznamy[cislo]

    def _aktivni(self, cislo):
        zaznam = self._najdi(cislo)
        if self.sklad.stav(cislo) != "rezervovana":
            raise ValueError("Stornovanou objednávku nelze měnit")
        return zaznam

    def prijmi(self, objednavka, balik, doprava, adresa):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def zmen_dopravu(self, cislo, nova):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def pridej_poznamku(self, cislo, text):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass

    def storno(self, cislo):
        self._najdi(cislo)
        return self.sklad.storno(cislo)

    def souhrn(self, cislo):
        # Doplňte podle rozhraní vysvětleného v lekci.
        pass


if __name__ == "__main__":
    sklad = RezervacniSklad()
    sklad.pridej("KNIHA", "Průvodce Pythonem", 5)
    centrum = ExpedicniCentrum(sklad)
    objednavka = NakupniObjednavka("OBJ-1")
    objednavka.pridej("KNIHA", "Průvodce Pythonem", 250, 2)
    centrum.prijmi(objednavka, Balik("B-1", 1200), OsobniOdber("Dílna"), Adresa("Javorová 1", "Brno", "60200"))
    print("Kurýr:", centrum.zmen_dopravu("OBJ-1", Kuryr("Javorová 1, Brno")))
    print("Cyklodoprava:", centrum.zmen_dopravu("OBJ-1", Cyklodoprava("Brno-střed")))
    centrum.pridej_poznamku("OBJ-1", "Nezvonit.")
    print("Nabídka:", centrum.souhrn("OBJ-1")["celkem"])
    print("Po stornu:", centrum.storno("OBJ-1"))
    try:
        centrum.zmen_dopravu("OBJ-1", Kuryr("Javorová 1, Brno"))
    except ValueError:
        print("Stornovanou objednávku již neměníme.")
