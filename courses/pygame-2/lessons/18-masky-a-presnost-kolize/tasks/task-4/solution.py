# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from masky import zasah_maskou

def dvojice_masek(prvni, druhe):
    vysledek = []
    for a in prvni:
        for b in druhe:
            if a is not b and zasah_maskou(a, b):
                vysledek.append((a, b))
    return vysledek

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Dvojice zásahů mezi skupinami')
    a = Bod(tvar(plny=True), (0, 0))
    b = Bod(tvar(plny=True), (40, 0))
    c = Bod(tvar(), (250, 0))
    dvojice = dvojice_masek(pygame.sprite.Group(a, c), pygame.sprite.Group(b, c))
    obrazky(plocha, [(a.image, 'První skupina'), (b.image, 'Druhá skupina')])
    print('Počet skutečných dvojic:', len(dvojice))
    radek(plocha, 'Vlastní sprite proti sobě nepočítáme; skupiny nemažeme.')
    uloz(plocha)
