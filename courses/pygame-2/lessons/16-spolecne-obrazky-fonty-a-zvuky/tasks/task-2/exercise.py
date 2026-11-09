# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class BankaFontu:

    def __init__(self, vytvor):
        raise NotImplementedError('Doplňte podle zadání.')

    def font(self, velikost):
        raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Cache velikostí fontu')
    pygame.font.init()
    volani = []

    def vytvor(velikost):
        volani.append(velikost)
        return pygame.font.Font(None, velikost)
    banka = BankaFontu(vytvor)
    a = banka.font(24)
    b = banka.font(24)
    c = banka.font(42)
    obrazky(plocha, [(a.render('Dílna', True, (90, 220, 175)), '24 bodů'), (c.render('Dílna', True, (80, 180, 255)), '42 bodů')])
    print('Tentýž font:', a is b, 'vytvořené velikosti:', volani)
    radek(plocha, 'Font stejné velikosti sdílíme; jeho nastavení dál neměníme.')
    uloz(plocha)
