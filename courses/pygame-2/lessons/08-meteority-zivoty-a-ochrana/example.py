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
        self.zivoty = pocet
        self.ochrana = ochrana
        self.nezranitelnost = 0.0

    def tick(self, dt):
        self.nezranitelnost = max(0, self.nezranitelnost - dt)

    def zasah(self):
        if self.zivoty == 0 or self.nezranitelnost > 0:
            return False
        self.zivoty -= 1
        self.nezranitelnost = self.ochrana
        return True

def zpracuj_zasahy(hrac, proud, zdravi):
    zasahy = pygame.sprite.spritecollide(hrac, proud.objekty, True, pygame.sprite.collide_circle)
    return zdravi.zasah() if zasahy else False

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac, ProudMeteoritu=ProudMeteoritu, Zdravi=Zdravi, zpracuj_zasahy=zpracuj_zasahy), precti_smer)
