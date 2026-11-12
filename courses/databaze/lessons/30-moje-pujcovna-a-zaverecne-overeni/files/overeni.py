"""Spusťte python overeni.py, všechny databáze jsou jen dočasné."""
import csv
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory
from contextlib import closing
from reseni import MojePujcovna
from sada import vytvor_sadu

class TestKaret(unittest.TestCase):
    def test_karty_a_vracena_historie(self):
        with closing(MojePujcovna(':memory:')) as model:
            ident = model.pridej_pomucku('Míč',2)
            model.pridej_pomucku('Krabice',0)
            a = model.pujc_kod(model.kod(ident),'Ada')
            model.vrat(a)
            model.pujc_kod(model.kod(ident),'Žofie')
            self.assertEqual(model.karty()[0]['vypujceno'],1)
            self.assertEqual(model.karty()[0]['celkem'],2)
            self.assertEqual(model.souhrn(),{'pomucky':2,'dostupne':1,'vypujceno':1})

    def test_csv(self):
        with TemporaryDirectory() as tmp,closing(MojePujcovna(':memory:')) as model:
            model.pridej_pomucku('Karty; "A"',1)
            cesta = Path(tmp)/'karty.csv'
            self.assertEqual(model.stitky_csv(cesta),1)
            with cesta.open(encoding='utf-8',newline='') as f:
                self.assertEqual(list(csv.DictReader(f,delimiter=';'))[0]['nazev'],'Karty; "A"')

if __name__ == '__main__':
    sada = vytvor_sadu(MojePujcovna)
    sada.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestKaret))
    vysledek = unittest.TextTestRunner(verbosity=2).run(sada)
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
