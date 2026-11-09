# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def vykresli_skupinu(skupina, pozadi):
    vysledek = pozadi.copy()
    skupina.draw(vysledek)
    return vysledek

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    skupina = pygame.sprite.Group(PohyblivaLod((160, 160), (0, 0)))
    pozadi = pygame.Surface((640, 360)); pozadi.fill((20, 30, 45))
    vysledek = vykresli_skupinu(skupina, pozadi)
    pygame.image.save(vysledek, 'nahled.png')
    print('Zdrojový pixel:', tuple(pozadi.get_at((160, 160))), 'výsledný:', tuple(vysledek.get_at((160, 160))))
