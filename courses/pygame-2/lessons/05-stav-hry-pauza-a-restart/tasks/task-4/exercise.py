# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class Rezimy:
    def __init__(self):
        raise NotImplementedError("Doplňte podle zadání.")

    def zpracuj(self, udalost):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Rezimy()
    for key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_ESCAPE):
        objekt.zpracuj(pygame.event.Event(pygame.KEYDOWN, key=key)); print(objekt.stav)
    nahled([ZakladSprite((280, 180))], 'Menu / hra / pauza')
