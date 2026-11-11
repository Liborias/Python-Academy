"""Jediná skutečná SDL smyčka a společný vzhled projektu."""
import math
import pygame
from zdroje import BankaFontu
from podklady import HRANICE,ZONA,OBRAZY,precti_smer,vstupy

FONTY=BankaFontu(lambda n:pygame.font.Font(None,n))

def napis(p,text,bod,velikost=22,barva=(220,235,246)):
    p.blit(FONTY.font(velikost).render(str(text),True,barva),bod)

def vykresli_paticku(p,plna):
    text='Šipky / WASD: pohyb   P: pauza   R: nový let   Esc: konec' if plna else 'Šipky / WASD: pohyb   Esc / zavření okna: konec'
    napis(p,text,(24,493),20,(155,186,205))
    napis(p,'Zelená data: sběr   Přístav: ochrana 2,5 s, obnova mimo něj',(24,518),19,(105,157,175))

def vykresli_svet(p,k):
    p.fill((10,20,32))
    for x in range(24,697,28):pygame.draw.line(p,(21,37,52),(x,90),(x,480))
    for y in range(90,481,26):pygame.draw.line(p,(21,37,52),(24,y),(696,y))
    pygame.draw.rect(p,(49,76,96),k.hranice,1)
    for bod in vstupy(k.hranice):pygame.draw.circle(p,(65,85,110),bod,7,1)
    zona=getattr(k,'zona',ZONA)
    pygame.draw.rect(p,(15,47,51),zona,border_radius=14)
    pygame.draw.rect(p,(50,165,145),zona,2,border_radius=14)
    napis(p,'PŘÍSTAV',(zona.centerx-35,zona.bottom-27),18,(85,185,165))
    napis(p,'HON NA DRONECH',(24,14),30,(100,225,210))
    napis(p,'DATOVÝ KURÝR / 03',(480,24),19,(150,180,200))
    napis(p,f'Data: {k.skore}/6',(24,61))
    vlny=getattr(k,'vlny',None)
    napis(p,f'Vlna: {vlny.cislo}/3' if vlny is not None else 'Trénink',(155,61))
    zbyva=getattr(k,'zbyva',None)
    napis(p,f'{zbyva:.1f} s' if zbyva is not None else 'Bez limitu',(285,61),22,(255,210,130))
    zivoty=getattr(k,'zivoty',None)
    napis(p,f'Životy: {zivoty}' if zivoty is not None else 'Bez zásahů',(400,61))
    stit=getattr(k,'stit',None)
    napis(p,f'Štít: {stit.energie:.1f} s' if stit is not None else 'Štít od kroku 24',(540,61),20,(105,225,180))
    old=p.get_clip()
    p.set_clip(old.clip(k.hranice))
    pulz=12+round(2*math.sin(k.cas*4))
    pygame.draw.circle(p,(40,95,75),k.data.rect.center,pulz,1)
    p.blit(k.data.image,k.data.rect)
    k.drony.draw(p)
    p.blit(k.hrac.image,k.hrac.rect)
    if getattr(k,'chraneno',False):pygame.draw.circle(p,(90,240,185),k.hrac.rect.center,23,2)
    if getattr(k,'nezranitelnost',0)>0:pygame.draw.circle(p,(255,175,110),k.hrac.rect.center,20,1)
    p.set_clip(old)

def panel(p,nadpis,radky):
    vrstva=pygame.Surface((560,240),pygame.SRCALPHA)
    vrstva.fill((9,20,33,242))
    pygame.draw.rect(vrstva,(75,185,180),vrstva.get_rect(),2,border_radius=14)
    napis(vrstva,nadpis,(25,22),34,(225,245,250))
    for i,text in enumerate(radky):napis(vrstva,text,(25,80+i*34),22,(180,210,225))
    p.blit(vrstva,(80,155))

def vykresli_pauzu(p):
    panel(p,'PAUZA',['Svět i čas čekají na pokračování.','P: pokračovat   R: nový let','Esc: konec aplikace'])

def vykresli_vysledek(p,k,plna):
    nadpis={'uspech':'MISE SPLNĚNA','data':'CHYBÍ DATA','zivoty':'DOŠLY ŽIVOTY'}.get(k.duvod,'KONEC LETU')
    volba='R: nový let   Mezerník: nabídka' if plna else 'Zavři okno a spusť ukázku znovu.'
    panel(p,nadpis,[f'Sesbíráno dat: {k.skore}   Dokončovaná vlna: {k.vlny.cislo}',volba,'Esc: konec aplikace'])

def vykresli_nabidku(p):
    p.fill((10,20,32))
    napis(p,'HON NA DRONECH',(180,48),42,(100,225,210))
    for x,jmeno in [(210,'dron'),(345,'hrac'),(480,'hlidac')]:p.blit(OBRAZY.obraz(jmeno),(x,110))
    panel(p,'Doruč data přes hlídané pole',[
        'Sesbírej alespoň 6 dat a přežij 3 vlny po 10 s.',
        'Přístav chrání krátce; štít obnovíš mimo něj.',
        'MEZERNÍK: start   Šipky / WASD: pohyb',
        'P: pauza   R: nový let   Esc: konec'])
    vykresli_paticku(p,True)

def spustit(hra):
    global FONTY
    pygame.display.init()
    pygame.font.init()
    FONTY=BankaFontu(lambda n:pygame.font.Font(None,n))
    p=pygame.display.set_mode((720,540))
    pygame.display.set_caption('Hon na dronech — Dílna Pythonu')
    hodiny=pygame.time.Clock()
    try:
        while hra.bezi:
            dt=min(hodiny.tick(60)/1000,0.05)
            for u in pygame.event.get():hra.zpracuj(u)
            hra.update(precti_smer(pygame.key.get_pressed()),dt)
            hra.kresli(p)
            pygame.display.flip()
    finally:
        pygame.image.save(p,'droni.png')
        pygame.quit()
        print('Poslední snímek: droni.png')
