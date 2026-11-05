import random
from had_kolize import BezpecnyHad
from had_potrava import vyber_potravu


class Partie:
    def __init__(self, body, sirka=20, vyska=16, vyber=random.choice):
        self.had = BezpecnyHad(body, sirka, vyska)
        self.vyber = vyber
        self.skore = 0
        self.potrava = vyber_potravu(self.had, self.vyber)
        if self.potrava is None:
            self.stav = "vyhra"
        else:
            self.stav = "hra"

    def krok(self):
        if self.stav != "hra":
            return self.stav
        try:
            hlava = self.had.krok(self.potrava)
        except ValueError:
            self.stav = "konec"
            return self.stav
        if hlava == self.potrava:
            self.skore += 10
            self.potrava = vyber_potravu(self.had, self.vyber)
            if self.potrava is None:
                self.stav = "vyhra"
        return self.stav


if __name__ == "__main__":
    def prvni(volne):
        return volne[0]
    partie = Partie([(1, 0), (0, 0)], 4, 2, prvni)
    print("Start:", partie.stav, "skóre:", partie.skore)
    for _ in range(2):
        print("Krok:", partie.krok(), "skóre:", partie.skore, "délka:", len(partie.had.body))
