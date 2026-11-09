# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from ovladace import Tlacitko

class Nabidka:
    def __init__(self, tlacitka):
        self.tlacitka = list(tlacitka)

    def zpracuj(self, udalost):
        for tlacitko in reversed(self.tlacitka):
            akce = tlacitko.zpracuj(udalost)
            if akce is not None:
                return akce
        return None

    def update(self, dt):
        pass

    def kresli(self, plocha):
        for tlacitko in self.tlacitka:
            tlacitko.kresli(plocha)

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Nabídka složená z tlačítek')
    pygame.font.init()
    font = pygame.font.Font(None, 26)
    nabidka = Nabidka([Tlacitko((180, 110, 360, 60), 'Nová hra', 'hra', font), Tlacitko((180, 200, 360, 60), 'Konec', 'konec', font)])
    nabidka.kresli(plocha)
    akce = nabidka.zpracuj(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(300, 225)))
    print('Akce nabídky:', akce)
    radek(plocha, 'Nabídka skládá tlačítka místo dědění jejich chování.')
    uloz(plocha)
