# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class Zvuky:

    def __init__(self, vytvor, povoleno=True):
        raise NotImplementedError('Doplňte podle zadání.')

    def prehraj(self, jmeno, hlasitost=0.3):
        raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Zvuk s bezpečným vypnutím')

    def vytvor(jmeno):
        return pygame.mixer.Sound(str(priprav_media() / 'ton.wav'))
    zvuky = Zvuky(vytvor, povoleno=False)
    prijato = zvuky.prehraj('ton', 0.2)
    obrazky(plocha, [(robot((195, 145, 255)), 'Zvuk je vypnutý')])
    print('Přehrání přijato:', prijato)
    radek(plocha, 'Bez zařízení pokračujeme. Volitelně: python prehraj_ton.py --play')
    uloz(plocha)
