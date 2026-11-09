# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class Zivoty:
    def __init__(self, pocet):
        self.pocatecni = pocet
        self.zbyva = pocet

    def zasah(self):
        self.zbyva = max(0, self.zbyva - 1)

    def restart(self):
        self.zbyva = self.pocatecni

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Zivoty(3)
    for _ in range(4):
        objekt.zasah(); print('Zbývá životů:', objekt.zbyva)
    objekt.restart(); print('Nový pokus:', objekt.zbyva)
    nahled([ZakladSprite((180 + i * 50, 180)) for i in range(objekt.zbyva)], 'Nový pokus obnoví životy')
