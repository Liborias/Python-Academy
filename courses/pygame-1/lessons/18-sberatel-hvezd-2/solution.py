import random
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Sběratel hvězd")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
hvezda = pygame.image.load("hvezda.png").convert_alpha()
font = pygame.font.Font(None, 32)
font_velky = pygame.font.Font(None, 64)
cinknuti = pygame.mixer.Sound("cinknuti.wav")
pygame.mixer.music.load("hudba.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

raketa_rect = raketa.get_rect(center=(200, 450))
hvezdy = []
for i in range(4):
    hvezdy.append(hvezda.get_rect(topleft=(30 + i * 90, -i * 80)))
skore = 0
zivoty = 3
stav = "hra"

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_r and stav == "konec":
            skore = 0
            zivoty = 3
            stav = "hra"
            raketa_rect.center = (200, 450)
            for i in range(len(hvezdy)):
                hvezdy[i].topleft = (30 + i * 90, -i * 80)

    if stav == "hra":
        klavesy = pygame.key.get_pressed()
        if klavesy[pygame.K_LEFT]:
            raketa_rect.x -= 6
        if klavesy[pygame.K_RIGHT]:
            raketa_rect.x += 6
        if raketa_rect.left < 0:
            raketa_rect.left = 0
        if raketa_rect.right > 400:
            raketa_rect.right = 400

        for rect in hvezdy:
            rect.y += 3
            if raketa_rect.colliderect(rect):
                skore += 1
                cinknuti.play()
                rect.bottom = 0
                rect.x = random.randint(0, 368)
            elif rect.top > 500:
                zivoty -= 1
                rect.bottom = 0
                rect.x = random.randint(0, 368)
        if zivoty <= 0:
            stav = "konec"

    if stav == "hra":
        screen.fill((0, 0, 30))
        for rect in hvezdy:
            screen.blit(hvezda, rect)
        screen.blit(raketa, raketa_rect)
        screen.blit(font.render(f"Skóre: {skore}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Životy: {zivoty}", True, (255, 255, 255)), (10, 40))
    else:
        screen.fill((60, 0, 0))
        nadpis = font_velky.render("Konec hry", True, (255, 220, 0))
        screen.blit(nadpis, nadpis.get_rect(center=(200, 200)))
        vysledek = font.render(f"Skóre: {skore}", True, (255, 255, 255))
        screen.blit(vysledek, vysledek.get_rect(center=(200, 260)))
        napoveda = font.render("Stiskni R", True, (255, 255, 255))
        screen.blit(napoveda, napoveda.get_rect(center=(200, 310)))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
