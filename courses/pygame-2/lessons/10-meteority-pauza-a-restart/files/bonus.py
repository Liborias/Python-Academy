import pygame

class BonusStitu(pygame.sprite.Sprite):
    def __init__(self, stred):
        super().__init__()
        self.radius = 12
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (90, 235, 190), (12, 12), 11)
        pygame.draw.line(self.image, (250, 255, 250), (6, 12), (18, 12), 3)
        pygame.draw.line(self.image, (250, 255, 250), (12, 6), (12, 18), 3)
        self.pozice = pygame.Vector2(stred)
        self.rect = self.image.get_rect(center=stred)

    def update(self, dt):
        self.pozice.y += 80 * dt
        self.rect.center = (round(self.pozice.x), round(self.pozice.y))
