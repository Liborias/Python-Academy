# Nová část projektu používá skutečné pygame-ce, bez zvuků a stažených obrázků.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import random
import pygame
from podklady import HRANICE, obraz_lodi, obraz_meteoritu
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, precti_smer

class Meteorit(pygame.sprite.Sprite):
    def __init__(self, stred, polomer, rychlost):
        raise NotImplementedError("Doplňte podle zadání projektu.")

    def update(self, dt):
        raise NotImplementedError("Doplňte podle zadání projektu.")

class ProudMeteoritu:
    def __init__(self, rng, interval=0.65):
        raise NotImplementedError("Doplňte podle zadání projektu.")

    def vytvor(self, hranice):
        raise NotImplementedError("Doplňte podle zadání projektu.")

    def update(self, dt, hranice):
        raise NotImplementedError("Doplňte podle zadání projektu.")

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac, ProudMeteoritu=ProudMeteoritu), precti_smer)
