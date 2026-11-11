# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet, HlidacBodu, posun_drony

class Vlny:

    def __init__(self, seed=23, interval=0.75):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def zahaj(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def pridej(self, hrac, hranice):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, dt, hrac, hranice):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet, posun_drony=posun_drony, HlidacBodu=HlidacBodu, Vlny=Vlny))
