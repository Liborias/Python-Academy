# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def posun_skupinu(skupina, dt):
    raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    skupina = pygame.sprite.Group(PohyblivaLod((120, 150), (80, 0)), PohyblivaLod((320, 220), (-40, 0)))
    print('Středy po půlsekundě:', posun_skupinu(skupina, 0.5))
    nahled(skupina, 'Letka po společné aktualizaci')
