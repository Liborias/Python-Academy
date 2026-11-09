# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from animator import Animace

class AnimovanySprite(pygame.sprite.Sprite):
    def __init__(self, snimky, stred, trvani=0.125):
        super().__init__()
        self.animace = Animace(snimky, trvani)
        self.image = self.animace.obraz()
        self.rect = self.image.get_rect(center=stred)

    def update(self, dt):
        stred = self.rect.center
        self.animace.update(dt)
        self.image = self.animace.obraz()
        self.rect = self.image.get_rect(center=stred)

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Sprite s měnícím se obrázkem')
    objekt = AnimovanySprite(snimky(), (100, 100))
    polozky = []
    for dt in (0, 0.125, 0.125, 0.125):
        objekt.update(dt)
        polozky.append((objekt.image.copy(), str(objekt.rect.center)))
    obrazky(plocha, polozky)
    print('Střed po změnách obrázku:', objekt.rect.center)
    radek(plocha, 'Obrázek se mění; aktuální střed objektu se zachová.')
    uloz(plocha)
