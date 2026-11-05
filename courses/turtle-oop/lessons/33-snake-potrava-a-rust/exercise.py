import random
from had_model import Had


class HladovyHad(Had):
    def krok(self, potrava=None):
        # Využijte základní krok a při snědení potravy zachovejte ocas.
        pass


def vyber_potravu(had, vyber=random.choice):
    # Připravte všechny volné buňky. Při plné ploše vraťte None.
    pass


if __name__ == "__main__":
    had = HladovyHad([(4, 1), (3, 1), (2, 1)], 6, 4)
    print("Nová hlava:", had.krok((5, 1)), "délka:", len(had.body))
    print("Přes okraj:", had.krok(), "délka:", len(had.body))
