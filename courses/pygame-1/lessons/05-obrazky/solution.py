import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Obrázky")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
hvezda = pygame.image.load("hvezda.png").convert_alpha()
raketa_rect = raketa.get_rect(center=(200, 150))

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((20, 20, 60))
    screen.blit(raketa, raketa_rect)
    screen.blit(hvezda, (50, 50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
