import pygame

class ZakladSprite(pygame.sprite.Sprite):
    """Připravený vzhled. Pohyb a herní pravidla doplní vlastní třídy."""
    def __init__(self, stred, velikost=(32, 24), barva=(80, 180, 255)):
        super().__init__()
        self.image = pygame.Surface(velikost, pygame.SRCALPHA)
        self.image.fill(barva)
        self.rect = self.image.get_rect(center=(round(stred[0]), round(stred[1])))
