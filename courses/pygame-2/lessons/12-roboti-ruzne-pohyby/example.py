# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota

class Hlidac(Robot):
    barva = (80, 170, 255)

    def __init__(self, stred, rychlost=(90, 55), polomer=22, body=10):
        super().__init__(stred, polomer, body)
        self.rychlost = pygame.Vector2(rychlost)

    def update(self, dt, hranice):
        self.pozice += self.rychlost * dt
        if self.pozice.x <= hranice.left + self.radius:
            self.pozice.x = hranice.left + self.radius
            self.rychlost.x = abs(self.rychlost.x)
        elif self.pozice.x >= hranice.right - self.radius:
            self.pozice.x = hranice.right - self.radius
            self.rychlost.x = -abs(self.rychlost.x)
        if self.pozice.y <= hranice.top + self.radius:
            self.pozice.y = hranice.top + self.radius
            self.rychlost.y = abs(self.rychlost.y)
        elif self.pozice.y >= hranice.bottom - self.radius:
            self.pozice.y = hranice.bottom - self.radius
            self.rychlost.y = -abs(self.rychlost.y)
        self.rect.center = round(self.pozice.x), round(self.pozice.y)

class Kyvac(Robot):
    barva = (195, 145, 255)

    def __init__(self, stred, amplituda=50, perioda=2, polomer=22, body=20):
        if perioda <= 0:
            raise ValueError('Perioda musí být kladná.')
        super().__init__(stred, polomer, body)
        self.kotva = pygame.Vector2(stred)
        self.amplituda = amplituda
        self.perioda = perioda
        self.cas = 0.0

    def update(self, dt, hranice):
        self.cas += dt
        x = self.kotva.x + self.amplituda * math.sin(2 * math.pi * self.cas / self.perioda)
        self.pozice.x = max(hranice.left + self.radius, min(hranice.right - self.radius, x))
        self.pozice.y = max(hranice.top + self.radius, min(hranice.bottom - self.radius, self.kotva.y))
        self.rect.center = round(self.pozice.x), round(self.pozice.y)

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(CvicnaHra(Robot, najdi_robota, Hlidac=Hlidac, Kyvac=Kyvac))
