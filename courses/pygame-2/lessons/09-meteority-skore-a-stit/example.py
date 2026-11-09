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
        self.hranice = HRANICE.copy()
        self.hrac = Hrac((320, 420), self.hranice)
        self.proud = ProudMeteoritu(random.Random(seed))
        self.zdravi = Zdravi()
        self.bonusy = pygame.sprite.Group()
        self.bonus_cas = 0.0
        self.skore = 0
        self.stit = False

    def update(self, smer, dt):
        if self.zdravi.zivoty == 0:
            return
        self.zdravi.tick(dt)
        self.hrac.update(smer, dt)
        self.proud.update(dt, self.hranice)
        self.skore = self.proud.minulo
        self.bonusy.update(dt)
        for bonus in self.bonusy.sprites():
            if bonus.rect.top >= self.hranice.bottom:
                bonus.kill()
        self.bonus_cas += dt
        while self.bonus_cas >= 6:
            self.bonus_cas -= 6
            self.bonusy.add(BonusStitu((self.hranice.centerx, self.hranice.top - 12)))
        if pygame.sprite.spritecollide(self.hrac, self.bonusy, True, pygame.sprite.collide_circle):
            self.stit = True
        zasahy = pygame.sprite.spritecollide(self.hrac, self.proud.objekty, True, pygame.sprite.collide_circle)
        if zasahy and self.zdravi.nezranitelnost == 0:
            if self.stit:
                self.stit = False
                self.zdravi.nezranitelnost = self.zdravi.ochrana
            else:
                self.zdravi.zasah()

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac, Kolo=Kolo), precti_smer)
