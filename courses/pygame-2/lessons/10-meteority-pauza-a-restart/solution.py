# Nová část projektu používá skutečné pygame-ce, bez zvuků a stažených obrázků.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import random
import pygame
from podklady import HRANICE, obraz_lodi, obraz_meteoritu
from sestava import CvicnaHra
from herni_okno import spustit
from bonus import BonusStitu
from predchozi import Hrac, precti_smer, Meteorit, ProudMeteoritu, Zdravi, zpracuj_zasahy, Kolo

class Hra:
    def __init__(self, seed=7):
        self.seed = seed
        self.kolo = Kolo(seed)
        self.bezi = True
        self.pauza = False
        self.restart_povolen = True

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT:
            self.bezi = False
        elif self.bezi and udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_ESCAPE:
                self.bezi = False
            elif udalost.key == pygame.K_r:
                self.kolo = Kolo(self.seed)
                self.pauza = False
            elif udalost.key == pygame.K_p and self.kolo.zdravi.zivoty > 0:
                self.pauza = not self.pauza

    def update(self, smer, dt):
        if self.bezi and not self.pauza and self.kolo.zdravi.zivoty > 0:
            self.kolo.update(smer, dt)

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(Hra(), precti_smer)
