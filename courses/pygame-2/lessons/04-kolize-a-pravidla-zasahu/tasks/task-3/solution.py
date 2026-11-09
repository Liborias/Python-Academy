# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def prvni_zasah(hrac, nepratele):
    return pygame.sprite.spritecollideany(hrac, nepratele)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    hrac = ZakladSprite((200, 180)); nepratele = pygame.sprite.Group(ZakladSprite((210, 180)))
    vysledek = prvni_zasah(hrac, nepratele)
    print('Nalezen objekt:', vysledek is not None)
    nahled([hrac, *nepratele], 'Stačí jeden zásah')
