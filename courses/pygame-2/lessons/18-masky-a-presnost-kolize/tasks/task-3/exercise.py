# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

def obnov_masku(sprite, novy_obraz, prah=127):
    raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Maska po změně obrázku')
    a = Bod(tvar(), (100, 100))
    puvodni = a.image.copy()
    obnov_masku(a, pygame.transform.rotate(robot(), 45))
    obrazky(plocha, [(puvodni, 'Původní obraz'), (a.image, 'Nový obraz'), (a.mask.to_surface(), 'Obnovená maska')])
    print('Střed zachován:', a.rect.center, 'maska:', a.mask.get_size())
    radek(plocha, 'Po změně obrázku potřebují rect i maska nová data.')
    uloz(plocha)
