# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class BankaVelikosti:
    def __init__(self, original, zmen):
        self.original = original.copy()
        self.zmen = zmen
        self._obrazy = {}

    def obraz(self, rozmer):
        klic = tuple(rozmer)
        if klic not in self._obrazy:
            self._obrazy[klic] = self.zmen(self.original, klic).copy()
        return self._obrazy[klic].copy()

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Cache změněných rozměrů')
    banka = BankaVelikosti(robot(), pygame.transform.smoothscale)
    a = banka.obraz((32, 32))
    b = banka.obraz([72, 72])
    c = banka.obraz((32, 32))
    obrazky(plocha, [(a, '32 × 32'), (b, '72 × 72'), (c, 'Další kopie 32')])
    print('Rozměry:', a.get_size(), b.get_size(), 'vlastní kopie:', a is not c)
    radek(plocha, 'Klíč tvoří dvojice rozměrů, originál se nedeformuje.')
    uloz(plocha)
