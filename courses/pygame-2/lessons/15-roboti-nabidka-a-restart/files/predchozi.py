# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota

class Robot(pygame.sprite.Sprite):
    barva = (55, 205, 177)

    def __init__(self, stred, polomer=22, body=10):
        super().__init__()
        self.radius = polomer
        self.body = body
        self.pozice = pygame.Vector2(stred)
        self.image = obraz_robota(polomer, self.barva)
        self.rect = self.image.get_rect(center=(round(self.pozice.x), round(self.pozice.y)))

    def obsahuje(self, bod):
        rozdil = pygame.Vector2(bod) - self.rect.center
        return rozdil.length_squared() <= self.radius ** 2

    def update(self, dt, hranice):
        # Stojící robot přijímá stejné rozhraní jako budoucí pohyblivé typy.
        pass

def najdi_robota(roboty, bod):
    for robot in reversed(roboty.sprites()):
        if robot.obsahuje(bod):
            return robot
    return None

class Hlidac(Robot):
    barva = (80, 170, 255)

    def __init__(self, stred, rychlost=(90, 55), polomer=22, body=10):
        super().__init__(stred, polomer, body)
        self.rychlost = pygame.Vector2(rychlost)

    def update(self, dt, hranice):
        self.pozice += self.rychlost * dt
        if self.pozice.x <= hranice.left + self.radius:
            self.pozice.x = hranice.left + self.radius
            self.rychlost.x = abs(self.rychlost.x)
        elif self.pozice.x >= hranice.right - self.radius:
            self.pozice.x = hranice.right - self.radius
            self.rychlost.x = -abs(self.rychlost.x)
        if self.pozice.y <= hranice.top + self.radius:
            self.pozice.y = hranice.top + self.radius
            self.rychlost.y = abs(self.rychlost.y)
        elif self.pozice.y >= hranice.bottom - self.radius:
            self.pozice.y = hranice.bottom - self.radius
            self.rychlost.y = -abs(self.rychlost.y)
        self.rect.center = round(self.pozice.x), round(self.pozice.y)

class Kyvac(Robot):
    barva = (195, 145, 255)

    def __init__(self, stred, amplituda=50, perioda=2, polomer=22, body=20):
        if perioda <= 0:
            raise ValueError('Perioda musí být kladná.')
        super().__init__(stred, polomer, body)
        self.kotva = pygame.Vector2(stred)
        self.amplituda = amplituda
        self.perioda = perioda
        self.cas = 0.0

    def update(self, dt, hranice):
        self.cas += dt
        x = self.kotva.x + self.amplituda * math.sin(2 * math.pi * self.cas / self.perioda)
        self.pozice.x = max(hranice.left + self.radius, min(hranice.right - self.radius, x))
        self.pozice.y = max(hranice.top + self.radius, min(hranice.bottom - self.radius, self.kotva.y))
        self.rect.center = round(self.pozice.x), round(self.pozice.y)

class Lov:
    def __init__(self, roboty, zivoty=3):
        self.roboty = pygame.sprite.Group(roboty)
        self.zivoty = zivoty
        self.skore = 0
        self.pokusy = 0
        self.zasahy = 0

    def klik(self, udalost):
        if udalost.type != pygame.MOUSEBUTTONDOWN or udalost.button != 1:
            return None
        if self.zivoty == 0 or not self.roboty:
            return None
        self.pokusy += 1
        robot = najdi_robota(self.roboty, udalost.pos)
        if robot is not None:
            robot.kill()
            self.skore += robot.body
            self.zasahy += 1
        else:
            self.zivoty -= 1
        return robot

    def presnost(self):
        return 100 * self.zasahy / self.pokusy if self.pokusy else 0.0

class Kolo:
    def __init__(self, seed=11, limit=30):
        if limit <= 0:
            raise ValueError('Limit musí být kladný.')
        self.hranice = HRANICE.copy()
        self.rng = random.Random(seed)
        self.lov = Lov(pygame.sprite.Group())
        self.zbyva = float(limit)
        self.cislo = 0
        self.konec = False
        self.duvod = ''
        self.dalsi_vlna()

    def dalsi_vlna(self):
        if self.konec or self.lov.roboty:
            return False
        self.cislo += 1
        pocet = min(2 + self.cislo, 6)
        rychlost = min(80 + 15 * (self.cislo - 1), 220)
        perioda = max(0.7, 2 - 0.15 * (self.cislo - 1))
        for index in range(pocet):
            x = self.rng.randint(self.hranice.left + 90, self.hranice.right - 90)
            y = self.rng.randint(self.hranice.top + 22, self.hranice.bottom - 22)
            if index % 2 == 0:
                smer = self.rng.choice((-1, 1))
                robot = Hlidac((x, y), (smer * rychlost, 50))
            else:
                robot = Kyvac((x, y), amplituda=50, perioda=perioda)
            self.lov.roboty.add(robot)
        return True

    def update(self, dt):
        if self.konec:
            return
        self.zbyva = max(0, self.zbyva - dt)
        if self.zbyva == 0:
            self.konec = True
            self.duvod = 'cas'
        elif self.lov.zivoty == 0:
            self.konec = True
            self.duvod = 'zivoty'
        else:
            self.lov.roboty.update(dt, self.hranice)
            self.dalsi_vlna()

    def klik(self, udalost):
        if self.konec:
            return None
        robot = self.lov.klik(udalost)
        if self.lov.zivoty == 0:
            self.konec = True
            self.duvod = 'zivoty'
        elif not self.lov.roboty:
            self.dalsi_vlna()
        return robot
