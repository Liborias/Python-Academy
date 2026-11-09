# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def sloucene_skupiny(prvni, druha):
    raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    a = PohyblivaLod((180, 180), (0, 0)); b = PohyblivaLod((360, 180), (0, 0))
    prvni = pygame.sprite.Group(a); druha = pygame.sprite.Group(a, b)
    vysledek = sloucene_skupiny(prvni, druha)
    print('Unikátní objekty:', len(vysledek))
    nahled(vysledek, 'Sdílená loď se nekopíruje')
