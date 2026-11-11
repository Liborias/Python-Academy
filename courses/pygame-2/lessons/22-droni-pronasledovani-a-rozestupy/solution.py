# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet

class HlidacBodu(Dron):
    vzhled = 'hlidac'

    def __init__(self, stred, rychlost=80, dosah=160):
        super().__init__(stred, rychlost)
        self.kotva = pygame.Vector2(stred)
        self.dosah = dosah

    def cil(self, hrac):
        if (pygame.Vector2(hrac.pozice) - self.kotva).length_squared() <= self.dosah ** 2:
            return pygame.Vector2(hrac.pozice)
        return self.kotva.copy()

def posun_drony(drony, hrac, dt, hranice, rozestup=42):
    objekty = list(drony)
    puvodni = {d: d.pozice.copy() for d in objekty}
    nove = []
    for dron in objekty:
        cesta = pygame.Vector2(dron.cil(hrac)) - puvodni[dron]
        vzdalenost = cesta.length()
        smer = cesta.normalize() if vzdalenost else pygame.Vector2()
        odpor = pygame.Vector2()
        for jiny in objekty:
            if jiny is dron:
                continue
            rozdil = puvodni[dron] - puvodni[jiny]
            delka = rozdil.length()
            if 0 < delka < rozestup:
                odpor += rozdil / delka * (rozestup - delka) / rozestup
        smer += odpor * 1.6
        krok = dron.rychlost * dt
        if not odpor.length_squared():
            krok = min(krok, vzdalenost)
        bod = puvodni[dron].copy()
        if smer.length_squared():
            bod += smer.normalize() * krok
        bod.x = max(hranice.left + 14, min(hranice.right - 14, bod.x))
        bod.y = max(hranice.top + 14, min(hranice.bottom - 14, bod.y))
        nove.append((dron, bod))
    for dron, bod in nove:
        dron.pozice = bod
        dron.rect.center = round(bod.x), round(bod.y)

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet, posun_drony=posun_drony, HlidacBodu=HlidacBodu))
