import pygame

pygame.init()
screen = pygame.display.set_mode((300, 150))
pygame.display.set_caption("Text")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 40)                       # písmo vytvoříme jednou před smyčkou
pocet = 0

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    pocet += 1
    screen.fill((30, 0, 30))
    text = font.render(f"Snímek {pocet}", True, (255, 255, 255))   # text je obrázek, vyrábí se při každé změně
    screen.blit(text, text.get_rect(center=(150, 75)))              # umístění podle středu
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
