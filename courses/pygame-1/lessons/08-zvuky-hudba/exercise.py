import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Zvuky")
clock = pygame.time.Clock()

# Úkol: hudba.wav (hlasitost 0.5, opakovat pořád dokola) a cinknuti.wav (přehrát při stisku mezerníku).
# Pozadí okna (30, 30, 30).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem patří překreslení pozadí a pokyny pro zvuk
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
