"""Spusťte python overeni.py; testy používají vlastní dočasné složky."""
import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from reseni import Tracker

class TestPredani(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.slozka = Path(self.tmp.name)
        self.model = Tracker(self.slozka / 'test.sqlite3')
        self.addCleanup(self.model.close)

    def test_prazdny_export(self):
        cesta = self.slozka / 'prazdny.csv'
        self.assertEqual(self.model.export_csv(cesta), 0)
        with cesta.open(encoding='utf-8', newline='') as f:
            self.assertEqual(list(csv.reader(f, delimiter=';')), [['id','datum','hmotnost_kg','vyska_cm','bmi','poznamka']])

    def test_csv_a_poznamka(self):
        note = 'Žofie; "ukázka"\ndalší řádek'
        self.model.pridej('2026-04-01', 81, 180, note)
        cesta = self.slozka / 'mereni.csv'
        self.assertEqual(self.model.export_csv(cesta), 1)
        with cesta.open(encoding='utf-8', newline='') as f:
            rows = list(csv.reader(f, delimiter=';'))
        self.assertEqual(rows[1][5], note)
        self.assertAlmostEqual(float(rows[1][4]), 25)

    def test_zaloha_nezavisi_na_puvodni_db(self):
        self.model.pridej('2026-04-01', 81, 180)
        cesta = self.model.zaloha(self.slozka / 'kopie.sqlite3')
        self.model.pridej('2026-04-02', 80, 180)
        kopie = Tracker(cesta)
        self.addCleanup(kopie.close)
        self.assertEqual(len(kopie.seznam()), 1)
        self.assertEqual(len(self.model.seznam()), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
