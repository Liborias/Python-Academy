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
        # Vytvořte paměť výsledků a připravte původní Hru.
        raise NotImplementedError

    def novy_let(self):
        raise NotImplementedError

    def update(self, smer, dt):
        raise NotImplementedError

    def kresli(self, plocha):
        raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    spustit(HraSPoradim(koren_aplikace(__file__, sys.executable, getattr(sys, 'frozen', False)) / 'data' / 'vysledky.json'))
