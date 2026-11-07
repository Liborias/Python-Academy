"""Druhý blok samostatného OOP: pravidla stavu, property a úplná rezervace."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/oop/lessons'
IDS = ['05-zapouzdreni-a-rozhrani', '06-pravidla-stavu-a-vyjimky', '07-property-a-dostupnost', '08-revize-skladu']


class OopStateTest(unittest.TestCase):
    def source(self, index):
        return (BASE/IDS[index]/'solution.py').read_text('utf-8')

    def verify(self, index, code, expected):
        with tempfile.TemporaryDirectory() as temp:
            result = run_check(BASE/IDS[index], code, ROOT/'lib', Path(temp))
        self.assertNotIn('error', result, result)
        self.assertEqual(result.get('ok'), expected, result)

    def variants(self, index, wrong, correct):
        source = self.source(index)
        for expected, variants in [(False, wrong), (True, correct)]:
            for code in variants:
                self.assertNotEqual(code, source)
                with self.subTest(expected=expected, code=code):
                    self.verify(index, code, expected)

    def test_public_interface(self):
        s = self.source(0)
        wrong = [
            s.replace('_pocet', 'pocet'),
            s.replace('return self._pocet', 'print(self._pocet)'),
            s.replace('self._pocet += kolik', 'pocet = self._pocet + kolik'),
            s.replace('self._pocet -= kolik', 'self._pocet += kolik'),
            s.replace('self._pocet', 'Zasoba._pocet'),
            s.replace('pocet=0', 'pocet=1'),
            s.replace('''    def stav(self):
        return self._pocet''', '''    def stav(self):
        self._pocet += 1
        return self._pocet'''),
        ]
        correct = [s.replace('_pocet', '_kusy'), s.replace('self._pocet += kolik', 'self._pocet = self._pocet + kolik')]
        self.variants(0, wrong, correct)

    def test_validation_before_mutation(self):
        s = self.source(1)
        wrong = [
            s.replace('if type(pocet) is not int or pocet < 0:', 'if False:'),
            s.replace('kolik <= 0', 'kolik < 0'),
            s.replace('kolik > self._pocet', 'kolik >= self._pocet'),
            s.replace(' or kolik > self._pocet', ''),
            s.replace('type(kolik) is not int', 'not isinstance(kolik, int)'),
            s.replace('''        if type(kolik) is not int or kolik <= 0:
            raise ValueError("Příjem musí být kladný celý počet")
        self._pocet += kolik''', '''        self._pocet += kolik
        if type(kolik) is not int or kolik <= 0:
            raise ValueError("Příjem musí být kladný celý počet")'''),
            s.replace('''        if type(kolik) is not int or kolik <= 0 or kolik > self._pocet:
            raise ValueError("Neplatný nebo nedostupný výdej")
        self._pocet -= kolik''', '''        self._pocet -= kolik
        if type(kolik) is not int or kolik <= 0 or self._pocet < 0:
            raise ValueError("Neplatný nebo nedostupný výdej")'''),
            s.replace('self._pocet -= kolik', 'self._pocet = 0'),
            s.replace('return self._pocet', 'print(self._pocet)'),
        ]
        correct = [
            s.replace('_pocet', '_kusy'),
            s.replace('type(kolik) is not int', '(not isinstance(kolik, int) or isinstance(kolik, bool))')
             .replace('type(pocet) is not int', '(not isinstance(pocet, int) or isinstance(pocet, bool))'),
        ]
        self.variants(1, wrong, correct)

    def test_readonly_computed_properties(self):
        s = self.source(2)
        wrong = [
            s.replace('return self._celkem - self._rezervovano', 'return self._celkem'),
            s.replace('kolik > self.dostupne', 'kolik >= self.dostupne'),
            s.replace('kolik > self.rezervovano', 'kolik >= self.rezervovano'),
            s.replace('kolik <= 0', 'kolik < 0'),
            s.replace('self._rezervovano += kolik', 'self._celkem -= kolik'),
            s.replace('self._rezervovano -= kolik', 'self._rezervovano += kolik'),
            s.replace('self._rezervovano', 'SkladovaKarta._rezervovano'),
            s.replace('self._rezervovano = 0', 'self._rezervovano = 0\n        self._stara = celkem')
             .replace('return self._celkem - self._rezervovano', 'return self._stara'),
            s.replace('''    def rezervuj(self, kolik):''', '''    @dostupne.setter
    def dostupne(self, hodnota):
        self._celkem = hodnota

    def rezervuj(self, kolik):'''),
        ]
        correct = [
            s.replace('_celkem', '_fyzicky').replace('_rezervovano', '_odlozeno'),
            s.replace('return self._celkem - self._rezervovano', 'return self.celkem - self.rezervovano'),
            s.replace('''    def rezervuj(self, kolik):''', '''    @dostupne.setter
    def dostupne(self, hodnota):
        raise AttributeError("Pouze čtení")

    def rezervuj(self, kolik):'''),
        ]
        self.variants(2, wrong, correct)

    def test_atomic_stock_reservation(self):
        s = self.source(3)
        wrong = [
            s.replace('''        if kod in self._karty:
            raise ValueError("Kód už ve skladu existuje")
''', ''),
            s.replace('self._karty', 'Sklad._karty'),
            s.replace('SkladovaKarta(nazev, celkem)', 'SkladovaKarta(nazev, max(0, celkem))'),
            s.replace('''        for kod, kolik in pozadavek.items():
            self._karty[kod].rezervuj(kolik)''', '            self._karty[kod].rezervuj(kolik)'),
            s.replace('return self.prehled()', 'return pozadavek'),
            s.replace('vysledek[kod] = karta.dostupne', 'vysledek[kod] = karta'),
            s.replace('self._karty[kod].rezervuj(kolik)', 'self._karty[kod]._rezervovano += kolik'),
            s.replace('type(kolik) is not int', 'not isinstance(kolik, int)'),
        ]
        correct = [
            s.replace('''        vysledek = {}
        for kod, karta in self._karty.items():
            vysledek[kod] = karta.dostupne
        return vysledek''', '        return {kod: karta.dostupne for kod, karta in self._karty.items()}'),
            s.replace('for kod, karta in self._karty.items():', 'for kod, karta in reversed(list(self._karty.items())):'),
            s.replace('''        for kod, kolik in pozadavek.items():
            self._karty[kod].rezervuj(kolik)''', '''        for kod, kolik in reversed(list(pozadavek.items())):
            self._karty[kod].rezervuj(kolik)'''),
        ]
        self.variants(3, wrong, correct)

    def test_prepared_card_matches_previous_solution(self):
        self.assertEqual((BASE/IDS[3]/'files/skladova_karta.py').read_text('utf-8'), self.source(2))


if __name__ == '__main__':
    unittest.main()
