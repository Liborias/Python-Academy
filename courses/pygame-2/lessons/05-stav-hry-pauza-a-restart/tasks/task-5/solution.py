# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class NovaHra:
    def __init__(self, tvorba):
        self.tvorba = tvorba
        self.skore = 0
        self.objekty = self.tvorba()

    def restart(self):
        self.objekty = self.tvorba()
        self.skore = 0

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    def tvorba():
        return pygame.sprite.Group(PohyblivaLod((180, 180), (80, 0)))
    hra = NovaHra(tvorba); puvodni = hra.objekty
    hra.skore = 12; hra.restart()
    print('Nová skupina:', hra.objekty is not puvodni, 'skóre:', hra.skore)
    nahled(hra.objekty, 'Restart podle předané funkce')
