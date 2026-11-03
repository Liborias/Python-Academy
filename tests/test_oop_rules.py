"""Kontroly pravidel objektů: chyby stavu, property, dědění a skutečné použití super."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

LESSONS = ['21-zapouzdreni-a-pravidla','22-property','23-dedeni-a-prepisovani','24-super-a-rozsireni']


class OopRulesTest(unittest.TestCase):
    def source(self, i):
        return (ROOT / 'courses/turtle-oop/lessons' / LESSONS[i] / 'solution.py').read_text('utf-8')

    def verify(self, i, code, expected):
        with tempfile.TemporaryDirectory() as temp:
            result = run_check(ROOT / 'courses/turtle-oop/lessons' / LESSONS[i], code, ROOT / 'lib', Path(temp))
        self.assertNotIn('error', result, result)
        self.assertEqual(result.get('ok'), expected, result)

    def test_account(self):
        source = self.source(0)
        mutants = [
            source.replace('if zacatek < 0:', 'if False:'),
            source.replace('castka <= 0', 'castka < 0'),
            source.replace(' or castka > self._zustatek', ''),
            source.replace('self._zustatek -= castka', 'self._zustatek += castka'),
            source.replace('return self._zustatek', 'print(self._zustatek)'),
            source.replace('self._zustatek', 'Ucet._zustatek'),
            source.replace('''        if castka <= 0 or castka > self._zustatek:
            raise ValueError("Neplatný výběr")
        self._zustatek -= castka''', '''        self._zustatek -= castka
        if castka <= 0 or self._zustatek < 0:
            raise ValueError("Neplatný výběr")'''),
            source.replace('''        if castka <= 0:
            raise ValueError("Vklad musí být kladný")
        self._zustatek += castka''', '''        self._zustatek += castka
        if castka <= 0:
            raise ValueError("Vklad musí být kladný")'''),
        ]
        for code in mutants:
            self.assertNotEqual(code, source)
            with self.subTest(code=code): self.verify(0, code, False)
        for code in [source.replace('_zustatek', '_cash'), source.replace('self._zustatek += castka', 'self._zustatek = self._zustatek + castka')]:
            self.verify(0, code, True)

    def test_property(self):
        source = self.source(1)
        mutants = [
            source.replace('hodnota < -50', 'hodnota <= -50'),
            source.replace('hodnota > 100', 'hodnota >= 100'),
            source.replace('self.teplota = teplota', 'self._teplota = teplota'),
            source.replace('return self._teplota\n', 'return self.teplota\n'),
            source.replace('self._teplota', 'Teplomer._teplota'),
            source.replace('return self._teplota * 1.8 + 32', 'return self._teplota'),
            source.replace('''        if hodnota < -50 or hodnota > 100:
            raise ValueError("Teplota mimo rozsah")
        self._teplota = hodnota''', '''        self._teplota = hodnota
        if hodnota < -50 or hodnota > 100:
            raise ValueError("Teplota mimo rozsah")'''),
            source + '\n    @fahrenheit.setter\n    def fahrenheit(self, hodnota):\n        pass\n',
            source.replace('self.teplota = teplota', 'self.teplota = teplota\n        self._cached = teplota * 1.8 + 32').replace('return self._teplota * 1.8 + 32', 'return self._cached'),
        ]
        for code in mutants:
            self.assertNotEqual(code, source)
            with self.subTest(code=code): self.verify(1, code, False)
        self.verify(1, source.replace('_teplota', '_celsius').replace('* 1.8', '* 9 / 5'), True)
        self.verify(1, source + '\n    @fahrenheit.setter\n    def fahrenheit(self, hodnota):\n        raise AttributeError("Pouze čtení")\n', True)

    def test_inheritance(self):
        source = self.source(2)
        mutants = [
            source.replace('class Pes(Zvire):', 'class Pes:'),
            source.replace('class Kocka(Zvire):', 'class Kocka:'),
            source.replace('return f"Mňau, jsem {self.jmeno}."', 'return f"Haf, jsem {self.jmeno}."'),
            source.replace('return f"Haf, jsem {self.jmeno}."', 'return "Haf, jsem Ema."'),
            source.replace('self.jmeno = jmeno', 'Zvire.jmeno = jmeno'),
            source + '\nZvire.pozdrav = Pes.pozdrav\n',
            source.replace('return f"Haf, jsem {self.jmeno}."', 'print(f"Haf, jsem {self.jmeno}.")'),
            source.replace('return f"Haf, jsem {self.jmeno}."', 'return super().pozdrav()'),
        ]
        for code in mutants:
            self.assertNotEqual(code, source)
            with self.subTest(code=code): self.verify(2, code, False)
        self.verify(2, source.replace('return f"Haf, jsem {self.jmeno}."', 'return "Haf, jsem " + self.jmeno + "."'), True)
        self.verify(2, source.replace('class Pes(Zvire):', 'class Pes(Zvire):\n    def __init__(self, jmeno):\n        self.jmeno = jmeno\n'), True)

    def test_super(self):
        source = self.source(3)
        mutants = [
            source.replace('super().__init__(jmeno)', 'self.jmeno = jmeno'),
            source.replace('super().__init__(jmeno)', 'Hrac(jmeno)'),
            source.replace('super().__init__(jmeno)', 'super().__init__(self, jmeno)'),
            source.replace('super().popis()', 'self.popis()'),
            source.replace('return f"{super().popis()}, body: {self.body}"', 'super().popis()\n        return f"Hráč: {self.jmeno}, body: {self.body}"'),
            source.replace('self.body = body', 'self.body = 0'),
            source.replace('self.body += kolik', 'body = self.body + kolik'),
            source.replace('self.body += kolik', 'self.body += max(kolik, 0)'),
            source.replace('self.body', 'BodovanyHrac.body'),
        ]
        for code in mutants:
            self.assertNotEqual(code, source)
            with self.subTest(code=code): self.verify(3, code, False)
        self.verify(3, source.replace('super().__init__(jmeno)', 'rodic = super()\n        rodic.__init__(jmeno)'), True)
        self.verify(3, source.replace('super()', 'super(BodovanyHrac, self)'), True)


if __name__ == '__main__':
    unittest.main()
