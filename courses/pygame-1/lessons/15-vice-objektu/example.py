import random
import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Déšť")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
hvezdy = []                                              # seznam obdélníků
for i in range(4):
    hvezdy.append(hvezda.get_rect(topleft=(20 + i * 70, 0)))

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    for rect in hvezdy:                                  # pohyb všech hvězd
        rect.y += 2
        if rect.top > 200:
            rect.bottom = 0
            rect.x = random.randint(0, 268)              # náhodné x, celé číslo včetně obou mezí
    screen.fill((0, 0, 30))
    for rect in hvezdy:                                  # kreslení všech hvězd
        screen.blit(hvezda, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
