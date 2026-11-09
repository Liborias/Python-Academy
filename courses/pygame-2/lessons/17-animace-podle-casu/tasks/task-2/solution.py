# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class AnimaceJednou:
    def __init__(self, snimky, trvani):
        if not snimky or trvani <= 0:
            raise ValueError('Animace potřebuje snímky a kladné trvání.')
        self.snimky = tuple(s.copy() for s in snimky)
        self.trvani = trvani
        self.cas = 0.0
        self.index = 0
        self.hotovo = False

    def update(self, dt):
        if self.hotovo:
            return
        self.cas += dt
        kroky = math.floor(self.cas / self.trvani + 1e-9)
        self.index = min(kroky, len(self.snimky) - 1)
        self.hotovo = kroky >= len(self.snimky)

    def obraz(self):
        return self.snimky[self.index]

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Animace přehraná jednou')
    animace = AnimaceJednou(snimky(), 0.25)
    polozky = []
    for dt in (0, 0.5, 0.25, 0.25):
        animace.update(dt)
        polozky.append((animace.obraz().copy(), f'{animace.index} / {animace.hotovo}'))
    obrazky(plocha, polozky)
    print('Poslední index:', animace.index, 'hotovo:', animace.hotovo)
    radek(plocha, 'Poslední snímek také trvá celou čtvrtsekundu; potom zůstane.')
    uloz(plocha)
