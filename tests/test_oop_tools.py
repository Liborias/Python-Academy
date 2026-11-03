"""Speciální metody a datové třídy: chyby chování i správné alternativy řešení."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

LESSONS = [
    '25-specialni-metody', '26-identita-a-rovnost',
    '27-poradi-dedeni-mro', '28-dataclass',
]


class OopToolsTest(unittest.TestCase):
    def source(self, index):
        return (ROOT/'courses/turtle-oop/lessons'/LESSONS[index]/'solution.py').read_text('utf-8')

    def verify(self, index, code, expected):
        with tempfile.TemporaryDirectory() as temp:
            result = run_check(ROOT/'courses/turtle-oop/lessons'/LESSONS[index], code, ROOT/'lib', Path(temp))
        self.assertNotIn('error', result, result)
        self.assertEqual(result.get('ok'), expected, result)

    def variants(self, index, source, wrong, correct):
        for code in wrong:
            self.assertNotEqual(code, source)
            with self.subTest(expected=False, code=code):
                self.verify(index, code, False)
        for code in correct:
            self.assertNotEqual(code, source)
            with self.subTest(expected=True, code=code):
                self.verify(index, code, True)

    def test_special_methods(self):
        source = self.source(0)
        wrong = [
            source.replace('self.body = list(body)', 'self.body = body'),
            source.replace('return len(self.body)', 'return 2'),
            source.replace('return len(self.body)', 'return len(self.jmeno)'),
            source.replace('return f"Trasa {self.jmeno}, bodů: {len(self.body)}"',
                           'print(f"Trasa {self.jmeno}, bodů: {len(self.body)}")'),
            source.replace('{self.jmeno!r}', '{self.jmeno}'),
            source.replace('self.jmeno = jmeno', 'self.jmeno = jmeno\n        self._name = jmeno')
                  .replace('f"Trasa {self.jmeno},', 'f"Trasa {self._name},'),
            source.replace('return len(self.body)', 'self.body.pop()\n        return len(self.body)'),
            source.replace('self.body = list(body)', 'self.body = sorted(body)'),
        ]
        correct = [
            source.replace('list(body)', 'body[:]'),
            source.replace('return f"Trasa(jmeno={self.jmeno!r}, body={self.body!r})"',
                           'return "Trasa(jmeno={!r}, body={!r})".format(self.jmeno, self.body)'),
        ]
        self.variants(0, source, wrong, correct)

    def test_equality(self):
        source = self.source(1)
        comparison = 'self.x == other.x and self.y == other.y'
        wrong = [
            source.replace(comparison, 'self.x == other.x'),
            source.replace(' and ', ' or '),
            source.replace(comparison, 'self is other'),
            source.replace('return NotImplemented', 'return False'),
            source.replace('not isinstance(other, Bod)', 'type(other) is not Bod'),
            source.replace('self.y = y', 'self.y = y\n        self._pair = (x, y)')
                  .replace(comparison, 'self._pair == other._pair'),
            source.replace('return ' + comparison, 'self.x = 0\n        return ' + comparison),
            source.replace('return ' + comparison, 'return str(' + comparison + ')'),
            source.replace('return NotImplemented', 'raise NotImplementedError'),
        ]
        correct = [
            source.replace(comparison, '(self.x, self.y) == (other.x, other.y)'),
            source.replace('other', 'druhy'),
        ]
        self.variants(1, source, wrong, correct)

    def test_mro(self):
        source = self.source(2)
        wrong = [
            source.replace('super().cesta()', 'Zaklad.cesta(self)'),
            source.replace('class Obracene(Pravy, Levy):', 'class Obracene(Levy, Pravy):'),
            source.replace('class Oba(Levy, Pravy):', 'class Oba(Levy):'),
            source.replace('return ["Zaklad"]', 'return Zaklad.spolecny') + '\nZaklad.spolecny = ["Zaklad"]\n',
            source.replace('return ["Levy"] + super().cesta()',
                           'super().cesta()\n        return ["Levy", "Zaklad"]'),
            source.replace('return ["Pravy"] + super().cesta()',
                           'super().cesta()\n        return ["Pravy"] + super().cesta()'),
            source.replace('return ["Levy"] + super().cesta()',
                           'return ["Levy"] + super().cesta() + super().cesta()'),
            source.replace('class Pravy(Zaklad):', 'class Pravy:'),
        ]
        correct = [
            source.replace('super().cesta()', 'super(Levy, self).cesta()', 1)
                  .replace('return ["Pravy"] + super().cesta()',
                           'return ["Pravy"] + super(Pravy, self).cesta()'),
            source.replace('return ["Levy"] + super().cesta()',
                           'cesta = super().cesta()\n        cesta.insert(0, "Levy")\n        return cesta')
                  .replace('return ["Pravy"] + super().cesta()',
                           'rodic = super()\n        return ["Pravy"] + rodic.cesta()'),
        ]
        self.variants(2, source, wrong, correct)

    def test_dataclass(self):
        source = self.source(3)
        wrong = [
            source.replace('@dataclass\n', ''),
            source.replace('@dataclass\n', '@dataclass(eq=False)\n'),
            source.replace('@dataclass\n', '@dataclass(repr=False)\n'),
            source.replace('default_factory=list', 'default_factory=list()'),
            source.replace('@dataclass\n', 'shared = []\n\n\n@dataclass\n')
                  .replace('default_factory=list', 'default_factory=lambda: shared'),
            source.replace('default_factory=list)', 'default_factory=list, compare=False)'),
            source.replace('body: int = 0', 'body: int = field(default=0, compare=False)'),
            source.replace('self.udalosti.append(text)', 'pass'),
            source.replace('return len(self.udalosti)', 'print(len(self.udalosti))'),
            source.replace('self.udalosti.append(text)',
                           'if text and text not in self.udalosti:\n            self.udalosti.append(text)'),
        ]
        correct = [
            source.replace('default_factory=list', 'default_factory=lambda: []'),
            source.replace('self.udalosti.append(text)', 'self.udalosti += [text]'),
        ]
        self.variants(3, source, wrong, correct)


if __name__ == '__main__':
    unittest.main()
