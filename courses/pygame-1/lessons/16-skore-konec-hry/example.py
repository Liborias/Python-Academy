import pygame

pygame.init()
screen = pygame.display.set_mode((300, 150))
pygame.display.set_caption("Stavy")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

kliky = 0
stav = "hra"

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE and stav == "hra":
            kliky += 1                                  # počítá jen ve stavu "hra"
            if kliky >= 3:
                stav = "pauza"                          # změna stavu
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_r and stav == "pauza":
            kliky = 0                                   # restart: proměnné zpět na začátek
            stav = "hra"
    if stav == "hra":
        screen.fill((0, 0, 40))
        text = font.render(f"Kliky: {kliky}", True, (255, 255, 255))
    else:
        screen.fill((60, 0, 0))
        text = font.render("Pauza, stiskni R", True, (255, 255, 0))
    screen.blit(text, (20, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
