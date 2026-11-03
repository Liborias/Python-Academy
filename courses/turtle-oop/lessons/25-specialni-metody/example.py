class Policka:
    def __init__(self, nazev, knihy):
        self.nazev = nazev
        self.knihy = list(knihy)  # Vlastní seznam, nezávislý na vstupu.

    def __str__(self):
        return f"{self.nazev}, knih: {len(self.knihy)}"

    def __repr__(self):
        return f"Policka(nazev={self.nazev!r}, knihy={self.knihy!r})"

    def __len__(self):
        return len(self.knihy)


policka = Policka("Doma", ["Les", "Řeka"])
print(policka)                    # Čitelný text přes __str__.
print(repr(policka))              # Podrobnosti přes __repr__.
print(len(policka))               # 2 přes __len__.
print([policka])                  # V seznamu se použije repr objektu.
