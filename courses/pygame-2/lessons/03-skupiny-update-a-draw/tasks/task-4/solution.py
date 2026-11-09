# Knihovna pygame-ce se importuje jménem pygame.
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from zaklad import ZakladSprite
from nahled import nahled
from pohyb import PohyblivaLod

def skupina_typu(skupina, typ):
    return pygame.sprite.Group(objekt for objekt in skupina if isinstance(objekt, typ))

# Spuštění vytvoří PNG, import pro kontrolu otevřené okno nepotřebuje.
if __name__ == "__main__":
    class Doprovod(PohyblivaLod):
        pass
    skupina = pygame.sprite.Group(PohyblivaLod((140, 150), (0, 0)), Doprovod((340, 220), (0, 0)))
    vyber = skupina_typu(skupina, Doprovod)
    print('Původní:', len(skupina), 'vybraná:', len(vyber))
    nahled(vyber, 'Výběr jednoho typu')
