import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Myš")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
tecky = []                                              # seznam míst, kde se kliklo

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.MOUSEBUTTONDOWN:
            tecky.append(udalost.pos)                   # pos = místo kliknutí
    mys = pygame.mouse.get_pos()                        # aktuální poloha kurzoru
    screen.fill((0, 40, 0))
    for pozice in tecky:
        pygame.draw.circle(screen, (255, 255, 255), pozice, 5)
    screen.blit(hvezda, hvezda.get_rect(center=mys))    # hvězda sleduje myš
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
