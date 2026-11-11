# Každý pokus vytváří vlastní objekt a ověřuje jeho skutečné chování.
# Sada musí přijmout správný model a odhalit porušené pravidlo.
import unittest
import pygame
import model_hry as model

class TestKola(unittest.TestCase):
    def kontakt(self, k):
        k.vlny.cekaji = 0
        k.hrac.pozice.update(100, 200)
        k.hrac.rect.center = (100, 200)
        for _ in range(2):
            k.drony.add(model.Dron((100, 200), 0))

    def test_davka_ubere_jeden_zivot(self):
        k = model.Kolo()
        self.kontakt(k)
        k.update((0, 0), 0)
        self.assertEqual(k.zivoty, 2)

    def test_smrt_predchazi_sberu(self):
        k = model.Kolo()
        self.kontakt(k)
        k.zivoty, k.skore = 1, 5
        k.data.rect.center = k.hrac.rect.center
        k.update((0, 0), 0)
        self.assertEqual((k.duvod, k.skore), ('zivoty', 5))

    def test_nova_vlna_neobnovi_zivoty(self):
        k = model.Kolo()
        k.vlny.cekaji, k.zivoty, k.skore, k.zbyva = 0, 2, 4, 0.01
        k.update((0, 0), 0.02)
        self.assertEqual((k.vlny.cislo, k.zivoty, k.skore), (2, 2, 4))

def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestKola)

if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(sestav_sadu())
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
