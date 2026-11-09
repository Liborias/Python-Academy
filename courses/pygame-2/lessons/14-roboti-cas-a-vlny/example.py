# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota, Hlidac, Kyvac, Lov

class Kolo:
    def __init__(self, seed=11, limit=30):
        if limit <= 0:
            raise ValueError('Limit musí být kladný.')
        self.hranice = HRANICE.copy()
        self.rng = random.Random(seed)
        self.lov = Lov(pygame.sprite.Group())
        self.zbyva = float(limit)
        self.cislo = 0
        self.konec = False
        self.duvod = ''
        self.dalsi_vlna()

    def dalsi_vlna(self):
        if self.konec or self.lov.roboty:
            return False
        self.cislo += 1
        pocet = min(2 + self.cislo, 6)
        rychlost = min(80 + 15 * (self.cislo - 1), 220)
        perioda = max(0.7, 2 - 0.15 * (self.cislo - 1))
        for index in range(pocet):
            x = self.rng.randint(self.hranice.left + 90, self.hranice.right - 90)
            y = self.rng.randint(self.hranice.top + 22, self.hranice.bottom - 22)
            if index % 2 == 0:
                smer = self.rng.choice((-1, 1))
                robot = Hlidac((x, y), (smer * rychlost, 50))
            else:
                robot = Kyvac((x, y), amplituda=50, perioda=perioda)
            self.lov.roboty.add(robot)
        return True

    def update(self, dt):
        if self.konec:
            return
        self.zbyva = max(0, self.zbyva - dt)
        if self.zbyva == 0:
            self.konec = True
            self.duvod = 'cas'
        elif self.lov.zivoty == 0:
            self.konec = True
            self.duvod = 'zivoty'
        else:
            self.lov.roboty.update(dt, self.hranice)
            self.dalsi_vlna()

    def klik(self, udalost):
        if self.konec:
            return None
        robot = self.lov.klik(udalost)
        if self.lov.zivoty == 0:
            self.konec = True
            self.duvod = 'zivoty'
        elif not self.lov.roboty:
            self.dalsi_vlna()
        return robot

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(CvicnaHra(Robot, najdi_robota, Hlidac=Hlidac, Kyvac=Kyvac, Lov=Lov, Kolo=Kolo))
