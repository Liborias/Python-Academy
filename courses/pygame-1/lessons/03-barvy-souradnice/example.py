import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Pruhy")
clock = pygame.time.Clock()

ZELENA = (0, 150, 70)                                  # konstanty: jména velkými písmeny
ORANGOVA = (255, 140, 0)

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill(ZELENA)                                # nejdřív celé okno
    screen.fill(ORANGOVA, (0, 0, 150, 100))            # pak obdélník: levý horní roh (0, 0), šířka 150, výška 100
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
