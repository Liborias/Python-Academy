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
        # Vraťte další Otazka, nebo None při dokončení.
        pass

    def odpovez(self, odpoved):
        # Přijměte jen bool, vyhodnoťte odpověď a posuňte se o otázku.
        pass


if __name__ == "__main__":
    kviz = Kviz([Otazka("Seznam lze měnit.", True), Otazka("is porovnává hodnoty.", False)])
    print(kviz.aktualni().text)
    print("První odpověď je správná:", kviz.odpovez(True))
    print("Druhá odpověď je správná:", kviz.odpovez(False))
    print("Skóre:", kviz.skore, "z", kviz.index)
