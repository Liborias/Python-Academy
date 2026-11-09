# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota, Hlidac, Kyvac, Lov, Kolo

class Hra:

    def __init__(self, seed=11):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def novy_lov(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def zpracuj(self, udalost):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, dt):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(Hra())
