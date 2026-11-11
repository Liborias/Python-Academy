import pygame

class BankaObrazu:
    def __init__(self, nacti):
        self.nacti = nacti
        self._obrazy = {}

    def obraz(self, jmeno):
        if jmeno not in self._obrazy:
            self._obrazy[jmeno] = self.nacti(jmeno).copy()
        return self._obrazy[jmeno].copy()

class BankaFontu:
    def __init__(self, vytvor):
        self.vytvor = vytvor
        self._fonty = {}

    def font(self, velikost):
        if velikost not in self._fonty:
            self._fonty[velikost] = self.vytvor(velikost)
        return self._fonty[velikost]
