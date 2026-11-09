import pygame
from zaklad import ZakladSprite


class PohyblivaLod(ZakladSprite):
    def __init__(self, stred, rychlost):
        super().__init__(stred)
        self.pozice = pygame.Vector2(stred)
        self.rychlost = pygame.Vector2(rychlost)

    def update(self, dt):
        self.pozice += self.rychlost * dt
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))
