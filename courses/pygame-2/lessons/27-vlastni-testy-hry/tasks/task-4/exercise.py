# Každý pokus vytváří vlastní objekt a ověřuje jeho skutečné chování.
# Sada musí přijmout správný model a odhalit porušené pravidlo.
import unittest
import pygame
import model_hry as model

class MojeTesty(unittest.TestCase):
    def test_doplnte_dulezite_pravidlo(self):
        # Samotná existence testu ještě neověřuje chování hry.
        self.assertTrue(True)

def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(MojeTesty)

if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(sestav_sadu())
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
