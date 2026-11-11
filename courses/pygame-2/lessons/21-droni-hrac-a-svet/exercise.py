# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit

class Hrac(pygame.sprite.Sprite):

    def __init__(self, stred, hranice):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, smer, dt):
        raise NotImplementedError('Doplňte podle zadání projektu.')

class Dron(pygame.sprite.Sprite):
    vzhled = 'dron'

    def __init__(self, stred, rychlost=95):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def cil(self, hrac):
        raise NotImplementedError('Doplňte podle zadání projektu.')

class Svet:

    def __init__(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def seber_data(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, smer, dt):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet))
