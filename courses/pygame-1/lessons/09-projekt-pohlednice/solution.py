import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pohlednice")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
raketa = pygame.image.load("raketa.png").convert_alpha()
raketa_rect = raketa.get_rect(center=(200, 180))
font = pygame.font.Font(None, 40)
nadpis = font.render("Pozdrav z kosmu", True, (255, 255, 255))
nadpis_rect = nadpis.get_rect(center=(200, 25))
HVEZDY = [(50, 60), (120, 100), (300, 70), (350, 150), (80, 200)]

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((10, 10, 40))
    for pozice in HVEZDY:
        screen.blit(hvezda, pozice)
    pygame.draw.circle(screen, (200, 60, 60), (330, 230), 40)
    screen.blit(raketa, raketa_rect)
    screen.blit(nadpis, nadpis_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
