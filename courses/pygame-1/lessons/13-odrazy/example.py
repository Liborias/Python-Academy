import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Odraz")
clock = pygame.time.Clock()

x, y = 50, 50                                          # poloha středu míče
vx, vy = 3, 2                                          # rychlost (body za snímek)
polomer = 10

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    x += vx
    y += vy
    if x - polomer < 0 or x + polomer > 300:           # narazil na levou nebo pravou stěnu
        vx = -vx                                       # obrátí se vodorovný směr
    if y - polomer < 0 or y + polomer > 200:           # narazil na horní nebo dolní stěnu
        vy = -vy
    screen.fill((20, 20, 20))
    pygame.draw.circle(screen, (0, 200, 255), (x, y), polomer)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
