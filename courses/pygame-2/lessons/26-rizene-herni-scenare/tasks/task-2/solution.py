# Pygame-ce používáme jako pygame. Import sám neotevírá herní okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from pathlib import Path
from model_hry import Hrac, Dron, HlidacBodu, Vlny, StitZakladny, Kolo, Hra
from scenare import snimek

def rozdel_cas(celkem, krok=0.05):
    if not math.isfinite(celkem) or celkem < 0 or not math.isfinite(krok) or not 0 < krok <= 0.05:
        raise ValueError('Čas musí být konečný, krok v intervalu (0; 0,05].')
    vysledek = []
    zbyva = celkem
    while zbyva > 1e-12:
        cast = min(krok, zbyva)
        vysledek.append(cast)
        zbyva -= cast
    return vysledek

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(rozdel_cas(0.12))
