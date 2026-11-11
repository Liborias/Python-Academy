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

class TestStitu(unittest.TestCase):
    def test_energie_pokryje_cely_krok(self):
        s = model.StitZakladny(1, 0.5)
        self.assertTrue(s.update(1, True))
        self.assertEqual(s.energie, 0)
        self.assertFalse(s.update(0, True))
        s.energie = 0.01
        self.assertFalse(s.update(0.02, True))
        self.assertEqual(s.energie, 0)

    def test_obnova_jen_mimo_pristav(self):
        s = model.StitZakladny()
        self.assertTrue(s.update(0.5, True))
        self.assertEqual(s.energie, 2)
        self.assertFalse(s.update(0.5, False))
        self.assertEqual(s.energie, 2.25)

    def test_obnova_ma_strop(self):
        s = model.StitZakladny()
        self.assertFalse(s.update(10, False))
        self.assertEqual(s.energie, 2.5)


if __name__ == '__main__':
    unittest.main()
