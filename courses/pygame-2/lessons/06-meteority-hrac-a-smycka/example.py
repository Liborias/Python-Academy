# Nová část projektu používá skutečné pygame-ce, bez zvuků a stažených obrázků.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import random
import pygame
from podklady import HRANICE, obraz_lodi, obraz_meteoritu
from sestava import CvicnaHra
from herni_okno import spustit

class Hrac(pygame.sprite.Sprite):
    def __init__(self, stred, hranice):
        super().__init__()
        self.image = obraz_lodi()
        self.rect = self.image.get_rect(center=(round(stred[0]), round(stred[1])))
        self.radius = 14
        self.pozice = pygame.Vector2(stred)
        self.hranice = hranice.copy()
        self.rychlost = 240

    def update(self, smer, dt):
        vektor = pygame.Vector2(smer)
        if vektor.length_squared() > 0:
            vektor = vektor.normalize()
        self.pozice += vektor * self.rychlost * dt
        pul_sirky, pul_vysky = self.rect.width / 2, self.rect.height / 2
        self.pozice.x = max(self.hranice.left + pul_sirky, min(self.hranice.right - pul_sirky, self.pozice.x))
        self.pozice.y = max(self.hranice.top + pul_vysky, min(self.hranice.bottom - pul_vysky, self.pozice.y))
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))

def precti_smer(klavesy):
    return pygame.Vector2(int(klavesy[pygame.K_RIGHT]) - int(klavesy[pygame.K_LEFT]),
                          int(klavesy[pygame.K_DOWN]) - int(klavesy[pygame.K_UP]))

# Okno se otevírá až při spuštění, nikoli při importu modelu.
if __name__ == "__main__":
    spustit(CvicnaHra(Hrac), precti_smer)
