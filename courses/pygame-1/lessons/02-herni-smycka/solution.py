import pygame

pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Herní smyčka")
clock = pygame.time.Clock()

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_ESCAPE:
            running = False
    screen.fill((30, 30, 60))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
