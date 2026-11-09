"""Vlastní kresba robota; žádné obrázky ani zvuky ze sítě."""
import pygame

HRANICE = pygame.Rect(24, 96, 672, 360)

def obraz_robota(polomer, barva):
    obraz = pygame.Surface((2 * polomer, 2 * polomer), pygame.SRCALPHA)
    pygame.draw.circle(obraz, (28, 44, 62), (polomer, polomer), polomer)
    pygame.draw.circle(obraz, barva, (polomer, polomer), polomer - 1, 2)
    telo = pygame.Rect(polomer // 3, polomer // 2, 4 * polomer // 3, polomer)
    pygame.draw.rect(obraz, barva, telo, border_radius=5)
    for x in (2 * polomer // 3, 4 * polomer // 3):
        pygame.draw.circle(obraz, (12, 24, 36), (x, 4 * polomer // 5), max(2, polomer // 8))
    pygame.draw.line(obraz, (12, 24, 36), (2 * polomer // 3, 6 * polomer // 5), (4 * polomer // 3, 6 * polomer // 5), 2)
    pygame.draw.line(obraz, barva, (polomer, polomer // 2), (polomer, polomer // 5), 2)
    return obraz
