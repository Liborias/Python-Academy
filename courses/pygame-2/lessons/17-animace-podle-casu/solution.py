# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

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

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Animace ve smyčce')
    animace = Animace(snimky(), 0.25)
    polozky = []
    for dt in (0, 0.25, 0.5, 0.25):
        animace.update(dt)
        polozky.append((animace.obraz().copy(), f'index {animace.index}'))
    obrazky(plocha, polozky)
    print('Index:', animace.index, 'zbytek:', animace.zbytek)
    radek(plocha, 'Čtyři fáze pokusu vedle sebe; PNG samo není animace.')
    uloz(plocha)
