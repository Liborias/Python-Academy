# Pygame-ce používáme jako pygame. Import sám neotevírá herní okno.
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import pygame
from pathlib import Path
from model_hry import Hrac, Dron, HlidacBodu, Vlny, StitZakladny, Kolo, Hra
from scenare import snimek

def naplanuj_vstup(pocet, zmeny):
    if type(pocet) is not int or pocet < 0:
        raise ValueError('Počet snímků musí být nezáporné celé číslo.')
    smer = (0, 0)
    vysledek = []
    for snimek_cislo in range(pocet):
        if snimek_cislo in zmeny:
            smer = tuple(zmeny[snimek_cislo])
        vysledek.append(tuple(smer))
    return vysledek

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(naplanuj_vstup(6, {1: [1, 0], 4: [0, -1]}))
