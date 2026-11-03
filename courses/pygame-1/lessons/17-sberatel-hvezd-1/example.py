import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Ukázka hry")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
raketa = pygame.image.load("raketa.png").convert_alpha()
raketa_rect = raketa.get_rect(center=(150, 160))
spadla = hvezda.get_rect(topleft=(130, 0))
chycene = 0
font = pygame.font.Font(None, 28)

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    spadla.y += 3                                       # hvězda padá
    if raketa_rect.colliderect(spadla):                 # chycena!
        chycene += 1
        spadla.bottom = 0                               # a začne padat znovu odshora
    elif spadla.top > 200:                              # minula raketu
        spadla.bottom = 0
    screen.fill((0, 0, 30))
    screen.blit(hvezda, spadla)
    screen.blit(raketa, raketa_rect)
    screen.blit(font.render(f"Chyceno: {chycene}", True, (255, 255, 255)), (5, 5))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
