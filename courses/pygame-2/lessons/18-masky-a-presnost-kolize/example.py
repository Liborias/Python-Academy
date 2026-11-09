# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class MaskovySprite(pygame.sprite.Sprite):
    def __init__(self, obraz, roh, prah=127):
        super().__init__()
        self.image = obraz.copy()
        self.rect = self.image.get_rect(topleft=roh)
        self.mask = pygame.mask.from_surface(self.image, prah)

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Sprite s vlastní maskou')
    a = MaskovySprite(tvar(), (0, 0))
    b = MaskovySprite(tvar(plny=True), (0, 0))
    obrazky(plocha, [(a.image, 'Průhledný střed'), (a.mask.to_surface(), 'Maska kruhu'), (b.image, 'Plný terč'), (b.mask.to_surface(), 'Maska terče')])
    print('Pevné pixely:', a.mask.count(), b.mask.count())
    radek(plocha, 'Maska počítá neprůhledné pixely podle prahu alfa kanálu.')
    uloz(plocha)
