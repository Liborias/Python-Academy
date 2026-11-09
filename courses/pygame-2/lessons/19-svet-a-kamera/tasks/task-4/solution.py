# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from kamera import Kamera

def viditelne(objekty, kamera):
    x, y = kamera.posun
    w, h = kamera.vyhled.size
    return [o for o in objekty if o.rect.right > x and o.rect.left < x + w
            and o.rect.bottom > y and o.rect.top < y + h]

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Výběr viditelných objektů')
    kamera = Kamera((60, 100, 600, 260), (0, 0, 1400, 800))
    kamera.sleduj((760, 450))
    objekty = [Bod(robot(), (x, 410)) for x in (0, 500, 700, 1200)]
    vysledek = viditelne(objekty, kamera)
    obrazky(plocha, [(o.image, str(o.rect.topleft)) for o in vysledek])
    print('Viditelné objekty:', len(vysledek), 'ze', len(objekty))
    radek(plocha, 'Vyřazení pro kreslení nemaže objekty ze světa.')
    uloz(plocha)
