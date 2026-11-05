"""První blok samostatného OOP: správné alternativy, vlastní stav a spolupráce."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/oop/lessons'
IDS = ['01-od-slovniku-k-objektu', '02-konstruktor-a-self', '03-metody-a-prubeh-volani', '04-objednavka-a-jeji-polozky']


class StandaloneOopTest(unittest.TestCase):
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

    def test_first_instances(self):
        s = self.source(0)
        wrong = [
            s.replace('return zasilka', 'return {"kod": kod, "prijemce": prijemce, "stav": "prijata"}'),
            s.replace('return zasilka', 'return Zasilka'),
            s.replace('zasilka.kod = kod', 'zasilka.kod = "Z-101"'),
            s.replace('zasilka.prijemce = prijemce', 'zasilka.prijemce = prijemce.strip()'),
            s.replace('zasilka.stav = "prijata"', 'zasilka.stav = "odeslana"'),
            s.replace('def vytvor_zasilku', 'jedina = Zasilka()\n\ndef vytvor_zasilku')
             .replace('zasilka = Zasilka()', 'zasilka = jedina'),
            s.replace('return zasilka', 'print(zasilka.kod)'),
        ]
        correct = [
            s.replace('zasilka', 'nova'),
            '''class Zasilka:
    def __init__(self, kod, prijemce):
        self.kod = kod
        self.prijemce = prijemce
        self.stav = "prijata"

def vytvor_zasilku(kod, prijemce):
    return Zasilka(kod, prijemce)
''',
        ]
        self.variants(0, wrong, correct)

    def test_constructor(self):
        s = self.source(1)
        wrong = [
            s.replace('self.cena_za_kus = cena_za_kus', 'cena_za_kus = cena_za_kus'),
            s.replace('self.cena_za_kus = cena_za_kus', 'self.cena_za_kus = pocet'),
            s.replace('pocet=1', 'pocet=2'),
            s.replace('self.pocet = pocet', 'self.pocet = pocet or 1'),
            s.replace('self.nazev', 'Polozka.nazev').replace('self.pocet', 'Polozka.pocet'),
            s.replace('self.pocet = pocet', 'self.pocet = pocet\n        return self'),
        ]
        correct = [
            s.replace('''        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet''', '        self.nazev, self.cena_za_kus, self.pocet = nazev, cena_za_kus, pocet'),
            s.replace('self', 'instance'),
        ]
        self.variants(1, wrong, correct)

    def test_methods_and_state(self):
        s = self.source(2)
        wrong = [
            s.replace('self.pocet += kolik', 'pocet = self.pocet + kolik'),
            s.replace('return self.pocet', 'print(self.pocet)'),
            s.replace('self.cena_za_kus * self.pocet', 'self.cena_za_kus + self.pocet'),
            s.replace('self.pocet = pocet', 'self.pocet = pocet\n        self._stara = cena_za_kus * pocet')
             .replace('return self.cena_za_kus * self.pocet', 'return self._stara'),
            s.replace('self.pocet', 'Polozka.pocet'),
            s.replace('return self.cena_za_kus * self.pocet', 'self.pocet += 1\n        return self.cena_za_kus * self.pocet'),
            s.replace('self.pocet += kolik', 'self.pocet += max(1, kolik)'),
            s.replace('kolik=1', 'kolik=2'),
        ]
        correct = [
            s.replace('self.pocet += kolik', 'self.pocet = self.pocet + kolik').replace('self.cena_za_kus * self.pocet', 'self.pocet * self.cena_za_kus'),
            s.replace('return self.cena_za_kus * self.pocet', 'return sum([self.cena_za_kus] * self.pocet)'),
        ]
        self.variants(2, wrong, correct)

    def test_composition_and_owned_lists(self):
        s = self.source(3)
        wrong = [
            s.replace('self.polozky', 'Objednavka.polozky'),
            s.replace('return list(self.polozky)', 'return self.polozky'),
            s.replace('return list(self.polozky)', 'return list(reversed(self.polozky))'),
            s.replace('self.polozky.append(polozka)', 'self.polozky = [polozka]'),
            s.replace('self.polozky.append(polozka)', 'if polozka not in self.polozky:\n            self.polozky.append(polozka)'),
            s.replace('soucet += polozka.celkem()', 'soucet += polozka.cena_za_kus * polozka.pocet'),
            s.replace('return len(self.polozky)', 'return sum(p.pocet for p in self.polozky)'),
            s.replace('self.polozky.append(polozka)', 'self.polozky.append(Polozka(polozka.nazev, polozka.cena_za_kus, polozka.pocet))'),
        ]
        correct = [
            s.replace('list(self.polozky)', 'self.polozky[:]'),
            s.replace('list(self.polozky)', 'self.polozky.copy()')
             .replace('self.polozky.append(polozka)', 'self.polozky = self.polozky + [polozka]'),
            s.replace('''        soucet = 0
        for polozka in self.polozky:
            soucet += polozka.celkem()
        return soucet''', '        return sum(p.celkem() for p in self.polozky)'),
        ]
        self.variants(3, wrong, correct)

    def test_prepared_item_module_matches_previous_solution(self):
        self.assertEqual((BASE/IDS[3]/'files/polozka.py').read_text('utf-8'), self.source(2))


if __name__ == '__main__':
    unittest.main()
