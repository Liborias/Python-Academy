# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from zdroje import BankaObrazu

def priprav_obrazy(jmena, banka):
    vysledek = {}
    for jmeno in jmena:
        if jmeno not in vysledek:
            vysledek[jmeno] = banka.obraz(jmeno)
    return vysledek

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Příprava sady zdrojů')
    slozka = priprav_media()
    banka = BankaObrazu(lambda j: pygame.image.load(str(slozka / (j + '.bmp'))))
    obrazy = priprav_obrazy(['robot', 'stit', 'robot'], banka)
    obrazky(plocha, [(o, j) for j, o in obrazy.items()])
    print('Jedinečná jména:', list(obrazy))
    radek(plocha, 'Sada má vlastní slovník; opakované jméno načítáme jen jednou.')
    uloz(plocha)
