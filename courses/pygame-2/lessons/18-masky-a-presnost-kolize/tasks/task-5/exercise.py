# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from masky import zasah_maskou

def porovnej_kolize(a, b):
    raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Rect, kruh a maska vedle sebe')
    a = Bod(tvar(), (40, 40), 34)
    b = Bod(robot(rozmer=(20, 20)), (70, 70), 10)
    vysledek = porovnej_kolize(a, b)
    spolu = a.image.copy()
    spolu.blit(b.image, (b.rect.x - a.rect.x, b.rect.y - a.rect.y))
    obrazky(plocha, [(a.image, 'Kruh s otvorem'), (b.image, 'Malý robot'), (spolu, 'Společná poloha')])
    print('Tři pravidla:', vysledek)
    radek(plocha, str(vysledek))
    uloz(plocha)
