# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class Stit(pygame.sprite.Sprite):
    def __init__(self, stred, velikost, barva):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Stit((220, 160), (90, 16), (100, 230, 150))
    print('Štít:', objekt.rect.size, objekt.rect.center)
    nahled([objekt], 'Štít podle parametrů')
