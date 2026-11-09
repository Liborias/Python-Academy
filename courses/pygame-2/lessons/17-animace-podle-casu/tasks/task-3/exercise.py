# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

def vyrez_snimky(pas, sirka):
    raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Výřezy z pásu snímků')
    pas = pas_snimku()
    vysledek = vyrez_snimky(pas, 48)
    obrazky(plocha, [(o, f'Výřez {i}') for i, o in enumerate(vysledek)])
    print('Počet vlastních výřezů:', len(vysledek))
    radek(plocha, 'Subsurface je pohled; copy vytvoří nezávislé pixely.')
    uloz(plocha)
