import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Rect")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
rect_a = raketa.get_rect(topleft=(10, 10))
rect_b = raketa.get_rect(topright=(390, 10))
rect_c = raketa.get_rect(bottomleft=(10, 290))
rect_d = raketa.get_rect(bottomright=(390, 290))
rect_e = raketa.get_rect()
rect_e.center = (200, 150)
print(rect_e.center)

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((20, 20, 60))
    for rect in (rect_a, rect_b, rect_c, rect_d, rect_e):
        screen.blit(raketa, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
