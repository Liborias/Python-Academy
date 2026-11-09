# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled

class Meteorit(pygame.sprite.Sprite):
    def __init__(self, stred, polomer):
        super().__init__()
        self.image = pygame.Surface((2 * polomer, 2 * polomer), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (235, 145, 75), (polomer, polomer), polomer)
        self.rect = self.image.get_rect(center=stred)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    objekt = Meteorit((240, 180), 22)
    print('Obdélník kruhu:', objekt.rect)
    nahled([objekt], 'Meteorit: obraz a obdélník')
