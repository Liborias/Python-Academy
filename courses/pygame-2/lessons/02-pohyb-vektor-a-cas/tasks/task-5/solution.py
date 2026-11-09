# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class CilovaLod(ZakladSprite):
    def __init__(self, stred, rychlost, cil):
        super().__init__(stred)
        self.pozice = pygame.Vector2(stred)
        self.rychlost = rychlost
        self.cil = pygame.Vector2(cil)

    def update(self, dt):
        rozdil = self.cil - self.pozice
        vzdalenost = rozdil.length()
        krok = self.rychlost * dt
        if vzdalenost <= krok:
            self.pozice = self.cil.copy()
        elif vzdalenost > 0:
            self.pozice += rozdil / vzdalenost * krok
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = CilovaLod((100, 120), 200, (220, 210))
    objekt.update(2)
    print('V cíli:', tuple(objekt.pozice))
    nahled([objekt], 'K cíli bez přeletu')
