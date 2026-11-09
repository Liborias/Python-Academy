import pygame

HRANICE = pygame.Rect(20, 70, 600, 390)
MODRA = (80, 180, 255)
ORANZOVA = (235, 145, 75)

def obraz_lodi():
    obraz = pygame.Surface((40, 32), pygame.SRCALPHA)
    pygame.draw.polygon(obraz, MODRA, [(20, 0), (0, 30), (20, 23), (39, 30)])
    pygame.draw.polygon(obraz, (180, 235, 255), [(20, 5), (16, 13), (24, 13)])
    return obraz

def obraz_meteoritu(polomer):
    obraz = pygame.Surface((2 * polomer, 2 * polomer), pygame.SRCALPHA)
    pygame.draw.circle(obraz, ORANZOVA, (polomer, polomer), polomer)
    pygame.draw.circle(obraz, (155, 84, 49), (polomer // 2, polomer // 2), max(2, polomer // 4))
    return obraz
