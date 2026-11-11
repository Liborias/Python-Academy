# Pygame-ce používáme jako pygame. Import sám neotevírá herní okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from pathlib import Path
from model_hry import Hrac, Dron, HlidacBodu, Vlny, StitZakladny, Kolo, Hra
from scenare import snimek

def prehraj(seed, kroky):
    kolo = Kolo(seed)
    stopa = [snimek(kolo)]
    for smer, dt in kroky:
        kolo.update(smer, dt)
        stopa.append(snimek(kolo))
    return stopa

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(prehraj(23, [((1, 0), 0.05)] * 25)[-1])
