# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class RizenaLod(ZakladSprite):
    def __init__(self, stred, rychlost):
        super().__init__(stred)
        self.pozice = pygame.Vector2(stred)
        self.rychlost = rychlost

    def update(self, smer, dt):
        vektor = pygame.Vector2(smer)
        if vektor.length_squared() > 0:
            vektor = vektor.normalize()
        self.pozice += vektor * self.rychlost * dt
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = RizenaLod((160, 160), 100)
    objekt.update((3, 4), 1)
    print('Směr 3:4:', tuple(objekt.pozice))
    nahled([objekt], 'Normalizovaný směr')
