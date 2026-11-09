# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota

class Hlidac(Robot):
    barva = (80, 170, 255)

    def __init__(self, stred, rychlost=(90, 55), polomer=22, body=10):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, dt, hranice):
        raise NotImplementedError('Doplňte podle zadání projektu.')

class Kyvac(Robot):
    barva = (195, 145, 255)

    def __init__(self, stred, amplituda=50, perioda=2, polomer=22, body=20):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, dt, hranice):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(CvicnaHra(Robot, najdi_robota, Hlidac=Hlidac, Kyvac=Kyvac))
