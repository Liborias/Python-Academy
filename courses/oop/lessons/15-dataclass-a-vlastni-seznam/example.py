# Dataclass připraví konstruktor, repr a hodnotovou rovnost.
# default_factory vytvoří seznam při každém vynechání argumentu.
from dataclasses import dataclass, field
from adresa import Adresa


@dataclass
class ExpedicniStitek:
    kod: str
    adresa: Adresa
    poznamky: list[str] = field(default_factory=list)

    def pridej_poznamku(self, text):
        self.poznamky.append(text)
        return len(self.poznamky)


if __name__ == "__main__":
    adresa = Adresa("Javorová 1", "Brno", "60200")
    prvni = ExpedicniStitek("E-001", adresa)
    druhy = ExpedicniStitek("E-002", adresa)
    print("Poznámek po zápisu:", prvni.pridej_poznamku("Nezvonit."))
    print("První poznámky:", prvni.poznamky)
    print("Druhý štítek:", druhy.poznamky)
    stejny = ExpedicniStitek("E-001", Adresa("Javorová 1", "Brno", "60200"), ["Nezvonit."])
    print("Shodná data:", prvni == stejny)
    print("Záznam:", prvni)
