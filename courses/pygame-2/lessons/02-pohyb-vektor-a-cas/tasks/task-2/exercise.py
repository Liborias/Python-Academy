# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class RizenaLod(ZakladSprite):
    def __init__(self, stred, rychlost):
        raise NotImplementedError("Doplňte podle zadání.")

    def update(self, smer, dt):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = RizenaLod((160, 160), 100)
    objekt.update((3, 4), 1)
    print('Směr 3:4:', tuple(objekt.pozice))
    nahled([objekt], 'Normalizovaný směr')
