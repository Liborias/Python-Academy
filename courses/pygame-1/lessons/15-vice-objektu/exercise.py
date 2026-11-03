import random
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Déšť hvězd")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
# Úkol: seznam pěti hvězd (get_rect(topleft=(40 + i * 80, -i * 60))), každá padá 3 body za snímek;
# pod oknem (rect.top > 300) se hvězda objeví nahoře (rect.bottom = 0) na náhodném x (0 až 368).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří pohyb a kreslení všech hvězd
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
