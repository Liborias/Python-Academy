import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Vlajka")
clock = pygame.time.Clock()

# 1) Pojmenujte tři barvy konstantami velkými písmeny: MODRA (0, 85, 164), BILA (255, 255, 255), CERVENA (239, 65, 53)
# 2) Ve smyčce vyplňte okno třemi svislými pruhy, každý široký 100 bodů: vlevo modrý, uprostřed bílý, vpravo červený
#    (nápověda: screen.fill(barva, (x, y, šířka, výška)) vybarví jen obdélník)

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    # TODO: sem kreslete
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
