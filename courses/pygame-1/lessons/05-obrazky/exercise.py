import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Obrázky")
clock = pygame.time.Clock()

# Soubory raketa.png (64 × 64) a hvezda.png (32 × 32) jsou ve složce vedle programu.
# 1) Načtěte oba obrázky pomocí pygame.image.load(...) a přidejte .convert_alpha()
# 2) Raketu vykreslete tak, aby její STŘED byl v bodě (200, 150): rect = raketa.get_rect(center=(200, 150))
# 3) Hvězdu vykreslete s levým horním rohem v bodě (50, 50)
# 4) Pozadí okna je tmavě modré (20, 20, 60)

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem kreslete
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
