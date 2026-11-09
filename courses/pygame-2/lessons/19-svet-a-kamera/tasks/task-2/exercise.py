# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from kamera import Kamera

def na_obrazovku(kamera, bod):
    raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Ze světa na obrazovku')
    kamera = Kamera((60, 100, 600, 260), (0, 0, 1400, 800))
    kamera.sleduj((760, 450))
    body = [(500, 400), (700, 440), (900, 400)]
    pygame.draw.rect(plocha, (35, 60, 85), kamera.vyhled)
    for bod in body:
        obraz = na_obrazovku(kamera, bod)
        plocha.blit(robot(), (round(obraz.x), round(obraz.y)))
    print('První bod na obrazovce:', tuple(na_obrazovku(kamera, body[0])))
    radek(plocha, 'Odečteme posun, přičteme levý horní roh výhledu.')
    uloz(plocha)
