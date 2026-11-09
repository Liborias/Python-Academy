# Pygame-ce importujeme jako pygame; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from podklady import robot, snimky, pas_snimku, tvar, Bod, BARVY, CvicnyRezim, priprav_media
from nahled import karta, obrazky, radek, uloz

class Kamera:
    def __init__(self, vyhled, svet):
        self.vyhled = pygame.Rect(vyhled)
        self.svet = pygame.Rect(svet)
        self.posun = pygame.Vector2(self.svet.topleft)

    def sleduj(self, bod):
        x = bod[0] - self.vyhled.width / 2
        y = bod[1] - self.vyhled.height / 2
        max_x = max(self.svet.left, self.svet.right - self.vyhled.width)
        max_y = max(self.svet.top, self.svet.bottom - self.vyhled.height)
        self.posun.x = max(self.svet.left, min(max_x, x))
        self.posun.y = max(self.svet.top, min(max_y, y))

# Program připraví skutečný PNG; nejde o animované herní okno.
if __name__ == '__main__':
    plocha = karta('Kamera sleduje bod')
    kamera = Kamera((60, 100, 600, 260), (0, 0, 1400, 800))
    kamera.sleduj((760, 450))
    pygame.draw.rect(plocha, (35, 60, 85), kamera.vyhled)
    for i in range(5):
        bod = pygame.Vector2(500 + i * 90, 400) - kamera.posun + kamera.vyhled.topleft
        plocha.blit(robot(BARVY[i % 4]), (round(bod.x), round(bod.y)))
    print('Posun kamery:', tuple(kamera.posun))
    radek(plocha, 'Kamera mění pohled; světové souřadnice robotů zůstávají stejné.')
    uloz(plocha)
