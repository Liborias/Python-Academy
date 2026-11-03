import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Let rakety")
clock = pygame.time.Clock()

# Úkol: raketa letí zleva doprava rychlostí 5 bodů za snímek, střed ve výšce 100 (začíná se středem v bodě (32, 100)).
# Když je celá za pravým okrajem okna, objeví se znovu zleva.

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří pohyb a kreslení
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
