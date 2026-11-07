from dataclasses import dataclass, field
from adresa import Adresa


# Doplňte dataclass a vlastní výchozí seznam poznámek.
class ExpedicniStitek:
    kod: str
    adresa: Adresa
    poznamky: list[str] = None

    def pridej_poznamku(self, text):
        # Přidejte poznámku a vraťte nový počet.
        pass


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
