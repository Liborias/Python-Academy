# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class OmezenaLod(ZakladSprite):
    def __init__(self, stred, rychlost, hranice):
        raise NotImplementedError("Doplňte podle zadání.")

    def update(self, dt):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = OmezenaLod((550, 180), (200, 0), pygame.Rect(40, 60, 560, 260))
    objekt.update(1)
    print('Zastaveno u pravé hrany:', tuple(objekt.pozice))
    nahled([objekt], 'Celá loď uvnitř hranic')
