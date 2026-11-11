"""Obal rozpracovaných kroků, který používá právě studentské modely."""
import pygame
from herni_okno import vykresli_svet, vykresli_paticku, vykresli_vysledek, napis

class CvicnaHra:
    def __init__(self, Svet, posun_drony=None, HlidacBodu=None, Vlny=None, Kolo=None):
        if Kolo is not None:
            self.kolo=Kolo()
        else:
            class Trenink(Svet):
                def __init__(self):
                    super().__init__()
                    if HlidacBodu is not None:
                        self.drony.sprites()[-1].kill()
                        self.drony.add(HlidacBodu((570,410)))
                    self.vlny=None
                    if Vlny is not None:
                        for d in self.drony.sprites():d.kill()
                        self.vlny=Vlny()
                        self.drony=self.vlny.drony

                def update(self,smer,dt):
                    super().update(smer,dt)
                    if self.vlny is not None:self.vlny.update(dt,self.hrac,self.hranice)
                    if posun_drony is not None:posun_drony(self.drony,self.hrac,dt,self.hranice)
            self.kolo=Trenink()
        self.trenink_vln=Kolo is None and Vlny is not None
        self.bezi=True
        self.stav='hra'

    def zpracuj(self,udalost):
        if udalost.type==pygame.QUIT or (udalost.type==pygame.KEYDOWN and udalost.key==pygame.K_ESCAPE):
            self.bezi=False
        elif self.bezi and self.trenink_vln and udalost.type==pygame.KEYDOWN and udalost.key==pygame.K_n:
            self.kolo.vlny.zahaj()

    def update(self,smer,dt):
        if self.bezi:
            self.kolo.update(smer,dt)
            if getattr(self.kolo,'konec',False):self.stav='vysledek'

    def kresli(self,plocha):
        vykresli_svet(plocha,self.kolo)
        vykresli_paticku(plocha,False)
        if self.trenink_vln:
            pygame.draw.rect(plocha,(10,20,32),(24,515,672,25))
            napis(plocha,'N: další tréninková vlna   Šipky / WASD: pohyb',(24,518),19)
        if self.stav=='vysledek':vykresli_vysledek(plocha,self.kolo,False)
