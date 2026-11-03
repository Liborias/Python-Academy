import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Domeček")
clock = pygame.time.Clock()

# Barvy: obloha (135, 206, 235), tráva (34, 139, 34), zeď (160, 110, 60), střecha (200, 40, 40), slunce (255, 220, 0)
# Kreslete v tomto pořadí (co se kreslí později, leží navrch):
#   1. obloha: vyplňte celé okno
#   2. tráva: pygame.draw.rect, obdélník (0, 220, 400, 80)
#   3. zeď: pygame.draw.rect, obdélník (150, 140, 100, 80)
#   4. střecha: pygame.draw.polygon s body [(140, 140), (260, 140), (200, 90)]
#   5. slunce: pygame.draw.circle, střed (340, 50), poloměr 30

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem kreslete
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
