# Nová část projektu používá skutečné pygame-ce, bez zvuků a stažených obrázků.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import random
import pygame
from podklady import HRANICE, obraz_lodi, obraz_meteoritu
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, precti_smer, Meteorit, ProudMeteoritu

class Zdravi:
    def __init__(self, pocet=3, ochrana=1.0):
        raise NotImplementedError("Doplňte podle zadání projektu.")

    def tick(self, dt):
        raise NotImplementedError("Doplňte podle zadání projektu.")

    def zasah(self):
        raise NotImplementedError("Doplňte podle zadání projektu.")

def zpracuj_zasahy(hrac, proud, zdravi):
    raise NotImplementedError("Doplňte podle zadání projektu.")

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac, ProudMeteoritu=ProudMeteoritu, Zdravi=Zdravi, zpracuj_zasahy=zpracuj_zasahy), precti_smer)
