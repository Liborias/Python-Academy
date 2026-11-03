import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Obrázky")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()    # načtení JEDNOU před smyčkou
rect = hvezda.get_rect(center=(150, 100))                   # obdélník obrázku se středem uprostřed okna

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((10, 10, 40))
    screen.blit(hvezda, rect)                               # vykreslení v každém průchodu
    screen.blit(hvezda, (20, 20))                           # stejný obrázek lze vykreslit víckrát
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
