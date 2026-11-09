"""Dočasné sestavení pro kroky 6–9. Pravidla dodají třídy z lekce."""
import random
import pygame
from podklady import HRANICE

class CvicneKolo:
    def __init__(self, Hrac, ProudMeteoritu=None, Zdravi=None, zpracuj_zasahy=None):
        self.hranice = HRANICE.copy()
        self.hrac = Hrac((320, 420), self.hranice)
        self.proud = ProudMeteoritu(random.Random(7)) if ProudMeteoritu else None
        self.zdravi = Zdravi() if Zdravi else None
        self.zasahy = zpracuj_zasahy
        self.bonusy = pygame.sprite.Group()
        self.stit = False
        self.skore = 0

    def update(self, smer, dt):
        if self.zdravi is not None and self.zdravi.zivoty == 0:
            return
        self.hrac.update(smer, dt)
        if self.proud is not None:
            self.proud.update(dt, self.hranice)
            self.skore = self.proud.minulo
        if self.zdravi is not None:
            self.zdravi.tick(dt)
            self.zasahy(self.hrac, self.proud, self.zdravi)

class CvicnaHra:
    def __init__(self, Hrac, ProudMeteoritu=None, Zdravi=None, zpracuj_zasahy=None, Kolo=None):
        self.bezi = True
        self.pauza = False
        self.restart_povolen = False
        self.kolo = Kolo(seed=7) if Kolo else CvicneKolo(Hrac, ProudMeteoritu, Zdravi, zpracuj_zasahy)

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT:
            self.bezi = False

    def update(self, smer, dt):
        if self.bezi:
            self.kolo.update(smer, dt)
