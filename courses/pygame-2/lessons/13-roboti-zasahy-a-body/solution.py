# Nový krok souvislého projektu; podklady kreslíme sami.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import random
import pygame
from podklady import HRANICE, obraz_robota
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Robot, najdi_robota, Hlidac, Kyvac

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

# GUI se spouští až zde, při importu se model pouze připraví.
if __name__ == "__main__":
    spustit(CvicnaHra(Robot, najdi_robota, Hlidac=Hlidac, Kyvac=Kyvac, Lov=Lov))
