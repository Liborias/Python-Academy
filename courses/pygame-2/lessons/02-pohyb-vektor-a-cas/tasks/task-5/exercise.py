# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class CilovaLod(ZakladSprite):
    def __init__(self, stred, rychlost, cil):
        raise NotImplementedError("Doplňte podle zadání.")

    def update(self, dt):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = CilovaLod((100, 120), 200, (220, 210))
    objekt.update(2)
    print('V cíli:', tuple(objekt.pozice))
    nahled([objekt], 'K cíli bez přeletu')
