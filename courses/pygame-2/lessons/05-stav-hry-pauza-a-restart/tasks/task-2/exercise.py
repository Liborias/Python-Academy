# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class Casovac:
    def __init__(self, limit):
        raise NotImplementedError("Doplňte podle zadání.")

    def update(self, dt):
        raise NotImplementedError("Doplňte podle zadání.")

    def restart(self):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Casovac(1)
    for _ in range(5):
        print('Vypršel právě teď:', objekt.update(0.25), 'zbývá:', objekt.zbyva)
    nahled([ZakladSprite((260, 180))], 'Časovač hlásí dokončení pouze jednou')
