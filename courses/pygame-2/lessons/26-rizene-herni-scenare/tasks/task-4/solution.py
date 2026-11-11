# Pygame-ce používáme jako pygame. Import sám neotevírá herní okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from pathlib import Path
from model_hry import Hrac, Dron, HlidacBodu, Vlny, StitZakladny, Kolo, Hra
from scenare import snimek

from simulace import prehraj

def souhrn_stopy(stopa):
    draha = 0.0
    for pred, po in zip(stopa, stopa[1:]):
        draha += math.dist(pred['pozice'], po['pozice'])
    prvni_konec = next((s['cas'] for s in stopa if s['konec']), None)
    return {
        'kroky': max(0, len(stopa) - 1),
        'draha': draha,
        'maximum_dronu': max((len(s['droni']) for s in stopa), default=0),
        'konec_v_case': prvni_konec,
    }

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(souhrn_stopy(prehraj(23, [((1, 0), 0.05)] * 25)))
