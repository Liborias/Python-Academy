"""Volitelná živá ukázka Úkolu 5: po uložení reseni.py spusťte python ziva_dilna.py."""
import pygame
from reseni import RidicScen
from rezimy import ZasobnikRezimu, Nabidka, Tlacitko, Pauza
from podklady import CvicnyRezim

def main():
    pygame.display.init();pygame.font.init()
    okno=pygame.display.set_mode((720,420))
    pygame.display.set_caption('Herní režimy — Dílna Pythonu')
    font=pygame.font.Font(None,28)
    def vytvor(jmeno):
        if jmeno=='nabidka':
            return Nabidka([Tlacitko((180,120,360,60),'Spustit dílnu','hra',font),Tlacitko((180,210,360,60),'Ukončit','konec',font)])
        if jmeno=='hra':return CvicnyRezim('P: pauza / pokračování    M: nabídka')
        if jmeno=='pauza':return Pauza(font)
        raise KeyError(jmeno)
    ridic=RidicScen(ZasobnikRezimu(vytvor('nabidka')),vytvor)
    hodiny=pygame.time.Clock()
    try:
        while ridic.bezi:
            dt=min(hodiny.tick(60)/1000,0.05)
            for udalost in pygame.event.get():
                if udalost.type==pygame.KEYDOWN and udalost.key==pygame.K_ESCAPE:
                    udalost=pygame.event.Event(pygame.QUIT)
                ridic.zpracuj(udalost)
            ridic.update(dt)
            okno.fill((14,23,37))
            ridic.kresli(okno)
            pygame.display.flip()
    finally:
        pygame.image.save(okno,'rezimy-zive.png')
        pygame.quit()
        print('Poslední snímek: rezimy-zive.png')

if __name__=='__main__':main()
