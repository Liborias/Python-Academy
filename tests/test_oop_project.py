"""Závěrečný OOP projekt: rezervace podle vlastníka, bezpečné storno a konzole."""
import sys
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check
from server.content import lesson_view
BASE = ROOT/'courses/oop/lessons'
IDS = ['17-navrh-expedicniho-centra', '18-rezervace-a-bezpecne-storno', '19-centrum-a-vymenna-doprava', '20-konzolove-expedicni-centrum']


class OopProjectTest(unittest.TestCase):
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

    def test_order_snapshot_and_freeze(self):
        s = self.source(0)
        wrong = [
            s.replace('self._pozadavek.get(kod, 0) + pocet', 'pocet'),
            s.replace('return dict(self._pozadavek)', 'return self._pozadavek'),
            s.replace('if self.uzavrena:', 'if False:'),
            s.replace('self._pozadavek', 'NakupniObjednavka._pozadavek'),
            s.replace('type(pocet) is not int', 'not isinstance(pocet, int)'),
            s.replace('cena < 0', 'cena <= 0'),
            s.replace('return self._model.celkem()', 'return sum(p.cena_za_kus * p.pocet for p in self._model.polozky)'),
            s.replace('return self._model.celkem()', 'print(self._model.celkem())\n        return self._model.celkem()'),
            s.replace('pocet=1', 'pocet=2'),
            s.replace('self.uzavrena or not self._pozadavek', 'self.uzavrena'),
        ]
        correct = [
            s.replace('_model', '_objednavka').replace('_pozadavek', '_kusy'),
            s.replace('return dict(self._pozadavek)', 'return self._pozadavek.copy()'),
            s.replace('self._pozadavek.get(kod, 0) + pocet', '(self._pozadavek[kod] if kod in self._pozadavek else 0) + pocet'),
        ]
        self.variants(0, wrong, correct)

    def test_owned_reservations_and_single_cancellation(self):
        s = self.source(1)
        wrong = [
            s.replace('''        vysledek = super().rezervuj(pozadavek)
        objednavka.uzavri()''', '''        objednavka.uzavri()
        vysledek = super().rezervuj(pozadavek)'''),
            s.replace('vysledek = super().rezervuj(pozadavek)', 'vysledek = {}\n        for kod, pocet in pozadavek.items():\n            vysledek = super().rezervuj({kod: pocet})'),
            s.replace('        objednavka.uzavri()\n', ''),
            s.replace('if self.stav(cislo) != "rezervovana":', 'if False:'),
            s.replace('self._karty[kod].uvolni(pocet)', 'self._karty[kod].uvolni(pocet + 1)'),
            s.replace('self._karty[kod].uvolni(pocet)', 'self._karty[kod]._rezervovano -= pocet'),
            s.replace('self._rezervace', 'RezervacniSklad._rezervace'),
            s.replace('cislo in self._rezervace or', '(cislo in self._rezervace and self._rezervace[cislo]["stav"] == "rezervovana") or'),
            s.replace('zaznam["stav"] = "stornovana"', 'zaznam["stav"] = "rezervovana"'),
        ]
        correct = [
            s.replace('_rezervace', '_evidence'),
            s.replace('for kod, pocet in zaznam["pozadavek"].items():', 'for kod, pocet in reversed(list(zaznam["pozadavek"].items())):'),
            s.replace('"pozadavek": dict(pozadavek)', '"pozadavek": pozadavek.copy()'),
        ]
        self.variants(1, wrong, correct)

    def test_cooperation_and_rejected_transport(self):
        s = self.source(2)
        wrong = [
            s.replace('balik.hmotnost_g > 2000', 'balik.hmotnost_g >= 2000'),
            s.replace('return 59', 'return 99'),
            s.replace('''        expedice = Expedice(balik, doprava)
        stitek = ExpedicniStitek(objednavka.cislo, adresa)
        self.sklad.rezervuj_objednavku(objednavka)''', '''        self.sklad.rezervuj_objednavku(objednavka)
        expedice = Expedice(balik, doprava)
        stitek = ExpedicniStitek(objednavka.cislo, adresa)'''),
            s.replace('list(stitek.poznamky)', 'stitek.poznamky'),
            s.replace('"stitek": stitek}', '"stitek": stitek, "cena": expedice.nabidka()}').replace('doprava = zaznam["expedice"].nabidka()', 'doprava = zaznam["cena"]'),
            s.replace('if self.sklad.stav(cislo) != "rezervovana":', 'if False:'),
            s.replace('zbozi + doprava', 'zbozi'),
            s.replace('        self._najdi(cislo)\n        return self.sklad.storno(cislo)', '        return self.sklad.storno(cislo)'),
            s.replace('self._zaznamy', 'ExpedicniCentrum._zaznamy'),
            s.replace('''        zaznam = self._aktivni(cislo)
        return zaznam["expedice"].zmen_dopravu(nova)''', '''        zaznam = self._aktivni(cislo)
        if not isinstance(nova, (OsobniOdber, Kuryr, Cyklodoprava)):
            raise ValueError("Neznámý typ")
        return zaznam["expedice"].zmen_dopravu(nova)'''),
        ]
        correct = [
            s.replace('_zaznamy', '_objednavky').replace('self._sklad', 'self._zasoby'),
            s.replace('list(stitek.poznamky)', 'stitek.poznamky.copy()'),
            s.replace('zbozi + doprava', 'sum((zbozi, doprava))'),
        ]
        self.variants(2, wrong, correct)

    def test_console_commands_and_state(self):
        s = self.source(3)
        wrong = [
            s.replace('    casti = radek.split()', '    centrum = vytvor_demo()\n    casti = radek.split()'),
            s.replace('raise ValueError("Neznámý příkaz nebo chybný počet argumentů")', 'return ""'),
            s.replace('"kolo": Cyklodoprava("Brno-střed")', '"kolo": Kuryr("Javorová 1, Brno")'),
            s.replace('250, knihy)', '250, 1)'),
            s.replace('        centrum.storno(casti[1])\n', ''),
            s.replace('return f"Přijato: {cislo}"', 'print(f"Přijato: {cislo}")'),
            s.replace('gramy = int(casti[4])', 'gramy = int(casti[3])'),
            s.replace('" ".join(casti[2:])', 'casti[2]'),
        ]
        correct = [
            s.replace('radek.split()', 'radek.strip().split()'),
            s.replace('sorted(prehled)', 'sorted(prehled.keys())'),
            s.replace('return f"Přijato: {cislo}"', 'return "Přijato: {}".format(cislo)'),
        ]
        self.variants(3, wrong, correct)

    def test_interactive_timeout_and_defaults(self):
        self.assertEqual(lesson_view(ROOT/'courses', 'oop', IDS[3])['run_timeout'], 600)
        self.assertEqual(lesson_view(ROOT/'courses', 'oop', IDS[0])['run_timeout'], 20)
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            directory = base/'demo/lessons/01-run'
            directory.mkdir(parents=True)
            (directory/'lesson.md').write_text('Test', encoding='utf-8')
            cases = [({}, 20), ({'kind': 'gui'}, 600), ({'run_timeout': 600}, 600), ({'run_timeout': 30}, 30)]
            cases += [({'run_timeout': value}, 20) for value in (0, -1, 601, True, '600', None, 1.5)]
            for meta, expected in cases:
                with self.subTest(meta=meta):
                    (directory/'lesson.json').write_text(json.dumps(meta), encoding='utf-8')
                    self.assertEqual(lesson_view(base, 'demo', '01-run')['run_timeout'], expected)

    def test_helpers_and_completed_outline(self):
        course = json.loads((BASE.parent/"course.json").read_text("utf-8"))
        lessons = [lid for module in course["modules"] for lid in module["lessons"]]
        self.assertEqual(len(lessons), 20)
        self.assertEqual(len(set(lessons)), 20)
        self.assertEqual(course["modules"][-1]["lessons"], IDS)
        mapping = {'polozka.py': '03-metody-a-prubeh-volani', 'objednavka.py': '04-objednavka-a-jeji-polozky'}
        expected = [dict(mapping)]
        mapping.update({'nakupni_objednavka.py': IDS[0], 'sklad.py': '08-revize-skladu', 'skladova_karta.py': '07-property-a-dostupnost'})
        expected.append(dict(mapping))
        mapping.update({'rezervacni_sklad.py': IDS[1], 'balik.py': '09-dedeni-a-jeho-hranice', 'doprava.py': '10-polymorfismus-dopravy', 'expres.py': '11-super-a-rozsireni', 'expedice.py': '12-doprava-jako-spoluprace', 'adresa.py': '14-identita-a-rovnost', 'stitek.py': '15-dataclass-a-vlastni-seznam'})
        expected.append(dict(mapping)); expected.append({**mapping, 'centrum.py': IDS[2]})
        for lid, helpers in zip(IDS, expected):
            for name, source in helpers.items():
                self.assertEqual((BASE/lid/'files'/name).read_bytes(), (BASE/source/'solution.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
