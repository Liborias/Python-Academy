# Každý pokus vytváří vlastní objekt a ověřuje jeho skutečné chování.
# Sada musí přijmout správný model a odhalit porušené pravidlo.
import unittest
import pygame
import model_hry as model

class TestRežimu(unittest.TestCase):
    def stisk(self, h, klavesa):
        h.zpracuj(pygame.event.Event(pygame.KEYDOWN, key=klavesa))

    def test_pauza_zachova_model(self):
        h = model.Hra()
        h.novy_let()
        self.stisk(h, pygame.K_p)
        pred = h.kolo.cas
        h.update((1, 0), 0.05)
        self.assertEqual(h.kolo.cas, pred)

    def test_restart_vytvori_nove_kolo(self):
        h = model.Hra()
        h.novy_let()
        stare = h.kolo
        h.kolo.skore = 4
        self.stisk(h, pygame.K_r)
        self.assertIsNot(h.kolo, stare)
        self.assertEqual(h.kolo.skore, 0)

    def test_quit_plati_i_v_pauze(self):
        h = model.Hra()
        h.novy_let()
        self.stisk(h, pygame.K_p)
        h.zpracuj(pygame.event.Event(pygame.QUIT))
        self.assertFalse(h.bezi)

def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestRežimu)

if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(sestav_sadu())
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
