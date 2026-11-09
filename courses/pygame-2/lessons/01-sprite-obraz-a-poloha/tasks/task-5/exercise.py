# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class Hrac(pygame.sprite.Sprite):
    def __init__(self, stred, skupina):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    skupina = pygame.sprite.Group()
    objekt = Hrac((280, 180), skupina)
    print('Ve skupině:', len(skupina), objekt in skupina)
    nahled(skupina, 'Hráč patří do skupiny')
