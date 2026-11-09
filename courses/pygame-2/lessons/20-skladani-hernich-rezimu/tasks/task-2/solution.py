# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class Pauza:
    def __init__(self, font):
        self.font = font

    def zpracuj(self, udalost):
        if udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_p:
            return 'zpet'
        return None

    def update(self, dt):
        pass

    def kresli(self, plocha):
        vrstva = pygame.Surface(plocha.get_size(), pygame.SRCALPHA)
        vrstva.fill((10, 18, 30, 170))
        napis = self.font.render('PAUZA', True, (240, 245, 255))
        vrstva.blit(napis, napis.get_rect(center=vrstva.get_rect().center))
        plocha.blit(vrstva, (0, 0))

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Průhledná pauza')
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    obsah = pygame.Surface((640, 260))
    CvicnyRezim('Podklad hry').kresli(obsah)
    pauza = Pauza(font)
    pauza.kresli(obsah)
    plocha.blit(obsah, (40, 85))
    print('Pokračování:', pauza.zpracuj(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)))
    radek(plocha, 'Pauza je průhledná vrstva; sama neposouvá model hry.')
    uloz(plocha)
