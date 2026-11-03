import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Odrazy")
clock = pygame.time.Clock()

x, y = 100, 100
vx, vy = 4, 3
polomer = 15

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    x += vx
    y += vy
    if x - polomer < 0 or x + polomer > 400:
        vx = -vx
    if y - polomer < 0 or y + polomer > 300:
        vy = -vy
    screen.fill((0, 0, 30))
    pygame.draw.circle(screen, (255, 200, 0), (x, y), polomer)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
