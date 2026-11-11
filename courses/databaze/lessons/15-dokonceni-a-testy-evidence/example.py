# Testy používají skutečný model a pro každý případ vlastní dočasný soubor.
import sqlite3
import unittest
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from prihlasky import Model

def vytvor_sadu(Model):
    class TestEvidence(unittest.TestCase):
        def setUp(self):
            self.adresar = TemporaryDirectory()
            self.addCleanup(self.adresar.cleanup)
            self.cesta = Path(self.adresar.name) / 'zkouska.sqlite3'
            self.model = Model(self.cesta)
            self.addCleanup(self.model.close)

        def test_trvale_pridani(self):
            ident = self.model.pridej("  Robotika O'Neil  ", 2)
            self.model.close()
            with closing(Model(self.cesta)) as znovu:
                self.assertEqual(znovu.seznam(), [(ident, "Robotika O'Neil", 2)])

        def test_jedinecnost(self):
            self.model.pridej('Šachy', 3)
            with self.assertRaises(sqlite3.IntegrityError):
                self.model.pridej('Šachy', 4)
            self.assertEqual(len(self.model.seznam()), 1)

        def test_plny_krouzek(self):
            ident = self.model.pridej('Robotika', 1)
            self.model.prihlas(ident, 'Žofie')
            with self.assertRaises(ValueError):
                self.model.prihlas(ident, 'Ada')
            self.assertEqual([r[1] for r in self.model.prihlasky(ident)], ['Žofie'])

        def test_opakovane_prihlaseni(self):
            ident = self.model.pridej('Robotika', 3)
            self.model.prihlas(ident, 'Ada')
            with self.assertRaises(sqlite3.IntegrityError):
                self.model.prihlas(ident, 'Ada')
            self.assertEqual(len(self.model.prihlasky(ident)), 1)

        def test_zmenseni_kapacity(self):
            ident = self.model.pridej('Hry', 3)
            self.model.prihlas(ident, 'Ada')
            self.model.prihlas(ident, 'Žofie')
            with self.assertRaises(ValueError):
                self.model.uprav(ident, 'Jiný název', 1)
            self.assertEqual(self.model.seznam(), [(ident, 'Hry', 3)])

        def test_odhlaseni_a_smazani(self):
            ident = self.model.pridej('Hry', 2)
            prihlaska = self.model.prihlas(ident, 'Ada')
            with self.assertRaises(sqlite3.IntegrityError):
                self.model.smaz(ident)
            self.assertTrue(self.model.odhlas(prihlaska))
            self.assertFalse(self.model.odhlas(prihlaska))
            self.assertTrue(self.model.smaz(ident))
            self.assertFalse(self.model.smaz(ident))
            self.assertEqual(self.model.souhrn(), [])
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestEvidence)

# Vytvoření sady samo nic nespouští; výsledek překládáme na návratový kód.
if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(vytvor_sadu(Model))
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
