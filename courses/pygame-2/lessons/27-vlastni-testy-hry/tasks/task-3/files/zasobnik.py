import pygame

class ZasobnikRezimu:
    def __init__(self, pocatecni):
        self.rezimy = [pocatecni]

    @property
    def aktualni(self):
        return self.rezimy[-1]

    def vloz(self, rezim):
        self.rezimy.append(rezim)

    def odeber(self):
        if len(self.rezimy) == 1:
            return False
        self.rezimy.pop()
        return True

    def zpracuj(self, udalost):
        return self.aktualni.zpracuj(udalost)

    def update(self, dt):
        self.aktualni.update(dt)

    def kresli(self, plocha):
        for rezim in self.rezimy:
            rezim.kresli(plocha)
