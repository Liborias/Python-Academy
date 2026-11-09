import math
import pygame
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

def na_obrazovku(kamera, bod):
    return pygame.Vector2(bod) - kamera.posun + kamera.vyhled.topleft

def viditelne(objekty, kamera):
    x, y = kamera.posun
    w, h = kamera.vyhled.size
    return [o for o in objekty if o.rect.right > x and o.rect.left < x + w
            and o.rect.bottom > y and o.rect.top < y + h]
