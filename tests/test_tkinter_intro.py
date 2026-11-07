"""Tkinter 1–4: smysluplné chyby a správná alternativní řešení."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check
from server.preparation import course_preparation

BASE = ROOT/'courses/tkinter-api/lessons'
IDS = ['01-prvni-okno-a-mainloop', '02-popisky-a-pack', '03-tlacitka-a-zpetna-volani', '04-vstupni-pole-a-grid']


class TkinterIntroTest(unittest.TestCase):
    def source(self, index):
        return (BASE/IDS[index]/'solution.py').read_text('utf-8')

    def verify(self, index, code, expected):
        with tempfile.TemporaryDirectory() as temp:
            result = run_check(BASE/IDS[index], code, ROOT/'lib', Path(temp))
        self.assertNotIn('error', result, result)
        self.assertEqual(result.get('ok'), expected, result)

    def variants(self, index, wrong, correct):
        original = self.source(index)
        for expected, variants in [(False, wrong), (True, correct)]:
            for source in variants:
                self.assertNotEqual(source, original)
                with self.subTest(expected=expected, source=source):
                    self.verify(index, source, expected)

    def test_window_and_mainloop(self):
        s = self.source(0)
        wrong = [s.replace('okno.mainloop()', ''), s.replace('Moje první okno', 'Jiné okno'),
                 s.replace('420x240', '240x420'), s.replace('minsize(320, 180)', 'minsize(180, 320)'),
                 s.replace('okno.mainloop()', 'tk.Tk()\nokno.mainloop()'),
                 s.replace('okno.mainloop()', 'okno.destroy()\nokno.mainloop()'),
                 s.replace('okno.mainloop()', 'while True:\n    pass')]
        correct = [s.replace('okno =', 'aplikace =').replace('okno.', 'aplikace.'), s.replace('.title(', '.wm_title(').replace('.geometry(', '.wm_geometry('), s.replace('420x240', '420x240+20+30')]
        self.variants(0, wrong, correct)

    def test_labels_and_pack(self):
        s = self.source(1)
        wrong = [s.replace('stav.pack(padx=16, pady=12)', ''),
                 s.replace('Stav: připraveno', 'Stav: chyba'),
                 s.replace('ttk.Label(okno, text="Stav:', 'ttk.Label(tk.Tk(), text="Stav:'),
                 s.replace('padx=16', 'padx=0'),
                 s.replace('pady=12', 'pady=0'),
                 s.replace('.pack(', '.grid('),
                 s.replace('Expediční přehled', 'DUPLIKÁT').replace('Stav: připraveno', 'Expediční přehled').replace('DUPLIKÁT', 'Stav: připraveno')]
        correct = [s.replace('padx=16, pady=12', 'padx=(12, 20), pady=(8, 14)'),
                   s.replace('nadpis', 'hlavicka').replace('stav', 'zprava'),
                   s.replace('''nadpis = ttk.Label(okno, text="Expediční přehled")
nadpis.pack(padx=16, pady=12)
stav = ttk.Label(okno, text="Stav: připraveno")
stav.pack(padx=16, pady=12)''', '''stav = ttk.Label(okno, text="Stav: připraveno")
nadpis = ttk.Label(okno, text="Expediční přehled")
nadpis.pack(padx=16, pady=12)
stav.pack(padx=16, pady=12)''')]
        self.variants(1, wrong, correct)

    def test_callback_timing_and_existing_label(self):
        s = self.source(2)
        wrong = [s.replace('command=potvrd)', 'command=potvrd())'),
                 s.replace('stav.configure(text="Akce potvrzena.")', 'return "Akce potvrzena."'),
                 s.replace('stav.configure(text="Akce potvrzena.")', 'ttk.Label(okno, text="Akce potvrzena.").pack()'),
                 s.replace('stav.configure(text="Akce potvrzena.")', 'okno.title("Akce potvrzena.")'),
                 s.replace('command=obnov', 'command=potvrd'),
                 s.replace('def obnov():\n    stav.configure(text="Čekám na potvrzení.")', 'def obnov():\n    pass'),
                 s.replace('text="Čekám na potvrzení.")\nstav.pack', 'text="Akce potvrzena.")\nstav.pack'),
                 s.replace('okno.mainloop()', 'okno.mainloop()\nokno.mainloop()')]
        correct = [s.replace('.configure(', '.config('),
                   s.replace('stav.configure(text="Akce potvrzena.")', 'stav["text"] = "Akce potvrzena."').replace('stav.configure(text="Čekám na potvrzení.")', 'stav["text"] = "Čekám na potvrzení."'),
                   s.replace('command=potvrd)', 'command=lambda: potvrd())').replace('command=obnov)', 'command=lambda: obnov())')]
        self.variants(2, wrong, correct)

    def test_entry_current_text_validation_and_grid(self):
        s = self.source(3)
        wrong = [s.replace('def pozdrav():\n    text = jmeno.get().strip()', 'text = jmeno.get().strip()\n\ndef pozdrav():'),
                 s.replace('jmeno.get().strip()', 'jmeno.get()'),
                 s.replace('if not text:', 'if False:'),
                 s.replace('f"Ahoj, {text}!"', '"Ahoj, Ema!"'),
                 s.replace('jmeno.get().strip()', '" ".join(jmeno.get().split())'),
                 s.replace('vysledek.configure(text=f"Ahoj, {text}!")', 'ttk.Label(okno, text=f"Ahoj, {text}!").grid(row=3, column=0)'),
                 s.replace('row=2, column=0, columnspan=2', 'row=1, column=0, columnspan=2'),
                 s.replace('jmeno.grid(', 'jmeno.pack('),
                 s.replace('weight=1', 'weight=0'),
                 s.replace('sticky="ew"', 'sticky="w"')]
        correct = [s.replace('jmeno', 'vstup'),
                   s.replace('''    if not text:
        vysledek.configure(text="Zadejte jméno.")
    else:
        vysledek.configure(text=f"Ahoj, {text}!")''', '''    if text:
        vysledek.config(text=f"Ahoj, {text}!")
    else:
        vysledek.config(text="Zadejte jméno.")'''),
                   s.replace('sticky="ew"', 'sticky="we"').replace('weight=1', 'weight=2')]
        self.variants(3, wrong, correct)

    def test_outline_preparation_and_quizzes(self):
        c = json.loads((BASE.parent/'course.json').read_text('utf-8'))
        self.assertEqual(c['modules'][0]['lessons'], IDS)
        self.assertEqual(c['requires_packages'], ['requests'])
        self.assertEqual(c['learning_plan']['level'], 3)
        catalog = json.loads((ROOT/'courses/catalog.json').read_text('utf-8'))['courses']
        row = next(r for r in catalog if r['id'] == 'tkinter-api')
        self.assertEqual((row['status'], row['lessons']), ('draft', 28))
        profile = course_preparation('tkinter-api')
        self.assertIn('První čtyři', profile['focus'])
        self.assertIn('-m tkinter', profile['system'])
        for lid in IDS:
            d = BASE/lid
            self.assertEqual(json.loads((d/'lesson.json').read_text())['kind'], 'gui')
            self.assertEqual(len(json.loads((d/'quiz.json').read_text())), 3)


if __name__ == '__main__':
    unittest.main()
