# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class BankaObrazu:
    def __init__(self, nacti):
        self.nacti = nacti
        self._obrazy = {}

    def obraz(self, jmeno):
        if jmeno not in self._obrazy:
            self._obrazy[jmeno] = self.nacti(jmeno).copy()
        return self._obrazy[jmeno].copy()

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Banka obrázků s vlastními kopiemi')
    slozka = priprav_media()
    volani = []

    def nacti(jmeno):
        volani.append(jmeno)
        return pygame.image.load(str(slozka / (jmeno + '.bmp')))
    banka = BankaObrazu(nacti)
    a = banka.obraz('robot')
    b = banka.obraz('robot')
    c = banka.obraz('stit')
    obrazky(plocha, [(a, 'Robot'), (b, 'Další kopie'), (c, 'Jiný zdroj')])
    print('Načtení z disku:', volani)
    radek(plocha, f'Tři požadavky, jen {len(volani)} načtení z disku.')
    uloz(plocha)
