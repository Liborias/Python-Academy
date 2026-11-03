import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Konec hry")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 32)
font_velky = pygame.font.Font(None, 64)
skore = 0
stav = "hra"

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
        elif udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_SPACE and stav == "hra":
                skore += 1
                if skore >= 5:
                    stav = "konec"
            elif udalost.key == pygame.K_r and stav == "konec":
                skore = 0
                stav = "hra"
    if stav == "hra":
        screen.fill((0, 0, 30))
        text = font.render(f"Skóre: {skore}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    else:
        screen.fill((60, 0, 0))
        nadpis = font_velky.render("Konec hry", True, (255, 220, 0))
        screen.blit(nadpis, nadpis.get_rect(center=(200, 110)))
        vysledek = font.render(f"Skóre: {skore}", True, (255, 255, 255))
        screen.blit(vysledek, vysledek.get_rect(center=(200, 170)))
        napoveda = font.render("Stiskni R", True, (255, 255, 255))
        screen.blit(napoveda, napoveda.get_rect(center=(200, 220)))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
