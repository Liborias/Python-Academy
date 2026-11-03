import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Text")
clock = pygame.time.Clock()

font_nadpis = pygame.font.Font(None, 48)
font_skore = pygame.font.Font(None, 32)
skore = 0

running = True
while running:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 40))
    nadpis = font_nadpis.render("Sběratel hvězd", True, (255, 220, 0))
    screen.blit(nadpis, nadpis.get_rect(center=(200, 50)))
    text_skore = font_skore.render(f"Skóre: {skore}", True, (255, 255, 255))
    screen.blit(text_skore, text_skore.get_rect(bottomleft=(10, 190)))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
