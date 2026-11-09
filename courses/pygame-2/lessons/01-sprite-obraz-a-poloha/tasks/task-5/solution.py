# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class Hrac(pygame.sprite.Sprite):
    def __init__(self, stred, skupina):
        super().__init__(skupina)
        self.image = pygame.Surface((32, 24), pygame.SRCALPHA)
        self.image.fill((80, 180, 255))
        self.rect = self.image.get_rect(center=stred)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    skupina = pygame.sprite.Group()
    objekt = Hrac((280, 180), skupina)
    print('Ve skupině:', len(skupina), objekt in skupina)
    nahled(skupina, 'Hráč patří do skupiny')
