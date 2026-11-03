import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Konec hry")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 32)
font_velky = pygame.font.Font(None, 64)

# Úkol: hra s mezerníkem a stavem hry.
#   stav "hra":   pozadí (0, 0, 30), vlevo nahoře bílý text "Skóre: N" (písmo 32, levý horní roh (10, 10)).
#                 Každý stisk mezerníku zvýší skóre o 1. Při skóre 5 se stav změní na "konec".
#   stav "konec": pozadí (60, 0, 0), žlutý (255, 220, 0) text "Konec hry" (písmo 64, střed (200, 110)),
#                 bílý text "Skóre: 5" (písmo 32, střed (200, 170)) a bílý text "Stiskni R" (písmo 32, střed (200, 220)).
#                 Mezerník už nic nedělá. Klávesa R vynuluje skóre a vrátí stav "hra".
#   Klávesa R v průběhu hry nic nedělá.

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: stav hry, skóre a kreslení
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
