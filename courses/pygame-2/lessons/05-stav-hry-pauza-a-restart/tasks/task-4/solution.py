# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class Rezimy:
    def __init__(self):
        self.stav = 'menu'

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT:
            self.stav = 'konec'
        elif udalost.type == pygame.KEYDOWN:
            if self.stav == 'menu' and udalost.key == pygame.K_RETURN:
                self.stav = 'hra'
            elif udalost.key == pygame.K_ESCAPE and self.stav in ('hra', 'pauza'):
                self.stav = 'pauza' if self.stav == 'hra' else 'hra'

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Rezimy()
    for key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_ESCAPE):
        objekt.zpracuj(pygame.event.Event(pygame.KEYDOWN, key=key)); print(objekt.stav)
    nahled([ZakladSprite((280, 180))], 'Menu / hra / pauza')
