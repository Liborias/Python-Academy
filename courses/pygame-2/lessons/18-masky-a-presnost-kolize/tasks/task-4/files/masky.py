import math
import pygame
def zasah_maskou(a, b):
    posun = b.rect.x - a.rect.x, b.rect.y - a.rect.y
    return a.mask.overlap(b.mask, posun) is not None
