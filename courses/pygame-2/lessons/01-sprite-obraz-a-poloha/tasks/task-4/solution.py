# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class Prekazka(pygame.sprite.Sprite):
    def __init__(self, obrazek, pozice):
        super().__init__()
        self.image = obrazek.copy()
        self.rect = self.image.get_rect(topleft=pozice)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    zdroj = pygame.Surface((80, 30)); zdroj.fill((180, 120, 240))
    objekt = Prekazka(zdroj, (200, 160))
    print('Levý horní roh:', objekt.rect.topleft)
    nahled([objekt], 'Vlastní kopie obrázku')
