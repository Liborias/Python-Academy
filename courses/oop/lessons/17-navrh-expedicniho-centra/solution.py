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
        if self.uzavrena:
            raise ValueError("Uzavřenou objednávku nelze upravit")
        if not isinstance(kod, str) or not kod.strip() or not isinstance(nazev, str) or not nazev.strip():
            raise ValueError("Vyplňte kód a název zboží")
        if type(cena) is not int or cena < 0 or type(pocet) is not int or pocet <= 0:
            raise ValueError("Cena musí být nezáporný int a počet kladný int")
        vysledek = self._model.pridej(Polozka(nazev, cena, pocet))
        self._pozadavek[kod] = self._pozadavek.get(kod, 0) + pocet
        return vysledek

    def celkem(self):
        return self._model.celkem()

    def pozadavek(self):
        return dict(self._pozadavek)

    def uzavri(self):
        if self.uzavrena or not self._pozadavek:
            raise ValueError("Uzavřít lze jen neprázdnou otevřenou objednávku")
        self._uzavrena = True


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
