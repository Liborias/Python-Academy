import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Kolize")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
hvezda = pygame.image.load("hvezda.png").convert_alpha()
raketa_rect = raketa.get_rect(center=(50, 100))
hvezda_rect = hvezda.get_rect(center=(300, 100))

# Úkol:
#   1. Dotýkají-li se raketa_rect a hvezda_rect (colliderect), je pozadí zelené (0, 60, 0), jinak (0, 0, 30).
#   2. Při kliknutí myší (MOUSEBUTTONDOWN) do hvězdy (collidepoint) vypište print("Zásah!"). Mimo hvězdu nic.

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        # TODO: sem patří kliknutí myší
    klavesy = pygame.key.get_pressed()          # pohyb rakety už je hotový
    if klavesy[pygame.K_LEFT]:
        raketa_rect.x -= 5
    if klavesy[pygame.K_RIGHT]:
        raketa_rect.x += 5
    # TODO: zjistěte kolizi a NAHRAĎTE následující řádek screen.fill výběrem barvy pozadí
    screen.fill((0, 0, 30))
    screen.blit(hvezda, hvezda_rect)
    screen.blit(raketa, raketa_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
