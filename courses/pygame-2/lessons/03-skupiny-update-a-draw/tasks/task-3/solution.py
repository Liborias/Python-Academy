# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def vyrad_mimo(skupina, hranice):
    pocet = 0
    for objekt in skupina.sprites():
        if not objekt.rect.colliderect(hranice):
            objekt.kill()
            pocet += 1
    return pocet

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    skupina = pygame.sprite.Group(PohyblivaLod((120, 160), (0, 0)), PohyblivaLod((700, 160), (0, 0)))
    print('Vyřazeno:', vyrad_mimo(skupina, pygame.Rect(0, 60, 640, 300)))
    nahled(skupina, 'Objekty, které ještě zasahují do plochy')
