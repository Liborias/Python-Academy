import math
import pygame
class BankaObrazu:
    def __init__(self, nacti):
        self.nacti = nacti
        self._obrazy = {}

    def obraz(self, jmeno):
        if jmeno not in self._obrazy:
            self._obrazy[jmeno] = self.nacti(jmeno).copy()
        return self._obrazy[jmeno].copy()
