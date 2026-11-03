import pygame

pygame.init()                                        # zapne pygame
screen = pygame.display.set_mode((320, 200))         # okno 320 × 200 bodů
pygame.display.set_caption("Ukázka")                 # nápis v liště okna

screen.fill((250, 220, 120))                         # žlutooranžové pozadí (červená, zelená, modrá)
pygame.display.flip()                                # teprve teď se nakreslené ukáže
pygame.time.wait(2000)                               # okno zůstane 2 sekundy

pygame.quit()                                        # úklid na konci
