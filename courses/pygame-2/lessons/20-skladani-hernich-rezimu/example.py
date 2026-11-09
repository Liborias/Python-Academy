# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class ZasobnikRezimu:
    def __init__(self, pocatecni):
        self.rezimy = [pocatecni]

    @property
    def aktualni(self):
        return self.rezimy[-1]

    def vloz(self, rezim):
        self.rezimy.append(rezim)

    def odeber(self):
        if len(self.rezimy) == 1:
            return False
        self.rezimy.pop()
        return True

    def zpracuj(self, udalost):
        return self.aktualni.zpracuj(udalost)

    def update(self, dt):
        self.aktualni.update(dt)

    def kresli(self, plocha):
        for rezim in self.rezimy:
            rezim.kresli(plocha)

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
