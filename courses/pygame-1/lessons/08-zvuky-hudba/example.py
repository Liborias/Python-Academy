import pygame

pygame.init()
screen = pygame.display.set_mode((300, 150))
pygame.display.set_caption("Zvuk")
clock = pygame.time.Clock()

cinknuti = pygame.mixer.Sound("cinknuti.wav")         # efekt: načteme jednou před smyčkou
cinknuti.set_volume(0.6)                              # hlasitost od 0.0 do 1.0

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE:
            cinknuti.play()                           # přehraje se při každém stisku mezerníku
    screen.fill((20, 40, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
