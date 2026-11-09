"""Společný vzhled a smyčka. Herní pravidla pocházejí z předaného modelu."""
import pygame

def vykresli(okno, hra, font, velky):
    kolo = hra.kolo
    okno.fill((12, 19, 34))
    for i in range(45):
        pygame.draw.circle(okno, (58, 77, 108), (20 + (i * 73 + 11) % 600, 70 + (i * 47 + 15) % 390), 1)
    pygame.draw.rect(okno, (42, 63, 94), kolo.hranice, 1)
    okno.blit(velky.render('METEORITY', True, (220, 237, 255)), (20, 12))
    okno.blit(font.render(f'Skóre: {kolo.skore}', True, (245, 220, 140)), (265, 22))
    if kolo.zdravi is not None:
        okno.blit(font.render(f'Životy: {kolo.zdravi.zivoty}', True, (220, 237, 255)), (445, 22))
    puvodni_vyrez = okno.get_clip()
    okno.set_clip(kolo.hranice)
    if kolo.proud is not None:
        kolo.proud.objekty.draw(okno)
    kolo.bonusy.draw(okno)
    okno.blit(kolo.hrac.image, kolo.hrac.rect)
    if kolo.stit:
        pygame.draw.circle(okno, (90, 235, 190), kolo.hrac.rect.center, 28, 2)
    if kolo.zdravi is not None and kolo.zdravi.nezranitelnost > 0:
        pygame.draw.circle(okno, (255, 175, 110), kolo.hrac.rect.center, 24, 1)
    okno.set_clip(puvodni_vyrez)
    napoveda = 'Šipky: pohyb   P: pauza   R: nový let   Esc: konec' if hra.restart_povolen else 'Šipky: pohyb   Zavření okna: konec'
    okno.blit(font.render(napoveda, True, (145, 166, 194)), (20, 462))
    konec = kolo.zdravi is not None and kolo.zdravi.zivoty == 0
    if hra.pauza or konec:
        panel = pygame.Surface((460, 145), pygame.SRCALPHA)
        panel.fill((8, 15, 29, 235))
        pygame.draw.rect(panel, (80, 150, 210), panel.get_rect(), 2, border_radius=12)
        panel.blit(velky.render('KONEC LETU' if konec else 'PAUZA', True, (230, 242, 255)), (24, 20))
        info = 'R: nový let   Esc: konec' if hra.restart_povolen else 'Zavři okno a spusť ukázku znovu.'
        if not konec:info = 'Pokračuj klávesou P.'
        panel.blit(font.render(info, True, (175, 202, 229)), (24, 84))
        okno.blit(panel, (90, 165))

def spustit(hra, precti_smer):
    pygame.display.init()
    pygame.font.init()
    okno = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Meteority — Dílna Pythonu')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)
    velky = pygame.font.Font(None, 34)
    try:
        while hra.bezi:
            # Dlouhá prodleva neposune svět jedním obrovským skokem.
            dt = min(clock.tick(60) / 1000, 0.05)
            for udalost in pygame.event.get():
                hra.zpracuj(udalost)
            smer = precti_smer(pygame.key.get_pressed())
            hra.update(smer, dt)
            vykresli(okno, hra, font, velky)
            pygame.display.flip()
    finally:
        # Před zavřením displeje zachováme poslední skutečný snímek.
        pygame.image.save(okno, 'meteority.png')
        pygame.quit()
        print('Poslední snímek: meteority.png')
