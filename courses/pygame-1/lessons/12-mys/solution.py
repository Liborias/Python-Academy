import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Myš")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
otisky = []

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
            otisky.append(udalost.pos)
    screen.fill((0, 0, 30))
    for pozice in otisky:
        pygame.draw.circle(screen, (200, 60, 60), pozice, 10)
    screen.blit(hvezda, hvezda.get_rect(center=pygame.mouse.get_pos()))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
