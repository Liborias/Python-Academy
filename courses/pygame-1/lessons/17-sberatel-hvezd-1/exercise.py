import random
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Sběratel hvězd")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
hvezda = pygame.image.load("hvezda.png").convert_alpha()
font = pygame.font.Font(None, 32)

raketa_rect = raketa.get_rect(center=(200, 450))
hvezdy = []
for i in range(4):
    hvezdy.append(hvezda.get_rect(topleft=(30 + i * 90, -i * 80)))
skore = 0

# Úkol (zadání je v lekci): ve smyčce
#   1. pohyb rakety šipkami doleva a doprava o 6 bodů za snímek, raketa nesmí vyjet z okna (rect.left >= 0, rect.right <= 400)
#   2. každá hvězda padá o 3 body za snímek; dotkne-li se rakety, skóre +1 a hvězda se vrátí nahoře (bottom = 0, náhodné x 0 až 368);
#      spadne-li pod okno (top > 500), vrátí se nahoře také, ale skóre se nemění
#   3. kreslení: pozadí (0, 0, 30), hvězdy, raketa, vlevo nahoře bílý text "Skóre: N" (písmo 32, levý horní roh (10, 10))

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří pohyb, kolize a kreslení
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
