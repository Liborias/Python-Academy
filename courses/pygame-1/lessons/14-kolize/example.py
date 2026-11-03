import pygame

pygame.init()
screen = pygame.display.set_mode((300, 150))
pygame.display.set_caption("Dotyk")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
a = hvezda.get_rect(center=(60, 75))                    # pohyblivá hvězda
b = hvezda.get_rect(center=(200, 75))                   # stojící hvězda

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    a.x += 2                                            # a se posouvá doprava
    if a.x > 300:
        a.x = -32
    dotyk = a.colliderect(b)                            # True, když se obdélníky překrývají
    screen.fill((60, 0, 0) if dotyk else (0, 0, 30))    # při dotyku je pozadí červené
    screen.blit(hvezda, a)
    screen.blit(hvezda, b)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
