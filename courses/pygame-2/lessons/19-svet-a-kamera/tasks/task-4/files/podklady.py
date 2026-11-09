"""Vlastní grafika a krátký tón. Import neotevírá okno ani zvukové zařízení."""
from pathlib import Path
import math
import struct
import wave
import pygame

BARVY = [(80,180,255), (90,220,175), (235,160,85), (195,145,255)]

def robot(barva=(80,180,255), rozmer=(48,48)):
    obraz = pygame.Surface(rozmer, pygame.SRCALPHA)
    w, h = rozmer
    pygame.draw.rect(obraz, barva, (4, 8, w-8, h-12), border_radius=6)
    for x in (w//3, 2*w//3):
        pygame.draw.circle(obraz, (15,25,40), (x,h//2), 3)
    pygame.draw.line(obraz, barva, (w//2,8), (w//2,1), 2)
    return obraz

def snimky(pocet=4):
    vysledek=[]
    for i in range(pocet):
        obraz=robot(BARVY[i % len(BARVY)])
        pygame.draw.circle(obraz,(245,240,160),(10+i*8,38),4)
        vysledek.append(obraz)
    return vysledek

def pas_snimku():
    obraz=pygame.Surface((192,48),pygame.SRCALPHA)
    for i,snimek in enumerate(snimky()):obraz.blit(snimek,(48*i,0))
    return obraz

def tvar(barva=(80,180,255), plny=False):
    obraz=pygame.Surface((80,80),pygame.SRCALPHA)
    pygame.draw.circle(obraz,barva,(40,40),34,0 if plny else 8)
    return obraz

class Bod(pygame.sprite.Sprite):
    def __init__(self, obraz, roh, radius=None):
        super().__init__()
        self.image=obraz.copy()
        self.rect=self.image.get_rect(topleft=roh)
        self.mask=pygame.mask.from_surface(self.image)
        self.radius=radius if radius is not None else min(self.rect.size)/2

class CvicnyRezim:
    def __init__(self, jmeno, barva=(30,65,90)):
        self.jmeno=jmeno
        self.barva=barva
        self.cas=0.0

    def zpracuj(self, udalost):
        if udalost.type==pygame.KEYDOWN:
            if udalost.key==pygame.K_p:return 'pauza'
            if udalost.key==pygame.K_m:return 'nabidka'
        return None

    def update(self, dt):self.cas+=dt

    def kresli(self, plocha):
        plocha.fill(self.barva)
        pygame.font.init()
        font=pygame.font.Font(None,28)
        plocha.blit(font.render(self.jmeno,True,(235,243,255)),(20,18))
        napis=font.render(f'Herní čas: {self.cas:.2f} s',True,(150,225,210))
        plocha.blit(napis,(20,55))
        x=40+(self.cas*120)%max(1,plocha.get_width()-80)
        plocha.blit(robot(),(round(x),max(80,plocha.get_height()//2)))

def priprav_media():
    slozka=Path(__file__).resolve().parent/'media'
    slozka.mkdir(exist_ok=True)
    for jmeno,barva in [('robot',BARVY[0]),('stit',BARVY[1])]:
        cesta=slozka/(jmeno+'.bmp')
        if not cesta.exists():pygame.image.save(robot(barva),str(cesta))
    cesta=slozka/'ton.wav'
    if not cesta.exists():
        vzorkovani=22050
        data=b''.join(struct.pack('<h',round(2500*math.sin(2*math.pi*440*i/vzorkovani))) for i in range(vzorkovani//5))
        with wave.open(str(cesta),'wb') as wav:
            wav.setparams((1,2,vzorkovani,0,'NONE','not compressed'))
            wav.writeframes(data)
    return slozka
