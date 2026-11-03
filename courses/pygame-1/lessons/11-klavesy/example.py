import pygame

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Klávesy")
clock = pygame.time.Clock()

hvezda = pygame.image.load("hvezda.png").convert_alpha()
rect = hvezda.get_rect(center=(150, 100))

running = True
while running:
    for udalost in pygame.event.get():                      # jednorázové události
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE:
            rect.center = (150, 100)                        # mezerník: skok do středu
    klavesy = pygame.key.get_pressed()                      # stav kláves: co se právě drží
    if klavesy[pygame.K_LEFT]:
        rect.x -= 4
    if klavesy[pygame.K_RIGHT]:
        rect.x += 4
    screen.fill((0, 0, 30))
    screen.blit(hvezda, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
