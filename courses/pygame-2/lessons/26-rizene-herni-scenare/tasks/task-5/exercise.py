# Pygame-ce používáme jako pygame. Import sám neotevírá herní okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from pathlib import Path
from model_hry import Hrac, Dron, HlidacBodu, Vlny, StitZakladny, Kolo, Hra
from scenare import snimek

from simulace import prehraj

def dvojice_behu(seed, kroky):
    # Doplňte podle zadání; různé správné postupy jsou vítané.
    raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    a, b = dvojice_behu(17, (((0, 0), 0.05) for _ in range(25)))
    print('Stejné hodnoty:', a == b, 'Různé seznamy:', a is not b)
