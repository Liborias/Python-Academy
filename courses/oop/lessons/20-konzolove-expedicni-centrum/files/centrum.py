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
        if balik.hmotnost_g > 2000:
            raise ValueError("Cyklodoprava přijímá nejvýš 2000 g")
        return 59


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
        if objednavka.cislo in self._zaznamy:
            raise ValueError("Číslo objednávky už centrum zná")
        expedice = Expedice(balik, doprava)
        stitek = ExpedicniStitek(objednavka.cislo, adresa)
        self.sklad.rezervuj_objednavku(objednavka)
        self._zaznamy[objednavka.cislo] = {"objednavka": objednavka, "expedice": expedice, "stitek": stitek}
        return objednavka.cislo

    def zmen_dopravu(self, cislo, nova):
        zaznam = self._aktivni(cislo)
        return zaznam["expedice"].zmen_dopravu(nova)

    def pridej_poznamku(self, cislo, text):
        zaznam = self._aktivni(cislo)
        return zaznam["stitek"].pridej_poznamku(text)

    def storno(self, cislo):
        self._najdi(cislo)
        return self.sklad.storno(cislo)

    def souhrn(self, cislo):
        zaznam = self._najdi(cislo)
        zbozi = zaznam["objednavka"].celkem()
        doprava = zaznam["expedice"].nabidka()
        stitek = zaznam["stitek"]
        adresa = stitek.adresa
        return {"cislo": stitek.kod, "stav": self.sklad.stav(cislo),
                "zbozi": zbozi, "doprava": doprava, "celkem": zbozi + doprava,
                "balik": zaznam["expedice"].balik.kod,
                "adresa": f"{adresa.ulice}, {adresa.psc} {adresa.mesto}",
                "poznamky": list(stitek.poznamky)}


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
