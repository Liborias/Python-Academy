"""Třetí blok OOP: skutečné dědění, delegování a zachování stavu při chybě."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/oop/lessons'
IDS = ['09-dedeni-a-jeho-hranice', '10-polymorfismus-dopravy', '11-super-a-rozsireni', '12-doprava-jako-spoluprace']


class OopTransportTest(unittest.TestCase):
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

    def test_inherited_parcel(self):
        s = self.source(0)
        wrong = [
            s.replace('class KrehkyBalik(Balik):', 'class KrehkyBalik:'),
            s.replace('Chránit před nárazy.', 'Chránit před vodou.'),
            s.replace('return "Chránit před nárazy."', 'print("Chránit před nárazy.")'),
            s.replace('class KrehkyBalik(Balik):', 'class KrehkyBalik(Balik):\n    def popis(self):\n        return f"Balík {self.kod}, {self.hmotnost_g} g"\n'),
            s.replace('type(hmotnost_g) is not int', 'not isinstance(hmotnost_g, int)'),
            s.replace('hmotnost_g <= 0', 'hmotnost_g < 0'),
            s.replace('self._hmotnost_g', 'Balik._hmotnost_g'),
            s.replace('    def popis(self):', '    @hmotnost_g.setter\n    def hmotnost_g(self, value):\n        self._hmotnost_g = value\n\n    def popis(self):'),
        ]
        correct = [s.replace('_hmotnost_g', '_vaha'), s.replace('return f"Balík {self.kod}, {self.hmotnost_g} g"', 'return "Balík {}, {} g".format(self.kod, self.hmotnost_g)')]
        self.variants(0, wrong, correct)

    def test_polymorphic_quotes(self):
        s = self.source(1)
        wrong = [
            s.replace('class OsobniOdber(Doprava):', 'class OsobniOdber:'),
            s.replace('return 0', 'return 99'),
            s.replace('balik.hmotnost_g > self.limit_g', 'balik.hmotnost_g >= self.limit_g'),
            s.replace('balik.hmotnost_g > self.limit_g', 'False'),
            s.replace('balik.hmotnost_g <= 5000', 'balik.hmotnost_g < 5000'),
            s.replace('return 149', 'return 99'),
            s.replace('ceny.append(doprava.cena(balik))', 'ceny.append(0 if isinstance(doprava, OsobniOdber) else 99)'),
            s.replace('for doprava in dopravy:', 'for doprava in reversed(dopravy):'),
            s.replace('for doprava in dopravy:', 'for doprava in dict.fromkeys(dopravy):'),
            s.replace('type(limit_g) is not int', 'not isinstance(limit_g, int)'),
            s.replace('self._adresa = adresa', 'self._adresa = adresa.strip()'),
        ]
        correct = [
            s.replace('''    ceny = []
    for doprava in dopravy:
        ceny.append(doprava.cena(balik))
    return ceny''', '    return [doprava.cena(balik) for doprava in dopravy]'),
            s.replace('_limit_g', '_maximum').replace('_adresa', '_cil').replace('_misto', '_vydejna'),
            s.replace('''        if balik.hmotnost_g <= 5000:
            return 99
        return 149''', '        return 99 if balik.hmotnost_g <= 5000 else 149'),
        ]
        self.variants(1, wrong, correct)

    def test_super_extends_same_instance(self):
        s = self.source(2)
        wrong = [
            s.replace('super().__init__(adresa, limit_g)', 'super().__init__(adresa)'),
            s.replace('super().__init__(adresa, limit_g)', 'Kuryr(adresa, limit_g)'),
            s.replace('super().__init__(adresa, limit_g)', 'Kuryr.__init__(self, adresa, limit_g)'),
            s.replace('super().cena(balik) + self.priplatek', '99 + self.priplatek'),
            s.replace('super().cena(balik) + self.priplatek', 'super().cena(balik)'),
            s.replace('super().cena(balik) + self.priplatek', 'super().cena(balik) + super().cena(balik) + self.priplatek'),
            s.replace('super().cena(balik) + self.priplatek', 'Kuryr.cena(self, balik) + self.priplatek'),
            s.replace('priplatek < 0', 'priplatek <= 0'),
            s.replace('type(priplatek) is not int', 'not isinstance(priplatek, int)'),
            s.replace('if termin not in ("dopoledne", "odpoledne"):', 'if False:'),
        ]
        correct = [
            s.replace('super()', 'super(ExpresniKuryr, self)'),
            s.replace('_termin', '_okno').replace('_priplatek', '_navic'),
            s.replace('return super().cena(balik) + self.priplatek', 'zaklad = super().cena(balik)\n        return self.priplatek + zaklad'),
        ]
        self.variants(2, wrong, correct)

    def test_composition_checks_before_change(self):
        s = self.source(3)
        wrong = [
            s.replace('        doprava.cena(balik)\n', ''),
            s.replace('''        cena = nova.cena(self.balik)
        self._doprava = nova''', '''        self._doprava = nova
        cena = nova.cena(self.balik)'''),
            s.replace('return cena', 'return None'),
            s.replace('self._doprava = nova', 'nova = self._doprava'),
            s.replace('return self.doprava.cena(self.balik)', 'return 99'),
            s.replace('doprava.cena(balik)\n', 'self._cena = doprava.cena(balik)\n').replace('return self.doprava.cena(self.balik)', 'return self._cena'),
            s.replace('        self._doprava = doprava', '        import copy\n        self._doprava = copy.deepcopy(doprava)'),
            s.replace('self._doprava', 'Expedice._doprava'),
            s.replace('        doprava.cena(balik)', '        if not isinstance(doprava, (OsobniOdber, Kuryr)):\n            raise ValueError("Neznámá doprava")\n        doprava.cena(balik)'),
            s.replace('    def nabidka(self):', '    @doprava.setter\n    def doprava(self, nova):\n        self._doprava = nova\n\n    def nabidka(self):'),
        ]
        correct = [
            s.replace('_doprava', '_volba').replace('_balik', '_zasilka'),
            s.replace('''        cena = nova.cena(self.balik)
        self._doprava = nova
        return cena''', '''        vysledek = nova.cena(self.balik)
        self._doprava = nova
        return vysledek'''),
            s.replace('return self.doprava.cena(self.balik)', 'vybrana = self.doprava\n        return vybrana.cena(self.balik)'),
        ]
        self.variants(3, wrong, correct)

    def test_helpers_match_previous_solutions(self):
        for index in (1, 2, 3):
            self.assertEqual((BASE/IDS[index]/'files/balik.py').read_text('utf-8'), self.source(0))
        for index in (2, 3):
            self.assertEqual((BASE/IDS[index]/'files/doprava.py').read_text('utf-8'), self.source(1))
        self.assertEqual((BASE/IDS[3]/'files/expres.py').read_text('utf-8'), self.source(2))


if __name__ == '__main__':
    unittest.main()
