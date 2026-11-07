"""Spusťte v pracovní složce: python -m unittest -v test_centrum."""
import unittest
from adresa import Adresa
from balik import Balik
from centrum import Cyklodoprava, ExpedicniCentrum
from doprava import Kuryr, OsobniOdber
from nakupni_objednavka import NakupniObjednavka
from rezervacni_sklad import RezervacniSklad


def priprav():
    sklad = RezervacniSklad()
    sklad.pridej('KNIHA', 'Průvodce', 5)
    sklad.pridej('OBAL', 'Obal', 2)
    return ExpedicniCentrum(sklad)


def objednej(cislo, knihy=1, obaly=0):
    objednavka = NakupniObjednavka(cislo)
    if knihy:
        objednavka.pridej('KNIHA', 'Průvodce', 250, knihy)
    if obaly:
        objednavka.pridej('OBAL', 'Obal', 30, obaly)
    return objednavka


class TestCentrum(unittest.TestCase):
    def test_cely_pozadavek_nebo_zadny(self):
        centrum = priprav()
        objednavka = objednej('A', 1, 3)
        with self.assertRaises(ValueError):
            centrum.prijmi(objednavka, Balik('BA', 1200), OsobniOdber('Dílna'), Adresa('Javorová 1', 'Brno', '60200'))
        self.assertEqual(centrum.sklad.prehled(), {'KNIHA': 5, 'OBAL': 2})
        self.assertFalse(objednavka.uzavrena)
        with self.assertRaises(ValueError):
            centrum.souhrn('A')

    def test_storno_vrati_jen_vlastni_kusy_jednou(self):
        centrum = priprav()
        for cislo, pocet in [('A', 3), ('B', 2)]:
            centrum.prijmi(objednej(cislo, pocet), Balik(cislo, 1000), OsobniOdber('Dílna'), Adresa('Javorová 1', 'Brno', '60200'))
        self.assertEqual(centrum.storno('A'), {'KNIHA': 3, 'OBAL': 2})
        with self.assertRaises(ValueError):
            centrum.storno('A')
        self.assertEqual(centrum.sklad.prehled(), {'KNIHA': 3, 'OBAL': 2})
        self.assertEqual(centrum.souhrn('B')['stav'], 'rezervovana')

    def test_doprava_se_overi_pred_rezervaci(self):
        centrum = priprav()
        objednavka = objednej('A')
        with self.assertRaises(ValueError):
            centrum.prijmi(objednavka, Balik('BA', 2001), Cyklodoprava('Střed'), Adresa('Javorová 1', 'Brno', '60200'))
        self.assertEqual(centrum.sklad.prehled(), {'KNIHA': 5, 'OBAL': 2})
        self.assertFalse(objednavka.uzavrena)

    def test_nova_doprava_a_zachovana_volba(self):
        centrum = priprav()
        centrum.prijmi(objednej('A', 2), Balik('BA', 1200), Kuryr('Javorová 1'), Adresa('Javorová 1', 'Brno', '60200'))
        self.assertEqual(centrum.zmen_dopravu('A', Cyklodoprava('Střed')), 59)
        with self.assertRaises(ValueError):
            centrum.zmen_dopravu('A', Kuryr('Javorová 1', 1000))
        self.assertEqual(centrum.souhrn('A')['celkem'], 559)
        centrum.storno('A')
        with self.assertRaises(ValueError):
            centrum.pridej_poznamku('A', 'Pozdě')


if __name__ == '__main__':
    unittest.main(verbosity=2)
