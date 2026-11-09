# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class Tlacitko:
    def __init__(self, rect, text, akce, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.akce = akce
        self.font = font

    def zpracuj(self, udalost):
        if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
            if self.rect.collidepoint(udalost.pos):
                return self.akce
        return None

    def kresli(self, plocha):
        pygame.draw.rect(plocha, (38, 68, 96), self.rect, border_radius=8)
        pygame.draw.rect(plocha, (90, 175, 225), self.rect, 2, border_radius=8)
        napis = self.font.render(self.text, True, (240, 245, 255))
        plocha.blit(napis, napis.get_rect(center=self.rect.center))

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
