import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pohlednice")
clock = pygame.time.Clock()

# Úkol: složte scénu podle zadání v lekci (hvězdy ze seznamu HVEZDY, planeta, raketa, nadpis).
# Obrázky a písmo vytvořte před smyčkou, pozadí je (10, 10, 40).

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem kreslete
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
