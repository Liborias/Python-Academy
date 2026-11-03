"""Nové OOP kontroly musejí odmítat typické chyby a přijímat správné alternativy."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

LESSONS = ['17-trida-a-instance','18-konstruktor-init','19-metody-a-stav','20-vlastni-seznam-objektu']


class OopIntroTest(unittest.TestCase):
    def check(self, lesson, code, expected):
        with tempfile.TemporaryDirectory() as temp:
            result = run_check(ROOT / 'courses/turtle-oop/lessons' / lesson,
                               code, ROOT / 'lib', Path(temp))
        self.assertNotIn('error', result, result)
        self.assertEqual(result.get('ok'), expected, result)

    def source(self, index):
        return (ROOT / 'courses/turtle-oop/lessons' / LESSONS[index] / 'solution.py').read_text('utf-8')

    def test_instances(self):
        source = self.source(0)
        mutants = [
            source.replace('return hrac', 'return {"jmeno": jmeno, "body": body}'),
            source.replace('hrac.body = body', 'hrac.body = 0'),
            source.replace('hrac.jmeno = jmeno', 'hrac.jmeno = "Ema"'),
            source.replace('    hrac.body = body\n', ''),
            source.replace('return hrac', 'return Hrac'),
            source.replace('def vytvor_hrace', 'jediny = Hrac()\n\ndef vytvor_hrace').replace('hrac = Hrac()', 'hrac = jediny'),
        ]
        for code in mutants:
            with self.subTest(code=code): self.check(LESSONS[0], code, False)
        self.check(LESSONS[0], source.replace('hrac =', 'novy =').replace('hrac.', 'novy.').replace('return hrac', 'return novy'), True)
        advanced = '''class Hrac:
    def __init__(self, jmeno, body):
        self.jmeno = jmeno
        self.body = body

def vytvor_hrace(jmeno, body):
    return Hrac(jmeno, body)
'''
        self.check(LESSONS[0], advanced, True)

    def test_constructor(self):
        source = self.source(1)
        mutants = [
            source.replace('self.sirka = sirka', 'self.sirka = vyska'),
            source.replace('self.sirka = sirka', 'sirka = sirka'),
            source.replace('self.vyska = vyska', 'self.vyska = 5'),
            source.replace('self.sirka', 'Obdelnik.sirka').replace('self.vyska', 'Obdelnik.vyska'),
            source + '        return self\n',
            source.replace('__init__(self, sirka, vyska)', '__init__(self)'),
        ]
        for code in mutants:
            with self.subTest(code=code): self.check(LESSONS[1], code, False)
        self.check(LESSONS[1], 'class Obdelnik:\n    def __init__(self, sirka, vyska):\n        self.sirka, self.vyska = sirka, vyska\n', True)

    def test_methods(self):
        source = self.source(2)
        mutants = [
            source.replace('self.hodnota += kolik', 'hodnota = self.hodnota + kolik'),
            source.replace('return self.hodnota', 'print(self.hodnota)'),
            source.replace('zacatek=0', 'zacatek=5'),
            source.replace('self.hodnota = zacatek', 'self.hodnota = 0'),
            source.replace('self.hodnota += kolik', 'self.hodnota += max(kolik, 0)'),
            source.replace('self.hodnota = 0', 'hodnota = 0'),
            source + '        return 0\n',
            source.replace('self.hodnota', 'Pocitadlo.hodnota'),
        ]
        for code in mutants:
            with self.subTest(code=code): self.check(LESSONS[2], code, False)
        alternative = source.replace('self.hodnota += kolik', 'self.hodnota = self.hodnota + kolik') + '        return None\n'
        self.check(LESSONS[2], alternative, True)

    def test_owned_lists(self):
        source = self.source(3)
        mutants = [
            source.replace('return list(self.veci)', 'return self.veci'),
            source.replace('return list(self.veci)', 'return list(reversed(self.veci))'),
            source.replace('return len(self.veci)', 'return None'),
            source.replace('self.veci.append(predmet)', 'self.veci = [predmet]'),
            source.replace('self.veci.append(predmet)', 'if predmet not in self.veci:\n            self.veci.append(predmet)'),
            source.replace('class Batoh:\n', 'class Batoh:\n    veci = []\n').replace('self.veci = []', 'pass'),
            'sdilene = []\n' + source.replace('self.veci = []', 'self.veci = sdilene\n        sdilene.clear()'),
            source.replace('self.veci', 'self.predmety'),
        ]
        for code in mutants:
            with self.subTest(code=code): self.check(LESSONS[3], code, False)
        for copy in ['self.veci.copy()', 'self.veci[:]', '[x for x in self.veci]']:
            with self.subTest(copy=copy):
                alternative = source.replace('list(self.veci)', copy).replace('self.veci.append(predmet)', 'self.veci = self.veci + [predmet]')
                self.check(LESSONS[3], alternative, True)


if __name__ == '__main__':
    unittest.main()
