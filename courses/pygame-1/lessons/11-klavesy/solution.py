import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Řízení rakety")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
rect = raketa.get_rect(center=(200, 150))
rychlost = 5

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE:
            rect.center = (200, 150)
    klavesy = pygame.key.get_pressed()
    if klavesy[pygame.K_LEFT]:
        rect.x -= rychlost
    if klavesy[pygame.K_RIGHT]:
        rect.x += rychlost
    if klavesy[pygame.K_UP]:
        rect.y -= rychlost
    if klavesy[pygame.K_DOWN]:
        rect.y += rychlost
    screen.fill((0, 0, 30))
    screen.blit(raketa, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
