# Hmotnost ukládáme v celých gramech a čteme přes property.
# Potomek přidá pokyny a ostatní chování zdědí.
class Balik:
    def __init__(self, kod, hmotnost_g):
        if type(hmotnost_g) is not int or hmotnost_g <= 0:
            raise ValueError("Hmotnost musí být kladný celý počet gramů")
        self.kod = kod
        self._hmotnost_g = hmotnost_g

    @property
    def hmotnost_g(self):
        return self._hmotnost_g

    def popis(self):
        return f"Balík {self.kod}, {self.hmotnost_g} g"


class KrehkyBalik(Balik):
    # Vlastní __init__ nemáme: použije se konstruktor Balik.
    def pokyny(self):
        return "Chránit před nárazy."


if __name__ == "__main__":
    bezny = Balik("B-001", 1200)
    krehky = KrehkyBalik("K-002", 800)
    print(bezny.popis())
    # Zděděná metoda pracuje s údaji křehkého balíku.
    print(krehky.popis())
    print(krehky.pokyny())
    print("Křehký je také balík:", isinstance(krehky, Balik))
