# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class AnimaceJednou:

    def __init__(self, snimky, trvani):
        raise NotImplementedError('Doplňte podle zadání.')

    def update(self, dt):
        raise NotImplementedError('Doplňte podle zadání.')

    def obraz(self):
        raise NotImplementedError('Doplňte podle zadání.')

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
