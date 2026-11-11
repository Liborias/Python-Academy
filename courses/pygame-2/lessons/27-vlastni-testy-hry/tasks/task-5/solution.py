# Každý pokus vytváří vlastní objekt a ověřuje jeho skutečné chování.
# Sada musí přijmout správný model a odhalit porušené pravidlo.
import unittest
import pygame
import model_hry as model

class TestRegrese(unittest.TestCase):
    def test_seed_a_vlastni_generatory(self):
        a, b = model.Vlny(17), model.Vlny(23)
        self.assertNotEqual(a.rng.getstate(), b.rng.getstate())

    def test_vlna_zachova_skupinu_a_zrusi_clenstvi(self):
        v = model.Vlny()
        k = model.Kolo()
        d = v.pridej(k.hrac, k.hranice)
        druha = pygame.sprite.Group(d)
        skupina = v.drony
        v.zahaj()
        self.assertIs(v.drony, skupina)
        self.assertFalse(druha)

    def test_hlidac_meri_od_kotvy(self):
        d = model.HlidacBodu((100, 200), dosah=160)
        d.pozice.update(260, 200)
        hrac = model.Hrac((270, 200), pygame.Rect(0, 0, 800, 600))
        self.assertEqual(tuple(d.cil(hrac)), (100, 200))

    def test_konec_zmrazi_model(self):
        k = model.Kolo()
        k.konec, k.duvod = True, 'data'
        pred = (k.cas, tuple(k.hrac.pozice), k.stit.energie, k.vlny.rng.getstate())
        k.update((1, 0), 0.05)
        self.assertEqual((k.cas, tuple(k.hrac.pozice), k.stit.energie, k.vlny.rng.getstate()), pred)

def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestRegrese)

if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(sestav_sadu())
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
