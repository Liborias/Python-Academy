# Každá testovací metoda připravuje vlastní objekty.
# unittest vypisuje průběh do chybového výstupu i při úspěchu.
import unittest
from balik import Balik
from doprava import OsobniOdber, Kuryr
from expedice import Expedice


class TestExpedice(unittest.TestCase):
    def test_osobni_odber(self):
        balik = Balik("B-1", 1200)
        odber = OsobniOdber("Dílna Brno")
        expedice = Expedice(balik, odber)
        self.assertEqual(expedice.nabidka(), 0)
        self.assertIs(expedice.balik, balik)
        self.assertIs(expedice.doprava, odber)

    def test_kuryr_na_hranicich(self):
        kuryr = Kuryr("Javorová 1, Brno")
        self.assertEqual(kuryr.cena(Balik("H-1", 5000)), 99)
        self.assertEqual(kuryr.cena(Balik("H-2", 5001)), 149)
        self.assertEqual(kuryr.cena(Balik("H-3", 10000)), 149)

    def test_zmena_dopravy(self):
        balik = Balik("B-2", 1200)
        expedice = Expedice(balik, OsobniOdber("Dílna Brno"))
        kuryr = Kuryr("Javorová 1, Brno")
        self.assertEqual(expedice.zmen_dopravu(kuryr), 99)
        self.assertIs(expedice.doprava, kuryr)
        self.assertIs(expedice.balik, balik)
        self.assertEqual(expedice.nabidka(), 99)

    def test_odmitnuta_zmena(self):
        balik = Balik("B-3", 1200)
        odber = OsobniOdber("Dílna Brno")
        expedice = Expedice(balik, odber)
        nevhodna = Kuryr("Javorová 1, Brno", 1000)
        # Nestačí zachytit chybu: následně ověříme také zachovaný stav.
        with self.assertRaises(ValueError):
            expedice.zmen_dopravu(nevhodna)
        self.assertIs(expedice.doprava, odber)
        self.assertIs(expedice.balik, balik)
        self.assertEqual(expedice.nabidka(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
