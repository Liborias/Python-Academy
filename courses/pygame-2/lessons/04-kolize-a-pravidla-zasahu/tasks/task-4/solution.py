# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def dvojice_zasahu(strely, nepratele):
    return pygame.sprite.groupcollide(strely, nepratele, False, False)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    strely = pygame.sprite.Group(ZakladSprite((200, 180)))
    nepratele = pygame.sprite.Group(ZakladSprite((210, 180)), ZakladSprite((390, 180)))
    vysledek = dvojice_zasahu(strely, nepratele)
    print('Střel se zásahem:', len(vysledek), 'počet dvojic:', sum(len(v) for v in vysledek.values()))
    nahled([*strely, *nepratele], 'Dvě skupiny a mapa zásahů')
