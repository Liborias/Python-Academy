# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class PohyblivaLod(ZakladSprite):
    def __init__(self, stred, rychlost):
        raise NotImplementedError("Doplňte podle zadání.")

    def update(self, dt):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = PohyblivaLod((120, 180), (80, -20))
    for _ in range(4):
        objekt.update(0.25)
    print('Po sekundě:', tuple(objekt.pozice), objekt.rect.center)
    nahled([objekt], 'Čtyři kroky po čtvrt sekundě')
