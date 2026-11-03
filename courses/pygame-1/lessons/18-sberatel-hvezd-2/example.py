import pygame

pygame.init()
screen = pygame.display.set_mode((300, 150))
pygame.display.set_caption("Životy")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

zivoty = 3
stav = "hra"
snimek = 0

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_r and stav == "konec":
            zivoty = 3                                  # restart: životy zpět na 3
            stav = "hra"
    if stav == "hra":
        snimek += 1
        if snimek % 60 == 0:                            # jednou za sekundu hráč přijde o život
            zivoty -= 1
            if zivoty == 0:
                stav = "konec"
        screen.fill((0, 0, 40))
        text = font.render(f"Životy: {zivoty}", True, (255, 255, 255))
    else:
        screen.fill((60, 0, 0))
        text = font.render("Konec, stiskni R", True, (255, 220, 0))
    screen.blit(text, (20, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
