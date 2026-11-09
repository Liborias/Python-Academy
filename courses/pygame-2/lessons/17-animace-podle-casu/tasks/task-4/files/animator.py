import math
import pygame
class Animace:
    def __init__(self, snimky, trvani):
        if not snimky or trvani <= 0:
            raise ValueError('Animace potřebuje snímky a kladné trvání.')
        self.snimky = tuple(s.copy() for s in snimky)
        self.trvani = trvani
        self.restart()

    def restart(self):
        self.index = 0
        self.zbytek = 0.0

    def update(self, dt):
        celkem = self.zbytek + dt
        kroky = math.floor(celkem / self.trvani + 1e-9)
        self.index = (self.index + kroky) % len(self.snimky)
        self.zbytek = max(0, celkem - kroky * self.trvani)

    def obraz(self):
        return self.snimky[self.index]
