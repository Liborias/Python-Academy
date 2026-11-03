import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Scéna")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
font = pygame.font.Font(None, 30)
POLOHY = [(20, 30), (240, 40), (130, 120)]            # seznam poloh, projdeme ho cyklem

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((10, 10, 40))
    for pozice in POLOHY:                              # stejný obrázek na třech místech
        screen.blit(hvezda, pozice)
    pygame.draw.circle(screen, (200, 60, 60), (230, 150), 30)
    text = font.render("Ahoj", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(150, 20)))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
