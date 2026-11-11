# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet, HlidacBodu, posun_drony, Vlny, StitZakladny, Kolo
from zasobnik import ZasobnikRezimu
from sceny import Menu, Let, PauzaLetu, Vysledek

class Hra:

    def __init__(self, seed=23):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    @property
    def stav(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def novy_let(self):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def zpracuj(self, udalost):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def update(self, smer, dt):
        raise NotImplementedError('Doplňte podle zadání projektu.')

    def kresli(self, plocha):
        raise NotImplementedError('Doplňte podle zadání projektu.')

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(Hra())
