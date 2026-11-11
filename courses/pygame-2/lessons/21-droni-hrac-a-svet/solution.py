# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit

class Hrac(pygame.sprite.Sprite):
    def __init__(self, stred, hranice):
        super().__init__()
        self.image = OBRAZY.obraz('hrac')
        self.radius = 14
        self.pozice = pygame.Vector2(stred)
        self.hranice = pygame.Rect(hranice)
        self.rychlost = 240
        self.rect = self.image.get_rect(center=(round(self.pozice.x), round(self.pozice.y)))

    def update(self, smer, dt):
        vektor = pygame.Vector2(smer)
        if vektor.length_squared():
            vektor = vektor.normalize()
        self.pozice += vektor * self.rychlost * dt
        self.pozice.x = max(self.hranice.left + 16, min(self.hranice.right - 16, self.pozice.x))
        self.pozice.y = max(self.hranice.top + 16, min(self.hranice.bottom - 16, self.pozice.y))
        self.rect.center = round(self.pozice.x), round(self.pozice.y)

class Dron(pygame.sprite.Sprite):
    vzhled = 'dron'

    def __init__(self, stred, rychlost=95):
        super().__init__()
        self.image = OBRAZY.obraz(self.vzhled)
        self.radius = 12
        self.pozice = pygame.Vector2(stred)
        self.rychlost = rychlost
        self.rect = self.image.get_rect(center=(round(self.pozice.x), round(self.pozice.y)))

    def cil(self, hrac):
        return pygame.Vector2(hrac.pozice)

class Svet:
    def __init__(self):
        self.hranice = HRANICE.copy()
        self.hrac = Hrac((360, 300), self.hranice)
        self.drony = pygame.sprite.Group(Dron((110, 140)), Dron((610, 140)), Dron((610, 430)))
        self.data = DatovyBod(DATOVE_BODY[0])
        self.skore = 0
        self.cas = 0.0

    def seber_data(self):
        vzdalenost = pygame.Vector2(self.data.rect.center) - self.hrac.rect.center
        if vzdalenost.length_squared() <= (self.data.radius + self.hrac.radius) ** 2:
            self.data.kill()
            self.skore += 1
            self.data = DatovyBod(DATOVE_BODY[self.skore % len(DATOVE_BODY)])
            return True
        return False

    def update(self, smer, dt):
        self.cas += dt
        self.hrac.update(smer, dt)
        self.seber_data()

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(CvicnaHra(Svet))
