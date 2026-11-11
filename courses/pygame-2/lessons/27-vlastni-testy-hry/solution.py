# Každý pokus vytváří vlastní objekt a ověřuje jeho skutečné chování.
# Sada musí přijmout správný model a odhalit porušené pravidlo.
import unittest
import pygame
import model_hry as model

class TestHrace(unittest.TestCase):
    def test_cas_a_nulovy_vstup(self):
        p = model.Hrac((200, 200), pygame.Rect(0, 0, 800, 600))
        p.update((0, 0), 0.05)
        self.assertEqual(tuple(p.pozice), (200, 200))
        p.update((1, 0), 0.025)
        self.assertAlmostEqual(p.pozice.x, 206)

    def test_diagonala_ma_stejnou_rychlost(self):
        p = model.Hrac((200, 200), pygame.Rect(0, 0, 800, 600))
        p.update((1, 1), 0.05)
        self.assertAlmostEqual((p.pozice - (200, 200)).length(), 12)

    def test_cely_obraz_zustane_uvnitr(self):
        hranice = pygame.Rect(10, 20, 500, 300)
        for smer in [(1, 1), (-1, -1)]:
            with self.subTest(smer=smer):
                p = model.Hrac(hranice.center, hranice)
                p.update(smer, 10)
                self.assertTrue(hranice.contains(p.rect))

def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestHrace)

if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(sestav_sadu())
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
