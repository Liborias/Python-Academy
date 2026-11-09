# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class PohyblivaLod(ZakladSprite):
    def __init__(self, stred, rychlost):
        super().__init__(stred)
        self.pozice = pygame.Vector2(stred)
        self.rychlost = pygame.Vector2(rychlost)

    def update(self, dt):
        self.pozice += self.rychlost * dt
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = PohyblivaLod((120, 180), (80, -20))
    for _ in range(4):
        objekt.update(0.25)
    print('Po sekundě:', tuple(objekt.pozice), objekt.rect.center)
    nahled([objekt], 'Čtyři kroky po čtvrt sekundě')
