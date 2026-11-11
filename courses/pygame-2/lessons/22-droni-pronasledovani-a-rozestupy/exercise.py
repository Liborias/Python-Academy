# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet

class HlidacBodu(Dron):
    vzhled = 'hlidac'

    def __init__(self, stred, rychlost=80, dosah=160):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def cil(self, hrac):
        raise NotImplementedError('Doplňte podle zadání projektu.')

def posun_drony(drony, hrac, dt, hranice, rozestup=42):
    raise NotImplementedError('Doplňte podle zadání projektu.')

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet, posun_drony=posun_drony, HlidacBodu=HlidacBodu))
