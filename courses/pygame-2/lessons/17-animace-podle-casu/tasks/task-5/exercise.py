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
        raise NotImplementedError('Doplňte podle zadání.')

    def prepni(self, jmeno):
        raise NotImplementedError('Doplňte podle zadání.')

    def update(self, dt):
        raise NotImplementedError('Doplňte podle zadání.')

    def obraz(self):
        raise NotImplementedError('Doplňte podle zadání.')

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
