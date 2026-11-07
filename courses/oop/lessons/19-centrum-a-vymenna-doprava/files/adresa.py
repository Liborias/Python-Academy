class Adresa:
    def __init__(self, ulice, mesto, psc):
        self.ulice = ulice
        self.mesto = mesto
        self.psc = psc

    def __repr__(self):
        return f"Adresa({self.ulice!r}, {self.mesto!r}, {self.psc!r})"

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return (self.ulice == other.ulice
                and self.mesto == other.mesto
                and self.psc == other.psc)


if __name__ == "__main__":
    prvni = Adresa("Javorová 1", "Brno", "60200")
    druha = Adresa("Javorová 1", "Brno", "60200")
    odkaz = prvni
    print("Dvě instance:", prvni is druha)
    print("Stejné údaje:", prvni == druha)
    print("Tentýž objekt:", prvni is odkaz)
    druha.psc = "60201"
    print("Po opravě PSČ:", prvni == druha)
    print("Původní PSČ:", prvni.psc)
