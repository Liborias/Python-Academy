# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet, HlidacBodu, posun_drony, Vlny

class StitZakladny:
    def __init__(self, kapacita=2.5, obnova=0.5):
        self.kapacita = kapacita
        self.obnova = obnova
        self.energie = kapacita

    def update(self, dt, uvnitr):
        if uvnitr:
            chraneno = self.energie > 0 and self.energie >= dt
            self.energie = max(0, self.energie - dt)
            return chraneno
        self.energie = min(self.kapacita, self.energie + dt * self.obnova)
        return False

class Kolo(Svet):
    def __init__(self, seed=23):
        super().__init__()
        for dron in self.drony.sprites():
            dron.kill()
        self.vlny = Vlny(seed)
        self.drony = self.vlny.drony
        self.zona = ZONA.copy()
        self.stit = StitZakladny()
        self.chraneno = False
        self.zivoty = 3
        self.nezranitelnost = 0.0
        self.zbyva = 10.0
        self.konec = False
        self.duvod = ''

    def update(self, smer, dt):
        if self.konec:
            return
        self.cas += dt
        self.hrac.update(smer, dt)
        self.chraneno = self.stit.update(dt, self.zona.contains(self.hrac.rect))
        self.nezranitelnost = max(0, self.nezranitelnost - dt)
        self.vlny.update(dt, self.hrac, self.hranice)
        posun_drony(self.drony, self.hrac, dt, self.hranice)
        zasah = any((pygame.Vector2(d.rect.center) - self.hrac.rect.center).length_squared()
                    <= (d.radius + self.hrac.radius) ** 2 for d in self.drony)
        if zasah and not self.chraneno and self.nezranitelnost == 0:
            self.zivoty -= 1
            self.nezranitelnost = 0.9
        if self.zivoty == 0:
            self.konec = True
            self.duvod = 'zivoty'
            return
        self.seber_data()
        self.zbyva = max(0, self.zbyva - dt)
        if self.zbyva < 1e-9:
            self.zbyva = 0.0
            if self.vlny.cislo < 3:
                self.vlny.zahaj()
                self.zbyva = 10.0
            else:
                self.konec = True
                self.duvod = 'uspech' if self.skore >= 6 else 'data'

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet, posun_drony=posun_drony, HlidacBodu=HlidacBodu, Vlny=Vlny, Kolo=Kolo))
