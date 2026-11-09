# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz
from kamera import Kamera

def do_sveta(kamera, bod):
    return pygame.Vector2(bod) + kamera.posun - kamera.vyhled.topleft

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Z obrazovky zpět do světa')
    kamera = Kamera((60, 100, 600, 260), (0, 0, 1400, 800))
    kamera.sleduj((760, 450))
    bod = do_sveta(kamera, (300, 230))
    pygame.draw.rect(plocha, (35, 60, 85), kamera.vyhled)
    pygame.draw.circle(plocha, (100, 230, 180), (300, 230), 12)
    print('Kliknutí ve světě:', tuple(bod))
    radek(plocha, f'Obrazovka (300, 230) odpovídá světovému bodu {tuple(bod)}.')
    uloz(plocha)
