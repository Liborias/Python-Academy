"""Připravený obal rozpracovaných kroků; finální Lov/Kolo/Hra dodá student."""
import pygame
from podklady import HRANICE

class CvicnyLov:
    def __init__(self, roboty, najdi):
        self.roboty = pygame.sprite.Group(roboty)
        self.najdi = najdi
        self.skore = self.pokusy = self.zasahy = 0
        self.zivoty = 3

    def klik(self, udalost):
        if udalost.type != pygame.MOUSEBUTTONDOWN or udalost.button != 1 or self.zivoty == 0 or not self.roboty:
            return None
        self.pokusy += 1
        robot = self.najdi(self.roboty, udalost.pos)
        if robot is not None:
            robot.kill()
            self.skore += robot.body
            self.zasahy += 1
        else:
            self.zivoty -= 1
        return robot

    def presnost(self):
        return 100 * self.zasahy / self.pokusy if self.pokusy else 0.0

class CvicneKolo:
    def __init__(self, Robot, najdi, Hlidac=None, Kyvac=None, Lov=None):
        self.hranice = HRANICE.copy()
        if Hlidac is None:
            roboty = [Robot((160, 200)), Robot((360, 280)), Robot((560, 200))]
        else:
            roboty = [Hlidac((160, 200), (90, 45)), Kyvac((360, 280)), Hlidac((560, 200), (-70, 65))]
        self.lov = Lov(roboty) if Lov is not None else CvicnyLov(roboty, najdi)
        self.zbyva = None
        self.cislo = 1
        self.konec = False
        self.duvod = ''

    def update(self, dt):
        if not self.konec:
            self.lov.roboty.update(dt, self.hranice)

    def klik(self, udalost):
        if self.konec:
            return None
        robot = self.lov.klik(udalost)
        if self.lov.zivoty == 0 or not self.lov.roboty:
            self.konec = True
            self.duvod = 'zivoty' if self.lov.zivoty == 0 else 'lapeni'
        return robot

class CvicnaHra:
    def __init__(self, Robot, najdi, Hlidac=None, Kyvac=None, Lov=None, Kolo=None):
        self.kolo = Kolo() if Kolo is not None else CvicneKolo(Robot, najdi, Hlidac, Kyvac, Lov)
        self.bezi = True
        self.stav = 'hra'
        self.nabidka_povolena = False

    def zpracuj(self, udalost):
        if udalost.type == pygame.QUIT or (udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_ESCAPE):
            self.bezi = False
        elif self.bezi and self.stav == 'hra':
            self.kolo.klik(udalost)
            if self.kolo.konec:
                self.stav = 'vysledek'

    def update(self, dt):
        if self.bezi and self.stav == 'hra':
            self.kolo.update(dt)
            if self.kolo.konec:
                self.stav = 'vysledek'
