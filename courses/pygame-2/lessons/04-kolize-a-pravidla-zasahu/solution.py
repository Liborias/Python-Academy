# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def zasahy(hrac, nepratele):
    return pygame.sprite.spritecollide(hrac, nepratele, False)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    hrac = ZakladSprite((200, 180))
    nepratele = pygame.sprite.Group(ZakladSprite((210, 180), barva=(235, 145, 75)), ZakladSprite((380, 180), barva=(235, 145, 75)))
    print('Počet zásahů:', len(zasahy(hrac, nepratele)))
    nahled([hrac, *nepratele], 'Obdélníky rozhodují o zásahu')
