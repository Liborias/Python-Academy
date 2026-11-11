import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from zasobnik import ZasobnikRezimu
from sceny import Menu, Let, PauzaLetu, Vysledek

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

class Hra:
    def __init__(self, seed=23):
        self.seed = seed
        self.bezi = True
        self.kolo = None
        self.zasobnik = ZasobnikRezimu(Menu())

    @property
    def stav(self):
        return self.zasobnik.aktualni.jmeno

    def novy_let(self):
        novy = Kolo(self.seed)
        self.kolo = novy
        self.zasobnik = ZasobnikRezimu(Let(novy))

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT:
            self.bezi = False
            return
        if not self.bezi:
            return
        if udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_ESCAPE:
            self.bezi = False
            return
        akce = self.zasobnik.zpracuj(udalost)
        if akce == 'start':
            self.novy_let()
        elif akce == 'nabidka':
            self.kolo = None
            self.zasobnik = ZasobnikRezimu(Menu())
        elif akce == 'pauza':
            self.zasobnik.vloz(PauzaLetu())
        elif akce == 'zpet':
            self.zasobnik.odeber()

    def update(self, smer, dt):
        if not self.bezi:
            return
        if self.stav == 'hra':
            self.zasobnik.aktualni.smer = pygame.Vector2(smer)
        self.zasobnik.update(dt)
        if self.stav == 'hra' and self.kolo.konec:
            self.zasobnik = ZasobnikRezimu(Vysledek(self.kolo))

    def kresli(self, plocha):
        self.zasobnik.kresli(plocha)
