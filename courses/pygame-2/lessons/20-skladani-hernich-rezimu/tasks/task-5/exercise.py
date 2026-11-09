# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from rezimy import ZasobnikRezimu, Pauza, Tlacitko, Nabidka

class RidicScen:

    def __init__(self, zasobnik, vytvor):
        raise NotImplementedError('Doplňte podle zadání.')

    def zpracuj(self, udalost):
        raise NotImplementedError('Doplňte podle zadání.')

    def update(self, dt):
        raise NotImplementedError('Doplňte podle zadání.')

    def kresli(self, plocha):
        raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Řidič přechodů mezi režimy')
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    def vytvor(jmeno):
        return Pauza(font) if jmeno == 'pauza' else CvicnyRezim(jmeno)
    hra = CvicnyRezim('Podklad hry')
    ridic = RidicScen(ZasobnikRezimu(hra), vytvor)
    ridic.update(0.5)
    ridic.zpracuj(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    ridic.update(3)
    obsah = pygame.Surface((640, 260))
    ridic.kresli(obsah)
    plocha.blit(obsah, (40, 85))
    print('Zamrzlý čas hry:', hra.cas)
    radek(plocha, 'Živá verze po uložení Úkolu 5: python ziva_dilna.py')
    uloz(plocha)
