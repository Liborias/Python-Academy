import random
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Déšť hvězd")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
hvezdy = []
for i in range(5):
    hvezdy.append(hvezda.get_rect(topleft=(40 + i * 80, -i * 60)))

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    for rect in hvezdy:
        rect.y += 3
        if rect.top > 300:
            rect.bottom = 0
            rect.x = random.randint(0, 368)
    screen.fill((0, 0, 30))
    for rect in hvezdy:
        screen.blit(hvezda, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
