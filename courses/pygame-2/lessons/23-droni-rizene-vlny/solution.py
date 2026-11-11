# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet, HlidacBodu, posun_drony

class Vlny:
    def __init__(self, seed=23, interval=0.75):
        if interval <= 0:
            raise ValueError('Interval musí být kladný.')
        self.rng = random.Random(seed)
        self.interval = interval
        self.drony = pygame.sprite.Group()
        self.cislo = 0
        self.cekaji = 0
        self.cas = 0.0
        self.vytvoreno = 0
        self.zahaj()

    def zahaj(self):
        for dron in self.drony.sprites():
            dron.kill()
        self.cislo += 1
        self.cekaji = min(2 + self.cislo, 6)
        self.cas = 0.0
        self.vytvoreno = 0

    def pridej(self, hrac, hranice):
        moznosti = vstupy(hranice)
        bezpecne = [b for b in moznosti if (pygame.Vector2(b) - hrac.pozice).length_squared() >= 150 ** 2]
        if bezpecne:
            bod = self.rng.choice(bezpecne)
        else:
            bod = max(moznosti, key=lambda b: (pygame.Vector2(b) - hrac.pozice).length_squared())
        rychlost = min(90 + 10 * (self.cislo - 1), 140)
        if self.vytvoreno % 2:
            dron = HlidacBodu(bod, rychlost - 10, dosah=200)
        else:
            dron = Dron(bod, rychlost)
        self.drony.add(dron)
        self.vytvoreno += 1
        return dron

    def update(self, dt, hrac, hranice):
        if not self.cekaji:
            return
        self.cas += dt
        while self.cekaji and self.cas >= self.interval:
            self.cas -= self.interval
            self.pridej(hrac, hranice)
            self.cekaji -= 1
        if not self.cekaji:
            self.cas = 0.0

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet, posun_drony=posun_drony, HlidacBodu=HlidacBodu, Vlny=Vlny))
