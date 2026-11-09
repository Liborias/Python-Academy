# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class ZrychlujiciLod(ZakladSprite):
    def __init__(self, stred, rychlost, zrychleni):
        super().__init__(stred)
        self.pozice = pygame.Vector2(stred)
        self.rychlost = pygame.Vector2(rychlost)
        self.zrychleni = pygame.Vector2(zrychleni)

    def update(self, dt):
        self.rychlost += self.zrychleni * dt
        self.pozice += self.rychlost * dt
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = ZrychlujiciLod((120, 180), (0, 0), (80, 0))
    objekt.update(0.5); objekt.update(0.5)
    print('Rychlost:', tuple(objekt.rychlost), 'poloha:', tuple(objekt.pozice))
    nahled([objekt], 'Dva kroky zrychlení')
