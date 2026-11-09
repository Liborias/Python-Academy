# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class Lod(pygame.sprite.Sprite):
    def __init__(self, stred):
        raise NotImplementedError("Doplňte podle zadání.")

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    loď = Lod((180, 170))
    print('Rozměr:', loď.image.get_size(), 'střed:', loď.rect.center)
    nahled([loď], 'První loď')
