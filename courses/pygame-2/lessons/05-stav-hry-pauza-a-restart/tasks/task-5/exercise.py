# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class NovaHra:
    def __init__(self, tvorba):
        raise NotImplementedError("Doplňte podle zadání.")

    def restart(self):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    def tvorba():
        return pygame.sprite.Group(PohyblivaLod((180, 180), (80, 0)))
    hra = NovaHra(tvorba); puvodni = hra.objekty
    hra.skore = 12; hra.restart()
    print('Nová skupina:', hra.objekty is not puvodni, 'skóre:', hra.skore)
    nahled(hra.objekty, 'Restart podle předané funkce')
