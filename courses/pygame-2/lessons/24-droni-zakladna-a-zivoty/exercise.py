# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet, HlidacBodu, posun_drony, Vlny

class StitZakladny:

    def __init__(self, kapacita=2.5, obnova=0.5):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, dt, uvnitr):
        raise NotImplementedError('Doplňte podle zadání projektu.')

class Kolo(Svet):

    def __init__(self, seed=23):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, smer, dt):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet, posun_drony=posun_drony, HlidacBodu=HlidacBodu, Vlny=Vlny, Kolo=Kolo))
