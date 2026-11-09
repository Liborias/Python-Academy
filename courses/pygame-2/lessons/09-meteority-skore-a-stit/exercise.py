# Nová část projektu používá skutečné pygame-ce, bez zvuků a stažených obrázků.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import random
import pygame
from podklady import HRANICE, obraz_lodi, obraz_meteoritu
from sestava import CvicnaHra
from herni_okno import spustit
from bonus import BonusStitu
from predchozi import Hrac, precti_smer, Meteorit, ProudMeteoritu, Zdravi, zpracuj_zasahy

class Kolo:
    def __init__(self, seed=7):
        raise NotImplementedError("Doplňte podle zadání projektu.")

    def update(self, smer, dt):
        raise NotImplementedError("Doplňte podle zadání projektu.")

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac, Kolo=Kolo), precti_smer)
