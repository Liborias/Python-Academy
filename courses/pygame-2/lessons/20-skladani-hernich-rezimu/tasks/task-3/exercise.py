# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class Tlacitko:

    def __init__(self, rect, text, akce, font):
        raise NotImplementedError('Doplňte podle zadání.')

    def zpracuj(self, udalost):
        raise NotImplementedError('Doplňte podle zadání.')

    def kresli(self, plocha):
        raise NotImplementedError('Doplňte podle zadání.')

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Tlačítko vrací akci')
    pygame.font.init()
    font = pygame.font.Font(None, 26)
    tlacitko = Tlacitko((180, 150, 360, 60), 'Spustit dílnu', 'hra', font)
    tlacitko.kresli(plocha)
    akce = tlacitko.zpracuj(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(300, 180)))
    print('Akce kliknutí:', akce)
    radek(plocha, 'Tlačítko vrací požadavek; samo hru nevytváří.')
    uloz(plocha)
