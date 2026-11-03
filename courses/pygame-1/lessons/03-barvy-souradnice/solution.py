import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Vlajka")
clock = pygame.time.Clock()

MODRA = (0, 85, 164)
BILA = (255, 255, 255)
CERVENA = (239, 65, 53)

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill(MODRA, (0, 0, 100, 200))
    screen.fill(BILA, (100, 0, 100, 200))
    screen.fill(CERVENA, (200, 0, 100, 200))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
