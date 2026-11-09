# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from animator import Animace

class StavoveAnimace:
    def __init__(self, animace, pocatecni):
        if pocatecni not in animace:
            raise KeyError(pocatecni)
        self.animace = dict(animace)
        self.stav = pocatecni

    def prepni(self, jmeno):
        if jmeno not in self.animace:
            raise KeyError(jmeno)
        if jmeno == self.stav:
            return False
        self.stav = jmeno
        self.animace[jmeno].restart()
        return True

    def update(self, dt):
        self.animace[self.stav].update(dt)

    def obraz(self):
        return self.animace[self.stav].obraz()

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Animace podle stavu')
    model = StavoveAnimace({'klid': Animace(snimky(2), 0.5), 'beh': Animace(snimky(), 0.125)}, 'klid')
    model.update(0.5)
    a = model.obraz().copy()
    model.prepni('beh')
    model.update(0.25)
    b = model.obraz().copy()
    model.prepni('klid')
    c = model.obraz().copy()
    obrazky(plocha, [(a, 'Klid před změnou'), (b, 'Běh'), (c, 'Nový začátek klidu')])
    print('Aktivní stav:', model.stav)
    radek(plocha, 'Stejný stav se nerestartuje; jiný začíná od nuly.')
    uloz(plocha)
