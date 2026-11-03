import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Text")
clock = pygame.time.Clock()

# Úkol: nadpis "Sběratel hvězd" (žlutá (255, 220, 0), velikost 48, střed v bodě (200, 50))
#       a text "Skóre: 0" (bílá, velikost 32, levý dolní roh v bodě (10, 190)); pozadí (0, 0, 40).
# Číslo skóre ukládejte do proměnné skore a text sestavte f-řetězcem.

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem kreslete
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
