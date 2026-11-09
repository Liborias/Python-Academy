# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota, Hlidac, Kyvac, Lov, Kolo

class Hra:
    def __init__(self, seed=11):
        self.seed = seed
        self.bezi = True
        self.stav = 'nabidka'
        self.kolo = None
        self.nabidka_povolena = True

    def novy_lov(self):
        self.kolo = Kolo(self.seed)
        self.stav = 'hra'

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT:
            self.bezi = False
            return
        if not self.bezi:
            return
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_ESCAPE:
                self.bezi = False
            elif udalost.key == pygame.K_SPACE and self.stav == 'nabidka':
                self.novy_lov()
            elif udalost.key == pygame.K_SPACE and self.stav == 'vysledek':
                self.stav = 'nabidka'
                self.kolo = None
            elif udalost.key == pygame.K_r and self.stav != 'nabidka':
                self.novy_lov()
            elif udalost.key == pygame.K_p and self.stav in ('hra', 'pauza'):
                self.stav = 'pauza' if self.stav == 'hra' else 'hra'
        elif self.stav == 'hra':
            self.kolo.klik(udalost)
            if self.kolo.konec:
                self.stav = 'vysledek'

    def update(self, dt):
        if self.bezi and self.stav == 'hra':
            self.kolo.update(dt)
            if self.kolo.konec:
                self.stav = 'vysledek'

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(Hra())
