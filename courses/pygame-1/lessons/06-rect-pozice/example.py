import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Rect")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
r1 = hvezda.get_rect(topleft=(10, 10))                # poloha už při vytvoření: levý horní roh
r2 = hvezda.get_rect()                                # nejdřív jen velikost 32 × 32 ...
r2.center = (150, 100)                                # ... a pak nastavíme střed
r3 = hvezda.get_rect(bottomright=(290, 190))          # pravý dolní roh
print(r1.size, r2.topleft, r3.top)                    # (32, 32) (134, 84) 158

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((10, 10, 40))
    for rect in (r1, r2, r3):
        screen.blit(hvezda, rect)                     # blit bere přímo Rect
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
