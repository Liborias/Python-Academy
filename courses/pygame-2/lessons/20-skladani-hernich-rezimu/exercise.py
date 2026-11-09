# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class ZasobnikRezimu:

    def __init__(self, pocatecni):
        raise NotImplementedError('Doplňte podle zadání.')

    @property
    def aktualni(self):
        raise NotImplementedError('Doplňte podle zadání.')

    def vloz(self, rezim):
        raise NotImplementedError('Doplňte podle zadání.')

    def odeber(self):
        raise NotImplementedError('Doplňte podle zadání.')

    def zpracuj(self, udalost):
        raise NotImplementedError('Doplňte podle zadání.')

    def update(self, dt):
        raise NotImplementedError('Doplňte podle zadání.')

    def kresli(self, plocha):
        raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Zásobník herních režimů')
    hra = CvicnyRezim('Podklad hry')
    zasobnik = ZasobnikRezimu(hra)
    zasobnik.update(0.5)
    zasobnik.vloz(CvicnyRezim('Vrchní režim', (55, 40, 90)))
    zasobnik.update(0.25)
    obsah = pygame.Surface((640, 260))
    zasobnik.kresli(obsah)
    plocha.blit(obsah, (40, 85))
    print('Čas podkladu:', hra.cas, 'čas vrchu:', zasobnik.aktualni.cas)
    radek(plocha, 'Aktualizuje se jen vršek; vykreslí se všechny vrstvy odspodu.')
    uloz(plocha)
