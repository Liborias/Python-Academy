import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Řízení rakety")
clock = pygame.time.Clock()

# Úkol: raketa začíná se středem v (200, 150), pozadí (0, 0, 30).
# Šipky: pohyb o 5 bodů za snímek (plynule, i šikmo). Mezerník (KEYDOWN): návrat do středu (200, 150).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří klávesy, pohyb a kreslení
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
