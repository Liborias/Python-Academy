# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota, Hlidac, Kyvac

class Lov:

    def __init__(self, roboty, zivoty=3):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def klik(self, udalost):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def presnost(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(CvicnaHra(Robot, najdi_robota, Hlidac=Hlidac, Kyvac=Kyvac, Lov=Lov))
