# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def zasahy_kruhem(hrac, nepratele):
    return pygame.sprite.spritecollide(hrac, nepratele, False, pygame.sprite.collide_circle)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    hrac = ZakladSprite((200, 180)); hrac.radius = 20
    cil = ZakladSprite((235, 180), barva=(235, 145, 75)); cil.radius = 20
    nepratele = pygame.sprite.Group(cil)
    print('Kruhové zásahy:', len(zasahy_kruhem(hrac, nepratele)))
    nahled([hrac, *nepratele], 'Kruhové pravidlo může být jiné než rect')
