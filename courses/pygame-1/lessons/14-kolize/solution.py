import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Kolize")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
hvezda = pygame.image.load("hvezda.png").convert_alpha()
raketa_rect = raketa.get_rect(center=(50, 100))
hvezda_rect = hvezda.get_rect(center=(300, 100))

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.MOUSEBUTTONDOWN:
            if hvezda_rect.collidepoint(udalost.pos):
                print("Zásah!")
    klavesy = pygame.key.get_pressed()
    if klavesy[pygame.K_LEFT]:
        raketa_rect.x -= 5
    if klavesy[pygame.K_RIGHT]:
        raketa_rect.x += 5
    if raketa_rect.colliderect(hvezda_rect):
        barva = (0, 60, 0)
    else:
        barva = (0, 0, 30)
    screen.fill(barva)
    screen.blit(hvezda, hvezda_rect)
    screen.blit(raketa, raketa_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
