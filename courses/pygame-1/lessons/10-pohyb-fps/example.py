import pygame

pygame.init()
screen = pygame.display.set_mode((300, 150))
pygame.display.set_caption("Pohyb")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
rect = hvezda.get_rect(center=(20, 75))
rychlost = 3                                          # body za snímek

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    rect.x += rychlost                                # posun o rychlost bodů doprava
    if rect.left > 300:                               # za pravým okrajem ...
        rect.right = 0                                # ... se objeví zleva
    screen.fill((0, 0, 30))                           # pozadí se musí překreslit, jinak zůstane stopa
    screen.blit(hvezda, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
