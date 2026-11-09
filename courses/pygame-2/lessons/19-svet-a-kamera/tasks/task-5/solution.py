# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from kamera import Kamera, na_obrazovku, viditelne

def vykresli_svet(plocha, objekty, kamera):
    puvodni = plocha.get_clip()
    try:
        plocha.set_clip(puvodni.clip(kamera.vyhled))
        for objekt in viditelne(objekty, kamera):
            bod = na_obrazovku(kamera, objekt.rect.topleft)
            plocha.blit(objekt.image, (round(bod.x), round(bod.y)))
    finally:
        plocha.set_clip(puvodni)

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Kreslení s ořezem výhledu')
    kamera = Kamera((60, 100, 600, 260), (0, 0, 1400, 800))
    kamera.sleduj((760, 450))
    objekty = [Bod(robot(BARVY[i % 4]), (x, 410)) for i, x in enumerate((430, 500, 700, 1030))]
    pygame.draw.rect(plocha, (35, 60, 85), kamera.vyhled)
    vykresli_svet(plocha, objekty, kamera)
    print('Původní světové polohy:', [o.rect.topleft for o in objekty])
    radek(plocha, 'Clip chrání okolí výhledu a obnoví se po dokončení kreslení.')
    uloz(plocha)
