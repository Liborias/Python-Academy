# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit

class Robot(pygame.sprite.Sprite):
    barva = (55, 205, 177)

    def __init__(self, stred, polomer=22, body=10):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def obsahuje(self, bod):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, dt, hranice):
        pass

def najdi_robota(roboty, bod):
    raise NotImplementedError('Doplňte podle zadání projektu.')

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(CvicnaHra(Robot, najdi_robota))
