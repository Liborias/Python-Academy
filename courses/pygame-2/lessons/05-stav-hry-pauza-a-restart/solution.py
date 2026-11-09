# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

class HerniStav:
    def __init__(self):
        self.bezi = True
        self.pauza = False

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT:
            self.bezi = False
        elif self.bezi and udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_p:
            self.pauza = not self.pauza

    def update(self, skupina, dt):
        if self.bezi and not self.pauza:
            skupina.update(dt)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    stav = HerniStav(); skupina = pygame.sprite.Group(PohyblivaLod((120, 180), (80, 0)))
    stav.update(skupina, 0.5)
    stav.zpracuj(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    stav.update(skupina, 2)
    print('Pauza:', stav.pauza, 'střed:', next(iter(skupina)).rect.center)
    nahled(skupina, 'Pauza: dvě sekundy bez pohybu')
