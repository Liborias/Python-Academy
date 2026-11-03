import random
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Sběratel hvězd")
clock = pygame.time.Clock()

raketa = pygame.image.load("raketa.png").convert_alpha()
hvezda = pygame.image.load("hvezda.png").convert_alpha()
font = pygame.font.Font(None, 32)

raketa_rect = raketa.get_rect(center=(200, 450))
hvezdy = []
for i in range(4):
    hvezdy.append(hvezda.get_rect(topleft=(30 + i * 90, -i * 80)))
skore = 0

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False

    klavesy = pygame.key.get_pressed()
    if klavesy[pygame.K_LEFT]:
        raketa_rect.x -= 6
    if klavesy[pygame.K_RIGHT]:
        raketa_rect.x += 6
    if raketa_rect.left < 0:
        raketa_rect.left = 0
    if raketa_rect.right > 400:
        raketa_rect.right = 400

    for rect in hvezdy:
        rect.y += 3
        if raketa_rect.colliderect(rect):
            skore += 1
            rect.bottom = 0
            rect.x = random.randint(0, 368)
        elif rect.top > 500:
            rect.bottom = 0
            rect.x = random.randint(0, 368)

    screen.fill((0, 0, 30))
    for rect in hvezdy:
        screen.blit(hvezda, rect)
    screen.blit(raketa, raketa_rect)
    text = font.render(f"Skóre: {skore}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
