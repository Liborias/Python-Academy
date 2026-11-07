"""OOP 13–16: hodnoty, dataclass a testy, které skutečně rozpoznají chyby."""
import ast
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/oop/lessons'
IDS = ['13-str-a-repr', '14-identita-a-rovnost', '15-dataclass-a-vlastni-seznam', '16-testy-objektu']


def empty_methods(source):
    lines = source.splitlines(keepends=True)
    methods = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
    for node in reversed(methods):
        lines[node.body[0].lineno-1:node.end_lineno] = ['        pass\n']
    return ''.join(lines)


class OopModelTest(unittest.TestCase):
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

    def test_str_and_repr(self):
        s = self.source(0)
        wrong = [
            s.replace('return self.popis()', 'print(self.popis())'),
            s.replace('return self.popis()', 'return f"Balík {self.kod}, {self.hmotnost_g} g"'),
            s.replace('self.kod!r', 'self.kod'),
            s.replace('return f"PopsanyBalik', 'return f"Balik'),
            s.replace('return self.popis()', 'return "Balík B-001, 1200 g"'),
            s.replace('return f"PopsanyBalik', 'self.kod = "ZMĚNA"\n        return f"PopsanyBalik'),
            s.replace('return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"', 'return self.hmotnost_g'),
        ]
        correct = [
            s.replace('return self.popis()', 'return super().popis()'),
            s.replace('return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"', 'return "PopsanyBalik({}, {})".format(repr(self.kod), self.hmotnost_g)'),
            s.replace('return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"', 'return f"PopsanyBalik( {self.kod!r},{self.hmotnost_g} )"'),
            s.replace('return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"', 'return f"PopsanyBalik(kod={self.kod!r}, hmotnost_g={self.hmotnost_g})"'),
        ]
        self.variants(0, wrong, correct)

    def test_value_equality(self):
        s = self.source(1)
        wrong = [
            s.replace('self.ulice == other.ulice', 'True'),
            s.replace('and self.mesto == other.mesto', ''),
            s.replace('and self.psc == other.psc', ''),
            s.replace('return NotImplemented', 'return False'),
            s.replace('type(other) is not type(self)', 'not isinstance(other, Adresa)'),
            s.replace('return NotImplemented', 'raise NotImplementedError'),
            s.replace('''        return (self.ulice == other.ulice
                and self.mesto == other.mesto
                and self.psc == other.psc)''', '        return self is other'),
            s.replace('''        return (self.ulice == other.ulice''', '''        self.psc = other.psc
        return (self.ulice == other.ulice'''),
            s.replace('self.psc = psc', 'self.psc = int(psc)'),
        ]
        correct = [
            s.replace('''        return (self.ulice == other.ulice
                and self.mesto == other.mesto
                and self.psc == other.psc)''', '        return (self.ulice, self.mesto, self.psc) == (other.ulice, other.mesto, other.psc)'),
            s.replace('type(other) is not type(self)', 'other.__class__ is not self.__class__'),
            s.replace('other', 'druha_adresa'),
        ]
        self.variants(1, wrong, correct)

    def test_dataclass_and_owned_defaults(self):
        s = self.source(2)
        wrong = [
            s.replace('@dataclass\n', ''),
            s.replace('@dataclass\n', '@dataclass(eq=False)\n'),
            s.replace('@dataclass\n', '@dataclass(repr=False)\n'),
            s.replace('field(default_factory=list)', 'None'),
            s.replace('@dataclass\n', 'spolecne = []\n\n@dataclass\n').replace('default_factory=list', 'default_factory=lambda: spolecne'),
            s.replace('kod: str', 'kod: str = field(compare=False)'),
            s.replace('adresa: Adresa', 'adresa: Adresa = field(compare=False)'),
            s.replace('field(default_factory=list)', 'field(default_factory=list, compare=False)'),
            s.replace('return len(self.poznamky)', 'return len(self.poznamky) - 1'),
            s.replace('self.poznamky.append(text)', 'self.poznamky = self.poznamky + [text]'),
        ]
        correct = [
            s.replace('default_factory=list', 'default_factory=lambda: []'),
            s.replace('self.poznamky.append(text)', 'self.poznamky += [text]'),
            s.replace('@dataclass\n', '@dataclass(eq=True, repr=True)\n').replace('poznamky: list[str]', 'poznamky: list'),
        ]
        self.variants(2, wrong, correct)

    def test_student_tests_detect_real_defects(self):
        s = self.source(3)
        wrong = [
            empty_methods(s),
            s.replace('class TestExpedice(unittest.TestCase):', 'class TestExpedice:'),
            s.replace('    def test_osobni_odber(self):', '    @unittest.skip("Přeskočeno")\n    def test_osobni_odber(self):'),
            s.replace('        self.assertEqual(kuryr.cena(Balik("H-1", 5000)), 99)\n', ''),
            s.replace('        self.assertEqual(kuryr.cena(Balik("H-2", 5001)), 149)\n', ''),
            s.replace('        self.assertEqual(kuryr.cena(Balik("H-3", 10000)), 149)\n', ''),
            s.replace('        self.assertIs(expedice.balik, balik)\n', ''),
            s.replace('self.assertEqual(expedice.zmen_dopravu(kuryr), 99)', 'expedice.zmen_dopravu(kuryr)'),
            s.replace('''        self.assertIs(expedice.doprava, odber)
        self.assertIs(expedice.balik, balik)
        self.assertEqual(expedice.nabidka(), 0)
''', ''),
            s.replace('''        self.assertIs(expedice.doprava, kuryr)
        self.assertIs(expedice.balik, balik)
        self.assertEqual(expedice.nabidka(), 99)''', '        self.assertIs(expedice.balik, balik)'),
        ]
        correct = [
            s.replace('self.assertIs(expedice.balik, balik)', 'self.assertTrue(expedice.balik is balik)')
             .replace('self.assertIs(expedice.doprava, odber)', 'self.assertTrue(expedice.doprava is odber)')
             .replace('self.assertIs(expedice.doprava, kuryr)', 'self.assertTrue(expedice.doprava is kuryr)'),
            s.replace('''        with self.assertRaises(ValueError):
            expedice.zmen_dopravu(nevhodna)''', '        self.assertRaises(ValueError, expedice.zmen_dopravu, nevhodna)'),
            s.replace('test_kuryr_na_hranicich', 'test_cenova_pasma'),
        ]
        self.variants(3, wrong, correct)

    def test_helpers_match_previous_solutions(self):
        expected = {
            (0, 'balik.py'): '09-dedeni-a-jeho-hranice',
            (2, 'adresa.py'): IDS[1],
            (3, 'balik.py'): '09-dedeni-a-jeho-hranice',
            (3, 'doprava.py'): '10-polymorfismus-dopravy',
            (3, 'expres.py'): '11-super-a-rozsireni',
            (3, 'expedice.py'): '12-doprava-jako-spoluprace',
        }
        for (index, name), source in expected.items():
            self.assertEqual((BASE/IDS[index]/'files'/name).read_bytes(), (BASE/source/'solution.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
