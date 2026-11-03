import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Odrazy")
clock = pygame.time.Clock()

# Úkol: míč (kruh (255, 200, 0), poloměr 15) začíná se středem v (100, 100), vx = 4, vy = 3.
# Odráží se od všech čtyř stěn okna a nikdy ho neopustí. Pozadí (0, 0, 30).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří pohyb, odrazy a kreslení
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
