"""Růst, kolize, partie a restart Snake: špatné varianty i správné alternativy."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/turtle-oop/lessons'
IDS = ['33-snake-potrava-a-rust', '34-snake-kolize-s-telem', '35-snake-skore-a-stav', '36-snake-hotova-hra']
SOURCES = {
    'had_model.py': '29-snake-model-a-mrizka', 'had_pohled.py': '30-snake-zobrazeni',
    'had_hra.py': '31-snake-casovac-a-pohyb', 'had_ovladani.py': '32-snake-ovladani',
    'had_potrava.py': IDS[0], 'had_kolize.py': IDS[1], 'had_partie.py': IDS[2],
}


class SnakeFinishTest(unittest.TestCase):
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

    def test_food_and_growth(self):
        s = self.source(0)
        wrong = [
            s.replace('ocas = self.body[-1]', 'ocas = self.body[0]'),
            s.replace('if nova == potrava:', 'if potrava is not None:'),
            s.replace('if nova == potrava:', 'if False:'),
            s.replace('return nova', 'return len(self.body)'),
            s.replace('if (x, y) not in had.body:', 'if True:'),
            s.replace('range(had.vyska)', 'range(had.sirka)'),
            s.replace('if not volne:', 'if False:'),
            s.replace('return vyber(volne)', 'return volne[0]'),
            s.replace('volne.append((x, y))', 'volne.extend([(x, y), (x, y)])'),
            s.replace('return vyber(volne)', 'had.krok()\n    return vyber(volne)'),
        ]
        correct = [
            s.replace('self.body.append(ocas)', 'self.body += [ocas]'),
            s.replace('return vyber(volne)', 'return vyber(list(reversed(volne)))'),
            s.replace('super().krok()', 'super(HladovyHad, self).krok()'),
        ]
        self.variants(0, wrong, correct)

    def test_collision(self):
        s = self.source(1)
        wrong = [
            s.replace('obsazene = self.body[:-1]', 'obsazene = self.body'),
            s.replace('obsazene = self.body\n', 'obsazene = self.body[:-1]\n'),
            s.replace('if nova in obsazene:', 'if False:'),
            s.replace(' % self.sirka', '').replace(' % self.vyska', ''),
            s.replace('return super().krok(potrava)', 'return super().krok()'),
            s.replace('raise ValueError("Had narazil do těla")', 'super().krok(potrava)\n            raise ValueError("Kolize")'),
            s.replace('raise ValueError("Had narazil do těla")', 'return None'),
            s.replace('return super().krok(potrava)', 'super().krok(potrava)\n        return super().krok(potrava)'),
        ]
        correct = [
            s.replace('if nova in obsazene:', 'if any(nova == bod for bod in obsazene):'),
            s.replace('super().krok(potrava)', 'super(BezpecnyHad, self).krok(potrava)'),
        ]
        self.variants(1, wrong, correct)

    def test_score_and_state(self):
        s = self.source(2)
        wrong = [
            s.replace('self.skore += 10', 'self.skore += 1'),
            s.replace('if self.stav != "hra":', 'if False:'),
            s.replace('hlava = self.had.krok(self.potrava)', 'hlava = self.had.krok()'),
            s.replace('self.stav = "konec"', 'self.stav = "hra"'),
            s.replace('''        except ValueError:
            self.stav = "konec"''', '''        except ValueError:
            self.skore += 10
            self.stav = "konec"'''),
            s.replace('            self.potrava = vyber_potravu(self.had, self.vyber)', '            self.potrava = self.potrava'),
            s.replace('if self.potrava is None:\n                self.stav = "vyhra"', 'if False:\n                self.stav = "vyhra"'),
            s.replace('''        return self.stav


if __name__''', '''        self.potrava = vyber_potravu(self.had, self.vyber)
        return self.stav


if __name__'''),
            s.replace('self.had', 'Partie.had'),
            s.replace('self.skore', 'Partie.skore'),
        ]
        correct = [
            s.replace('self.skore += 10', 'self.skore = self.skore + 10'),
            s.replace('self.stav != "hra"', 'self.stav in ("konec", "vyhra")'),
        ]
        self.variants(2, wrong, correct)

    def test_restart_and_timers(self):
        s = self.source(3)
        wrong = [
            s.replace('self.generace += 1', 'self.generace = 1'),
            s.replace('self.cekajici = None\n        self.spusteno', 'self.spusteno'),
            s.replace('lambda: self.tik_generace(generace)', 'lambda: self.tik_generace(self.generace)'),
            s.replace('if generace == self.generace:', 'if True:'),
            s.replace('if self.partie.stav == "hra":', 'if True:'),
            s.replace('self.interval)', '160)'),
            s.replace('self.partie.krok()', 'super().tik()'),
            s.replace('self.had = self.partie.had', 'pass'),
            s.replace('self.partie.krok()', 'self.partie.krok()\n        self.partie.krok()'),
            s.replace('''        if self.partie.stav != "hra":
            return
''', ''),
            s.replace('self.zacatek = list(body)', 'self.zacatek = body'),
            s.replace('''        if generace == self.generace:
            self.naplanuj()''', '        self.naplanuj()'),
        ]
        correct = [
            s.replace('lambda: self.tik_generace(generace)', 'lambda cislo=generace: self.tik_generace(cislo)'),
            s.replace('self.cekajici is not None', 'not self.cekajici is None'),
        ]
        self.variants(3, wrong, correct)

    def test_delivered_modules_match_previous_solutions(self):
        for lid in IDS:
            for filename, previous in SOURCES.items():
                path = BASE/lid/'files'/filename
                if path.exists():
                    with self.subTest(lesson=lid, file=filename):
                        self.assertEqual(path.read_text('utf-8'), (BASE/previous/'solution.py').read_text('utf-8'))


if __name__ == '__main__':
    unittest.main()
