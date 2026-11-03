import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Ukázka smyčky")
clock = pygame.time.Clock()
pocet = 0                                             # počítadlo průchodů smyčkou

running = True
while running:                                        # herní smyčka: opakuje se pořád dokola
    for udalost in pygame.event.get():                # všechny události od minulého průchodu
        if udalost.type == pygame.QUIT:               # někdo zavřel okno
            running = False
        elif udalost.type == pygame.KEYDOWN:
            print("Stisk klávesy", pygame.key.name(udalost.key))
    pocet += 1
    screen.fill((40 + pocet % 200, 80, 120))          # barva se pomalu mění
    pygame.display.flip()
    clock.tick(60)                                    # nejvýš 60 snímků za sekundu

pygame.quit()
