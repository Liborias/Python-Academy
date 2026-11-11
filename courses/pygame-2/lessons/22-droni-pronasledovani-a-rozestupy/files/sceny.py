"""Malé režimy delegují na model a renderer. Zásobník pochází z lekce 20."""
import pygame
from herni_okno import vykresli_svet, vykresli_paticku, vykresli_pauzu, vykresli_nabidku, vykresli_vysledek

class Menu:
    jmeno='nabidka'
    def zpracuj(self,u):
        if u.type==pygame.KEYDOWN and u.key==pygame.K_SPACE:return 'start'
    def update(self,dt):pass
    def kresli(self,p):vykresli_nabidku(p)

class Let:
    jmeno='hra'
    def __init__(self,kolo):self.kolo=kolo;self.smer=pygame.Vector2()
    def zpracuj(self,u):
        if u.type==pygame.KEYDOWN:
            if u.key==pygame.K_p:return 'pauza'
            if u.key==pygame.K_r:return 'start'
    def update(self,dt):self.kolo.update(self.smer,dt)
    def kresli(self,p):vykresli_svet(p,self.kolo);vykresli_paticku(p,True)

class PauzaLetu:
    jmeno='pauza'
    def zpracuj(self,u):
        if u.type==pygame.KEYDOWN:
            if u.key==pygame.K_p:return 'zpet'
            if u.key==pygame.K_r:return 'start'
    def update(self,dt):pass
    def kresli(self,p):vykresli_pauzu(p)

class Vysledek:
    jmeno='vysledek'
    def __init__(self,kolo):self.kolo=kolo
    def zpracuj(self,u):
        if u.type==pygame.KEYDOWN:
            if u.key==pygame.K_r:return 'start'
            if u.key==pygame.K_SPACE:return 'nabidka'
    def update(self,dt):pass
    def kresli(self,p):
        vykresli_svet(p,self.kolo)
        vykresli_paticku(p,True)
        vykresli_vysledek(p,self.kolo,True)
