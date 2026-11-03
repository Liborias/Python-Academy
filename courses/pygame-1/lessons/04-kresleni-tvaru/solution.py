import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Domeček")
clock = pygame.time.Clock()

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (34, 139, 34), (0, 220, 400, 80))
    pygame.draw.rect(screen, (160, 110, 60), (150, 140, 100, 80))
    pygame.draw.polygon(screen, (200, 40, 40), [(140, 140), (260, 140), (200, 90)])
    pygame.draw.circle(screen, (255, 220, 0), (340, 50), 30)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
