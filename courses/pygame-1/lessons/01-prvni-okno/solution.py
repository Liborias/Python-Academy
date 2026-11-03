import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Moje první okno")
screen.fill((135, 206, 235))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
