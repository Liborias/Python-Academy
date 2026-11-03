import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Tvary")
clock = pygame.time.Clock()

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((20, 20, 40))                                           # pozadí se kreslí jako první
    pygame.draw.rect(screen, (200, 60, 60), (20, 20, 100, 60))          # vyplněný obdélník
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 100, 60), 3)     # obrys tlustý 3 body
    pygame.draw.circle(screen, (250, 220, 0), (200, 50), 30)            # střed (200, 50), poloměr 30
    pygame.draw.line(screen, (0, 200, 120), (20, 150), (280, 120), 4)   # úsečka tlustá 4 body
    pygame.draw.polygon(screen, (90, 140, 255), [(150, 190), (200, 120), (250, 190)])   # trojúhelník
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
