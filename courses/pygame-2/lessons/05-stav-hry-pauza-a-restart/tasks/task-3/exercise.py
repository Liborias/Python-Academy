# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class Zivoty:
    def __init__(self, pocet):
        raise NotImplementedError("Doplňte podle zadání.")

    def zasah(self):
        raise NotImplementedError("Doplňte podle zadání.")

    def restart(self):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Zivoty(3)
    for _ in range(4):
        objekt.zasah(); print('Zbývá životů:', objekt.zbyva)
    objekt.restart(); print('Nový pokus:', objekt.zbyva)
    nahled([ZakladSprite((180 + i * 50, 180)) for i in range(objekt.zbyva)], 'Nový pokus obnoví životy')
