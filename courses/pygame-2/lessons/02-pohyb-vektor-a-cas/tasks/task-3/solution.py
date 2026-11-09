# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class OmezenaLod(ZakladSprite):
    def __init__(self, stred, rychlost, hranice):
        super().__init__(stred)
        self.pozice = pygame.Vector2(stred)
        self.rychlost = pygame.Vector2(rychlost)
        self.hranice = hranice.copy()

    def update(self, dt):
        self.pozice += self.rychlost * dt
        self.pozice.x = max(self.hranice.left + 16, min(self.hranice.right - 16, self.pozice.x))
        self.pozice.y = max(self.hranice.top + 12, min(self.hranice.bottom - 12, self.pozice.y))
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = OmezenaLod((550, 180), (200, 0), pygame.Rect(40, 60, 560, 260))
    objekt.update(1)
    print('Zastaveno u pravé hrany:', tuple(objekt.pozice))
    nahled([objekt], 'Celá loď uvnitř hranic')
