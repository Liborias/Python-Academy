# Každý pokus vytváří vlastní objekt a ověřuje jeho skutečné chování.
# Sada musí přijmout správný model a odhalit porušené pravidlo.
import unittest
import pygame
import model_hry as model

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

def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestStitu)

if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(sestav_sadu())
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
