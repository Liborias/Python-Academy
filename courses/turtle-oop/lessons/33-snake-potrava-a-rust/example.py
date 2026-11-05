# Ukázka navazuje na předchozí moduly projektu Snake.
# Připravené pomocné soubory leží vedle tohoto programu.
import random
from had_model import Had


class HladovyHad(Had):
    def krok(self, potrava=None):
        ocas = self.body[-1]
        nova = super().krok()
        if nova == potrava:
            self.body.append(ocas)
        return nova


def vyber_potravu(had, vyber=random.choice):
    volne = []
    for y in range(had.vyska):
        for x in range(had.sirka):
            if (x, y) not in had.body:
                volne.append((x, y))
    if not volne:
        return None
    return vyber(volne)


if __name__ == "__main__":
    had = HladovyHad([(4, 1), (3, 1), (2, 1)], 6, 4)
    print("Nová hlava:", had.krok((5, 1)), "délka:", len(had.body))
    print("Přes okraj:", had.krok(), "délka:", len(had.body))
