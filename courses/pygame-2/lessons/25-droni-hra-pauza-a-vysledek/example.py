# Nový krok návazné hry; import modelu neotevírá okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import random
import pygame
from podklady import HRANICE, ZONA, DATOVE_BODY, OBRAZY, DatovyBod, vstupy
from sestava import CvicnaHra
from herni_okno import spustit
from predchozi import Hrac, Dron, Svet, HlidacBodu, posun_drony, Vlny, StitZakladny, Kolo
from zasobnik import ZasobnikRezimu
from sceny import Menu, Let, PauzaLetu, Vysledek

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

# Okno vznikne až při spuštění tohoto souboru.
if __name__ == '__main__':
    spustit(Hra())
