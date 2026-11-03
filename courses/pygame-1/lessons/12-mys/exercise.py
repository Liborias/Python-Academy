import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Myš")
clock = pygame.time.Clock()

# Úkol: hvězda má střed v místě kurzoru; levé tlačítko po sobě nechá trvalý červený otisk
# (kruh (200, 60, 60), poloměr 10); pravé tlačítko nic nedělá. Pozadí (0, 0, 30).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří poloha myši, otisky a kreslení
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
