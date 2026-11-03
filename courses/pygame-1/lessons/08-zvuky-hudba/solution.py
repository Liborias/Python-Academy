import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Zvuky")
clock = pygame.time.Clock()

pygame.mixer.music.load("hudba.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
cinknuti = pygame.mixer.Sound("cinknuti.wav")

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE:
            cinknuti.play()
    screen.fill((30, 30, 30))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
