class Popisek:
    def cesta(self):
        return ["popisek"]               # Společný základ se použije jednou.


class Ramovani(Popisek):
    def cesta(self):
        return ["rámeček"] + super().cesta()


class Zvyrazneni(Popisek):
    def cesta(self):
        return ["zvýraznění"] + super().cesta()


class Znacka(Ramovani, Zvyrazneni):
    pass


print([trida.__name__ for trida in Znacka.__mro__])
print(Znacka().cesta())                  # Super pokračuje podle MRO Znacka.
print(Ramovani().cesta())                # Samostatná instance má kratší řetězec.
