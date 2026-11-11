"""Vlastní kresby a vstup; import neotevírá displej, fonty ani zvuk."""
import pygame
from zdroje import BankaObrazu

HRANICE = pygame.Rect(24, 90, 672, 390)
ZONA = pygame.Rect(300, 240, 120, 120)
DATOVE_BODY = ((150,160), (570,160), (570,430), (150,430), (360,160))

def vytvor_obraz(jmeno):
    if jmeno == 'hrac':
        obraz = pygame.Surface((32,32),pygame.SRCALPHA)
        pygame.draw.circle(obraz,(80,185,255),(16,16),14)
        pygame.draw.polygon(obraz,(230,245,255),[(16,4),(24,23),(16,19),(8,23)])
    elif jmeno in ('dron','hlidac'):
        obraz = pygame.Surface((28,28),pygame.SRCALPHA)
        barva = (245,135,90) if jmeno=='dron' else (190,145,255)
        for x,y in ((6,6),(22,6),(6,22),(22,22)):
            pygame.draw.line(obraz,barva,(14,14),(x,y),2)
            pygame.draw.circle(obraz,barva,(x,y),5,2)
        pygame.draw.circle(obraz,barva,(14,14),6)
    elif jmeno == 'data':
        obraz = pygame.Surface((20,20),pygame.SRCALPHA)
        pygame.draw.polygon(obraz,(90,235,170),[(10,0),(20,10),(10,20),(0,10)])
        pygame.draw.circle(obraz,(220,255,235),(10,10),3)
    else:
        raise KeyError(jmeno)
    return obraz

OBRAZY = BankaObrazu(vytvor_obraz)

class DatovyBod(pygame.sprite.Sprite):
    def __init__(self, stred):
        super().__init__()
        self.image=OBRAZY.obraz('data')
        self.rect=self.image.get_rect(center=stred)
        self.radius=10

def vstupy(hranice):
    l,r,t,b=hranice.left+14,hranice.right-14,hranice.top+14,hranice.bottom-14
    x,y=hranice.center
    return [(l,t),(x,t),(r,t),(r,y),(r,b),(x,b),(l,b),(l,y)]

def precti_smer(klavesy):
    prava=bool(klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d])
    leva=bool(klavesy[pygame.K_LEFT] or klavesy[pygame.K_a])
    dolu=bool(klavesy[pygame.K_DOWN] or klavesy[pygame.K_s])
    nahoru=bool(klavesy[pygame.K_UP] or klavesy[pygame.K_w])
    return pygame.Vector2(int(prava)-int(leva),int(dolu)-int(nahoru))
