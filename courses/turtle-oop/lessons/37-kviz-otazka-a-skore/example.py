# Kód odděluje pravidla kvízu od vstupu a zdroje otázek.
# Připravené soubory se automaticky kopírují vedle programu.
from dataclasses import dataclass


@dataclass
class Otazka:
    text: str
    spravne: bool


class Kviz:
    def __init__(self, otazky):
        self.otazky = list(otazky)
        self.index = 0
        self.skore = 0

    def aktualni(self):
        if self.index >= len(self.otazky):
            return None
        return self.otazky[self.index]

    def odpovez(self, odpoved):
        if not isinstance(odpoved, bool):
            raise ValueError("Odpověď musí být True nebo False")
        otazka = self.aktualni()
        if otazka is None:
            raise ValueError("Kvíz už skončil")
        spravne = odpoved == otazka.spravne
        if spravne:
            self.skore += 1
        self.index += 1
        return spravne


if __name__ == "__main__":
    kviz = Kviz([Otazka("Seznam lze měnit.", True), Otazka("is porovnává hodnoty.", False)])
    print(kviz.aktualni().text)
    print("První odpověď je správná:", kviz.odpovez(True))
    print("Druhá odpověď je správná:", kviz.odpovez(False))
    print("Skóre:", kviz.skore, "z", kviz.index)
