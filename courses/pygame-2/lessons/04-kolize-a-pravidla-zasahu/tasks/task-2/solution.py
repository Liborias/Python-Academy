# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def seber_bonusy(hrac, bonusy):
    chycené = pygame.sprite.spritecollide(hrac, bonusy, True)
    return sum(bonus.hodnota for bonus in chycené)

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    hrac = ZakladSprite((200, 180)); bonus = ZakladSprite((210, 180), barva=(100, 230, 150)); bonus.hodnota = 7
    bonusy = pygame.sprite.Group(bonus)
    print('Získané body:', seber_bonusy(hrac, bonusy), 'zůstává:', len(bonusy))
    nahled([hrac, *bonusy], 'Bonus už byl odebrán')
