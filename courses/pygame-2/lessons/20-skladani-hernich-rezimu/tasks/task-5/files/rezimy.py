import math
import pygame
class ZasobnikRezimu:
    def __init__(self, pocatecni):
        self.rezimy = [pocatecni]

    @property
    def aktualni(self):
        return self.rezimy[-1]

    def vloz(self, rezim):
        self.rezimy.append(rezim)

    def odeber(self):
        if len(self.rezimy) == 1:
            return False
        self.rezimy.pop()
        return True

    def zpracuj(self, udalost):
        return self.aktualni.zpracuj(udalost)

    def update(self, dt):
        self.aktualni.update(dt)

    def kresli(self, plocha):
        for rezim in self.rezimy:
            rezim.kresli(plocha)

class Pauza:
    def __init__(self, font):
        self.font = font

    def zpracuj(self, udalost):
        if udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_p:
            return 'zpet'
        return None

    def update(self, dt):
        pass

    def kresli(self, plocha):
        vrstva = pygame.Surface(plocha.get_size(), pygame.SRCALPHA)
        vrstva.fill((10, 18, 30, 170))
        napis = self.font.render('PAUZA', True, (240, 245, 255))
        vrstva.blit(napis, napis.get_rect(center=vrstva.get_rect().center))
        plocha.blit(vrstva, (0, 0))

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

class Nabidka:
    def __init__(self, tlacitka):
        self.tlacitka = list(tlacitka)

    def zpracuj(self, udalost):
        for tlacitko in reversed(self.tlacitka):
            akce = tlacitko.zpracuj(udalost)
            if akce is not None:
                return akce
        return None

    def update(self, dt):
        pass

    def kresli(self, plocha):
        for tlacitko in self.tlacitka:
            tlacitko.kresli(plocha)
