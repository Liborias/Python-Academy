# Pygame-ce používáme jako pygame. Import sám neotevírá herní okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from pathlib import Path
from model_hry import Hrac, Dron, HlidacBodu, Vlny, StitZakladny, Kolo, Hra
from scenare import snimek

import sys
from vysledky import nacti_vysledky, serad_vysledky, uloz_vysledky
from cesty import koren_aplikace
from pamet import vykresli_pamet
from herni_okno import spustit

class HraSPoradim(Hra):
    def __init__(self, cesta, jmeno='Kurýr', rychlost=260, seed=23):
        if not isinstance(jmeno, str) or not 1 <= len(jmeno.strip()) <= 24:
            raise ValueError('Jméno musí mít 1–24 znaků.')
        if not math.isfinite(rychlost) or rychlost <= 0:
            raise ValueError('Rychlost musí být kladná a konečná.')
        super().__init__(seed)
        self.cesta = Path(cesta)
        self.jmeno = jmeno.strip()
        self.rychlost = rychlost
        self.zapsane_kolo = None
        self.zprava = 'Výsledky připravené.'
        try:
            self.vysledky = serad_vysledky(nacti_vysledky(self.cesta), 5)
        except OSError:
            self.vysledky = []
            self.zprava = 'Výsledky nejsou dostupné.'

    def novy_let(self):
        super().novy_let()
        self.kolo.hrac.rychlost = self.rychlost

    def update(self, smer, dt):
        super().update(smer, dt)
        if not self.bezi or self.stav != 'vysledek' or self.zapsane_kolo is self.kolo:
            return
        self.zapsane_kolo = self.kolo
        novy = {'jmeno': self.jmeno, 'body': self.kolo.skore, 'uspech': self.kolo.duvod == 'uspech'}
        poradi = serad_vysledky([*self.vysledky, novy], 5)
        try:
            uloz_vysledky(self.cesta, poradi)
        except OSError:
            self.zprava = 'Výsledek se nepodařilo uložit.'
        else:
            self.vysledky = poradi
            self.zprava = 'Výsledek uložen.'

    def kresli(self, plocha):
        super().kresli(plocha)
        vykresli_pamet(plocha, self)

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    spustit(HraSPoradim(koren_aplikace(__file__, sys.executable, getattr(sys, 'frozen', False)) / 'data' / 'vysledky.json'))
