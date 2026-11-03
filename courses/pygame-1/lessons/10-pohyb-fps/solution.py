import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Let rakety")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
rect = raketa.get_rect(center=(32, 100))
rychlost = 5

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 30))
    screen.blit(raketa, rect)
    rect.x += rychlost
    if rect.left > 400:
        rect.right = 0
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
