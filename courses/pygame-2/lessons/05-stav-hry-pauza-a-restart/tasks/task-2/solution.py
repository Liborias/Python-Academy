# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class Casovac:
    def __init__(self, limit):
        self.limit = limit
        self.zbyva = limit

    def update(self, dt):
        pred = self.zbyva
        self.zbyva = max(0, self.zbyva - dt)
        return pred > 0 and self.zbyva == 0

    def restart(self):
        self.zbyva = self.limit

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Casovac(1)
    for _ in range(5):
        print('Vypršel právě teď:', objekt.update(0.25), 'zbývá:', objekt.zbyva)
    nahled([ZakladSprite((260, 180))], 'Časovač hlásí dokončení pouze jednou')
