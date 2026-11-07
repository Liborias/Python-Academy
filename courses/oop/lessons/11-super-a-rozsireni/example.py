# Ceny jsou celé koruny, hmotnosti celé gramy.
# Výpočet nabídky nic neodesílá a nemění zásoby.
from balik import Balik
from doprava import Kuryr


class ExpresniKuryr(Kuryr):
    def __init__(self, adresa, termin, priplatek=50, limit_g=5000):
        if termin not in ("dopoledne", "odpoledne"):
            raise ValueError("Vyberte dopoledne nebo odpoledne")
        if type(priplatek) is not int or priplatek < 0:
            raise ValueError("Příplatek musí být nezáporný celý počet korun")
        # Základní konstruktor nastaví adresu a limit této instance.
        super().__init__(adresa, limit_g)
        self._termin = termin
        self._priplatek = priplatek

    @property
    def termin(self):
        return self._termin

    @property
    def priplatek(self):
        return self._priplatek

    def cena(self, balik):
        # Základ hlídá limit; jeho případná výjimka výpočet přeruší.
        return super().cena(balik) + self.priplatek


if __name__ == "__main__":
    expres = ExpresniKuryr("Javorová 1, Brno", "dopoledne")
    print("Termín:", expres.termin)
    print("Cena expresu:", expres.cena(Balik("B-001", 1200)))
    try:
        expres.cena(Balik("B-002", 5001))
    except ValueError:
        print("Expresní limit zůstal v platnosti.")
