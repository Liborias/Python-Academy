# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy

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
