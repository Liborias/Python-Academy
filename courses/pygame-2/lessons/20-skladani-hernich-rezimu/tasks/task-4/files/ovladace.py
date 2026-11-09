import math
import pygame
class Tlacitko:
    def __init__(self, rect, text, akce, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.akce = akce
        self.font = font

    def zpracuj(self, udalost):
        if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
            if self.rect.collidepoint(udalost.pos):
                return self.akce
        return None

    def kresli(self, plocha):
        pygame.draw.rect(plocha, (38, 68, 96), self.rect, border_radius=8)
        pygame.draw.rect(plocha, (90, 175, 225), self.rect, 2, border_radius=8)
        napis = self.font.render(self.text, True, (240, 245, 255))
        plocha.blit(napis, napis.get_rect(center=self.rect.center))
