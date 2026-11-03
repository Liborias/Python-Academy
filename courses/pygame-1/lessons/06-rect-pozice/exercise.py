import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Rect")
clock = pygame.time.Clock()

# Načtěte raketa.png (jednou, před smyčkou) a vytvořte pět obdélníků (Rect) podle zadání:
#   levý horní roh (10, 10), pravý horní roh (390, 10), levý dolní roh (10, 290),
#   pravý dolní roh (390, 290) a střed (200, 150).
# Střed prostřední rakety vypište pomocí print(...). Pozadí je (20, 20, 60).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem kreslete
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
