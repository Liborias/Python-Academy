# Nová část projektu používá skutečné pygame-ce, bez zvuků a stažených obrázků.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import random
import pygame
from podklady import HRANICE, obraz_lodi, obraz_meteoritu
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, precti_smer

class Meteorit(pygame.sprite.Sprite):
    def __init__(self, stred, polomer, rychlost):
        super().__init__()
        self.radius = polomer
        self.image = obraz_meteoritu(polomer)
        self.rect = self.image.get_rect(center=(round(stred[0]), round(stred[1])))
        self.pozice = pygame.Vector2(stred)
        self.rychlost = rychlost

    def update(self, dt):
        self.pozice.y += self.rychlost * dt
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

class ProudMeteoritu:
    def __init__(self, rng, interval=0.65):
        if interval <= 0:
            raise ValueError('Interval musí být kladný.')
        self.rng = rng
        self.interval = interval
        self.cas = 0.0
        self.objekty = pygame.sprite.Group()
        self.minulo = 0

    def vytvor(self, hranice):
        polomer = self.rng.randint(12, 26)
        x = self.rng.randint(hranice.left + polomer, hranice.right - polomer)
        rychlost = self.rng.randint(90, 160)
        meteorit = Meteorit((x, hranice.top - polomer), polomer, rychlost)
        self.objekty.add(meteorit)
        return meteorit

    def update(self, dt, hranice):
        self.objekty.update(dt)
        for meteorit in self.objekty.sprites():
            if meteorit.rect.top >= hranice.bottom:
                meteorit.kill()
                self.minulo += 1
        self.cas += dt
        while self.cas >= self.interval:
            self.cas -= self.interval
            self.vytvor(hranice)

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac, ProudMeteoritu=ProudMeteoritu), precti_smer)
