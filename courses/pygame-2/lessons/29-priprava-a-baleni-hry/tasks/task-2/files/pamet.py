import pygame
import herni_okno
def vykresli_pamet(plocha, hra):
    font = herni_okno.FONTY.font(20)
    pygame.draw.rect(plocha, (10, 20, 32), (20, 489, 680, 51))
    jmeno = hra.jmeno if len(hra.jmeno) <= 16 else hra.jmeno[:15] + '…'
    radky = [
        'Šipky/WASD: pohyb   P: pauza   R: nový let   Esc: konec',
        f'{jmeno} | {hra.rychlost:g} px/s | {hra.zprava}',
    ]
    for i, text in enumerate(radky):
        plocha.blit(font.render(text, True, (155, 205, 210)), (24, 493 + i * 24))
    if hra.stav == 'nabidka' and hra.vysledky:
        plocha.blit(font.render('Nejlepší výsledky', True, (255, 210, 130)), (110, 403))
        maly = herni_okno.FONTY.font(18)
        for poradi, z in enumerate(hra.vysledky[:5], 1):
            y = 423 + (poradi - 1) * 14
            plocha.blit(maly.render(f"{poradi}. {z['jmeno']}", True, (205, 225, 235)), (110, y))
            plocha.blit(maly.render(f"{z['body']} dat", True, (205, 225, 235)), (440, y))
            stav = 'mise hotová' if z['uspech'] else 'nedokončeno'
            plocha.blit(maly.render(stav, True, (155, 205, 210)), (530, y))
