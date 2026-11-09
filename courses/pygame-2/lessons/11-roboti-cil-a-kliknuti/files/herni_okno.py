"""Skutečné SDL okno. Pravidla a kliknutí patří předanému modelu."""
import pygame
from podklady import HRANICE, obraz_robota

def vykresli(okno, hra, font, maly, velky):
    okno.fill((13, 23, 35))
    for x in range(24, 697, 24):
        pygame.draw.line(okno, (23, 39, 53), (x, 96), (x, 456))
    for y in range(96, 457, 24):
        pygame.draw.line(okno, (23, 39, 53), (24, y), (696, y))
    pygame.draw.rect(okno, (56, 90, 112), HRANICE, 1)
    okno.blit(velky.render('CHYŤ ROBOTA', True, (100, 235, 205)), (24, 15))
    okno.blit(maly.render('ZÁCHRANNÁ DÍLNA / 03', True, (154, 183, 201)), (485, 27))
    kolo = hra.kolo
    if kolo is not None:
        lov = kolo.lov
        for text, x in [(f'Body: {lov.skore}', 24), (f'Životy: {lov.zivoty}', 156), (f'Přesnost: {lov.presnost():.0f} %', 286), (f'Vlna: {kolo.cislo}', 470)]:
            okno.blit(font.render(text, True, (222, 234, 242)), (x, 62))
        cas = 'bez limitu' if kolo.zbyva is None else f'{kolo.zbyva:.1f} s'
        okno.blit(font.render(cas, True, (255, 208, 120)), (580, 62))
        predchozi = okno.get_clip()
        okno.set_clip(kolo.hranice)
        lov.roboty.draw(okno)
        okno.set_clip(predchozi)
        bod = pygame.mouse.get_pos()
        if kolo.hranice.collidepoint(bod) and hra.stav == 'hra':
            pygame.draw.circle(okno, (245, 238, 195), bod, 9, 1)
            pygame.draw.line(okno, (245, 238, 195), (bod[0] - 13, bod[1]), (bod[0] + 13, bod[1]), 1)
            pygame.draw.line(okno, (245, 238, 195), (bod[0], bod[1] - 13), (bod[0], bod[1] + 13), 1)
    text = 'Levé tlačítko: chytit   P: pauza   R: nový lov   Esc: konec' if hra.nabidka_povolena else 'Levé tlačítko: chytit robota   Esc / zavření okna: konec'
    okno.blit(maly.render(text, True, (161, 189, 205)), (24, 477))
    okno.blit(maly.render('Chycení: body podle robota   Minutí: -1 život   Klikáme do kruhu', True, (117, 152, 173)), (24, 499))
    if hra.stav == 'nabidka':
        panel = pygame.Surface((600, 300), pygame.SRCALPHA)
        panel.fill((10, 22, 34, 245))
        pygame.draw.rect(panel, (55, 205, 177), panel.get_rect(), 2, border_radius=14)
        panel.blit(velky.render('Roboti utekli z dílny!', True, (226, 242, 248)), (28, 22))
        panel.blit(font.render('Chytej je kliknutím do kruhu. Každé minutí stojí život.', True, (173, 201, 218)), (28, 67))
        panel.blit(font.render('Máš 30 herních sekund a tři životy. Přibývají rychlejší vlny.', True, (173, 201, 218)), (28, 95))
        for x, barva in [(120, (55, 205, 177)), (290, (80, 170, 255)), (460, (195, 145, 255))]:
            panel.blit(obraz_robota(28, barva), (x - 28, 145))
        panel.blit(font.render('MEZERNÍK: začít lov', True, (255, 217, 133)), (190, 236))
        okno.blit(panel, (60, 125))
    elif hra.stav in ('pauza', 'vysledek'):
        panel = pygame.Surface((500, 190), pygame.SRCALPHA)
        panel.fill((10, 22, 34, 245))
        pygame.draw.rect(panel, (55, 205, 177), panel.get_rect(), 2, border_radius=14)
        duvody = {'cas': 'ČAS VYPRŠEL', 'zivoty': 'DOŠLY ŽIVOTY', 'lapeni': 'ROBOTI LAPENI'}
        titulek = 'PAUZA' if hra.stav == 'pauza' else duvody.get(kolo.duvod, 'KONEC LOVU')
        panel.blit(velky.render(titulek, True, (226, 242, 248)), (24, 22))
        panel.blit(font.render(f'Body: {kolo.lov.skore}   Zásahy: {kolo.lov.zasahy}   Přesnost: {kolo.lov.presnost():.0f} %', True, (183, 211, 226)), (24, 77))
        if hra.nabidka_povolena:
            info = 'P: pokračovat   R: nový lov' if hra.stav == 'pauza' else 'R: nový lov   Mezerník: nabídka'
        else:
            info = 'Zavři okno a spusť ukázku znovu.'
        panel.blit(font.render(info, True, (255, 217, 133)), (24, 132))
        okno.blit(panel, (110, 175))

def spustit(hra):
    pygame.display.init()
    pygame.font.init()
    okno = pygame.display.set_mode((720, 520))
    pygame.display.set_caption('Chyť robota — Dílna Pythonu')
    font, maly, velky = (pygame.font.Font(None, n) for n in (23, 20, 34))
    hodiny = pygame.time.Clock()
    try:
        while hra.bezi:
            dt = min(hodiny.tick(60) / 1000, 0.05)
            # Nejdřív uplyne čas. Kliknutí po vypršení limitu už nemůže bodovat.
            hra.update(dt)
            for udalost in pygame.event.get():
                hra.zpracuj(udalost)
            vykresli(okno, hra, font, maly, velky)
            pygame.display.flip()
    finally:
        pygame.image.save(okno, 'roboti.png')
        pygame.quit()
        print('Poslední snímek: roboti.png')
