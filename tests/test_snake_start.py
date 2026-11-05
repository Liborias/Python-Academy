"""Návaznost Snake a kontroly chybných i alternativních řešení lekcí 29–32."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/turtle-oop/lessons'
IDS = ['29-snake-model-a-mrizka', '30-snake-zobrazeni', '31-snake-casovac-a-pohyb', '32-snake-ovladani']


class SnakeStartTest(unittest.TestCase):
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

    def test_model(self):
        s = self.source(0)
        wrong = [
            s.replace(' % self.sirka', ''),
            s.replace('% self.vyska', '% self.sirka'),
            s.replace('dx, dy = self.smer', 'dx, dy = (1, 0)'),
            s.replace('self.body.insert(0, nova)', 'self.body.append(nova)'),
            s.replace('self.body.pop()', 'self.body.pop(0)'),
            s.replace('        self.body.pop()\n', ''),
            s.replace('return nova', 'print(nova)'),
            s.replace('self.body = list(body)', 'self.body = body'),
            s.replace('self.sirka = sirka', 'self.sirka = 20'),
        ]
        correct = [
            s.replace('list(body)', 'body[:]'),
            s.replace('self.body.insert(0, nova)\n        self.body.pop()', 'self.body[:] = [nova] + self.body[:-1]'),
        ]
        self.variants(0, wrong, correct)

    def test_view(self):
        s = self.source(1)
        wrong = [
            s.replace('(sirka - 1) / 2', '(sirka - 1) // 2'),
            s.replace('(vyska - 1) / 2', '(sirka - 1) / 2'),
            s.replace(') * 20,', ') * 10,'),
            s.replace('    pero.clear()\n', ''),
            s.replace('pero.color("yellow")', 'pero.color("green")'),
            s.replace('enumerate(had.body)', 'enumerate(had.body[:-1])'),
            s.replace('    pero.clear()', '    had.krok()\n    pero.clear()'),
            s.replace('        pero.stamp()', '        pero.stamp()\n        pero.stamp()'),
        ]
        correct = [
            s.replace('((x - (sirka - 1) / 2) * 20, (y - (vyska - 1) / 2) * 20)',
                      '(x * 20 - (sirka - 1) * 10, y * 20 - (vyska - 1) * 10)'),
            s.replace('''        if i == 0:
            pero.color("yellow")
        else:
            pero.color("green")''', '        pero.color("yellow" if i == 0 else "green")'),
        ]
        self.variants(1, wrong, correct)

    def test_timer(self):
        s = self.source(2)
        schedule = 'self.okno.ontimer(self.tik, self.interval)'
        wrong = [
            s.replace('''    def tik(self):
        self.had.krok()''', '''    def tik(self):
        pass'''),
            s.replace('''        self.had.krok()
        vykresli(self.had, self.pero)''', '''        vykresli(self.had, self.pero)
        self.had.krok()'''),
            s.replace('''        self.had.krok()''', '''        self.had.krok()
        self.had.krok()'''),
            s.replace('''        self.spusteno = True
        vykresli''', '''        self.spusteno = True
        self.had.krok()
        vykresli'''),
            s.replace('''        if self.spusteno:
            return
''', ''),
            s.replace(schedule, 'self.okno.ontimer(self.tik, 160)'),
            s.replace(schedule, schedule + '\n        ' + schedule),
            s.replace('self.tik, self.interval', 'self.tik(), self.interval'),
            s.replace('self.had', 'Hra.had'),
            s.replace('''        self.okno.ontimer(self.tik, self.interval)


if __name__''', '''

if __name__'''),
        ]
        correct = [
            s.replace(schedule, 'self.okno.ontimer(lambda: self.tik(), self.interval)'),
            s.replace('self.spusteno', 'self._aktivni').replace('self.interval', 'self._cekej'),
            s.replace('import priprav_okno, vykresli', 'import priprav_okno, vykresli as maluj')
             .replace('        vykresli(', '        maluj('),
        ]
        self.variants(2, wrong, correct)

    def test_controls(self):
        s = self.source(3)
        wrong = [
            s.replace('if smer == (-dx, -dy):', 'if False:'),
            s.replace('self.cekajici is not None or ', ''),
            s.replace(' or smer == self.had.smer', ''),
            s.replace('return False\n        self.cekajici = smer', 'return False\n        self.had.smer = smer\n        self.cekajici = smer'),
            s.replace('return True', 'return None'),
            s.replace('self.cekajici = None\n        super().tik()', 'super().tik()'),
            s.replace('        super().tik()', '        super().tik()\n        super().tik()'),
            s.replace('self.nahoru, "Up"', 'self.dolu, "Up"'),
            s.replace('self.nahoru, "Up"', 'self.nahoru(), "Up"'),
            s.replace('        self.okno.listen()', '        pass'),
            s.replace('self.cekajici', 'RizenaHra.cekajici'),
            s.replace('return self.nastav_smer((0, 1))', 'self.had.krok()\n        return self.nastav_smer((0, 1))'),
        ]
        correct = [
            s.replace('        super().tik()', '        rodic = super()\n        rodic.tik()'),
            s.replace('smer == (-dx, -dy)', 'smer[0] + dx == 0 and smer[1] + dy == 0'),
            s.replace('self.nahoru, "Up"', 'lambda: self.nastav_smer((0, 1)), "Up"'),
        ]
        self.variants(3, wrong, correct)

    def test_previous_solutions_are_supplied_as_modules(self):
        for index in range(1, 4):
            for previous, filename in enumerate(['had_model.py', 'had_pohled.py', 'had_hra.py'][:index]):
                with self.subTest(lesson=IDS[index], file=filename):
                    self.assertEqual((BASE/IDS[index]/'files'/filename).read_text('utf-8'), self.source(previous))


if __name__ == '__main__':
    unittest.main()
