from pathlib import Path
import pygame

def nahled(objekty, nadpis):
    """Stejný Surface/Sprite jako ve hře, uložený bez otevírání okna."""
    pygame.font.init()
    plocha = pygame.Surface((640, 360))
    plocha.fill((16, 23, 38))
    for x in range(0, 640, 40):
        pygame.draw.line(plocha, (27, 39, 58), (x, 48), (x, 359))
    for y in range(80, 360, 40):
        pygame.draw.line(plocha, (27, 39, 58), (0, y), (639, y))
    font = pygame.font.Font(None, 24)
    plocha.blit(font.render(nadpis, True, (230, 238, 250)), (16, 12))
    skupina = pygame.sprite.Group(objekty)
    skupina.draw(plocha)
    for objekt in skupina:
        pygame.draw.rect(plocha, (160, 178, 201), objekt.rect, 1)
        popis = font.render(str(objekt.rect.center), True, (180, 196, 217))
        plocha.blit(popis, (objekt.rect.left, objekt.rect.bottom + 5))
    cesta = Path('nahled.png')
    pygame.image.save(plocha, str(cesta))
    print('Náhled:', cesta)
