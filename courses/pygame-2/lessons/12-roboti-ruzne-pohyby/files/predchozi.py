# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota

class Robot(pygame.sprite.Sprite):
    barva = (55, 205, 177)

    def __init__(self, stred, polomer=22, body=10):
        super().__init__()
        self.radius = polomer
        self.body = body
        self.pozice = pygame.Vector2(stred)
        self.image = obraz_robota(polomer, self.barva)
        self.rect = self.image.get_rect(center=(round(self.pozice.x), round(self.pozice.y)))

    def obsahuje(self, bod):
        rozdil = pygame.Vector2(bod) - self.rect.center
        return rozdil.length_squared() <= self.radius ** 2

    def update(self, dt, hranice):
        # Stojící robot přijímá stejné rozhraní jako budoucí pohyblivé typy.
        pass

def najdi_robota(roboty, bod):
    for robot in reversed(roboty.sprites()):
        if robot.obsahuje(bod):
            return robot
    return None
