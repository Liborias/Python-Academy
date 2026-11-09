"""Obrázková laboratoř: skutečné Surface bez smyčky a bez displeje."""
from pathlib import Path
import pygame

def karta(nadpis):
    pygame.font.init()
    plocha=pygame.Surface((720,420))
    plocha.fill((14,23,37))
    font=pygame.font.Font(None,29)
    plocha.blit(font.render(nadpis,True,(120,225,205)),(20,18))
    pygame.draw.line(plocha,(50,75,98),(20,58),(700,58),1)
    return plocha

def radek(plocha, text, y=370):
    font=pygame.font.Font(None,22)
    plocha.blit(font.render(str(text),True,(205,222,239)),(24,y))

def obrazky(plocha, polozky):
    font=pygame.font.Font(None,21)
    for i,(obraz,popis) in enumerate(polozky):
        x=25+(i%4)*174;y=88+(i//4)*135
        for a in range(0,144,12):
            for b in range(0,96,12):
                barva=(35,49,65) if (a//12+b//12)%2 else (47,62,78)
                pygame.draw.rect(plocha,barva,(x+a,y+b,12,12))
        w,h=obraz.get_size()
        pomer=min(1,132/w,88/h)
        kresba=pygame.transform.scale(obraz,(max(1,round(w*pomer)),max(1,round(h*pomer))))
        plocha.blit(kresba,kresba.get_rect(center=(x+72,y+48)))
        plocha.blit(font.render(str(popis),True,(220,233,246)),(x,y+102))

def uloz(plocha):
    cesta=Path('soucasti.png')
    pygame.image.save(plocha,str(cesta))
    print('Náhled:',cesta)
